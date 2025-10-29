# Code Improvements & Known Issues

This document outlines areas for improvement in the Jazz + Reflex Starter Template.

## 1. Jazz Integration is Incomplete

**Location:** `app/state.py:56-67`

The current implementation simulates Jazz with `asyncio.sleep()` but doesn't actually use the TypeScript schemas defined in `app/jazz/schema.ts`.

**Current Code:**
```python
async def initialize_jazz(self) -> None:
    """Initialize Jazz system."""
    try:
        logger.info("Initializing Jazz...")
        # In a real implementation, this would initialize Jazz
        # For this template, we'll simulate it
        import asyncio
        await asyncio.sleep(0.5)
```

**Options to Fix:**
- Implement actual Jazz integration via WebSocket/JavaScript bridge
- Remove the Jazz mock and focus on local-only storage
- Clearly document this as a template requiring implementation

## 2. Type Hints Missing

**Location:** `app/state.py:46-51, 95-107, 109-117`

Several methods lack return type annotations.

**Missing Annotations:**
```python
def set_new_note_title(self, value: str):      # ❌ Missing -> None
def set_new_note_content(self, value: str):    # ❌ Missing -> None
def toggle_note(self, note_id: int):           # ❌ Missing -> None
def delete_note(self, note_id: int):           # ❌ Missing -> None
```

**Fix:** Add `-> None` return type to all these methods.

## 3. `on_load` Return Type is Wrong

**Location:** `app/state.py:116-117`

The method returns a callable but is typed as `-> None`.

**Current Code:**
```python
def on_load(self) -> None:
    """Handle page load."""
    return AppState.initialize_jazz  # ⚠️ Returns callable, not None
```

**Fix:** Either change return type to match actual return value, or refactor to not return anything.

## 4. ID Generation is Fragile

**Location:** `app/state.py:79`

Note IDs use `len(self.notes) + 1` which breaks after deletions.

**Current Code:**
```python
"id": len(self.notes) + 1,  # ⚠️ Breaks if notes are deleted
```

**Problem:** After deleting notes, new notes can get duplicate IDs.

**Fix Options:**
- Use UUID/ULID for global uniqueness: `import uuid; "id": str(uuid.uuid4())`
- Use a proper auto-incrementing counter stored in state
- Use timestamp-based IDs: `"id": int(time.time() * 1000)`

## 5. Missing Input Validation

**Location:** `app/state.py:69-94`

No validation on user input.

**Missing Checks:**
- No maximum title/content length (could cause memory issues)
- No sanitization of user input (XSS potential if rendered as HTML)
- No rate limiting on note creation (spam potential)

**Suggested Fixes:**
```python
MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 10000

def add_note(self) -> None:
    if len(self.new_note_title) > MAX_TITLE_LENGTH:
        logger.warning("Title too long")
        return
    if len(self.new_note_content) > MAX_CONTENT_LENGTH:
        logger.warning("Content too long")
        return
    # ... rest of implementation
```

## 6. Unused/Dead Code

**Locations:**
- `rxconfig.py:10-14` - Commented-out Jazz packages
- `app/jazz/schema.ts` - Complete schema definitions never used
- `rxconfig.py:16` - Database URL comment for future use

**Action Items:**
- Either implement Jazz integration and uncomment packages
- Or remove unused TypeScript schemas
- Clean up comments about features not being implemented

## 7. Generic Exception Catching

**Location:** `app/state.py:92-94, 102-104, 113-115`

All state methods use `except Exception as e:` which catches everything.

**Current Pattern:**
```python
try:
    # ... logic ...
except Exception as e:
    logger.error(f"Failed to add note: {e}")
```

**Issues:**
- Catches system errors (KeyboardInterrupt, SystemExit, etc.)
- No distinction between different error types
- Silent failures with no user feedback

**Suggested Fixes:**
```python
# Be more specific
except (ValueError, KeyError) as e:
    logger.error(f"Failed to add note: {e}")
    # Optionally set an error state variable for UI feedback
    self.error_message = "Failed to add note"
```

## 8. PEP 8 Formatting

**Locations:** `app/state.py`, `config.py`, test files

Need consistent formatting:
- Blank line after module docstring
- Two blank lines between top-level definitions

## Priority

**High Priority:**
1. Fix ID generation (security/correctness issue)
2. Add input validation (security issue)
3. Fix return type annotations (code quality)

**Medium Priority:**
4. Improve exception handling (error handling)
5. Clean up unused code (maintainability)
6. Fix PEP 8 formatting (code quality)

**Low Priority:**
7. Complete Jazz integration (feature implementation)
8. Fix on_load return type (minor type issue)
