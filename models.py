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


def parse_number(raw: Any, field: str) -> float:
    """Safely convert raw input into a finite float."""
    if isinstance(raw, bool) or raw is None or isinstance(raw, (list, dict)):
        raise ValidationError(f"Field '{field}' must be a valid number.")

    try:
        val = float(raw)
    except (ValueError, TypeError):
        raise ValidationError(f"Field '{field}' must be a valid number.") from None

    if not math.isfinite(val):
        raise ValidationError(f"Field '{field}' must be a finite number.")

    return val


def parse_text(raw: Any, field: str) -> str:
    """Safely convert raw input into a stripped, non-blank string."""
    if not isinstance(raw, str):
        raise ValidationError(f"Field '{field}' must be a text string.")

    cleaned = raw.strip()
    if not cleaned:
        raise ValidationError(f"Field '{field}' cannot be empty.")

    return cleaned


def parse_student(payload: Any) -> Student:
    """Parse and validate a Student request dictionary."""
    if not isinstance(payload, dict):
        raise ValidationError("Payload must be a JSON object.")

    if "id" not in payload or "name" not in payload:
        raise ValidationError("Missing required student fields ('id', 'name').")

    return Student(
        id=parse_text(payload["id"], "id"),
        name=parse_text(payload["name"], "name"),
    )


def parse_assessment(payload: Any) -> Assessment:
    """Parse and validate an Assessment request dictionary."""
    if not isinstance(payload, dict):
        raise ValidationError("Payload must be a JSON object.")

    required = ["id", "title", "weight", "total"]
    for field in required:
        if field not in payload:
            raise ValidationError(f"Missing required assessment field '{field}'.")

    return Assessment(
        id=parse_text(payload["id"], "id"),
        title=parse_text(payload["title"], "title"),
        weight=parse_number(payload["weight"], "weight"),
        total=parse_number(payload["total"], "total"),
    )


def parse_mark(payload: Any) -> Mark:
    """Parse and validate a Mark request dictionary."""
    if not isinstance(payload, dict):
        raise ValidationError("Payload must be a JSON object.")

    required = ["student", "assessment", "score"]
    for field in required:
        if field not in payload:
            raise ValidationError(f"Missing required mark field '{field}'.")

    return Mark(
        student=parse_text(payload["student"], "student"),
        assessment=parse_text(payload["assessment"], "assessment"),
        score=parse_number(payload["score"], "score"),
    )