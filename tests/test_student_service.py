"""Unit tests for StudentService.

Every test uses its own temporary folder, so the real data/students.json
is never touched.
"""

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from src.services.student_service import (
    DuplicateStudentError,
    StudentNotFoundError,
    StudentService,
    StudentValidationError,
)
from src.utils.logger import setup_logger


def make_student(student_id="STU-0001", **overrides):
    data = {
        "student_id": student_id,
        "first_name": "Juan",
        "middle_name": "Dela",
        "last_name": "Cruz",
        "age": 20,
        "gender": "Male",
        "course": "BS Information Technology",
        "year_level": "2nd Year",
        "email": "juan.cruz@example.com",
        "phone": "09123456789",
        "address": "Binalonan, Pangasinan",
    }
    data.update(overrides)
    return data


class StudentServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.data_file = self.temp_dir / "students.json"
        self.data_file.write_text("[]", encoding="utf-8")
        setup_logger(self.temp_dir / "test.log")
        self.service = StudentService(self.data_file, min_age=1, max_age=100)

    def tearDown(self):
        # Close log handlers so the temp folder can be removed on Windows.
        import logging
        logger = logging.getLogger("student_info_system")
        for handler in list(logger.handlers):
            handler.close()
            logger.removeHandler(handler)
        shutil.rmtree(self.temp_dir, ignore_errors=True)


class TestAddAndRead(StudentServiceTestCase):
    def test_add_student_saves_to_json(self):
        self.service.add_student(make_student())
        saved = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["student_id"], "STU-0001")

    def test_get_all_students(self):
        self.service.add_student(make_student("STU-0001"))
        self.service.add_student(make_student("STU-0002", first_name="Maria", last_name="Santos"))
        self.assertEqual(len(self.service.get_all_students()), 2)

    def test_get_student_by_id_is_case_insensitive(self):
        self.service.add_student(make_student())
        self.assertEqual(self.service.get_student_by_id("stu-0001").first_name, "Juan")

    def test_get_missing_student_raises(self):
        with self.assertRaises(StudentNotFoundError):
            self.service.get_student_by_id("STU-9999")

    def test_data_persists_between_service_instances(self):
        self.service.add_student(make_student())
        new_service = StudentService(self.data_file)
        self.assertEqual(len(new_service.get_all_students()), 1)


class TestSearch(StudentServiceTestCase):
    def setUp(self):
        super().setUp()
        self.service.add_student(make_student("STU-0001"))
        self.service.add_student(make_student(
            "STU-0002", first_name="Maria", middle_name="", last_name="Santos",
            course="BS Computer Science", email="maria.santos@example.com"))

    def test_search_by_last_name_case_insensitive(self):
        results = self.service.search_students("SANTOS")
        self.assertEqual([s.student_id for s in results], ["STU-0002"])

    def test_search_by_course(self):
        self.assertEqual(len(self.service.search_students("computer")), 1)

    def test_search_by_email_and_id(self):
        self.assertEqual(len(self.service.search_students("juan.cruz@")), 1)
        self.assertEqual(len(self.service.search_students("stu-0002")), 1)

    def test_search_no_match_and_empty_keyword(self):
        self.assertEqual(self.service.search_students("zzz"), [])
        self.assertEqual(self.service.search_students("   "), [])


class TestUpdateDelete(StudentServiceTestCase):
    def setUp(self):
        super().setUp()
        self.service.add_student(make_student())

    def test_update_student_changes_only_given_fields(self):
        updated = self.service.update_student("STU-0001", {"age": 21, "year_level": "3rd Year"})
        self.assertEqual(updated.age, 21)
        self.assertEqual(updated.first_name, "Juan")
        self.assertEqual(self.service.get_student_by_id("STU-0001").year_level, "3rd Year")

    def test_update_cannot_change_student_id(self):
        self.service.update_student("STU-0001", {"student_id": "STU-7777"})
        self.assertEqual(self.service.get_all_students()[0].student_id, "STU-0001")

    def test_update_missing_student_raises(self):
        with self.assertRaises(StudentNotFoundError):
            self.service.update_student("STU-9999", {"age": 30})

    def test_update_with_invalid_data_is_rejected_and_not_saved(self):
        with self.assertRaises(StudentValidationError):
            self.service.update_student("STU-0001", {"age": 500})
        self.assertEqual(self.service.get_student_by_id("STU-0001").age, 20)

    def test_delete_student(self):
        self.service.delete_student("STU-0001")
        self.assertEqual(self.service.get_all_students(), [])

    def test_delete_missing_student_raises(self):
        with self.assertRaises(StudentNotFoundError):
            self.service.delete_student("STU-9999")


class TestValidationAndErrors(StudentServiceTestCase):
    def test_duplicate_student_id_rejected(self):
        self.service.add_student(make_student())
        with self.assertRaises(DuplicateStudentError):
            self.service.add_student(make_student(first_name="Other"))
        self.assertEqual(len(self.service.get_all_students()), 1)

    def test_duplicate_id_check_ignores_case(self):
        self.service.add_student(make_student("STU-0001"))
        with self.assertRaises(DuplicateStudentError):
            self.service.add_student(make_student("stu-0001"))

    def test_invalid_data_rejected(self):
        bad_inputs = [
            {"student_id": ""},
            {"first_name": ""},
            {"last_name": "  "},
            {"age": "abc"},
            {"age": 0},
            {"age": 101},
            {"email": "not-an-email"},
            {"phone": "12ab"},
            {"course": ""},
            {"year_level": ""},
        ]
        for overrides in bad_inputs:
            with self.subTest(overrides=overrides):
                with self.assertRaises(StudentValidationError):
                    self.service.add_student(make_student(**overrides))
        self.assertEqual(self.service.get_all_students(), [])

    def test_missing_file_is_recreated(self):
        self.data_file.unlink()
        self.assertEqual(self.service.get_all_students(), [])
        self.assertTrue(self.data_file.exists())

    def test_corrupted_json_is_backed_up_and_reset(self):
        self.data_file.write_text("{ this is not json", encoding="utf-8")
        self.assertEqual(self.service.get_all_students(), [])
        backups = list(self.temp_dir.glob("students.json.corrupt-*"))
        self.assertEqual(len(backups), 1)
        self.service.add_student(make_student())  # service is usable again
        self.assertEqual(len(self.service.get_all_students()), 1)

    def test_invalid_records_are_skipped(self):
        records = [make_student("STU-0001"), {"student_id": "STU-0002"}, "garbage"]
        self.data_file.write_text(json.dumps(records), encoding="utf-8")
        students = self.service.get_all_students()
        self.assertEqual([s.student_id for s in students], ["STU-0001"])


class TestExport(StudentServiceTestCase):
    def test_export_to_csv(self):
        self.service.add_student(make_student())
        out = self.temp_dir / "export.csv"
        self.assertEqual(self.service.export_to_csv(out), 1)
        with open(out, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["student_id"], "STU-0001")


if __name__ == "__main__":
    unittest.main()
