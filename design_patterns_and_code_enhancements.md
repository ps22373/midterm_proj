# Design Patterns and Code Enhancements

## Overview

The calculator application uses several software design patterns and additional features to improve modularity, maintainability, extensibility, and usability. These enhancements separate responsibilities across the application, simplify testing, and make it easier to introduce new functionality.

## Design Patterns

### Factory Pattern

The Factory pattern centralizes the registration and retrieval of mathematical operations. The OperationFactory in ***app/operations.py*** provides a consistent way to obtain operation instances without requiring the command-line interface to create each operation directly.

**Benefit:** New mathematical operations can be registered and made available to the application without placing their implementation details in the REPL.

### Strategy Pattern

The Strategy pattern represents mathematical operations as separate implementations of a common interface. Each operation class provides its own calculation logic.

**Benefit:** Operations can be developed, tested, and maintained independently. New operations can be added without combining all mathematical logic into a single class.

### Observer Pattern

The Observer pattern allows the calculator to notify registered observers when relevant calculation events occur. The application uses *LoggingObserver* and *AutoSaveObserver* in ***app/history.py*** to support logging and automatic history persistence.

**Benefit:** Logging and history saving remain separate from the core calculation logic, improving modularity and maintainability.

### Memento Pattern

The Memento pattern supports undo and redo by preserving calculator state so that previous states can be restored.

The implementation involves ***app/calculator_memento.py*** and ***app/calculator.py***.

**Benefit:** Users can undo previous actions and redo them when needed without manually recreating the calculator's earlier state.

### Decorator Pattern

The Decorator pattern allows additional functionality to be added to an existing component without modifying its original implementation. In ***app/calculator_repl.py***, *OperationHelpDecorator* extends *BasicHelpMenu* with information about available mathematical operations.

**Benefit:** The help menu can be extended while keeping the basic help functionality separate from operation-specific information.

## Optional Feature 1: Dynamic Help Menu Using the Decorator Pattern

The calculator implements a dynamic help menu using the Decorator design pattern. The *BasicHelpMenu* provides help for general calculator commands, while *OperationHelpDecorator* adds the currently available mathematical operations to the help output.

The available operation names are obtained from ***OperationFactory.get_available_operations()***, allowing the help menu to reflect the registered operations rather than requiring a separate hardcoded list of operation names.

### How it works:
- The application creates a basic help menu
- The *OperationHelpDecorator* wraps the basic help menu
- When the user enters *help*, the decorated menu displays both general calculator commands and available mathematical operations

### Benefits:
- Keeps general command help separate from operation-specific help
- Automatically reflects registered operations
- Reduces duplication and the need to maintain a separate hardcoded operation list
- Demonstrates the Decorator pattern through a practical application feature

## Optional Feature 2: Color-Coded Terminal Output Using Colorama

The calculator uses the *colorama* library to make terminal output easier to distinguish visually. Color formatting is implemented in ***app/calculator_repl.py***.

The application initializes Colorama with ***init(autoreset=True)*** and uses foreground colors to distinguish different categories of output.

The Colorama dependency is included in requirements.txt, so it is installed with the project's other dependencies.

### Color usage:
- Cyan: Startup messages and help information.
- Green: Calculation results and successful operations.
- Yellow: Warnings and unknown commands.
- Red: Errors and failed operations.

### How it works:
- Colorama is imported and initialized when the REPL module is loaded
- The REPL applies the appropriate color to output messages
- With automatic color resetting enabled, formatting does not unintentionally carry over to subsequent terminal output

### Benefits:
- Makes calculation results easier to identify
- Helps users distinguish warnings from errors
- Improves readability and the overall command-line experience
- Adds visual feedback without changing the underlying calculation logic

## Additional Enhancements

### Expanded Mathematical Operations

In addition to basic arithmetic, the calculator supports power, nth root, modulus, integer division, percentage calculations, and absolute difference. The operation classes implement the corresponding mathematical logic through the shared operation interface.

### Input Validation and Exception Handling

The application validates numerical input and uses custom exceptions to handle invalid values, unsupported operations, and calculation errors. This helps prevent invalid inputs from reaching the calculation logic unchecked.

### Configurable Application Settings

The application uses environment variables loaded from a .env file to configure settings such as calculation precision, maximum input values, history size, automatic saving, file locations, and default encoding.

### CSV History Persistence

The calculator uses pandas to save and load calculation history in CSV format. The history records include the operation, operands, result, and timestamp.

### Logging

The application uses Python's built-in logging module to record application activity, warnings, and errors. It supports the INFO, WARNING, and ERROR logging levels.

### Automated Testing and Continuous Integration

The project uses pytest for automated testing and pytest-cov for code coverage measurement. GitHub Actions runs the test suite when code is pushed to main or a pull request targets main, enforcing a minimum coverage threshold of 90%.