# Enhanced Calculator Command-Line Application

A Python-based command-line calculator demonstrating object-oriented programming, software design patterns, robust input validation, calculation history, file persistence, logging, automated testing, and continuous integration.

## Project Overview

The Enhanced Calculator Command-Line Application is an interactive calculator developed in Python using the Read-Eval-Print Loop (REPL) pattern. Users can perform mathematical operations, inspect calculation history, undo and redo calculations, and save or load historical results.

The application emphasizes maintainable software design by separating calculations, operations, configuration, history, validation, and user interaction into individual modules. It also incorporates custom exceptions, configurable application settings, logging, and automated testing.

Two optional features are included: a dynamically generated help menu implemented with the Decorator Design Pattern and color-coded terminal output implemented with Colorama.

## Features

- **Arithmetic Operations**: addition, subtraction, multiplication, division, powers, root, modulus, integer division, percentage calculation, and absolute difference
- **Interactive Command-Line Interface**: A REPL interface with a built-in help menu
- **Dynamic Help Menu**: automatically lists registered mathematical operations
- **Color-Coded Output**: uses terminal colors to distinguish results, errors, and warnings
- **Input Validation**: validates numerical inputs and enforces configured input limits
- **Custom Exception Handling**: provides meaningful error messages for invalid inputs and calculation failures
- **Calculation History**: displays and clears recorded calculations
- **Undo and Redo**: supports reverting and restoring calculation state using the Memento pattern
- **Automatic History Saving**: uses an observer to save calculation history after new calculations
- **CSV Persistence**: uses pandas to save and load calculation records
- **Logging**: records calculation activity and application errors
- **Environment-Based Configuration**: uses a .env file for configurable application settings
- **Automated Testing**: uses pytest and pytest-cov to test functionality and measure code coverage
- **Continuous Integration**: rRuns automated tests through GitHub Actions on pushes and pull requests targeting main

## Installation Instructions

### Clone the Project
Clone your GitHub repository, replacing the placeholder with your repository URL:

```bash
git clone <repository-url>
cd midterm_proj
```

If you already have the project locally, navigate to its root directory:

```bash
cd ~/projects/midterm_proj
```
---
### Install Python 3.10+

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```
---
### Create a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```
---
### Install Packages/Dependencies

```bash
pip install -r requirements.txt
```

---
### Configure Environment Variables
Create a .env file in the project root. The next section explains the available configuration options.

---
### Run the Calculator
Start the application from the project root:
```bash
python main.py
```
The application displays a startup message and prompts you to enter a command.


## Configuration Setup

The application uses the python-dotenv package to load settings from a .env file. Configuration is managed by app/calculator_config.py, which provides default values when environment variables are not supplied.

### Creating the .env file
Create a file named .env in the project root with the following settings:
```bash
# Base Directories
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=1000000
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8

# Other Settings
# CALCULATOR_HISTORY_FILE=calculator_history.csv
# CALCULATOR_LOG_FILE=calculator.log
```

### Environment variables

| Variable                   | Description           | Example           |
| -------------------------- | --------------------- | ------------------|
| CALCULATOR_LOG_DIR | Directory for application log files | logs |
| CALCULATOR_HISTORY_DIR | Directory for calculation history | history |
| CALCULATOR_MAX_HISTORY_SIZE | Configured maximum history size | 1000000 |
| CALCULATOR_AUTO_SAVE | Enables automatic history saving when set to true or 1 | true |
| CALCULATOR_PRECISION | Calculation precision setting | 10000 |
| CALCULATOR_MAX_INPUT_VALUE | Maximum permitted input value | 1000000 |
| CALCULATOR_DEFAULT_ENCODING | Default text-file encoding | utf-8 |
| CALCULATOR_HISTORY_FILE | Optional explicit history file path | calculator_history.csv |
| CALCULATOR_LOG_FILE | Optional explicit log file path | calculator.log |


The default history and log file locations are:
```bash
history/calculator_history.csv
logs/calculator.log
```
The optional CALCULATOR_HISTORY_FILE and CALCULATOR_LOG_FILE variables can override the default file paths. If you do not need custom paths, leave these variables unset so the application uses its default locations.

### Configuration Considerations

- Use true or 1 to enable automatic saving; use false to disable it.
- Set the maximum input value according to the range of numbers the application should accept.
- Use a positive precision value and a positive maximum history size.
- Keep .env in the project root so the application can load it during startup.
- Do not commit local environment configuration to a public repository. Ensure .env is listed in .gitignore if it contains machine-specific settings.


## Usage Guide

### Starting the Application

Run:
```bash
python main.py
```

