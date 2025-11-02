# flake.nix - Use Reflex's REFLEX_USE_SYSTEM_BUN
{
  description = "Jazz + Reflex Starter - Offline-first app with CRDT sync and Python UI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

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

        pythonEnv = pkgs.python311.withPackages pythonPackages;

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python environment
            pythonEnv
            
            # JavaScript runtimes
            nodejs_24
            bun              # Reflex's preferred JS runtime
            nodePackages.npm
            nodePackages.typescript
            
            # Reflex dependencies
            unzip          # Required by Reflex to install Bun
            caddy          # Optional: for production deployment
            
            # Development tools
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
            export PYTHONPATH="$PWD:$PYTHONPATH"
            
            # Tell Reflex to use system Bun (NixOS compatibility)
            export REFLEX_USE_SYSTEM_BUN=true
            export BUN_PATH="${pkgs.bun}/bin/bun"
            
            # Create virtual environment if it doesn't exist
            if [ ! -d .venv ]; then
              echo "📦 Creating Python virtual environment..."
              python -m venv .venv
            fi
            
            # Activate virtual environment
            source .venv/bin/activate

            echo "🎺 Jazz + Reflex Development Environment"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📦 Python $(python --version | cut -d' ' -f2)"
            echo "📦 Node.js $(node --version)"
            echo "📦 Bun $(bun --version)"
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
            
            # Auto-install if requirements.txt exists but packages aren't installed
            if [ -f requirements.txt ] && ! pip show reflex > /dev/null 2>&1; then
              echo "📥 Installing Python dependencies..."
              pip install -q -r requirements.txt
              echo "✅ Dependencies installed!"
              echo ""
            fi
          '';
        };
      });
}