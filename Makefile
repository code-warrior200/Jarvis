.PHONY: help install install-dev test lint format type-check clean build run

help:
	@echo "JARVIS - AI Voice Assistant"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run test suite"
	@echo "  make lint          - Run code linter"
	@echo "  make format        - Format code with black and isort"
	@echo "  make type-check    - Run type checker"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make build         - Build package"
	@echo "  make run           - Run JARVIS GUI"
	@echo "  make coverage      - Generate coverage report"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

lint:
	flake8 jarvis tests
	pylint jarvis

format:
	black jarvis tests
	isort jarvis tests

type-check:
	mypy jarvis --ignore-missing-imports

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

build: clean
	python setup.py sdist bdist_wheel

run:
	python -m jarvis

coverage:
	pytest tests/ --cov=jarvis --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

.DEFAULT_GOAL := help
