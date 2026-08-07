#!/bin/bash
# Run all tests with coverage

echo "Running test suite..."
pytest tests/ -v --cov=src/ --cov-report=html --cov-report=term

echo ""
echo "Coverage report generated in htmlcov/index.html"
