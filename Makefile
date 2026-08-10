# For Your Service - Makefile

.PHONY: help install test lint format clean

help:
	@echo "For Your Service - Development Commands"
	@echo ""
	@echo "make install   - Install dependencies"
	@echo "make test      - Run test suite"
	@echo "make lint      - Run linters"
	@echo "make format    - Format code"
	@echo "make clean     - Clean build artifacts"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ tests/
	pylint src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/
