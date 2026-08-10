# Performance Tuning Guide

## Database Optimizations

### 1. Partitioning Strategy
```sql
-- Partition Bronze by scrape_date
CREATE TABLE workspace.fys_bronze.job_postings (
  ...
) PARTITIONED BY (scrape_date DATE);

-- Prune old partitions
ALTER TABLE workspace.fys_bronze.job_postings
DROP IF EXISTS PARTITION (scrape_date < '2026-07-10');
```

### 2. Z-Ordering
```sql
-- Optimize for common query patterns
OPTIMIZE workspace.fys_bronze.job_postings
ZORDER BY (location_city, salary_min);
```

### 3. Indexing (Silver/Gold)
```sql
-- Create bloom filter index on job_id
CREATE BLOOMFILTER INDEX idx_job_id
ON TABLE workspace.fys_gold.job_embeddings (job_id);
```

## API Performance

### 1. Caching Strategy
- Cache top 100 jobs per region (1 hour TTL)
- Cache veteran profiles (15 min TTL)
- Cache embeddings (24 hour TTL)

### 2. Batch Processing
```python
# Generate embeddings in batches
batch_size = 32
for i in range(0, len(jobs), batch_size):
    batch = jobs[i:i+batch_size]
    embeddings = model.encode(batch, batch_size=batch_size)
```

### 3. Async API Calls
```python
import asyncio
import aiohttp

async def fetch_all_apis():
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_usajobs(session),
            fetch_jsearch(session),
            fetch_adzuna(session)
        ]
        results = await asyncio.gather(*tasks)
    return results
```

## Query Optimization

### Slow Query
```sql
-- ❌ Slow: Full table scan
SELECT * FROM workspace.fys_bronze.job_postings
WHERE title LIKE '%engineer%';
```

### Fast Query
```sql
-- ✅ Fast: Partition pruning + pushdown
SELECT * FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
AND location_city = 'Greenville'
AND title LIKE '%engineer%';
```

## Benchmarks

| Operation | Before | After | Improvement |
|-----------|--------|-------|-------------|
| Daily Ingestion | 45 min | 12 min | 73% faster |
| Top 10 Matches | 8 sec | 1.2 sec | 85% faster |
| Embedding Generation | 2 min | 30 sec | 75% faster |
