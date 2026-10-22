import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

# Fixture to initialize Calculator with a temporary directory for file paths
@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # Patch properties to use the temporary directory paths
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            # Set return values to use paths within the temporary directory
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            # Return an instance of Calculator with the mocked config
            yield Calculator(config=config)

# Test Calculator Initialization

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

# Test Logging Setup

@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')
        
        # Instantiate calculator to trigger logging
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")

# Test History Loading Failure Handling
def test_calculator_initialization_history_load_failure(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)

    with patch.object(
        Calculator, 'load_history',
        side_effect=OperationError("History load failed")
    ), patch('app.calculator.logging.warning') as mock_warning:
        calculator = Calculator(config=config)

    assert calculator.history == []
    mock_warning.assert_called_once()


# Test Adding and Removing Observers

def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

# Test Setting Operations

def test_set_operation(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

# Test Performing Operations

def test_perform_operation_addition(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(2, 3)
    assert result == Decimal('5')

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('invalid', 3)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(2, 3)

# Test History Size Limit Enforcement
def test_perform_operation_trims_history(calculator, monkeypatch):
    monkeypatch.setattr(calculator.config, 'max_history_size', 1)

    calculator.set_operation(OperationFactory.create_operation('add'))
    calculator.perform_operation(2, 3)
    calculator.perform_operation(4, 5)

    assert len(calculator.history) == 1
    assert calculator.history[0].operand1 == Decimal('4')
    assert calculator.history[0].operand2 == Decimal('5')

# Tests Unexpected Operation Exception
def test_perform_operation_wraps_unexpected_exception(calculator):
    operation = Mock()
    operation.execute.side_effect = RuntimeError("Unexpected failure")
    calculator.set_operation(operation)

    with pytest.raises(OperationError, match="Operation failed: Unexpected failure"):
        calculator.perform_operation(2, 3)

# Test Undo/Redo Functionality

def test_undo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1

# Tests Undo w/ Empty Stack
def test_undo_empty_stack(calculator):
    assert calculator.undo() is False
    assert calculator.history == []

# Tests Redo w/ Empty Stack
def test_redo_empty_stack(calculator):
    assert calculator.redo() is False
    assert calculator.history == []


# Test History Management

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    # Mock CSV data to match the expected format in from_dict
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['Addition'],
        'operand1': ['2'],
        'operand2': ['3'],
        'result': ['5'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })
    
    # Test the load_history functionality
    try:
        calculator.load_history()
        # Verify history length after loading
        assert len(calculator.history) == 1
        # Verify the loaded values
        assert calculator.history[0].operation == "Addition"
        assert calculator.history[0].operand1 == Decimal("2")
        assert calculator.history[0].operand2 == Decimal("3")
        assert calculator.history[0].result == Decimal("5")
    except OperationError:
        pytest.fail("Loading history failed due to OperationError")

# Test Loading Empty History
@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_empty_history(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame()

    calculator.load_history()

    assert calculator.history == []

# Test History Loading Failures
@patch(
    'app.calculator.pd.read_csv',
    side_effect=OSError("Cannot read history")
)
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history_failure(mock_exists, mock_read_csv, calculator):
    with pytest.raises(OperationError):
        calculator.load_history()        
            
# Test Clearing History

def test_clear_history(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

# Test REPL Commands (using patches for input/output handling)

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        assert any(call.args and "History saved successfully." in call.args[0] for call in mock_print.call_args_list)
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    assert any(call.args and "\nAvailable commands:" in call.args[0] for call in mock_print.call_args_list)

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    assert any(call.args and "\nResult: 5" in call.args[0] for call in mock_print.call_args_list)


# Test Empty History
@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_history_empty(mock_calculator, mock_print, mock_input):
    mock_calculator.return_value.show_history.return_value = []

    calculator_repl()

    mock_print.assert_any_call("No calculations in history")

# Test History w/ Entries
@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_history_with_entries(mock_calculator, mock_print, mock_input):
    mock_calculator.return_value.show_history.return_value = ["2 + 3 = 5"]

    calculator_repl()

    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1. 2 + 3 = 5")

# Test Clear Command
@patch('builtins.input', side_effect=['clear', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_clear_history(mock_calculator, mock_print, mock_input):
    calculator_repl()

    mock_calculator.return_value.clear_history.assert_called_once()
    assert any(call.args and "History cleared" in call.args[0] for call in mock_print.call_args_list)

# Test Undo/Redo
@pytest.mark.parametrize(
    "command, method_name, expected_message, return_value",
    [
        ('undo', 'undo', "Operation undone", True),
        ('undo', 'undo', "Nothing to undo", False),
        ('redo', 'redo', "Operation redone", True),
        ('redo', 'redo', "Nothing to redo", False),
    ],
)
def test_repl_undo_redo_commands(
    command, method_name, expected_message, return_value
):
    with patch('builtins.input', side_effect=[command, 'exit']), \
         patch('builtins.print') as mock_print, \
         patch('app.calculator_repl.Calculator') as mock_calculator:

        getattr(
            mock_calculator.return_value, method_name
        ).return_value = return_value

        calculator_repl()

        getattr(
            mock_calculator.return_value, method_name
        ).assert_called_once()
        assert any(call.args and expected_message in call.args[0] for call in mock_print.call_args_list)

# Test Save and Load
@patch('builtins.input', side_effect=['save', 'load', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_save_and_load(mock_calculator, mock_print, mock_input):
    calculator_repl()

    mock_calculator.return_value.save_history.assert_called()
    mock_calculator.return_value.load_history.assert_called_once()

    assert any(call.args and "History saved successfully" in call.args[0] for call in mock_print.call_args_list)
    assert any(call.args and "History loaded successfully" in call.args[0] for call in mock_print.call_args_list)

# Test Save and Load Errors
@patch('builtins.input', side_effect=['save', 'load', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_save_and_load_errors(mock_calculator, mock_print, mock_input):
    calc = mock_calculator.return_value
    calc.save_history.side_effect = OperationError("Save failed")
    calc.load_history.side_effect = OperationError("Load failed")

    calculator_repl()

    assert any(call.args and "Error saving history: Save failed" in call.args[0] for call in mock_print.call_args_list)
    assert any(call.args and "Error loading history: Load failed" in call.args[0] for call in mock_print.call_args_list)

# Test Cancel
@pytest.mark.parametrize(
    "inputs", [['add', 'cancel', 'exit'],
               ['add', '2', 'cancel', 'exit'],],
)
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_cancel_operation(
    mock_calculator, mock_print, inputs
):
    with patch('builtins.input', side_effect=inputs):
        calculator_repl()

    mock_print.assert_any_call("Operation cancelled")
    mock_calculator.return_value.perform_operation.assert_not_called()

# Test Validation Error
@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_operation_validation_error(
    mock_calculator, mock_print, mock_input
):
    mock_calculator.return_value.perform_operation.side_effect = (
        ValidationError("Invalid input")
    )

    calculator_repl()

    assert any(call.args and "Error: Invalid input" in call.args[0] for call in mock_print.call_args_list)

# Test Unexpected Error
@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_unexpected_operation_error(
    mock_calculator, mock_print, mock_input
):
    mock_calculator.return_value.perform_operation.side_effect = (
        RuntimeError("Unexpected failure")
    )

    calculator_repl()

    assert any(call.args and "Unexpected error: Unexpected failure" in call.args[0] for call in mock_print.call_args_list)

# Test Unknown Command
@patch('builtins.input', side_effect=['unknown', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_unknown_command(mock_calculator, mock_print, mock_input):
    calculator_repl()

    assert any(call.args and "Unknown command: 'unknown'. Type 'help' for available commands."
               in call.args[0] for call in mock_print.call_args_list)

# Test Ctrl+C Interruption
@patch('builtins.input', side_effect=[KeyboardInterrupt(), 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_keyboard_interrupt(mock_calculator, mock_print, mock_input):
    calculator_repl()

    mock_print.assert_any_call("\nOperation cancelled")

# Testing End-of-File EOFError
@patch('builtins.input', side_effect=EOFError())
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_eof(mock_calculator, mock_print, mock_input):
    calculator_repl()

    mock_print.assert_any_call("\nInput terminated. Exiting...")

# Test Fatal Initialization Error
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_fatal_initialization_error(mock_calculator, mock_print):
    mock_calculator.side_effect = RuntimeError("Initialization failed")

    with pytest.raises(RuntimeError, match="Initialization failed"):
        calculator_repl()

    assert any(call.args and "Fatal error: Initialization failed" in call.args[0] for call in mock_print.call_args_list)

# Test Save Failure During Exit
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_exit_save_error(mock_calculator, mock_print, mock_input):
    mock_calculator.return_value.save_history.side_effect = (
        OperationError("Cannot save")
    )

    calculator_repl()

    assert any(call.args and "Warning: Could not save history: Cannot save" in call.args[0] for call in mock_print.call_args_list)
    mock_print.assert_any_call("Goodbye!")

# Test Other Unexpected Exceptions
@patch('builtins.input', side_effect=[RuntimeError("Input failure"), 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_repl_unexpected_loop_error(
    mock_calculator, mock_print, mock_input
):
    calculator_repl()

    assert any(call.args and "Error: Input failure" in call.args[0] for call in mock_print.call_args_list)


# More Tests
# Test History DataFrame and Formatted History
def test_get_history_dataframe_and_show_history(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    calculator.perform_operation(2, 3)

    df = calculator.get_history_dataframe()

    assert len(df) == 1
    assert list(df.columns) == ['operation', 'operand1', 'operand2', 'result', 'timestamp']
    assert df.iloc[0]['operation'] == 'Addition'
    assert df.iloc[0]['operand1'] == '2'
    assert df.iloc[0]['operand2'] == '3'
    assert df.iloc[0]['result'] == '5'

    assert calculator.show_history() == ['Addition(2, 3) = 5']


# Test Logging Setup Failure
def test_logging_setup_failure(calculator, capsys):
    with patch(
        'app.calculator.os.makedirs',
        side_effect=OSError("Cannot create log directory")
    ):
        with pytest.raises(OSError, match="Cannot create log directory"):
            calculator._setup_logging()

    captured = capsys.readouterr()
    assert "Error setting up logging: Cannot create log directory" in captured.out