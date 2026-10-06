"""Data models and parser functions for the gradebook service."""

import math
from dataclasses import dataclass
from typing import Any
from errors import ValidationError


@dataclass(frozen=True)
class Student:
    """Represents a student in the gradebook."""

    id: str
    name: str

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValidationError("Student id cannot be empty.")
        if not self.name or not self.name.strip():
            raise ValidationError("Student name cannot be empty.")


@dataclass(frozen=True)
class Assessment:
    """Represents an assessment in the gradebook."""

    id: str
    title: str
    weight: float
    total: float

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValidationError("Assessment id cannot be empty.")
        if not self.title or not self.title.strip():
            raise ValidationError("Assessment title cannot be empty.")
        if not (0.0 <= self.weight <= 100.0):
            raise ValidationError("Assessment weight must be between 0 and 100.")
        if self.total <= 0.0:
            raise ValidationError("Assessment total must be greater than 0.")


@dataclass(frozen=True)
class Mark:
    """Represents a mark recorded for a student on an assessment."""

    student: str
    assessment: str
    score: float

    def __post_init__(self) -> None:
        if not self.student or not self.student.strip():
            raise ValidationError("Mark student id cannot be empty.")
        if not self.assessment or not self.assessment.strip():
            raise ValidationError("Mark assessment id cannot be empty.")
        if self.score < 0.0:
            raise ValidationError("Mark score cannot be negative.")