.PHONY: install run test lint clean help ci setup

help:
	@echo "Available commands:"
	@echo "  make setup      - First-time setup (creates venv)"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the application"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make lint       - Run linting and type checking"
	@echo "  make ci         - Run all CI checks locally"
	@echo "  make clean      - Clean generated files"

setup:
	@echo "🔧 Setting up development environment..."
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	@echo "✅ Virtual environment created!"
	@echo "Run: source .venv/bin/activate (or enter nix shell)"

install:
	@echo "📥 Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ All dependencies installed!"

run:
	@command -v reflex >/dev/null 2>&1 || { echo "❌ reflex not found. Run 'make install' first."; exit 1; }
	reflex run

test:
	pytest -v

test-cov:
	APP_ENV=testing pytest --cov=app --cov=config --cov-report=html --cov-report=term

lint:
	@echo "Running ruff..."
	ruff check app/ tests/ config.py
	@echo "Running mypy..."
	mypy app/ tests/ config.py --ignore-missing-imports
	@echo "Running bandit..."
	bandit -r app/ config.py -ll

ci: lint test-cov
	@echo "✅ All CI checks passed locally!"

clean:
	rm -rf .web/
	rm -rf assets/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf bandit-report.json
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf .venv/
	@echo "✅ Cleaned everything including virtual environment"