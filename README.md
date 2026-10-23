
# HeavyTech Diagnostics

A Python-based service report management application for heavy construction equipment.

## Overview

HeavyTech Diagnostics is a beginner software development project designed to organize equipment service records and simplify basic maintenance tracking.

The application uses Python for its logic and SQLite for persistent data storage.

## Features

- Create equipment service reports
- Record equipment model and serial number
- Store service dates, engine hours, and reported problems
- Calculate the next service point based on the configured service interval
- Track maintenance status and service urgency
- Search for reports by serial number
- View service history for specific equipment
- Search reports by problem keywords
- Store records in a local SQLite database

## Technologies

- **Python** — application logic and input validation
- **SQLite** — local database storage
- **SQL** — database queries and record management
- **Git and GitHub** — version control and project hosting

## Requirements

- Python 3.10 or newer
- No external Python packages are required

## How to Run

1. Download or clone this repository.
2. Open the project folder in a terminal.
3. Run the application:

   ```bash
   python heavytech.py
   ```

4. Follow the instructions displayed in the terminal.

The application creates its local database automatically when it is first launched.

## Database

The application stores service reports in a local SQLite database.

The database file is generated locally and is excluded from version control. This keeps local service records separate from the public source code.

## Project Scope and Limitations

HeavyTech Diagnostics is a service record management application, not a real-time diagnostic scanner.

It does not currently connect to equipment ECUs, CAN bus networks, or diagnostic adapters.

Service interval calculations are based on configurable application logic and should be verified against the relevant equipment manufacturer's maintenance documentation before real-world use.

## Learning Objectives

This project demonstrates practical experience with:

- Python functions and control flow
- Input validation and exception handling
- SQLite database operations
- SQL queries and filtering
- Organizing and documenting a software project

## Future Improvements

Potential future development includes:

- Exporting service reports to CSV or PDF
- Adding equipment-specific maintenance schedules
- Building a graphical user interface
- Adding CAN bus data support after compatible hardware and protocols are verified

## Author

A beginner developer with a background in heavy equipment maintenance, exploring software development and equipment diagnostics.
