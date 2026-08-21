# Code Style Guide

## Python

Follow PEP 8 with these additions:

### Formatting
- **Line length:** 88 characters (Black default)
- **Indentation:** 4 spaces
- **String quotes:** Double quotes preferred
- **Import order:** Standard → Third-party → Local

### Naming
```python
# Classes: PascalCase
class VeteranMatcher:
    pass

# Functions/methods: snake_case
def calculate_match_score():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_MATCH_RESULTS = 50

# Private: _leading_underscore
def _internal_helper():
    pass
```

### Docstrings
```python
def match_veteran(veteran_id: str, top_k: int = 20) -> list:
    """Match veteran to top K jobs.

    Args:
        veteran_id: Unique veteran identifier
        top_k: Number of results to return

    Returns:
        List of job matches with scores

    Raises:
        ValueError: If veteran_id not found
    """
    pass
```

---

## SQL

### Formatting
- **Keywords:** UPPERCASE
- **Identifiers:** snake_case
- **Indentation:** 2 spaces
- **One clause per line**

### Example
```sql
SELECT
  v.veteran_id,
  v.name,
  COUNT(m.job_id) as match_count
FROM workspace.fys_silver.veterans v
LEFT JOIN workspace.fys_gold.matches m
  ON v.veteran_id = m.veteran_id
WHERE v.active = TRUE
GROUP BY v.veteran_id, v.name
ORDER BY match_count DESC
LIMIT 20;
```

---

## JSON

- **Indentation:** 2 spaces
- **Keys:** snake_case
- **No trailing commas**

---

## Git Commits

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `chore`: Maintenance

Example: `feat: Add salary normalization`

---

## Pre-commit Hooks

Run before committing:
```bash
black .
flake8 .
pytest tests/unit/
```
