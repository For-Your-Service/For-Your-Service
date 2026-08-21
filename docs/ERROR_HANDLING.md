# Error Handling & Recovery

## For Your Service - Robust Error Management

### Error Categories

#### 1. API Errors (4xx, 5xx)
```python
def handle_api_error(response, provider):
    if response.status_code == 401:
        # Authentication failure
        rotate_api_key(provider)
        return "RETRY"
    elif response.status_code == 429:
        # Rate limited
        wait_time = int(response.headers.get('Retry-After', 60))
        time.sleep(wait_time)
        return "RETRY"
    elif response.status_code == 503:
        # Service unavailable
        log_provider_outage(provider)
        return "SKIP"
    elif 500 <= response.status_code < 600:
        # Server error - exponential backoff
        return "BACKOFF"
    else:
        # Client error - log and skip
        log_error(f"Client error {response.status_code}: {response.text}")
        return "SKIP"
```

#### 2. Data Validation Errors
```python
def validate_veteran_profile(profile):
    errors = []

    if not profile.get('military_branch'):
        errors.append("Missing military_branch")

    if not profile.get('clearance_level'):
        errors.append("Missing clearance_level")

    if not profile.get('target_location'):
        errors.append("Missing target_location")

    if errors:
        raise ValidationError(f"Profile incomplete: {', '.join(errors)}")
```

#### 3. Database Errors
```python
from pyspark.sql.utils import AnalysisException

try:
    df = spark.table("veteran_intake.bronze_profiles")
except AnalysisException as e:
    if "Table or view not found" in str(e):
        create_bronze_table()
        df = spark.table("veteran_intake.bronze_profiles")
    else:
        raise
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
def fetch_jobs_with_retry(provider, params):
    response = requests.get(provider.url, params=params)
    response.raise_for_status()
    return response.json()
```

### Dead Letter Queue

When retries fail, send to DLQ for manual review:

```python
def send_to_dlq(record, error, source):
    dlq_record = {
        'timestamp': datetime.now().isoformat(),
        'source': source,
        'record': record,
        'error': str(error),
        'retry_count': record.get('retry_count', 0)
    }

    spark.createDataFrame([dlq_record]).write \
        .mode('append') \
        .saveAsTable('veteran_intake.dead_letter_queue')

    # Alert on high DLQ volume
    dlq_count = spark.table('veteran_intake.dead_letter_queue') \
        .filter(F.col('timestamp') > F.current_date()) \
        .count()

    if dlq_count > 100:
        send_slack_alert(f"⚠️ DLQ has {dlq_count} records today")
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=300):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpen(f"Circuit open for {func.__name__}")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            send_alert(f"Circuit breaker opened after {self.failure_count} failures")
```

### Monitoring & Alerting

```python
# Log all errors to dedicated table
def log_error(error_type, message, context):
    error_record = {
        'timestamp': datetime.now(),
        'error_type': error_type,
        'message': message,
        'context': json.dumps(context),
        'stack_trace': traceback.format_exc()
    }

    spark.createDataFrame([error_record]).write \
        .mode('append') \
        .saveAsTable('veteran_intake.error_log')
```

### Recovery Procedures

#### API Key Rotation
1. Check Databricks Secrets for backup key
2. Update primary key from backup
3. Generate new backup key
4. Update secret scope
5. Test connectivity

#### Data Corruption
1. Identify corrupted partition (by date)
2. Drop partition: `ALTER TABLE DROP PARTITION (date='2026-08-10')`
3. Re-run ingestion for that date
4. Validate row counts match source

---

**Maintained by:** 7 Eagle Group
**Last Updated:** 2026-08-10
