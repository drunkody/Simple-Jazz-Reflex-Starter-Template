# Jazz + Reflex Starter Template

A minimal starter template for building offline-first apps with **Jazz** (CRDT sync) and **Reflex** (Python UI framework). No backend or database required!

## Features

✨ **No Backend Required** - Jazz handles all data storage and sync
🔄 **Real-time Sync** - Automatic sync across devices and users
📴 **Offline-First** - Works perfectly without internet
🐍 **Python UI** - Build reactive UIs with pure Python
🚀 **Zero Config** - Just install and run

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure (Optional)

```bash
cp .env.example .env
# Edit .env if needed
```

### 3. Run

```bash
reflex run
```

Visit `http://localhost:3000`

## How It Works

### Jazz CRDTs

Jazz uses **Conflict-free Replicated Data Types (CRDTs)** for automatic sync:

```typescript
// app/jazz/schema.ts
export class Note extends CoMap {
  title = co.string;
  content = co.string;
  completed = co.boolean;
  createdAt = co.string;
}
```

### Reflex State

```python
# app/state.py
class AppState(rx.State):
    notes: list[dict] = []
    def add_note(self, title: str):
        # Data saved to Jazz automatically
        pass
```

### Sync Modes

**With Sync Server** (Default)

```bash
JAZZ_SYNC_SERVER=wss://cloud.jazz.tools
```
- Syncs across all devices
- Real-time collaboration
- Cloud backup

**Local-Only** (Offline)

```bash
JAZZ_SYNC_SERVER=
```
- No internet needed
- Data stored locally
- Perfect for privacy

**Self-Hosted**

```bash
JAZZ_SYNC_SERVER=wss://your-server.com
```
- Full control
- Custom domain
- Private infrastructure

## Project Structure

```
├── app/
│   ├── app.py      # Main Reflex app
│   ├── state.py    # State management
│   └── jazz/
│       └── schema.ts # Jazz CRDT schemas
├── config.py     # Configuration
└── rxconfig.py   # Reflex config
```

## Customization

### Add New Data Types

1. **Define Schema** (`app/jazz/schema.ts`):
```typescript
export class Task extends CoMap {
  name = co.string;
  priority = co.number;
  done = co.boolean;
}
```

2. **Use in State** (`app/state.py`):
```python
def create_task(self, name: str):
    # Jazz handles persistence automatically
    self.tasks.append({"name": name, "done": False})
```

### Styling

Edit components in `app/app.py` using Tailwind classes:

```python
rx.box(
    "Hello Jazz!",
    class_name="bg-blue-500 text-white p-4 rounded-lg"
)
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_state.py -v

# Run tests in watch mode
pytest-watch
```

## Deployment

### Deploy to Reflex Cloud

```bash
reflex deploy
```

### Deploy to Vercel/Netlify

```bash
reflex export
# Upload .web folder
```

## Examples

### Todo App

See `app/app.py` for a complete todo list example.

### Chat App

Check out [Jazz Examples](https://jazz.tools/examples) for more.

## Learn More

- [Jazz Documentation](https://jazz.tools/docs)
- [Reflex Documentation](https://reflex.dev/docs)
- [CRDT Explained](https://crdt.tech/)

## License

MIT

