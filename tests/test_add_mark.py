"""Unit tests for the add_mark seam function."""

from unittest.mock import Mock
import pytest
from errors import NotFoundError, ValidationError
from gradebook import add_mark
from models import Mark


def fixed_now() -> str:
    """Provide a fixed timestamp for testing."""
    return "2026-10-12 09:00:00"


def test_valid_mark_is_stored_with_the_time(state: dict) -> None:
    """A valid mark should be recorded along with the current timestamp."""
    save = Mock()
    add_mark(state, Mark("S1", "A1", 15.0), fixed_now, save)
    assert state["marks"] == [
        {"student": "S1", "assessment": "A1", "score": 15.0, "at": "2026-10-12 09:00:00"}
    ]


def test_valid_mark_calls_save_once(state: dict) -> None:
    """Adding a valid mark must trigger saving the gradebook state exactly once."""
    save = Mock()
    add_mark(state, Mark("S1", "A1", 15.0), fixed_now, save)
    save.assert_called_once_with()


@pytest.mark.parametrize(
    ("mark", "error"),
    [
        pytest.param(Mark("NOPE", "A1", 5.0), NotFoundError, id="unknown-student"),
        pytest.param(Mark("S1", "GHOST", 5.0), NotFoundError, id="unknown-assessment"),
        pytest.param(Mark("S1", "A1", 21.0), ValidationError, id="score-above-total"),
    ],
)
def test_rejected_mark_changes_nothing(state: dict, mark: Mark, error: type[Exception]) -> None:
    """Invalid marks should raise an error, mutate nothing, and never save."""
    save = Mock()
    with pytest.raises(error):
        add_mark(state, mark, fixed_now, save)
    assert state["marks"] == []
    save.assert_not_called()