.PHONY: install run test lint clean help ci

help:
@echo "Available commands:"
@echo " make install - Install dependencies"
@echo " make run - Run the application"
@echo " make test - Run tests"
@echo " make test-cov - Run tests with coverage"
@echo " make lint - Run linting and type checking"
@echo " make ci - Run all CI checks locally"
@echo " make clean - Clean generated files"

install:
pip install -r requirements.txt

run:
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
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
