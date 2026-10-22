########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging
from colorama import Fore, init

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

# Initialize Colorama for cross-platform terminal colors
init(autoreset=True)


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Initialize the decorated help menu
        help_menu = OperationHelpDecorator(BasicHelpMenu())

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(Fore.CYAN + "Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print("\nAvailable commands:")
                    # print("  add, subtract, multiply, divide, power, root - Perform calculations")
                    # print("  history - Show calculation history")
                    # print("  clear - Clear calculation history")
                    # print("  undo - Undo the last calculation")
                    # print("  redo - Redo the last undone calculation")
                    # print("  save - Save calculation history to file")
                    # print("  load - Load calculation history from file")
                    # print("  exit - Exit the calculator")
                    print(help_menu.display())
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully.")
                    except Exception as e:
                        print(Fore.YELLOW + f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print(Fore.GREEN + "History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print(Fore.GREEN + "Operation undone")
                    else:
                        print(Fore.YELLOW + "Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print(Fore.GREEN + "Operation redone")
                    else:
                        print(Fore.YELLOW + "Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print(Fore.GREEN + "History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                # if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root']:
                if command in OperationFactory.get_available_operations():
                    # Perform the specified arithmetic operation
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(Fore.GREEN + f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(Fore.RED + f"Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(Fore.RED + f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                print(Fore.YELLOW + f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print("\nOperation cancelled")
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(Fore.RED + f"Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(Fore.RED + f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise




class HelpMenuComponent:
    """Base component for the help menu."""

    def display(self) -> str:
        """Return the help menu text."""
        raise NotImplementedError


class BasicHelpMenu(HelpMenuComponent):
    """Provide the standard calculator commands."""

    def display(self) -> str:
        return (
            "  history - Show calculation history\n"
            "  clear - Clear calculation history\n"
            "  undo - Undo the last calculation\n"
            "  redo - Redo the last undone calculation\n"
            "  save - Save calculation history to file\n"
            "  load - Load calculation history from file\n"
            "  exit - Exit the calculator\n"
        )


class HelpMenuDecorator(HelpMenuComponent):
    """Base decorator for extending a help menu."""

    def __init__(self, help_menu: HelpMenuComponent):
        self._help_menu = help_menu

    def display(self) -> str:
        return self._help_menu.display()


class OperationHelpDecorator(HelpMenuDecorator):
    """Add registered operations to the existing help menu."""

    def display(self) -> str:
        help_text = super().display()
        operations = OperationFactory.get_available_operations()

        # Add registered operations before the other commands
        return (
            f"  {', '.join(operations)} - Perform calculations\n"
            + help_text
        )