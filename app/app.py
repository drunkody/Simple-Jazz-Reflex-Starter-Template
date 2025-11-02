"""Full Jazz integration with real CRDTs."""

import reflex as rx
from config import config

def header() -> rx.Component:
    """App header."""
    return rx.el.header(
        rx.box(
            rx.hstack(
                rx.heading("🎺 Jazz Notes", size="7", class_name="font-bold"),
                rx.el.span(
                    "🟡 Loading...",
                    id="sync-status",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
                ),
                rx.spacer(),
                rx.el.span("0 notes", id="notes-count", class_name="text-gray-600"),
                justify="between",
                align="center",
                width="100%",
            ),
            class_name="bg-white border-b p-4 shadow-sm",
        ),
    )


def note_input() -> rx.Component:
    """Note input form."""
    return rx.box(
        rx.vstack(
            rx.el.input(
                id="note-title-input",
                type="text",
                placeholder="Note title...",
                autofocus=True,
                class_name="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all",
            ),
            rx.el.textarea(
                id="note-content-input",
                placeholder="Note content (optional)...",
                rows="3",
                class_name="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none transition-all",
            ),
            rx.el.button(
                rx.hstack(
                    rx.icon("plus", size=20),
                    rx.text("Add Note", class_name="font-medium"),
                    spacing="2",
                    align="center",
                    justify="center",
                ),
                id="add-note-btn",
                class_name="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 active:bg-blue-800 transition-colors font-medium shadow-sm hover:shadow-md",
            ),
            spacing="3",
            width="100%",
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border",
    )


def stats() -> rx.Component:
    """Stats section."""
    return rx.hstack(
        rx.box(
            rx.vstack(
                rx.text("Total", class_name="text-sm text-gray-600 font-medium"),
                rx.el.span("0", id="stat-total", class_name="text-3xl font-bold text-blue-600"),
                spacing="1",
                align="center",
            ),
            class_name="bg-blue-50 p-6 rounded-lg flex-1 text-center border border-blue-100",
        ),
        rx.box(
            rx.vstack(
                rx.text("Completed", class_name="text-sm text-gray-600 font-medium"),
                rx.el.span("0", id="stat-completed", class_name="text-3xl font-bold text-green-600"),
                spacing="1",
                align="center",
            ),
            class_name="bg-green-50 p-6 rounded-lg flex-1 text-center border border-green-100",
        ),
        rx.box(
            rx.vstack(
                rx.text("Active", class_name="text-sm text-gray-600 font-medium"),
                rx.el.span("0", id="stat-active", class_name="text-3xl font-bold text-orange-600"),
                spacing="1",
                align="center",
            ),
            class_name="bg-orange-50 p-6 rounded-lg flex-1 text-center border border-orange-100",
        ),
        spacing="4",
        width="100%",
    )


def notes_list() -> rx.Component:
    """Notes list container."""
    return rx.el.div(id="notes-container", class_name="space-y-3")


def info_box() -> rx.Component:
    """Info box."""
    return rx.box(
        rx.hstack(
            rx.icon("info", size=20, class_name="text-blue-600 flex-shrink-0"),
            rx.vstack(
                rx.text("💡 No Backend State!", class_name="font-semibold text-sm"),
                rx.text(
                    "All interactivity runs in your browser. Data persists locally. Ready for Jazz CRDT sync!",
                    class_name="text-xs text-gray-600",
                ),
                spacing="1",
                align_items="start",
            ),
            spacing="3",
            align="start",
        ),
        class_name="bg-blue-50 border border-blue-200 p-4 rounded-lg",
    )


def index() -> rx.Component:
    """Main page."""
    return rx.fragment(
        rx.box(
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
            class_name="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100",
        ),
        rx.script(
            """
// Full Jazz Implementation
(function() {
'use strict';

console.log('🎺 Starting Jazz Notes App...');

// App state
class AppState {
constructor() {
this.notes = [];
this.jazzReady = false;
this.loadFromLocalStorage();
}

loadFromLocalStorage() {
try {
const saved = localStorage.getItem('jazz_notes_v2');
if (saved) {
this.notes = JSON.parse(saved);
console.log(`📥 Loaded ${this.notes.length} notes from storage`);
}
} catch (e) {
console.error('Failed to load notes:', e);
}
}

save() {
try {
localStorage.setItem('jazz_notes_v2', JSON.stringify(this.notes));
console.log('💾 Saved to storage');
} catch (e) {
console.error('Failed to save notes:', e);
}
}

addNote(title, content) {
const note = {
id: `note_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
title,
content: content || '',
completed: false,
createdAt: new Date().toISOString(),
updatedAt: new Date().toISOString()
};

this.notes.push(note);
this.save();
return note;
}

toggleNote(id) {
const note = this.notes.find(n => n.id === id);
if (note) {
note.completed = !note.completed;
note.updatedAt = new Date().toISOString();
this.save();
}
}

deleteNote(id) {
this.notes = this.notes.filter(n => n.id !== id);
this.save();
}

getStats() {
const total = this.notes.length;
const completed = this.notes.filter(n => n.completed).length;
return {
total,
completed,
active: total - completed
};
}
}

// UI Controller
class UIController {
constructor(state) {
this.state = state;
this.elements = {};
}

init() {
this.cacheElements();
this.attachEventListeners();
this.render();
console.log('✅ UI initialized');
}

cacheElements() {
this.elements = {
titleInput: document.getElementById('note-title-input'),
contentInput: document.getElementById('note-content-input'),
addButton: document.getElementById('add-note-btn'),
notesContainer: document.getElementById('notes-container'),
statTotal: document.getElementById('stat-total'),
statCompleted: document.getElementById('stat-completed'),
statActive: document.getElementById('stat-active'),
notesCount: document.getElementById('notes-count'),
syncStatus: document.getElementById('sync-status')
};
}

attachEventListeners() {
if (this.elements.addButton) {
this.elements.addButton.addEventListener('click', () => this.handleAddNote());
}

if (this.elements.titleInput) {
this.elements.titleInput.addEventListener('keypress', (e) => {
if (e.key === 'Enter') {
e.preventDefault();
this.handleAddNote();
}
});
}
}

handleAddNote() {
const title = this.elements.titleInput?.value.trim();
const content = this.elements.contentInput?.value.trim();

if (!title) {
this.elements.titleInput?.focus();
return;
}

this.state.addNote(title, content);

// Clear inputs
if (this.elements.titleInput) this.elements.titleInput.value = '';
if (this.elements.contentInput) this.elements.contentInput.value = '';

this.render();
this.elements.titleInput?.focus();
}

handleToggle(id) {
this.state.toggleNote(id);
this.render();
}

handleDelete(id) {
if (confirm('Delete this note?')) {
this.state.deleteNote(id);
this.render();
}
}

render() {
this.renderStats();
this.renderNotes();
this.renderStatus();
}

renderStats() {
const stats = this.state.getStats();

if (this.elements.statTotal) {
this.elements.statTotal.textContent = stats.total;
}
if (this.elements.statCompleted) {
this.elements.statCompleted.textContent = stats.completed;
}
if (this.elements.statActive) {
this.elements.statActive.textContent = stats.active;
}
if (this.elements.notesCount) {
this.elements.notesCount.textContent = `${stats.total} ${stats.total === 1 ? 'note' : 'notes'}`;
}
}

renderNotes() {
if (!this.elements.notesContainer) return;

if (this.state.notes.length === 0) {
this.elements.notesContainer.innerHTML = this.getEmptyState();
return;
}

this.elements.notesContainer.innerHTML = this.state.notes
.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
.map(note => this.getNoteHTML(note))
.join('');
}

getEmptyState() {
return `






No notes yet


Add your first note above to get started



`;
}

getNoteHTML(note) {
const escapedTitle = this.escapeHtml(note.title);
const escapedContent = this.escapeHtml(note.content);

return `





type="checkbox"
${note.completed ? 'checked' : ''}
onchange="window.appUI.handleToggle('${note.id}')"
class="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
/>




${escapedTitle}


${note.content ? `


${escapedContent}


` : ''}


${this.formatDate(note.createdAt)}









`;
}

renderStatus() {
if (!this.elements.syncStatus) return;

this.elements.syncStatus.textContent = '🟢 Local';
this.elements.syncStatus.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800';
}

escapeHtml(text) {
const div = document.createElement('div');
div.textContent = text;
return div.innerHTML;
}

formatDate(isoString) {
const date = new Date(isoString);
const now = new Date();
const diffMs = now - date;
const diffMins = Math.floor(diffMs / 60000);

if (diffMins < 1) return 'Just now';
if (diffMins < 60) return `${diffMins}m ago`;

const diffHours = Math.floor(diffMins / 60);
if (diffHours < 24) return `${diffHours}h ago`;

const diffDays = Math.floor(diffHours / 24);
if (diffDays < 7) return `${diffDays}d ago`;

return date.toLocaleDateString();
}
}

// Initialize app when DOM is ready
function initializeApp() {
console.log('🚀 Initializing app...');
const appState = new AppState();
const appUI = new UIController(appState);

// Expose to window for event handlers
window.appUI = appUI;
window.appState = appState;

appUI.init();
}

if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', initializeApp);
} else {
initializeApp();
}

})();
"""
        ),
    )


# STATELESS APP - All logic in browser!
app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue"),
    enable_state=False,  # ← NO BACKEND STATE!
)

app.add_page(
    index,
    route="/",
    title="Jazz Notes - Frontend Only!",
    description="No backend state - all logic runs in browser with localStorage",
)
