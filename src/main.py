"""Command-line interface for the Student Information System."""

import sys
from pathlib import Path

# Allow running this file directly as well as through run.py.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.services.student_service import (  # noqa: E402
    DuplicateStudentError,
    StorageError,
    StudentNotFoundError,
    StudentService,
    StudentServiceError,
    StudentValidationError,
)
from src.utils import validators  # noqa: E402
from src.utils.config_manager import ConfigError, ConfigManager  # noqa: E402
from src.utils.logger import get_logger, setup_logger  # noqa: E402

LINE = "=" * 41
THIN_LINE = "-" * 75


# ----------------------------------------------------------------------
# Display helpers
# ----------------------------------------------------------------------
def print_header(title):
    print(f"\n{LINE}\n{title.center(41)}\n{LINE}")


def print_menu(app_name):
    print_header(app_name.upper())
    print("\n[1] Add Student")
    print("[2] View Students")
    print("[3] Find Student")
    print("[4] Update Student")
    print("[5] Delete Student")
    print("[6] Search Students")
    print("[7] Exit\n")


def _short(text, width):
    return text if len(text) <= width else text[: width - 3] + "..."


def print_student_table(students):
    """Print students as a compact table."""
    if not students:
        print("\nNo students found.")
        return
    print(THIN_LINE)
    print(f"{'ID':<10} {'Name':<26} {'Course':<26} {'Year':<10}")
    print(THIN_LINE)
    for s in students:
        print(f"{_short(s.student_id, 10):<10} {_short(s.full_name, 26):<26} "
              f"{_short(s.course, 26):<26} {_short(s.year_level, 10):<10}")
    print(THIN_LINE)
    print(f"Total: {len(students)} student(s)")


def print_student_details(student):
    """Print every field of one student."""
    print(f"\n{THIN_LINE}")
    for label, value in [
        ("Student ID", student.student_id),
        ("First Name", student.first_name),
        ("Middle Name", student.middle_name),
        ("Last Name", student.last_name),
        ("Age", student.age),
        ("Gender", student.gender),
        ("Course", student.course),
        ("Year Level", student.year_level),
        ("Email", student.email),
        ("Phone", student.phone),
        ("Address", student.address),
    ]:
        print(f"{label:<12}: {value}")
    print(THIN_LINE)


# ----------------------------------------------------------------------
# Input helpers
# ----------------------------------------------------------------------
def ask(prompt, validator=None, default=None):
    """Ask until the answer passes ``validator`` (returns (ok, message)).

    If ``default`` is given, pressing Enter keeps it (used for updates).
    """
    while True:
        suffix = f" [{default}]" if default not in (None, "") else ""
        answer = input(f"{prompt}{suffix}: ").strip()
        if not answer and default is not None:
            return str(default)
        if validator is None:
            return answer
        ok, message = validator(answer)
        if ok:
            return answer
        get_logger().warning("Invalid input for '%s': %s", prompt, message)
        print(f"  [!] {message} Please try again.")


def confirm(question):
    while True:
        answer = input(f"{question}\n(Y/N): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  [!] Please enter Y or N.")


# ----------------------------------------------------------------------
# Menu actions
# ----------------------------------------------------------------------
def add_student(service):
    print_header("ADD STUDENT")

    def unique_id(value):
        ok, msg = validators.validate_student_id(value)
        if not ok:
            return ok, msg
        try:
            service.get_student_by_id(value)
        except StudentNotFoundError:
            return True, ""
        return False, f"Student ID {value} already exists."

    data = {
        "student_id": ask("Student ID (e.g. STU-0002)", unique_id),
        "first_name": ask("First Name", lambda v: validators.validate_name(v, "First name")),
        "middle_name": ask("Middle Name (optional)", lambda v: validators.validate_name(v, "Middle name", False)),
        "last_name": ask("Last Name", lambda v: validators.validate_name(v, "Last name")),
        "age": ask("Age", lambda v: validators.validate_age(v, service.min_age, service.max_age)),
        "gender": ask("Gender (optional)"),
        "course": ask("Course", lambda v: validators.validate_not_empty(v, "Course")),
        "year_level": ask("Year Level (e.g. 2nd Year)", lambda v: validators.validate_not_empty(v, "Year level")),
        "email": ask("Email (optional)", validators.validate_email),
        "phone": ask("Phone (optional)", validators.validate_phone),
        "address": ask("Address (optional)"),
    }
    student = service.add_student(data)
    print(f"\nStudent added successfully!\n\nStudent ID: {student.student_id}")


