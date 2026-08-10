# 📊 Monitoring & Observability

## Daily Health Checks

Run these queries every morning:

### 1. Ingestion Status
```sql
-- Check if yesterday's ingestion completed
SELECT COUNT(*) as jobs_ingested
FROM workspace.fys_bronze.job_postings
WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS;
```

**Expected:** 200-500 jobs for Greenville MSA

### 2. Per-Source Breakdown
```sql
SELECT source, COUNT(*) as count
FROM workspace.fys_bronze.job_postings
WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS
GROUP BY source;
```

**Expected:**
- USAJOBS: 50-100
- JSearch: 100-300  
- Adzuna: 50-150

### 3. Data Quality Score
```sql
SELECT 
  ROUND(100.0 * SUM(CASE WHEN salary.min IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) as salary_completeness,
  ROUND(100.0 * SUM(CASE WHEN description != '' THEN 1 ELSE 0 END) / COUNT(*), 1) as description_completeness
FROM workspace.fys_bronze.job_postings
WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS;
```

**Expected:** Both >70%

## Alert Conditions

### Critical
- ❌ Zero jobs ingested yesterday
- ❌ Any source returning 0 jobs
- ❌ Ingestion job failed

### Warning
- ⚠️ <100 jobs ingested (normally 200-500)
- ⚠️ Salary completeness <50%
- ⚠️ Ingestion duration >30 min

## Dashboards

Use Databricks SQL dashboards:
1. **Daily Ingestion**: Trends over 30 days
2. **Source Health**: Per-source metrics
3. **Regional Coverage**: Jobs by city/state
4. **Salary Intelligence**: Compensation trends
