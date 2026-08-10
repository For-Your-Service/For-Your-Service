# Data Validation Rules

## For Your Service - Data Quality Standards

### Bronze Layer Validation

#### Required Fields
* `job_id` - Unique, not null
* `title` - Not null, min 5 characters
* `company` - Not null
* `location` - Valid format (City, STATE)
* `data_source` - Enum: [indeed, linkedin, monster, usajobs]
* `ingestion_timestamp` - ISO 8601 format

#### Validation Rules
```python
from pyspark.sql import functions as F

def validate_bronze_jobs(df):
    """Apply validation rules to bronze jobs table"""
    
    # Rule 1: No nulls in required fields
    null_check = df.filter(
        F.col('job_id').isNull() | 
        F.col('title').isNull() | 
        F.col('company').isNull()
    )
    assert null_check.count() == 0, f"Found {null_check.count()} records with null required fields"
    
    # Rule 2: Valid salary ranges
    invalid_salary = df.filter(
        (F.col('salary_min') < 0) | 
        (F.col('salary_max') < F.col('salary_min'))
    )
    assert invalid_salary.count() == 0
    
    # Rule 3: Recent ingestion timestamps
    old_records = df.filter(
        F.col('ingestion_timestamp') < F.current_timestamp() - F.expr('INTERVAL 7 DAYS')
    )
    assert old_records.count() == 0, "Found records older than 7 days"
```

### Silver Layer Validation

#### Deduplication
```python
def check_duplicates(df):
    """Ensure no duplicate job_ids in silver layer"""
    duplicates = df.groupBy('job_id').count().filter('count > 1')
    if duplicates.count() > 0:
        print(f"⚠️ Found {duplicates.count()} duplicate job_ids")
        duplicates.show()
        return False
    return True
```

#### Clearance Level Mapping
```python
VALID_CLEARANCE_LEVELS = [
    'None',
    'Public Trust',
    'Secret',
    'Top Secret',
    'TS/SCI'
]

def validate_clearance(df):
    invalid = df.filter(~F.col('clearance_required').isin(VALID_CLEARANCE_LEVELS))
    assert invalid.count() == 0, f"Invalid clearance levels found"
```

### Gold Layer Validation

#### Match Score Ranges
```python
def validate_match_scores(df):
    """Ensure all match scores are between 0 and 1"""
    invalid_scores = df.filter(
        (F.col('match_score') < 0) | 
        (F.col('match_score') > 1)
    )
    assert invalid_scores.count() == 0
    
    # Warn on low average scores
    avg_score = df.select(F.avg('match_score')).collect()[0][0]
    if avg_score < 0.6:
        print(f"⚠️ Low average match score: {avg_score:.3f}")
```

#### Top-N Validation
```python
def validate_top_n_per_veteran(df, n=10):
    """Ensure each veteran has exactly N matches"""
    counts = df.groupBy('veteran_id').count()
    
    incorrect_counts = counts.filter(f'count != {n}')
    if incorrect_counts.count() > 0:
        print(f"⚠️ {incorrect_counts.count()} veterans don't have exactly {n} matches")
        incorrect_counts.show()
```

### Automated Data Quality Checks

```python
def run_daily_dq_checks():
    """Execute all data quality validations"""
    
    results = {
        'bronze_validation': False,
        'silver_deduplication': False,
        'gold_score_validation': False,
        'timestamp': datetime.now()
    }
    
    try:
        # Bronze checks
        bronze_df = spark.table('veteran_intake.bronze_jobs')
        validate_bronze_jobs(bronze_df)
        results['bronze_validation'] = True
        
        # Silver checks
        silver_df = spark.table('veteran_intake.silver_jobs')
        results['silver_deduplication'] = check_duplicates(silver_df)
        
        # Gold checks
        gold_df = spark.table('veteran_intake.gold_matches')
        validate_match_scores(gold_df)
        results['gold_score_validation'] = True
        
    except AssertionError as e:
        print(f"❌ Data quality check failed: {e}")
        send_alert(f"DQ Check Failed: {e}")
    
    # Log results
    spark.createDataFrame([results]).write \
        .mode('append') \
        .saveAsTable('veteran_intake.dq_check_log')
    
    return results
```

### Anomaly Detection

```python
def detect_anomalies():
    """Identify unusual patterns in data"""
    
    # Check for sudden drops in ingestion volume
    daily_counts = spark.sql("""
        SELECT date(ingestion_timestamp) as date, COUNT(*) as count
        FROM veteran_intake.bronze_jobs
        WHERE ingestion_timestamp > current_date() - INTERVAL 7 DAYS
        GROUP BY 1
        ORDER BY 1
    """)
    
    avg_count = daily_counts.select(F.avg('count')).collect()[0][0]
    today_count = daily_counts.filter(F.col('date') == F.current_date()).select('count').collect()[0][0]
    
    if today_count < avg_count * 0.5:
        send_alert(f"⚠️ Today's ingestion is {(1 - today_count/avg_count)*100:.0f}% below 7-day average")
```

---

**Maintained by:** 7 Eagle Group  
**Last Updated:** 2026-08-10
