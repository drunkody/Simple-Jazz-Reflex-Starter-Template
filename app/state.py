"""Application state with Jazz sync."""
import reflex as rx
from typing import List
import logging

logger = logging.getLogger(__name__)

class AppState(rx.State):
    """Main application state."""

    # UI State
    notes: List[dict] = []
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
    def can_add_note(self) -> bool:
        """Check if can add note."""
        return len(self.new_note_title.strip()) > 0

    @rx.event
    def set_new_note_title(self, value: str):
        """Set new note title."""
        self.new_note_title = value

    @rx.event
    def set_new_note_content(self, value: str):
        """Set new note content."""
        self.new_note_content = value

    @rx.event(background=True)
    async def initialize_jazz(self):
        """Initialize Jazz system."""
        async with self:
            logger.info("Initializing Jazz...")
            # In a real implementation, this would initialize Jazz
            # For this template, we'll simulate it
            import asyncio
            await asyncio.sleep(0.5)
            self.jazz_initialized = True
            self.sync_status = "connected"
            logger.info("✅ Jazz initialized")

    @rx.event
    def add_note(self):
        """Add a new note."""
        if not self.can_add_note:
            return

        # Create note object
        import datetime
        note = {
            "id": len(self.notes) + 1,
            "title": self.new_note_title,
            "content": self.new_note_content,
            "completed": False,
            "created_at": datetime.datetime.now().isoformat(),
        }

        # Create new list to trigger state update (in real app, this would save to Jazz)
        self.notes = self.notes + [note]

        # Reset form
        self.new_note_title = ""
        self.new_note_content = ""
        logger.info(f"Added note: {note['title']}")

    @rx.event
    def toggle_note(self, note_id: int):
        """Toggle note completion status."""
        self.notes = [
            {**note, "completed": not note.get("completed", False)} if note["id"] == note_id else note
            for note in self.notes
        ]

    @rx.event
    def delete_note(self, note_id: int):
        """Delete a note."""
        self.notes = [n for n in self.notes if n["id"] != note_id]
        logger.info(f"Deleted note: {note_id}")

    @rx.event
    async def on_load(self):
        """Handle page load."""
        yield AppState.initialize_jazz
