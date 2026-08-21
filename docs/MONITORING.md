# Monitoring & Observability

## For Your Service - Production Monitoring

### Key Metrics

#### 1. Ingestion Health
* **Jobs ingested per hour** - Target: >1,000
* **API success rate** - Target: >95%
* **Data freshness** - Max lag: 15 minutes
* **Duplicate rate** - Target: <2%

#### 2. Matching Engine Performance
* **Match latency** - Target: <500ms per veteran
* **Neural network inference time** - Target: <100ms
* **Top-10 accuracy** - Target: >85% (validated by 7 Eagle Group)
* **Matches generated per day** - Target: >500

#### 3. System Health
* **CPU utilization** - Warning: >70%, Critical: >85%
* **Memory usage** - Warning: >75%, Critical: >90%
* **Disk I/O** - Monitor for bottlenecks
* **Network latency** - API response times

### Databricks Monitoring

```sql
-- Job ingestion rate (last 24 hours)
SELECT
  date_trunc('hour', ingestion_timestamp) as hour,
  data_source,
  COUNT(*) as jobs_ingested
FROM veteran_intake.bronze_jobs
WHERE ingestion_timestamp > current_timestamp() - INTERVAL 1 DAY
GROUP BY 1, 2
ORDER BY 1 DESC

-- Match quality metrics
SELECT
  veteran_id,
  COUNT(*) as total_matches,
  AVG(match_score) as avg_score,
  MAX(match_score) as best_score
FROM veteran_intake.silver_matches
WHERE match_date = current_date()
GROUP BY 1
HAVING COUNT(*) < 10  -- Alert on low match counts
```

### Alerting Rules

#### Critical Alerts (Page On-Call)
* API authentication failures >3 in 10 minutes
* Zero jobs ingested for >30 minutes during business hours
* Neural network inference errors >5% of requests
* Database connection failures

#### Warning Alerts (Slack/Email)
* Ingestion rate drops >50% compared to 24h average
* Match scores consistently <0.5 (quality issue)
* Dead letter queue >100 records
* API rate limits hit >10 times per hour

### Dashboards

#### 1. Executive Dashboard (Databricks SQL)
* Total veterans served
* Jobs matched today/week/month
* Placement success rate
* Cost per match (infrastructure)

#### 2. Engineering Dashboard
* API health by provider (Indeed, LinkedIn, etc.)
* Pipeline run status (success/failed/running)
* Error rates by component
* Resource utilization trends

#### 3. Data Quality Dashboard
* Schema validation failures
* Null percentage by column
* Data freshness by source
* Duplicate detection rate

### Log Aggregation

```python
# Structured logging for all components
import logging
import json

logger = logging.getLogger(__name__)

def log_event(event_type, message, context={}):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'message': message,
        'context': context,
        'service': 'for-your-service',
        'environment': 'production'
    }
    logger.info(json.dumps(log_entry))
```

### Health Check Endpoints

```python
# /health endpoint for Kubernetes liveness
def health_check():
    checks = {
        'database': check_database_connection(),
        'model_loaded': check_model_loaded(),
        'api_keys': check_api_keys_valid()
    }

    if all(checks.values()):
        return {'status': 'healthy', 'checks': checks}, 200
    else:
        return {'status': 'unhealthy', 'checks': checks}, 503
```

### Performance Optimization

* **Index key columns**: veteran_id, job_id, match_date
* **Partition tables**: By date for time-series data
* **Cache frequent queries**: Job descriptions, veteran profiles
* **Optimize joins**: Broadcast small tables (<10MB)

---

**Owner:** 7 Eagle Group
**Updated:** 2026-08-10
