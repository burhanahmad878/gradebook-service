"""Unit tests for student percentage calculation via get_student."""

import gradebook


def test_student_with_no_marks_has_zero_percent(loaded: dict) -> None:
    """A student with no marks should have a percentage of 0."""
    result = gradebook.get_student("S1")
    assert result["percentage"] == "0"


def test_mark_of_15_out_of_20_on_weight_10_gives_7_5(loaded: dict) -> None:
    """A mark of 15/20 should calculate the correct weighted percentage."""
    loaded["marks"].append({"student": "S1", "assessment": "A1", "score": 15})
    result = gradebook.get_student("S1")
    assert result["percentage"] == "7.5"


def test_mark_for_unknown_assessment_is_ignored(loaded: dict) -> None:
    """Marks tied to an unknown assessment ID should be ignored."""
    loaded["marks"].append({"student": "S1", "assessment": "GHOST", "score": 15})
    result = gradebook.get_student("S1")
    assert result["percentage"] == "0"