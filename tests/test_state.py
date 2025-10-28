"""Tests for application state."""
import pytest
from app.state import AppState


class TestAppState:
    """Test AppState functionality."""

    def test_initial_state(self):
        """Test initial state values."""
        state = AppState()
        assert state.notes == []
        assert state.new_note_title == ""
        assert state.new_note_content == ""
        assert state.jazz_initialized is False
        assert state.sync_status == "initializing"

    def test_notes_count(self):
        """Test notes_count computed var."""
        state = AppState()
        assert state.notes_count == 0

        state.notes = [
            {"id": 1, "title": "Test", "completed": False},
            {"id": 2, "title": "Test 2", "completed": True},
        ]
        assert state.notes_count == 2

    def test_completed_count(self):
        """Test completed_count computed var."""
        state = AppState()
        state.notes = [
            {"id": 1, "title": "Test 1", "completed": False},
            {"id": 2, "title": "Test 2", "completed": True},
            {"id": 3, "title": "Test 3", "completed": True},
        ]
        assert state.completed_count == 2

    def test_can_add_note(self):
        """Test can_add_note computed var."""
        state = AppState()
        assert state.can_add_note is False

        state.new_note_title = "   "
        assert state.can_add_note is False

        state.new_note_title = "Valid Title"
        assert state.can_add_note is True

    def test_set_new_note_title(self):
        """Test setting note title."""
        state = AppState()
        state.set_new_note_title("New Title")
        assert state.new_note_title == "New Title"

    def test_set_new_note_content(self):
        """Test setting note content."""
        state = AppState()
        state.set_new_note_content("New Content")
        assert state.new_note_content == "New Content"

    def test_add_note(self):
        """Test adding a note."""
        state = AppState()
        state.new_note_title = "Test Note"
        state.new_note_content = "Test Content"

        state.add_note()

        assert len(state.notes) == 1
        assert state.notes[0]["title"] == "Test Note"
        assert state.notes[0]["content"] == "Test Content"
        assert state.notes[0]["completed"] is False
        assert state.new_note_title == ""
        assert state.new_note_content == ""

    def test_add_note_empty_title(self):
        """Test adding note with empty title is blocked."""
        state = AppState()
        state.new_note_title = ""

        state.add_note()

        assert len(state.notes) == 0

    def test_toggle_note(self):
        """Test toggling note completion."""
        state = AppState()
        state.notes = [
            {"id": 1, "title": "Test", "completed": False},
            {"id": 2, "title": "Test 2", "completed": False},
        ]

        state.toggle_note(1)

        assert state.notes[0]["completed"] is True
        assert state.notes[1]["completed"] is False

        # Toggle again
        state.toggle_note(1)
        assert state.notes[0]["completed"] is False

    def test_toggle_note_creates_new_list(self):
        """Test that toggle_note creates new list (not mutation)."""
        state = AppState()
        original_note = {"id": 1, "title": "Test", "completed": False}
        state.notes = [original_note]

        state.toggle_note(1)

        # Original dict should not be mutated
        assert original_note["completed"] is False
        # State should have new list with new dict
        assert state.notes[0]["completed"] is True
        assert state.notes[0] is not original_note

    def test_delete_note(self):
        """Test deleting a note."""
        state = AppState()
        state.notes = [
            {"id": 1, "title": "Test 1", "completed": False},
            {"id": 2, "title": "Test 2", "completed": False},
            {"id": 3, "title": "Test 3", "completed": False},
        ]

        state.delete_note(2)

        assert len(state.notes) == 2
        assert all(note["id"] != 2 for note in state.notes)

    def test_delete_nonexistent_note(self):
        """Test deleting note that doesn't exist."""
        state = AppState()
        state.notes = [
            {"id": 1, "title": "Test", "completed": False},
        ]

        state.delete_note(999)

        assert len(state.notes) == 1


@pytest.mark.asyncio
async def test_initialize_jazz():
    """Test Jazz initialization."""
    state = AppState()
    assert state.jazz_initialized is False

    # Note: This would need proper async context in real Reflex app
    # Just testing the logic exists
    assert hasattr(state, 'initialize_jazz')
    assert state.sync_status == "initializing"
