# flake.nix - Nix Flake configuration for Jazz + Reflex Starter
# This creates a reproducible development environment with Python and Node.js
# for building offline-first apps with CRDT sync
{
description = "Jazz + Reflex Starter - Offline-first app with CRDT sync and Python UI";

# Inputs are external dependencies for our flake
inputs = {
# nixpkgs is the main package repository for Nix
# Using "nixos-unstable" gives us the latest packages
nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

# flake-utils helps us write flakes that work on multiple systems
flake-utils.url = "github:numtide/flake-utils";
};

# Outputs define what our flake produces
outputs = { self, nixpkgs, flake-utils }:
# Create outputs for each system (x86_64-linux, aarch64-darwin, etc.)
flake-utils.lib.eachDefaultSystem (system:
let
# Import nixpkgs for our specific system
pkgs = nixpkgs.legacyPackages.${system};

# Define Python packages we want available in the environment
# These are packages available in nixpkgs
# We'll use pip for Reflex-specific packages
pythonPackages = ps: with ps; [
pip # Package installer
setuptools # Package development
wheel # Package building
python-dotenv # Environment variables
pytest # Testing framework
pytest-asyncio # Async testing
pytest-cov # Coverage reporting
black # Code formatter
mypy # Type checker
ruff # Fast linter
];

# Create a Python environment with our packages
pythonEnv = pkgs.python311.withPackages pythonPackages;

in
{
# devShells.default is the development environment
devShells.default = pkgs.mkShell {
# Packages to include in the shell environment
buildInputs = with pkgs; [
# Python with our selected packages
pythonEnv

# Node.js and npm for Jazz tools (CRDT sync)
nodejs_24
nodePackages.npm

# TypeScript for Jazz schema files
nodePackages.typescript

# Development tools
git # Version control
gnumake # Build automation (for Makefile)
ripgrep # Fast file search
jq # JSON processor

# Optional: useful for debugging
curl # HTTP client
wget # File downloader
];

# Shell hook runs when entering the development environment
shellHook = ''
echo "🎺 Jazz + Reflex Development Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Python $(python --version | cut -d' ' -f2)"
echo "📦 Node.js $(node --version)"
echo "📦 npm v$(npm --version)"
echo ""
echo "🚀 Quick Start:"
echo " 1. Install dependencies: make install"
echo " 2. Copy environment: cp .env.example .env"
echo " 3. Run application: make run"
echo ""
echo "📚 Available Commands:"
echo " make install - Install Python & Node dependencies"
echo " make run - Run the application (reflex run)"
echo " make test - Run test suite"
echo " make test-cov - Run tests with coverage"
echo " make lint - Run linting (ruff + mypy)"
echo " make clean - Clean generated files"
echo ""
echo "💡 Features:"
echo " ✨ No Backend Required - Jazz handles data & sync"
echo " 🔄 Real-time Sync - Automatic CRDT sync across devices"
echo " 📴 Offline-First - Works without internet"
echo " 🐍 Python UI - Build with Reflex framework"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
echo "⚠️ No .env file found. Creating from .env.example..."
cp .env.example .env
echo "✅ Created .env file. You can edit it if needed."
echo ""
fi

# Check if dependencies are installed
if [ ! -d "venv" ] && ! python -c "import reflex" 2>/dev/null; then
echo "📦 Installing Python dependencies..."
pip install --user -r requirements.txt
echo ""
fi
'';

# Environment variables
PROJECT_NAME = "jazz-reflex-starter";
NODE_ENV = "development";

# Python environment
PYTHONPATH = ".";

# Make pip install to user directory by default
# This keeps packages isolated and doesn't require virtual env
PIP_USER = "1";
};
});
}