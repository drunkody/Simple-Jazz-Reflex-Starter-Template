"""Main application with Jazz sync."""
import reflex as rx
from app.state import AppState
from config import config

def header() -> rx.Component:
    """App header with sync status."""
    return rx.box(
        rx.hstack(
            rx.heading(
                "🎺 Jazz Notes",
                size="7",
                class_name="font-bold",
            ),
            rx.badge(
                rx.cond(
                    AppState.jazz_initialized,
                    "🟢 Synced",
                    "🟡 Initializing..."
                ),
                color_scheme=rx.cond(
                    AppState.jazz_initialized, "green", "yellow"
                ),
                variant="soft",
            ),
            rx.spacer(),
            rx.text(
                f"{AppState.notes_count} notes",
                class_name="text-gray-600",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        class_name="bg-white border-b p-4 shadow-sm",
    )

def note_input() -> rx.Component:
    """Note input form."""
    return rx.box(
        rx.vstack(
            rx.input(
                placeholder="Note title...",
                value=AppState.new_note_title,
                on_change=AppState.set_new_note_title,
                size="3",
                class_name="w-full",
            ),
            rx.text_area(
                placeholder="Note content (optional)...",
                value=AppState.new_note_content,
                on_change=AppState.set_new_note_content,
                rows="3",
                class_name="w-full",
            ),
            rx.button(
                rx.icon("plus", size=18),
                " Add Note",
                on_click=AppState.add_note,
                disabled=~AppState.can_add_note,
                size="3",
                class_name="w-full",
            ),
            spacing="3",
            width="100%",
        ),
        class_name="bg-white p-4 rounded-lg shadow-sm border",
    )

def note_card(note: dict) -> rx.Component:
    """Individual note card."""
    note_id = note["id"]
    return rx.box(
        rx.hstack(
            rx.checkbox(
                checked=note["completed"],
                on_change=AppState.toggle_note(note_id),
                size="2",
            ),
            rx.vstack(
                rx.text(
                    note["title"],
                    class_name=rx.cond(
                        note["completed"],
                        "line-through text-gray-400 font-medium",
                        "font-medium",
                    ),
                ),
                rx.cond(
                    note["content"] != "",
                    rx.text(
                        note["content"],
                        class_name="text-sm text-gray-600",
                    ),
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            rx.icon_button(
                rx.icon("trash-2", size=16),
                on_click=AppState.delete_note(note_id),
                variant="ghost",
                color_scheme="red",
                size="1",
            ),
            align="center",
            width="100%",
        ),
        class_name="bg-white p-4 rounded-lg shadow-sm border hover:shadow-md transition-shadow",
    )

def notes_list() -> rx.Component:
    """List of notes."""
    return rx.cond(
        AppState.notes_count > 0,
        rx.vstack(
            rx.foreach(AppState.notes, note_card),
            spacing="3",
            width="100%",
        ),
        rx.box(
            rx.vstack(
                rx.icon("inbox", size=48, class_name="text-gray-300"),
                rx.text(
                    "No notes yet",
                    class_name="text-gray-500 text-lg",
                ),
                rx.text(
                    "Add your first note above to get started",
                    class_name="text-gray-400 text-sm",
                ),
                spacing="2",
                align="center",
            ),
            class_name="bg-gray-50 p-12 rounded-lg border-2 border-dashed border-gray-200 text-center",
        ),
    )

def stats() -> rx.Component:
    """Stats section."""
    return rx.hstack(
        rx.box(
            rx.vstack(
                rx.text("Total", class_name="text-sm text-gray-600"),
                rx.text(
                    AppState.notes_count,
                    class_name="text-2xl font-bold text-blue-600",
                ),
                spacing="1",
            ),
            class_name="bg-blue-50 p-4 rounded-lg flex-1",
        ),
        rx.box(
            rx.vstack(
                rx.text("Completed", class_name="text-sm text-gray-600"),
                rx.text(
                    AppState.completed_count,
                    class_name="text-2xl font-bold text-green-600",
                ),
                spacing="1",
            ),
            class_name="bg-green-50 p-4 rounded-lg flex-1",
        ),
        rx.box(
            rx.vstack(
                rx.text("Active", class_name="text-sm text-gray-600"),
                rx.text(
                    AppState.notes_count - AppState.completed_count,
                    class_name="text-2xl font-bold text-orange-600",
                ),
                spacing="1",
            ),
            class_name="bg-orange-50 p-4 rounded-lg flex-1",
        ),
        spacing="4",
        width="100%",
    )

def info_box() -> rx.Component:
    """Info box about Jazz."""
    return rx.box(
        rx.hstack(
            rx.icon("info", size=20, class_name="text-blue-600"),
            rx.vstack(
                rx.text(
                    "💡 No Backend Required!",
                    class_name="font-semibold text-sm",
                ),
                rx.text(
                    "Your notes are stored with Jazz CRDTs and sync automatically across devices. Works offline too!",
                    class_name="text-xs text-gray-600",
                ),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="start",
        ),
        class_name="bg-blue-50 border border-blue-200 p-4 rounded-lg",
    )

def index() -> rx.Component:
    """Main page."""
    return rx.box(
        header(),
        rx.box(
            rx.vstack(
                info_box(),
                note_input(),
                stats(),
                notes_list(),
                spacing="6",
                width="100%",
            ),
            class_name="container max-w-2xl mx-auto p-6",
        ),
        class_name="min-h-screen bg-gray-50",
        on_mount=AppState.on_load,
    )

# Prepare head components
head_components = []
if config.JAZZ_SYNC_SERVER:
    head_components.append(
        rx.script(src="https://unpkg.com/jazz-tools@latest/dist/index.js")
    )

# Create app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
    ),
    head_components=head_components,
)

# Add page
app.add_page(
    index,
    route="/",
    title="Jazz Notes - No Backend Required!",
    description="A simple notes app built with Jazz CRDTs and Reflex",
)