def view_students(service):
    print_header("ALL STUDENTS")
    students = service.get_all_students()
    print_student_table(students)
    if students and confirm("\nExport these records to a CSV file?"):
        export_csv(service)


def find_student(service):
    print_header("FIND STUDENT")
    student_id = ask("Enter Student ID", lambda v: validators.validate_not_empty(v, "Student ID"))
    print_student_details(service.get_student_by_id(student_id))


def update_student(service):
    print_header("UPDATE STUDENT")
    student_id = ask("Enter Student ID to update", lambda v: validators.validate_not_empty(v, "Student ID"))
    current = service.get_student_by_id(student_id)
    print_student_details(current)
    print("Press Enter to keep the current value.\n")

    changes = {
        "first_name": ask("First Name", lambda v: validators.validate_name(v, "First name"), current.first_name),
        "middle_name": ask("Middle Name", lambda v: validators.validate_name(v, "Middle name", False), current.middle_name),
        "last_name": ask("Last Name", lambda v: validators.validate_name(v, "Last name"), current.last_name),
        "age": ask("Age", lambda v: validators.validate_age(v, service.min_age, service.max_age), current.age),
        "gender": ask("Gender", None, current.gender),
        "course": ask("Course", lambda v: validators.validate_not_empty(v, "Course"), current.course),
        "year_level": ask("Year Level", lambda v: validators.validate_not_empty(v, "Year level"), current.year_level),
        "email": ask("Email", validators.validate_email, current.email),
        "phone": ask("Phone", validators.validate_phone, current.phone),
        "address": ask("Address", None, current.address),
    }
    updated = service.update_student(current.student_id, changes)
    print("\nStudent updated successfully!")
    print_student_details(updated)


def delete_student(service):
    print_header("DELETE STUDENT")
    student_id = ask("Enter Student ID to delete", lambda v: validators.validate_not_empty(v, "Student ID"))
    student = service.get_student_by_id(student_id)
    print_student_details(student)
    if confirm(f"Are you sure you want to delete student {student.student_id}?"):
        service.delete_student(student.student_id)
        print(f"\nStudent {student.student_id} deleted successfully.")
    else:
        print("\nDeletion cancelled.")


def search_students(service):
    print_header("SEARCH STUDENTS")
    print("Searches Student ID, first name, last name, course and email.")
    keyword = ask("Search students", lambda v: validators.validate_not_empty(v, "Search text"))
    print_student_table(service.search_students(keyword))


def export_csv(service):
    path = ask("CSV file name", None, "data/students_export.csv")
    count = service.export_to_csv(path)
    print(f"\nExported {count} student(s) to {path}")


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------
ACTIONS = {
    "1": add_student,
    "2": view_students,
    "3": find_student,
    "4": update_student,
    "5": delete_student,
    "6": search_students,
}


def run_action(action, service, logger):
    """Run one menu action, turning errors into friendly messages."""
    try:
        action(service)
    except StudentValidationError as exc:
        for error in exc.errors:
            print(f"  [!] {error}")
    except (DuplicateStudentError, StudentNotFoundError) as exc:
        print(f"\n  [!] {exc}")
    except StorageError as exc:
        print(f"\n  [!] Storage problem: {exc}")
    except StudentServiceError as exc:
        print(f"\n  [!] {exc}")
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperation cancelled.")
    except ValueError as exc:
        logger.error("Value error: %s", exc)
        print(f"\n  [!] Invalid value: {exc}")
    except Exception as exc:  # last-resort handler so the app never crashes
        logger.exception("Unexpected error: %s", exc)
        print("\n  [!] An unexpected error occurred. Details were saved to the log file.")


def main():
    try:
        config = ConfigManager()
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 1

    logger = setup_logger(config.log_file)
    logger.info("Application started.")
    service = StudentService(config.data_file, config.min_age, config.max_age)

    try:
        while True:
            print_menu(config.app_name)
            try:
                choice = input("Choose an option: ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                break
            if choice == "7":
                break
            action = ACTIONS.get(choice)
            if action is None:
                logger.warning("Invalid menu choice: %r", choice)
                print("\n  [!] Invalid option. Please choose a number from 1 to 7.")
                continue
            run_action(action, service, logger)
            try:
                input("\nPress Enter to return to the main menu...")
            except (KeyboardInterrupt, EOFError):
                print()
                break
    except Exception as exc:
        logger.critical("Fatal error: %s", exc, exc_info=True)
        print("A fatal error occurred. See logs/application.log.")
        return 1

    logger.info("Application closed.")
    print("\nThank you for using the Student Information System. Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
