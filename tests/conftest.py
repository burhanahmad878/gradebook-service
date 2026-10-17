"""Shared pytest fixtures for gradebook tests."""

import pytest
import gradebook


@pytest.fixture
def state() -> dict:
    """Provide a standard fake gradebook state."""
    return {
        "students": {"S1": {"id": "S1", "name": "Ayesha"}},
        "assessments": {
            "A1": {"id": "A1", "title": "Quiz 1", "weight": 10, "total": 20},
            "A2": {"id": "A2", "title": "Midterm", "weight": 30, "total": 50},
        },
        "marks": [],
    }


@pytest.fixture
def loaded(state: dict, monkeypatch: pytest.MonkeyPatch) -> dict:
    """Monkeypatch gradebook.STATE with the fake state fixture."""
    monkeypatch.setattr(gradebook, "STATE", state)
    return state