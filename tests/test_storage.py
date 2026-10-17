"""Unit tests for gradebook file storage (load/save)."""

import json
import pytest
import gradebook


@pytest.fixture
def data_file(tmp_path: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch) -> object:
    """Provide a temporary gradebook.json file path."""
    path = tmp_path / "gradebook.json"
    monkeypatch.setattr(gradebook, "DATA", str(path))
    return path


def test_saved_gradebook_loads_back_unchanged(data_file: object, state: dict, monkeypatch: pytest.MonkeyPatch) -> None:
    """Saving and loading state should preserve data accurately."""
    monkeypatch.setattr(gradebook, "STATE", state)
    gradebook.save()
    monkeypatch.setattr(gradebook, "STATE", {})
    gradebook.load()
    assert gradebook.STATE == state


def test_missing_file_gives_an_empty_gradebook(data_file: object, monkeypatch: pytest.MonkeyPatch) -> None:
    """Loading when the data file is missing initializes an empty state."""
    monkeypatch.setattr(gradebook, "STATE", {})
    gradebook.load()
    assert gradebook.STATE == {"students": {}, "assessments": {}, "marks": []}


def test_corrupt_file_stops_loading_with_a_json_error(data_file: object) -> None:
    """Loading a malformed JSON file should raise a JSONDecodeError."""
    data_file.write_text("{bad", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        gradebook.load()