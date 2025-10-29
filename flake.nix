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
        pythonPackages = ps: with ps; [
          pip
          setuptools
          wheel
          python-dotenv
          pytest
          pytest-asyncio
          pytest-cov
          black
          mypy
          ruff
        ];

        # Create a Python environment with our packages
        pythonEnv = pkgs.python311.withPackages pythonPackages;

      in
      {
        # devShells.default is the development environment
        devShells.default = pkgs.mkShell {
          # Packages to include in the shell environment
          buildInputs = with pkgs; [
            pythonEnv
            nodejs_24
            nodePackages.npm
            nodePackages.typescript
            git
            gnumake
            ripgrep
            jq
            curl
            wget
          ];

          shellHook = ''
            # Set environment variables
            export PROJECT_NAME="jazz-reflex-starter"
            export NODE_ENV="development"
            export PYTHONPATH="."
            export PIP_USER="1"

            echo "🎺 Jazz + Reflex Development Environment"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📦 Python $(python --version | cut -d' ' -f2)"
            echo "📦 Node.js $(node --version)"
            echo "📦 npm v$(npm --version)"
            echo ""
            echo "🚀 Quick Start:"
            echo "  1. Install dependencies:  make install"
            echo "  2. Copy environment:      cp .env.example .env"
            echo "  3. Run application:       make run"
            echo ""
            echo "📚 Commands: make help"
            echo ""

            # Create .env if it doesn't exist
            if [ ! -f .env ]; then
              echo "⚠️  No .env file found. Creating from .env.example..."
              cp .env.example .env
              echo "✅ Created .env file"
              echo ""
            fi
          '';
        };
      });
}
