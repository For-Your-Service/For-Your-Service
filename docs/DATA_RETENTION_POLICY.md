# Data Retention Policy

## For Your Service - 7 Eagle Group

### Bronze Layer (Raw Data)
**Retention:** 90 days

**Rationale:**
- Job postings expire/fill quickly
- Bronze used for backfill only
- Silver layer has enriched copy

**Cleanup Job:**
```sql
-- Run monthly
DELETE FROM workspace.fys_bronze.job_postings
WHERE scrape_date < CURRENT_DATE - INTERVAL 90 DAYS;

VACUUM workspace.fys_bronze.job_postings RETAIN 0 HOURS;
```

### Silver Layer (Enriched)
**Retention:** 180 days

**Rationale:**
- Used for historical analytics
- Skill trend analysis
- Salary benchmarking

### Gold Layer (Embeddings)
**Retention:** 365 days

**Rationale:**
- Embedding model may change
- Need historical for A/B testing
- Training data for model improvements

### Veteran Profiles
**Retention:** Indefinite (user controls)

**User Rights:**
- Download profile data
- Delete account (GDPR)
- Opt-out of matching

### Audit Logs
**Retention:** 2 years

**Compliance:**
- Track all PII access
- API usage logs
- Match result logs

## Archive Strategy

### S3 Glacier for Long-term
```python
# Archive Bronze older than 90 days
df = spark.read.table("workspace.fys_bronze.job_postings")
df.filter("scrape_date < CURRENT_DATE - INTERVAL 90 DAYS") \
  .write.parquet("s3://fys-archive/bronze/")
```

### Cost Savings
- Active storage: $0.023/GB/month
- Glacier: $0.004/GB/month
- **83% cheaper** for archived data
