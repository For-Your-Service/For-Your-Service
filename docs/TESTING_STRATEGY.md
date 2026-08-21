# Testing Strategy

## For Your Service - Test Coverage Plan

### Test Pyramid

```
           /\
          /  \  E2E Tests (5%)
         /____\
        /      \  Integration Tests (25%)
       /________\
      /          \  Unit Tests (70%)
     /____________\
```

### Unit Tests

#### Veteran Profile Validation
```python
def test_validate_veteran_profile():
    profile = {
        'name': 'John Doe',
        'military_branch': 'Army',
        'mos': '11B',
        'clearance_level': 'Secret',
        'years_experience': 8
    }
    assert validate_profile(profile) == True

def test_missing_required_field():
    profile = {'name': 'John Doe'}
    with pytest.raises(ValidationError):
        validate_profile(profile)
```

#### Neural Network Inference
```python
def test_embedding_dimensions():
    veteran_vector = encode_veteran_profile(sample_profile)
    assert veteran_vector.shape == (384,)
    assert isinstance(veteran_vector, np.ndarray)

def test_similarity_score_range():
    score = calculate_similarity(vec1, vec2)
    assert 0.0 <= score <= 1.0
```

### Integration Tests

#### API Ingestion
```python
@mock.patch('requests.get')
def test_indeed_api_integration(mock_get):
    mock_get.return_value.json.return_value = {'jobs': [...]}
    jobs = fetch_indeed_jobs('software engineer', 'Greenville, SC')
    assert len(jobs) > 0
    assert 'job_id' in jobs[0]
```

#### Database Operations
```python
def test_write_to_bronze_layer():
    test_df = spark.createDataFrame([{
        'job_id': 'TEST001',
        'title': 'Test Engineer',
        'source': 'test'
    }])
    test_df.write.mode('append').saveAsTable('veteran_intake.bronze_jobs')

    result = spark.table('veteran_intake.bronze_jobs') \
        .filter("job_id = 'TEST001'") \
        .count()
    assert result == 1
```

### End-to-End Tests

```python
def test_veteran_matching_pipeline():
    """Full pipeline: intake → bronze → silver → gold → matches"""

    # 1. Ingest test data
    test_veteran = create_test_veteran()
    test_jobs = create_test_jobs(count=100)

    # 2. Run matching engine
    matches = run_matching_engine(test_veteran, test_jobs)

    # 3. Validate results
    assert len(matches) == 10  # Top 10
    assert matches[0]['score'] >= matches[-1]['score']  # Descending order
    assert all(m['score'] > 0.5 for m in matches)  # Quality threshold
```

### Performance Tests

```python
import time

def test_matching_latency():
    start = time.time()
    matches = generate_matches(veteran_profile, job_pool=10000)
    duration = time.time() - start

    assert duration < 1.0  # Must complete in <1 second
    assert len(matches) == 10

def test_api_rate_limiting():
    limiter = RateLimiter(rate_per_minute=100)

    # Attempt 150 requests
    allowed = sum(1 for _ in range(150) if limiter.allow_request())

    assert allowed <= 100  # Should block excess requests
```

### Test Data Management

```python
# tests/fixtures/sample_veteran.json
{
  "veteran_id": "TEST_VET_001",
  "name": "Test Veteran",
  "military_branch": "Army",
  "mos": "18F",
  "clearance_level": "TS/SCI",
  "years_service": 10,
  "target_location": "Greenville, SC",
  "desired_roles": ["DevOps Engineer", "Cloud Architect"]
}
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Run Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: pytest tests/unit/ -v
      - name: Run integration tests
        run: pytest tests/integration/ -v
```

### Test Coverage Goals

* Unit tests: >80% code coverage
* Integration tests: All API endpoints
* E2E tests: Critical user journeys
* Performance tests: <1s match latency

### Running Tests Locally

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# With coverage report
pytest tests/ --cov=src/ --cov-report=html

# Specific test file
pytest tests/unit/test_matching_engine.py -v
```

---

**Maintained by:** 7 Eagle Group
**Last Updated:** 2026-08-10
