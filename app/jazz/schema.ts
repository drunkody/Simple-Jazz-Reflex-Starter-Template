/**
 * Jazz CRDT Schemas
 *
 * Define your data structures here. They automatically sync across devices!
 * No database, no API, no backend needed.
 */
import { co, CoMap, CoList, Group, Account } from "jazz-tools";

/**
 * Note Schema
 * A simple note with title and content
 */
export class Note extends CoMap {
    title = co.string;
    content = co.string;
    completed = co.boolean;
    createdAt = co.string;
    updatedAt = co.string;
}

/**
 * Notes Collection
 * List of all notes (auto-syncs!)
 */
export class NotesCollection extends CoList.Of(co.ref(Note)) {}

/**
 * App State
 * Root state for the entire app
 */
export class AppState extends CoMap {
    notes = co.ref(NotesCollection);
    lastSync = co.string;
}

/**
 * Helper Functions
 */
export const JazzHelpers = {
    /**
     * Create a new note
     */
    createNote(data: { title: string; content: string; }): Partial<Note> {
        const now = new Date().toISOString();
        return {
            title: data.title,
            content: data.content || "",
            completed: false,
            createdAt: now,
            updatedAt: now,
        };
    },

    /**
     * Convert note to plain object
     */
    noteToJSON(note: Note): any {
        return {
            title: note.title,
            content: note.content,
            completed: note.completed,
            created_at: note.createdAt,
            updated_at: note.updatedAt,
        };
    },

    /**
     * Toggle note completion
     */
    toggleNote(note: Note): void {
        note.completed = !note.completed;
        note.updatedAt = new Date().toISOString();
    },
};

/**
 * Initialize Jazz App
 * Call this when the app starts
 */
export async function initializeJazzApp(account: Account): Promise<AppState> {
    // Try to load existing state
    const stateId = localStorage.getItem("jazz_app_state_id");
    let appState: AppState;

    if (stateId) {
        appState = await AppState.load(stateId, account, {});
        if (appState) return appState;
    }

    // Create new state
    const group = await Group.create(account);
    appState = AppState.create(
        {
            notes: NotesCollection.create([], { owner: group }),
            lastSync: new Date().toISOString(),
        },
        { owner: group }
    );

    // Save for next time
    localStorage.setItem("jazz_app_state_id", appState.id);

    return appState;
}

/**
 * Usage Example:
 *
 * // Initialize
 * const appState = await initializeJazzApp(myAccount);
 *
 * // Add note
 * const noteData = JazzHelpers.createNote({
 *   title: "My Note",
 *   content: "Some content"
 * });
 * const note = Note.create(noteData, { owner: appState._owner });
 * appState.notes.push(note);

 * // Notes automatically sync across all devices!
 */
