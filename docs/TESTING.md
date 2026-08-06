# Testing Guide

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### With Coverage
```bash
pytest tests/ --cov=src/ --cov-report=html
open htmlcov/index.html
```

### Specific Module
```bash
pytest tests/api/test_usajobs.py -v
```

## Test Structure

```
tests/
├── api/              # API client tests
├── features/         # Feature engineering tests
├── matching/         # Neural network tests
├── ingestion/        # Data pipeline tests
└── conftest.py       # Shared fixtures
```

## Writing Tests

### Example Test
```python
import pytest
from src.api.usajobs.client import USAJobsClient

def test_usajobs_search():
    client = USAJobsClient(
        api_key="test_key",
        user_agent="test@example.com"
    )
    # Test logic here
    assert client is not None
```

### Fixtures
Use fixtures from `conftest.py`:
```python
def test_with_config(api_config):
    assert api_config.USAJOBS_API_KEY is not None
```

## Coverage Goals
* Minimum: 80% overall
* Critical paths: 95%
* Unit tests: 90%
