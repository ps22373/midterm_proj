# Enhanced Calculator Command-Line Application

A Python-based command-line calculator demonstrating object-oriented programming, software design patterns, robust input validation, calculation history, file persistence, logging, automated testing, and continuous integration.

## Project Overview

The Enhanced Calculator Command-Line Application is an interactive calculator developed in Python using the Read-Eval-Print Loop (REPL) pattern. Users can perform mathematical operations, inspect calculation history, undo and redo calculations, and save or load historical results.

The application emphasizes maintainable software design by separating calculations, operations, configuration, history, validation, and user interaction into individual modules. It also incorporates custom exceptions, configurable application settings, logging, and automated testing.

Two optional features are included: a dynamically generated help menu implemented with the Decorator Design Pattern and color-coded terminal output implemented with Colorama.

## Features

- Arithmetic Operations: addition, subtraction, multiplication, division, powers, root, modulus, integer division, percentage calculation, and absolute difference
- Interactive Command-Line Interface: A REPL interface with a built-in help menu
- Dynamic Help Menu: automatically lists registered mathematical operations
- Color-Coded Output: uses terminal colors to distinguish results, errors, and warnings
- Input Validation: validates numerical inputs and enforces configured input limits
- Custom Exception Handling: provides meaningful error messages for invalid inputs and calculation failures
- Calculation History: displays and clears recorded calculations
- Undo and Redo: supports reverting and restoring calculation state using the Memento pattern
- Automatic History Saving: uses an observer to save calculation history after new calculations
- CSV Persistence: uses pandas to save and load calculation records
- Logging: records calculation activity and application errors
- Environment-Based Configuration: uses a .env file for configurable application settings
- Automated Testing: uses pytest and pytest-cov to test functionality and measure code coverage
- Continuous Integration: rRuns automated tests through GitHub Actions on pushes and pull requests targeting main

## Tools and Libraries

The project dependencies and their pinned versions are maintained in requirements.txt.

