"""Application state with Jazz sync."""
from datetime import datetime
from typing import List, Dict, Any

import reflex as rx
import logging

logger = logging.getLogger(__name__)


# Type alias for note dictionaries
NoteDict = Dict[str, Any]


class AppState(rx.State):
    """Main application state."""

    # UI State
    notes: List[NoteDict] = []
    new_note_title: str = ""
    new_note_content: str = ""
    jazz_initialized: bool = False
    sync_status: str = "initializing"

    @rx.var
    def notes_count(self) -> int:
        """Get total notes count."""
        return len(self.notes)

    @rx.var
    def completed_count(self) -> int:
        """Get completed notes count."""
        return sum(1 for note in self.notes if note.get("completed", False))

    @rx.var
    def active_count(self) -> int:
        """Get active notes count."""
        return self.notes_count - self.completed_count

    @rx.var
    def can_add_note(self) -> bool:
        """Check if can add note."""
        return len(self.new_note_title.strip()) > 0

    def set_new_note_title(self, value: str):
        """Set new note title."""
        self.new_note_title = value

    def set_new_note_content(self, value: str):
        """Set new note content."""
        self.new_note_content = value

    async def initialize_jazz(self) -> None:
        """Initialize Jazz system."""
        try:
            logger.info("Initializing Jazz...")
            # In a real implementation, this would initialize Jazz
            # For this template, we'll simulate it
            import asyncio
            await asyncio.sleep(0.5)
            async with self:
                self.jazz_initialized = True
                self.sync_status = "connected"
            logger.info("✅ Jazz initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Jazz: {e}")
            async with self:
                self.sync_status = "error"

    def add_note(self) -> None:
        """Add a new note."""
        if not self.can_add_note:
            return

        try:
            # Create note object
            note: NoteDict = {
                "id": len(self.notes) + 1,
                "title": self.new_note_title.strip(),
                "content": self.new_note_content.strip(),
                "completed": False,
                "created_at": datetime.now().isoformat(),
            }

            # Create new list to trigger state update (in real app, this would save to Jazz)
            self.notes = self.notes + [note]

            # Reset form
            self.new_note_title = ""
            self.new_note_content = ""
            logger.info(f"Added note: {note['title']}")
        except Exception as e:
            logger.error(f"Failed to add note: {e}")

    def toggle_note(self, note_id: int):
        """Toggle note completion status."""
        try:
            self.notes = [
                {**note, "completed": not note.get("completed", False)} if note["id"] == note_id else note
                for note in self.notes
            ]
            logger.info(f"Toggled note: {note_id}")
        except Exception as e:
            logger.error(f"Failed to toggle note {note_id}: {e}")

    def delete_note(self, note_id: int):
        """Delete a note."""
        try:
            self.notes = [n for n in self.notes if n["id"] != note_id]
            logger.info(f"Deleted note: {note_id}")
        except Exception as e:
            logger.error(f"Failed to delete note {note_id}: {e}")

    def on_load(self) -> None:
        """Handle page load."""
        return AppState.initialize_jazz
