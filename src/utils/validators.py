"""Input validation helpers.

Each validator returns (is_valid, message). ``message`` is empty when valid.
"""

import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9]{7,15}$")
NAME_PATTERN = re.compile(r"^[A-Za-zÀ-ÿ\s.'-]+$")


def validate_not_empty(value, field_name):
    if value is None or not str(value).strip():
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_student_id(student_id):
    ok, msg = validate_not_empty(student_id, "Student ID")
    if not ok:
        return ok, msg
    if " " in student_id.strip():
        return False, "Student ID must not contain spaces."
    return True, ""


def validate_name(value, field_name, required=True):
    if not str(value).strip():
        if required:
            return False, f"{field_name} cannot be empty."
        return True, ""
    if not NAME_PATTERN.match(value.strip()):
        return False, f"{field_name} may only contain letters, spaces, . ' and -."
    return True, ""


def validate_age(value, min_age, max_age):
    try:
        age = int(str(value).strip())
    except ValueError:
        return False, "Age must be a whole number."
    if age < min_age or age > max_age:
        return False, f"Age must be between {min_age} and {max_age}."
    return True, ""


def validate_email(email, required=False):
    if not email.strip():
        return (False, "Email cannot be empty.") if required else (True, "")
    if not EMAIL_PATTERN.match(email.strip()):
        return False, "Email format is invalid (example: name@example.com)."
    return True, ""


def validate_phone(phone, required=False):
    cleaned = phone.strip().replace(" ", "").replace("-", "")
    if not cleaned:
        return (False, "Phone cannot be empty.") if required else (True, "")
    if not PHONE_PATTERN.match(cleaned):
        return False, "Phone must contain 7-15 digits (optional leading +)."
    return True, ""


def validate_student_data(data, min_age, max_age):
    """Validate a whole student dictionary. Returns a list of error messages."""
    errors = []
    checks = [
        validate_student_id(str(data.get("student_id", ""))),
        validate_name(str(data.get("first_name", "")), "First name"),
        validate_name(str(data.get("middle_name", "")), "Middle name", required=False),
        validate_name(str(data.get("last_name", "")), "Last name"),
        validate_age(data.get("age", ""), min_age, max_age),
        validate_not_empty(data.get("course", ""), "Course"),
        validate_not_empty(data.get("year_level", ""), "Year level"),
        validate_email(str(data.get("email", ""))),
        validate_phone(str(data.get("phone", ""))),
    ]
    for ok, msg in checks:
        if not ok:
            errors.append(msg)
    return errors
