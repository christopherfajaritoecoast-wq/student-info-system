"""Student data model."""

from dataclasses import dataclass, asdict


@dataclass
class Student:
    """Represents a single student record."""

    student_id: str
    first_name: str
    last_name: str
    age: int
    course: str
    year_level: str
    middle_name: str = ""
    gender: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""

    def to_dict(self):
        """Convert the student to a dictionary (ready for JSON)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Create a Student from a dictionary.

        Raises:
            ValueError: if required fields are missing or data is not a dict.
        """
        if not isinstance(data, dict):
            raise ValueError("Student record must be a JSON object.")
        required = ["student_id", "first_name", "last_name", "age", "course", "year_level"]
        missing = [f for f in required if f not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        return cls(
            student_id=str(data["student_id"]).strip(),
            first_name=str(data["first_name"]).strip(),
            last_name=str(data["last_name"]).strip(),
            age=int(data["age"]),
            course=str(data["course"]).strip(),
            year_level=str(data["year_level"]).strip(),
            middle_name=str(data.get("middle_name", "")).strip(),
            gender=str(data.get("gender", "")).strip(),
            email=str(data.get("email", "")).strip(),
            phone=str(data.get("phone", "")).strip(),
            address=str(data.get("address", "")).strip(),
        )

    @property
    def full_name(self):
        """Return 'First Middle Last' (middle name optional)."""
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p)

    def __str__(self):
        return f"{self.student_id} - {self.full_name} ({self.course}, {self.year_level})"
