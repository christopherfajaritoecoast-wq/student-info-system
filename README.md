# \# Student Information System

# 

# \## Description

# 

# A command-line application for managing student records. Users can add, view, find, update, delete, and search students through a simple menu. All data is stored in a JSON file, so records remain available after the program is restarted.

# 

# The project is written in Python 3 using only the standard library. It is designed as a clean and modular example for a college programming and cloud computing exam.

# 

# \## Objectives

# 

# This project demonstrates:

# 

# \* CRUD operations (Create, Read, Update, Delete)

# \* JSON data persistence

# \* Modular architecture using models, services, and utilities

# \* Configuration management using an external configuration file

# \* Error handling

# \* Logging

# \* GitHub version control and feature branching

# 

# \## Features

# 

# \* Add a student with validation for ID, names, age, course, year level, email, and phone

# \* Prevent duplicate student IDs using case-insensitive checking

# \* View all students in a formatted table

# \* View complete details of one student by ID

# \* Update a student while allowing the user to press Enter to keep an existing value

# \* Delete a student with Y/N confirmation

# \* Search students by ID, first name, last name, course, or email

# \* Case-insensitive search

# \* Export all records to CSV

# \* Load and validate settings from `config/config.json`

# \* Log application activities to `logs/application.log`

# \* Handle missing data files

# \* Recover from corrupted JSON files

# \* Skip and log invalid records

# \* Use atomic file saving to reduce the risk of incomplete data files

# \* 22 unit tests using Python's `unittest` framework

# \* Tests use isolated temporary data

# 

# \## Technologies Used

# 

# \* Python 3

# \* JSON

# \* Git

# \* GitHub

# \* VS Code

# \* Python Standard Library

# 

# \## Project Structure

# 

# ```text

# student-info-system/

# ├── src/

# │   ├── models/

# │   │   ├── \_\_init\_\_.py

# │   │   └── student.py            # Student dataclass

# │   ├── services/

# │   │   ├── \_\_init\_\_.py

# │   │   └── student\_service.py    # CRUD, search, export, JSON storage

# │   ├── utils/

# │   │   ├── \_\_init\_\_.py

# │   │   ├── config\_manager.py     # Loads and validates config.json

# │   │   ├── logger.py             # Logging setup

# │   │   └── validators.py         # Input validation

# │   ├── \_\_init\_\_.py               # Makes src importable as a package

# │   └── main.py                   # Command-line menu

# ├── data/

# │   └── students.json             # Persistent student data

# ├── config/

# │   └── config.json               # Application settings

# ├── logs/

# │   └── .gitkeep                  # Keeps the folder in Git

# ├── tests/

# │   ├── \_\_init\_\_.py

# │   └── test\_student\_service.py

# ├── README.md

# ├── SUBMISSION\_DOCUMENT.md        # Template for the Word/PDF submission

# ├── requirements.txt

# ├── .gitignore

# └── run.py                        # Application launcher

# ```

# 

# Two small additions beyond the required layout are `src/\_\_init\_\_.py`, which allows reliable package imports, and `SUBMISSION\_DOCUMENT.md`, which is included for the required Word/PDF submission.

# 

# \## Installation

# 

# \### Requirements

# 

# \* Python 3.8 or newer

# \* Git

# \* VS Code or another code editor

# 

# No external Python packages are required because the project uses the Python standard library.

# 

# \### Clone the Repository

# 

# ```bash

# git clone <repository-url>

# cd student-info-system

# ```

# 

# Replace `<repository-url>` with the URL of the GitHub repository.

# 

# \## Running the Application

# 

# From the project root, run:

# 

# ```bash

# python run.py

# ```

# 

# On some systems, the command may be:

# 

# ```bash

# python3 run.py

# ```

# 

# If using VS Code, open the project folder, open the integrated terminal, and run the same command.

# 

# \## Running Tests

# 

# Run the following command from the project root:

# 

# ```bash

# python -m unittest discover tests

# ```

# 

# The project currently has 22 unit tests covering CRUD operations, JSON persistence, search, validation, error recovery, and CSV export.

# 

# The latest test result was:

# 

# ```text

# Ran 22 tests in 0.174s

# 

# OK

# ```

# 

# The tests use temporary data, so the actual `data/students.json` file is not modified during testing.

# 

# \## Data Storage

# 

# Student records are stored as a JSON array in:

