# Running Your App with Nix Flake

A comprehensive guide to running the Jazz + Reflex Starter using Nix.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Common Tasks](#common-tasks)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Install Nix

If you don't have Nix installed yet:

**Linux/macOS/WSL:**
```bash
# Install Nix with flakes support
sh <(curl -L https://nixos.org/nix/install) --daemon

# Enable flakes (add to ~/.config/nix/nix.conf or /etc/nix/nix.conf)
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

**Verify installation:**
```bash
nix --version
```

---

## Quick Start

```bash
# 1. Clone/navigate to your project
cd jazz-reflex-starter

# 2. Enter Nix development environment
nix develop

# 3. Install Python/Node dependencies
make install

# 4. Run the app
make run
```

Visit **http://localhost:3000** 🎉

---

## Step-by-Step Guide

### 1️⃣ Enter the Development Environment

```bash
nix develop
```

**What this does:**
- ✅ Installs Python 3.11
- ✅ Installs Node.js 24
- ✅ Sets up all development tools
- ✅ Creates isolated environment
- ✅ Automatically creates `.env` if missing

**You should see:**
```
🎺 Jazz + Reflex Development Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Python 3.11.x
📦 Node.js v24.x.x
📦 npm v10.x.x

🚀 Quick Start:
  1. Install dependencies:  make install
  2. Copy environment:      cp .env.example .env
  3. Run application:       make run

📚 Commands: make help
```

### 2️⃣ Install Dependencies

**Install everything at once:**
```bash
make install
```

**Or manually:**
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (optional, for TypeScript checking)
npm install
```

### 3️⃣ Configure Environment (Optional)

The `.env` file is auto-created from `.env.example`. Edit if needed:

```bash
# Edit configuration
nano .env
```

**Default settings:**
```bash
# Jazz Sync Server
JAZZ_SYNC_SERVER=wss://cloud.jazz.tools  # Cloud sync
# JAZZ_SYNC_SERVER=                       # Local-only mode

JAZZ_ENABLE_P2P=true
JAZZ_AUTH_PROVIDER=anonymous
APP_ENV=development
LOG_LEVEL=INFO
```

### 4️⃣ Run the Application

```bash
make run
```

**Or directly:**
```bash
reflex run
```

**Output:**
```
─────────────────────────────────── Reflex ────────────────────────────────────
Reflex 0.4.0

─────────────────────────────────────────────────────────────────────────────
App running at:
  http://localhost:3000

Backend running at:
  http://localhost:8000
```

### 5️⃣ Access the App

Open your browser to:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000

---

## Common Tasks

### View All Commands

```bash
make help
```

### Run Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# View coverage in browser
make test-cov
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Lint & Type Check

```bash
# Run all linting
make lint

# Individual tools
ruff check app/ tests/ config.py  # Linter
mypy app/ tests/ config.py        # Type checker
bandit -r app/ config.py -ll      # Security scanner
```

### Run Full CI Suite Locally

```bash
make ci
```

This runs:
1. Ruff linting
2. MyPy type checking
3. Bandit security scan
4. All tests with coverage

### Clean Generated Files

```bash
make clean
```

Removes:
- `.web/` (Reflex build artifacts)
- `__pycache__/` directories
- Test cache and coverage files
- Temporary files

---

## Development Workflow

### Option 1: Stay in Nix Shell (Recommended)

```bash
# Enter once
nix develop

# Now you have persistent environment
make install
make run

# In another terminal (also in nix develop)
make test
```

### Option 2: One-off Commands

```bash
# Run commands without entering shell
nix develop -c make run
nix develop -c make test
nix develop -c pytest tests/test_state.py -v
```

### Option 3: Use direnv (Auto-activate)

```bash
# Install direnv
nix profile install nixpkgs#direnv

# Enable for this project
echo "use flake" > .envrc
direnv allow

# Now Nix environment activates automatically when you cd into the directory!
```

---

## Project Structure

```
jazz-reflex-starter/
├── flake.nix              # Nix flake configuration
├── flake.lock             # Locked dependency versions
├── Makefile               # Common commands
├── .env.example           # Environment template
├── .env                   # Your config (auto-created)
│
├── app/
│   ├── app.py            # Main Reflex application
│   ├── state.py          # Application state management
│   └── jazz/
│       └── schema.ts     # Jazz CRDT schemas (TypeScript)
│
├── config.py             # Python configuration
├── rxconfig.py           # Reflex configuration
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
│
└── tests/
    ├── test_state.py     # State tests
    └── test_config.py    # Config tests
```

---

## Troubleshooting

### Issue: "experimental-features" Error

**Error:**
```
error: experimental Nix feature 'nix-command' is disabled
```

**Fix:**
```bash
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

Restart your terminal.

### Issue: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Fix:**
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or change port in rxconfig.py
# frontend_port=3001
```

### Issue: Python Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'reflex'
```

**Fix:**
```bash
# Make sure you're in nix develop shell
nix develop

# Reinstall dependencies
make install
```

### Issue: `.env` File Missing

**Fix:**
```bash
# Automatically created when you run:
nix develop

# Or manually:
cp .env.example .env
```

### Issue: Reflex Build Fails

**Fix:**
```bash
# Clean and rebuild
make clean
rm -rf .web/
make run
```

### Issue: Permission Denied on `pip install`

This is normal in Nix! The flake sets `PIP_USER=1` automatically to install in user space.

**If you still see errors:**
```bash
# Exit and re-enter
exit
nix develop
```

---

## Advanced Usage

### Update Dependencies

**Update Nix flake inputs:**
```bash
nix flake update
```

**Update Python packages:**
```bash
pip install --upgrade -r requirements.txt
```

**Update Node packages:**
```bash
npm update
```

### Build for Production

```bash
# Export static build
reflex export

# Files will be in .web/ directory
```

### Deploy

**Reflex Cloud:**
```bash
reflex deploy
```

**Docker (future):**
```bash
# Build Docker image (when Dockerfile is added)
docker build -t jazz-reflex-app .
docker run -p 3000:3000 jazz-reflex-app
```

### Use Different Python/Node Versions

Edit `flake.nix`:

```nix
# Change Python version
pythonEnv = pkgs.python312.withPackages pythonPackages;

# Change Node version
nodejs_24  # Change to nodejs_20, nodejs_22, etc.
```

Then reload:
```bash
exit
nix develop
```

---

## Performance Tips

### Faster First Load

The first `nix develop` downloads packages. Speed it up:

```bash
# Use binary cache (usually automatic)
nix develop --option substituters https://cache.nixos.org
```

### Garbage Collection

Clean up old Nix generations:

```bash
# Delete old versions
nix-collect-garbage -d

# Delete generations older than 30 days
nix-collect-garbage --delete-older-than 30d
```

---

## Getting Help

### Check Logs

```bash
# Reflex logs are in the terminal where you ran `make run`

# Python logs
tail -f app.log

# Test with verbose output
pytest -vv -s
```

### Debug Mode

```bash
# Run with debug logging
LOG_LEVEL=DEBUG make run
```

### Verify Environment

```bash
nix develop

# Check Python
python --version
which python

# Check Node
node --version
which node

# Check installed packages
pip list
npm list --depth=0
```

---

## Next Steps

1. ✅ **Read the main README.md** - Learn about Jazz and Reflex
2. ✅ **Check IMPROVE.md** - Known issues and improvements
3. ✅ **Review REVIEW.md** - Code review checklist
4. ✅ **Run tests** - `make test-cov`
5. ✅ **Customize the app** - Edit `app/app.py`

---

## Quick Reference Card

```bash
# Essential Commands (inside nix develop)
nix develop          # Enter environment
make install         # Install dependencies  
make run             # Start app
make test            # Run tests
make lint            # Check code quality
make ci              # Run full CI locally
make clean           # Clean build files
make help            # Show all commands

# URLs
http://localhost:3000   # App frontend
http://localhost:8000   # App backend
```

---

## FAQ

**Q: Do I need to run `nix develop` every time?**  
A: Yes, each new terminal session. Or use `direnv` for auto-activation.

**Q: Can I use my system Python instead?**  
A: Yes, but Nix ensures consistency. Outside nix shell, use `pip install -r requirements.txt`

**Q: How do I exit the Nix shell?**  
A: Type `exit` or press `Ctrl+D`

**Q: Will this work on Windows?**  
A: Use WSL2 (Windows Subsystem for Linux) first, then follow Linux instructions.

**Q: Where are packages installed?**  
A: Nix packages are in `/nix/store/`. Python packages are in `~/.local/` (user space).

---

**Happy coding! 🎺**

If you run into issues, check the [Troubleshooting](#troubleshooting) section or open an issue.