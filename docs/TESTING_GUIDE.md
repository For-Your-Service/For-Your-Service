# Testing Guide

## Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
├── integration/       # Integration tests (slower, DB access)
└── e2e/              # End-to-end tests (full workflows)
```

---

## Running Tests

### All Tests
```bash
pytest tests/
```

### Unit Tests Only
```bash
pytest tests/unit/ -m unit
```

### Integration Tests
```bash
pytest tests/integration/ -m integration
```

### With Coverage
```bash
pytest --cov=src --cov-report=html
```

---

## Writing Tests

### Unit Test Example
```python
def test_normalize_salary():
    result = normalize_salary(50, "hour")
    assert result == 104000  # 50 * 40 * 52
```

### Integration Test Example
```python
@pytest.mark.integration
def test_bronze_table_read(spark):
    df = spark.read.table("workspace.fys_bronze.job_postings")
    assert df.count() > 0
```

---

## Test Coverage Goals

- **Overall:** >80%
- **Critical paths:** 100%
- **New features:** 100%

---

## Mocking

Use `pytest-mock` for external dependencies:
```python
def test_api_call(mocker):
    mock_response = {"jobs": []}
    mocker.patch("requests.get", return_value=mock_response)
```

---

## CI/CD Integration

Tests run automatically on:
- Every PR
- Merges to main
- Nightly builds
