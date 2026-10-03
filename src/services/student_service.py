"""Business logic for managing students, backed by a JSON file."""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

from src.models.student import Student
from src.utils.logger import get_logger
from src.utils.validators import validate_student_data


class StudentServiceError(Exception):
    """Base class for service-level errors."""


class StudentValidationError(StudentServiceError):
    """Raised when student data fails validation. ``errors`` lists the problems."""

    def __init__(self, errors):
        self.errors = errors
        super().__init__("; ".join(errors))


class DuplicateStudentError(StudentServiceError):
    """Raised when a student ID already exists."""


class StudentNotFoundError(StudentServiceError):
    """Raised when a student ID does not exist."""


class StorageError(StudentServiceError):
    """Raised when the data file cannot be read or written."""


class StudentService:
    """CRUD, search and export operations for students."""

    SEARCH_FIELDS = ("student_id", "first_name", "last_name", "course", "email")
    UPDATABLE_FIELDS = (
        "first_name", "middle_name", "last_name", "age", "gender",
        "course", "year_level", "email", "phone", "address",
    )

    def __init__(self, data_file, min_age=1, max_age=100):
        self.data_file = Path(data_file)
        self.min_age = min_age
        self.max_age = max_age
        self.logger = get_logger()

    # ------------------------------------------------------------------
    # Storage helpers
    # ------------------------------------------------------------------
    def _load_students(self):
        """Read all students from the JSON file.

        - Missing file  -> create an empty file.
        - Corrupted JSON -> back up the bad file, start with an empty list.
        - Invalid records -> skipped and logged.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            self.logger.warning("Data file %s not found. Creating a new one.", self.data_file)
            self._save_students([])
            return []
        except json.JSONDecodeError as exc:
            self.logger.error("Corrupted JSON in %s: %s", self.data_file, exc)
            self._backup_corrupted_file()
            self._save_students([])
            return []
        except PermissionError as exc:
            self.logger.error("Permission denied reading %s: %s", self.data_file, exc)
            raise StorageError(f"No permission to read {self.data_file}.") from exc
        except OSError as exc:
            self.logger.error("Could not read %s: %s", self.data_file, exc)
            raise StorageError(f"Could not read data file: {exc}") from exc

        if not isinstance(raw, list):
            self.logger.error("Data file %s must contain a JSON array.", self.data_file)
            self._backup_corrupted_file()
            self._save_students([])
            return []

        students = []
        for index, record in enumerate(raw):
            try:
                students.append(Student.from_dict(record))
            except (ValueError, TypeError) as exc:
                self.logger.warning("Skipping invalid record #%d: %s", index, exc)
        return students

    def _backup_corrupted_file(self):
        """Rename a corrupted data file so the user's data is not lost."""
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = self.data_file.with_name(f"{self.data_file.name}.corrupt-{stamp}")
        try:
            os.replace(self.data_file, backup)
            self.logger.warning("Corrupted file backed up to %s", backup)
        except OSError as exc:
            self.logger.error("Could not back up corrupted file: %s", exc)

    def _save_students(self, students):
        """Write students to JSON atomically (temp file, then replace)."""
        temp_file = self.data_file.with_suffix(".tmp")
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in students], f, indent=4, ensure_ascii=False)
            os.replace(temp_file, self.data_file)
        except PermissionError as exc:
            self.logger.error("Permission denied writing %s: %s", self.data_file, exc)
            raise StorageError(f"No permission to write {self.data_file}.") from exc
        except OSError as exc:
            self.logger.error("Could not write %s: %s", self.data_file, exc)
            raise StorageError(f"Could not save data: {exc}") from exc

    @staticmethod
    def _clean(data):
        """Strip whitespace from string values."""
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

    def _find_index(self, students, student_id):
        wanted = student_id.strip().lower()
        for i, student in enumerate(students):
            if student.student_id.lower() == wanted:
                return i
        return -1

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def add_student(self, data):
        """Validate and add a new student. Returns the created Student."""
        data = self._clean(data)
        errors = validate_student_data(data, self.min_age, self.max_age)
        if errors:
            self.logger.warning("Invalid student data rejected: %s", "; ".join(errors))
            raise StudentValidationError(errors)

        students = self._load_students()
        if self._find_index(students, data["student_id"]) != -1:
            self.logger.warning("Duplicate student ID rejected: %s", data["student_id"])
            raise DuplicateStudentError(f"Student ID {data['student_id']} already exists.")

        student = Student.from_dict(data)
        students.append(student)
        self._save_students(students)
        self.logger.info("Student %s added successfully.", student.student_id)
        return student

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def get_all_students(self):
        """Return a list of all students."""
        return self._load_students()

    def get_student_by_id(self, student_id):
        """Return the Student with the given ID, or raise StudentNotFoundError."""
        students = self._load_students()
        index = self._find_index(students, student_id)
        if index == -1:
            self.logger.warning("Student %s not found.", student_id)
            raise StudentNotFoundError("Student not found.")
        return students[index]

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update_student(self, student_id, changes):
        """Apply ``changes`` (dict of field -> new value). Returns the updated Student.

        The student ID itself cannot be changed.
        """
        students = self._load_students()
        index = self._find_index(students, student_id)
        if index == -1:
            self.logger.warning("Update failed: student %s not found.", student_id)
            raise StudentNotFoundError("Student not found.")

        merged = students[index].to_dict()
        merged.update({k: v for k, v in self._clean(changes).items() if k in self.UPDATABLE_FIELDS})

        errors = validate_student_data(merged, self.min_age, self.max_age)
        if errors:
            self.logger.warning("Invalid update for %s: %s", student_id, "; ".join(errors))
            raise StudentValidationError(errors)

        students[index] = Student.from_dict(merged)
        self._save_students(students)
        self.logger.info("Student %s updated successfully.", students[index].student_id)
        return students[index]

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete_student(self, student_id):
        """Delete a student. Returns the removed Student."""
        students = self._load_students()
        index = self._find_index(students, student_id)
        if index == -1:
            self.logger.warning("Delete failed: student %s not found.", student_id)
            raise StudentNotFoundError("Student not found.")
        removed = students.pop(index)
        self._save_students(students)
        self.logger.info("Student %s deleted successfully.", removed.student_id)
        return removed

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    def search_students(self, keyword):
        """Case-insensitive search across ID, names, course and email."""
        keyword = keyword.strip().lower()
        if not keyword:
            return []
        results = [
            s for s in self._load_students()
            if any(keyword in str(getattr(s, field)).lower() for field in self.SEARCH_FIELDS)
        ]
        self.logger.info("Search for '%s' returned %d result(s).", keyword, len(results))
        return results

    # ------------------------------------------------------------------
    # EXPORT (bonus)
    # ------------------------------------------------------------------
    def export_to_csv(self, csv_path):
        """Export all students to a CSV file. Returns the number of rows written."""
        students = self._load_students()
        fieldnames = list(Student.__dataclass_fields__.keys())
        try:
            csv_path = Path(csv_path)
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(s.to_dict() for s in students)
        except (OSError, PermissionError) as exc:
            self.logger.error("CSV export failed: %s", exc)
            raise StorageError(f"Could not export CSV: {exc}") from exc
        self.logger.info("Exported %d student(s) to %s.", len(students), csv_path)
        return len(students)