The calculator starts in an interactive session:
```bash
Calculator started. Type 'help' for commands.

Enter command:
```
Enter one command at a time. For mathematical operations, the application prompts for two numerical inputs.

### Viewing Available Commands

Enter
```bash
help
```
The help menu lists the registered mathematical operations and the supported application commands. The operation list is generated dynamically, so newly registered operations can appear without manually adding each operation to the base help menu.

### Performing a Calculation

For example, to add two numbers:
```bash
Enter command: add

Enter numbers (or 'cancel' to abort):
First number: 5
Second number: 3

Result: 8
```

To calculate a percentage:
```bash
Enter command: percent

Enter numbers (or 'cancel' to abort):
First number: 25
Second number: 200

Result: 12.5
```

If you enter ***cancel*** at either number prompt, the current operation is aborted.

### Mathematical Operations Avaliable

| Command | Description |
| ------- | ----------- |
| add | Adds two numbers| 
| subtract | Subtracts the second number from the first |
| multiply | Multiplies two numbers |
| divide | Divides the first number by the second |
| power | Raises the first number to the power of the second |
| root | Calculates the nth root of a number |
| modulus | Compute the remainder of the division of two numbers |
| int_divide | Perform division that results in an integer quotient, discarding any fractional part |
| percent | Calculate the percentage of one number with respect to another (e.g., Percentage(a, b) computes (a / b) * 100) |
| abs_diff | Calculate the absolute difference between two numbers |

Each operation accepts two numerical inputs. Invalid operations and unsupported inputs are handled through the application's validation and exception-handling mechanisms.

### Application Commands

| Command | Description |
| ------- | ----------- |
| help | Displays available operations and application commands |
| history | Displays calculation history |
| clear | Clears calculation history |
| undo | Undoes the most recent calculation |
| redo | Redoes the most recently undone calculation |
| save | Saves calculation history to CSV |
| load | Loads calculation history from CSV |
| exit | Attempts to save history before exiting |

### Undo and Redo
The undo command reverts the most recent calculation and updates the calculator's state. The redo command restores a calculation that was previously undone.

For example:
1. Perform an addition.
2. Enter undo to revert the most recent calculation.
3. Enter redo to restore the undone calculation.

If no operation is available to undo or redo, the calculator displays a warning rather than treating the situation as a successful operation.

### Color-Coded Output
Colorama improves terminal readability by distinguishing different message types:
- **Cyan:** Application startup message and help menu.
- **Green:** Successful calculation results and successful history actions.
- **Yellow:** Warnings, unknown commands, and unavailable undo or redo actions.
- **Red:** Calculation errors, validation errors, and save/load errors.

Color-coded output is an optional enhancement included in this project.

## Testing Instructions

The project uses pytest for unit testing and pytest-cov for coverage measurement. The test suite includes coverage for calculations, operations, configuration, exceptions, history, undo/redo, and input validation.

Run commands from the project root with the virtual environment activated.

### Run All Tests
```bash
pytest
```
This executes the configured test suite.

### Measure Code Coverage
```bash
pytest --cov=app
```
This reports the percentage of application code executed during the test run.

### Display Uncovered Lines
```bash
pytest --cov=app --cov-report=term-missing
```
The report identifies executable lines that were not covered by tests.

### Generate HTML Report
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```
Open htmlcov/index.html in a browser to explore coverage by file and line.

### Enforce the 90% coverage requirement
```bash
pytest --cov=app --cov-fail-under=90
```
The command exits unsuccessfully if overall application coverage is below 90%, allowing coverage requirements to be enforced automatically.

Tests covers normal operation, edge cases, invalid input, and error-handling behavior. Coverage exclusions should be used only for intentionally excluded code, not to avoid testing meaningful application logic.

## CI/CD Information

This project uses GitHub Actions to automate testing and help maintain code quality. The workflow runs automatically whenever code is pushed to the main branch or when a pull request is opened targeting main.

### Workflow Process

1. **Checkout Code:** Retrieves the latest version of the project repository.

2. **Set Up Python:** Configures the environment to use Python 3.12.

3. **Install Dependencies:** Installs the packages listed in requirements.txt, along with the testing and code coverage tools.

4. **Run Automated Tests:** Executes the test suite using pytest and measures code coverage with pytest-cov.

5. **Enforce Coverage Requirement:** Requires at least 90% code coverage. If the tests fail or coverage falls below this threshold, the workflow fails.

### Purpose

The GitHub Actions workflow helps identify errors early, verifies that changes do not break existing functionality, and ensures that the project maintains the required test coverage. Automating these checks supports reliable development and helps maintain the overall quality and stability of the calculator application.

**Workflow file:** *.github/workflows/tests.yml*