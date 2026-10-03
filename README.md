# Student Information System

## Description

A command-line application for managing student records. Users can add, view, find, update, delete and search students through a simple menu. All data is stored in a JSON file, so records are still there after the program is restarted.

The project is written in Python 3 using only the standard library and is designed as a clean, modular example for a college programming / cloud computing exam.

## Objectives

This project demonstrates:

- CRUD operations (Create, Read, Update, Delete)
- JSON data persistence
- Modular architecture (models, services, utilities)
- Configuration management (settings kept outside the code)
- Error handling
- Logging
- GitHub version control

## Features

- Add a student with full validation (ID, names, age, course, year level, email, phone)
- Prevent duplicate student IDs (case-insensitive)
- View all students in a formatted table
- View complete details of one student by ID
- Update a student; press Enter to keep a field unchanged
- Delete a student with a Y/N confirmation
- Case-insensitive search by ID, first name, last name, course or email
- Export all records to CSV (bonus, offered after "View Students")
- Settings loaded and validated from `config/config.json`
- Logging to `logs/application.log` (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Recovery from a missing data file, corrupted JSON and invalid records
- Atomic saves (write to a temp file, then replace) to avoid half-written data
- 22 unit tests using `unittest` with isolated temporary data

## Technologies Used

- Python 3
- JSON
- Git
- GitHub
- VS Code

## Project Structure

```
student-info-system/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py            # Student dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── student_service.py    # CRUD, search, export, JSON storage
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config_manager.py     # Loads/validates config.json
│   │   ├── logger.py             # Logging setup
│   │   └── validators.py         # Input validation
│   ├── __init__.py               # Makes `src` importable as a package
│   └── main.py                   # Command-line menu
├── data/
│   └── students.json             # Persistent student data
├── config/
│   └── config.json               # Application settings
├── logs/
│   └── .gitkeep                  # Keeps the folder in Git
├── tests/
│   ├── __init__.py
│   └── test_student_service.py
├── README.md
├── SUBMISSION_DOCUMENT.md        # Template for the Word/PDF submission
├── requirements.txt
├── .gitignore
└── run.py                        # Launcher
```

Two small additions beyond the required layout: `src/__init__.py` (so `from src...` imports work reliably) and `SUBMISSION_DOCUMENT.md` (requested by the exam).

## Installation

Requirements: Python 3.8 or newer and Git. No packages need to be installed.

```bash
git clone <repository-url>
cd student-info-system
```

Replace `<repository-url>` with the URL of your own GitHub repository.

## Running the Application

From the project root:

```bash
python run.py
```

On some systems the command is `python3 run.py`. In VS Code, open the project folder, open the integrated terminal (`Ctrl + ~`) and run the same command.

## Running Tests

```bash
python -m unittest discover tests
```

Tests use a temporary folder, so your real `data/students.json` is never modified.

## Data Storage

Student records are stored as a JSON array in `data/students.json`. Every add, update and delete is saved immediately. If the file is missing, an empty one is created. If it contains corrupted JSON, it is renamed to `students.json.corrupt-<timestamp>` and a fresh file is started, so nothing is silently lost. Records with missing fields are skipped and logged.

## Configuration

Settings live in `config/config.json`:

| Setting     | Purpose                                  |
|-------------|------------------------------------------|
| `app_name`  | Title shown in the menu                  |
| `data_file` | Path to the student JSON file            |
| `log_file`  | Path to the log file                     |
| `min_age`   | Smallest age accepted                    |
| `max_age`   | Largest age accepted                     |

Paths are relative to the project root. `ConfigManager` reports a clear error if the file is missing, is not valid JSON, or contains invalid values (for example `min_age` greater than `max_age`).

## Logging

Logs are written to `logs/application.log` in this format:

```
2026-10-03 10:30:15 - INFO - Student STU-0001 added successfully.
```

Logged events include startup and shutdown, students added/updated/deleted, searches, invalid input, file errors, JSON errors and unexpected exceptions. Log files are ignored by Git; the `logs/` folder is kept with `.gitkeep`.

## GitHub Workflow

### 1. Create the GitHub repository
On github.com click **New repository**, name it `student-info-system`, and do not add a README (the project already has one).

### 2. Initialize Git
```bash
git init
git branch -M main
```

### 3. Connect the local repository
```bash
git remote add origin https://github.com/<your-username>/student-info-system.git
```

### 4. Commit changes
```bash
git add .
git commit -m "Initial project setup"
```
Use short, meaningful messages. A suggested commit sequence:

1. Initial project setup
2. Create Student model
3. Implement JSON data persistence
4. Implement CRUD operations
5. Add input validation
6. Add configuration management
7. Add logging system
8. Add search functionality
9. Add unit tests
10. Improve README documentation
11. Final project cleanup

### 5. Push to GitHub
```bash
git push -u origin main
```

### 6. Create branches
Recommended branches: `main`, `feature/student-crud`, `feature/validation`, `feature/logging`, `feature/testing`, `feature/documentation`.

```bash
git checkout -b feature/student-crud
# ...make changes...
git add .
git commit -m "Implement CRUD operations"
git push -u origin feature/student-crud
```

### 7. Merge changes
```bash
git checkout main
git merge feature/student-crud
git push origin main
```
Alternatively, open a Pull Request on GitHub from the feature branch into `main` and click **Merge pull request**.

## Challenges Faced

*(Write your own experience here after completing the project, for example problems you ran into while setting up Git, running the tests, or pushing to GitHub, and how you solved them.)*

## Future Improvements

- Import students from CSV
- Sort students by name, course or year level
- Pagination for long student lists
- Grades, subjects and enrollment records
- A simple GUI or web interface
- Store data in a database once the exam restriction no longer applies
