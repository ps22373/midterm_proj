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

## Installation

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

---

## Configuration

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