# 

# ```text

# data/students.json

# ```

# 

# Every add, update, and delete operation is saved immediately.

# 

# If the data file is missing, the application creates an empty data file. If the JSON file is corrupted, it is renamed with a timestamp and a fresh data file is created so the original corrupted file is not silently lost.

# 

# Records with missing or invalid fields are skipped and logged.

# 

# The application also uses atomic saving by writing to a temporary file before replacing the original file. This helps reduce the risk of a partially written data file.

# 

# \## Configuration

# 

# Application settings are stored in:

# 

# ```text

# config/config.json

# ```

# 

# The main settings include:

# 

# | Setting     | Purpose                             |

# | ----------- | ----------------------------------- |

# | `app\_name`  | Title shown in the application menu |

# | `data\_file` | Path to the student JSON file       |

# | `log\_file`  | Path to the application log         |

# | `min\_age`   | Smallest accepted student age       |

# | `max\_age`   | Largest accepted student age        |

# 

# Paths are relative to the project root.

# 

# The `ConfigManager` validates the configuration file and reports an error if the file is missing, contains invalid JSON, or contains invalid values, such as a minimum age that is greater than the maximum age.

# 

# \## Logging

# 

# Application logs are written to:

# 

# ```text

# logs/application.log

# ```

# 

# Example:

# 

# ```text

# 2026-10-03 10:30:15 - INFO - Student STU-0001 added successfully.

# ```

# 

# The logging system records important application activities, including:

# 

# \* Application startup and shutdown

# \* Student creation

# \* Student updates

# \* Student deletion

# \* Searches

# \* Invalid input

# \* File errors

# \* JSON errors

# \* Unexpected exceptions

# 

# Log files are ignored by Git, while the `.gitkeep` file keeps the `logs` directory in the repository.

# 

# \## GitHub Workflow

# 

# The project uses Git for version control and GitHub for repository hosting.

# 

# \### Repository

# 

# The GitHub repository is named:

# 

# ```text

# student-info-system

# ```

# 

# The project uses:

# 

# \* `main` for the main version of the project

# \* `feature/student-crud` for feature development

# 

# \### Feature Branch

# 

# The main feature branch used during development is:

# 

# ```text

# feature/student-crud

# ```

# 

# The feature branch was used to develop and test the student CRUD functionality before being pushed to GitHub.

# 

# \### Git Commands Used

# 

# Some of the Git commands used during development include:

# 

# ```bash

# git status

# git log --oneline --decorate --graph --all

# git branch -a

# git remote -v

# git add .

# git commit -m "Meaningful commit message"

# git push -u origin feature/student-crud

# ```

# 

# \### Current Commit History

# 

# The project currently includes meaningful commits such as:

# 

# ```text

# Improve student update handling

# Initial project setup

# ```

# 

# The `feature/student-crud` branch has been pushed to the GitHub repository.

# 

# The feature branch will be merged into `main` after the final testing and documentation checks are completed.

# 

# \## Challenges Faced

# 

# One challenge was making sure that updating a student would not accidentally remove information when the user wanted to keep an existing value. This was handled by allowing the user to press Enter to keep the current value.

# 

# Another challenge was testing the system without changing the actual student data. The unit tests were designed to use temporary data so that the main JSON file remains safe during testing.

# 

# I also had to learn how to use Git branches and GitHub while developing the project. I used the `feature/student-crud` branch for development, committed the changes, and pushed the branch to GitHub.

# 

# Another challenge was checking the Git status and commit history before pushing the project. This helped make sure that the correct files were committed and that the working directory was clean.

# 

# Testing was also an important part of the project. The system was tested using 22 unit tests, and all 22 tests passed successfully.

# 

# \## Future Improvements

# 

# Possible future improvements include:

# 

# \* Import students from CSV

# \* Sort students by name, course, or year level

# \* Add pagination for long student lists

# \* Add grades, subjects, and enrollment records

# \* Create a simple GUI or web interface

# \* Store student records in a database once the exam restriction no longer applies

# 

# \## Project Status

# 

# The Student Information System currently supports CRUD operations, JSON persistence, validation, search, CSV export, configuration management, error handling, logging, and automated unit testing.

# 

# The latest test run completed successfully with:

# 

# ```text

# 22 tests passed

# ```

# 

# The project is also connected to GitHub and uses the `feature/student-crud` branch for development.



