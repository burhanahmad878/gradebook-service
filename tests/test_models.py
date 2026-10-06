"""Unit tests for models and parsers."""

import pytest
from errors import ValidationError
from models import Assessment, parse_assessment, parse_number, parse_student


def test_parse_number_valid_numeric_string() -> None:
    """Accept numeric string input."""
    assert parse_number("10.5", "score") == 10.5


def test_parse_number_rejects_invalid_types() -> None:
    """Reject booleans, text, and non-finite numbers."""
    with pytest.raises(ValidationError):
        parse_number(True, "score")
    with pytest.raises(ValidationError):
        parse_number("abc", "score")
    with pytest.raises(ValidationError):
        parse_number("nan", "score")


def test_assessment_zero_total_rejected() -> None:
    """Reject zero or negative total."""
    with pytest.raises(ValidationError):
        Assessment(id="A1", title="Quiz", weight=10.0, total=0.0)


def test_mark_negative_score_rejected() -> None:
    """Reject negative scores."""
    with pytest.raises(ValidationError):
        parse_assessment({"id": "A1", "title": "Quiz", "weight": -5.0, "total": 10.0})


def test_parse_student_missing_field() -> None:
    """Reject missing fields or non-dict payloads."""
    with pytest.raises(ValidationError):
        parse_student({"id": "S1"})
    with pytest.raises(ValidationError):
        parse_student("not a dict")


def test_parse_assessment_valid() -> None:
    """Successfully parse a valid assessment object."""
    asm = parse_assessment({"id": "A1", "title": "Quiz 1", "weight": "20", "total": "100"})
    assert asm.id == "A1"
    assert asm.title == "Quiz 1"
    assert asm.weight == 20.0
    assert asm.total == 100.0