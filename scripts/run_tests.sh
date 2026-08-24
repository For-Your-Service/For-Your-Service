#!/bin/bash
# Run test suite

echo "Running tests..."

# Unit tests
pytest tests/unit/ -v --cov=src/

# Integration tests
pytest tests/integration/ -v

echo "✅ Tests complete!"
