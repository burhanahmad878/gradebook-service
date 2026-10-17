"""Unit tests for student percentage calculation (pct)."""

import gradebook


def test_student_with_no_marks_has_zero_percent(loaded: dict) -> None:
    """A student with no marks should have a percentage of 0."""
    result = gradebook.pct("S1")
    assert result == "0"


def test_mark_of_15_out_of_20_on_weight_10_gives_7_5(loaded: dict) -> None:
    """A mark of 15/20 on an assessment weighing 10 should give 7.5."""
    loaded["marks"].append({"student": "S1", "assessment": "A1", "score": 15})
    result = gradebook.pct("S1")
    assert result == "7.5"


def test_mark_for_unknown_assessment_is_ignored(loaded: dict) -> None:
    """Marks tied to an unknown assessment ID should be ignored."""
    loaded["marks"].append({"student": "S1", "assessment": "GHOST", "score": 15})
    result = gradebook.pct("S1")
    assert result == "0"