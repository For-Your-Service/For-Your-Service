# JSearch API Integration Guide

**Integration Date:** August 10, 2026  
**API Provider:** RapidAPI (JSearch)  
**Purpose:** Private sector job aggregation for veteran matching  
**Status:** ✅ Credentials configured, ready for production

---

## Overview

JSearch via RapidAPI aggregates job postings from multiple sources:
- Indeed
- LinkedIn
- ZipRecouiter
- Glassdoor
- Monster
- CareerBuilder

**Complementary to USAJobs:** JSearch provides private sector coverage while USAJobs.gov API covers federal positions.

---

## API Specifications

### Base Configuration

```python
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}/search"
```

### Required Headers

```python
headers = {
    "X-RapidAPI-Key": "<YOUR_API_KEY>",  # Stored in Databricks Secrets
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}
```

### Rate Limits

- **Free Tier:** 300 requests/month
- **Pro Tier:** 10,000 requests/month
- **Recommended:** Implement request caching and result persistence

---

## Search Parameters

### Veteran-Optimized Query Structure

```python
params = {
    "query": "DevOps Engineer in Greenville SC",
    "page": "1",
    "num_pages": "1",           # Max 20 per request
    "date_posted": "month",      # Options: all, today, 3days, week, month
    "remote_jobs_only": "false", # Set true for remote-only
    "employment_types": "FULLTIME",
    "job_requirements": "no_degree"  # Optional: under_3_years_experience, etc.
}
```

### Location Targeting

**For Greenville, SC veterans:**
```python
queries = [
    "DevOps Engineer in Greenville SC",
    "Cloud Architect remote South Carolina",
    "Site Reliability Engineer Greenville SC",
    "Platform Engineer remote",
    "Solutions Architect Greenville South Carolina"
]
```

---

## Response Structure

### Sample Job Object

```json
{
  "job_id": "abc123",
  "job_title": "Senior DevOps Engineer",
  "employer_name": "Tech Corp",
  "employer_logo": "https://...",
  "job_city": "Greenville",
  "job_state": "SC",
  "job_country": "US",
  "job_latitude": 34.8526,
  "job_longitude": -82.3940,
  "job_employment_type": "FULLTIME",
  "job_min_salary": 120000,
  "job_max_salary": 150000,
  "job_salary_currency": "USD",
  "job_salary_period": "YEAR",
  "job_is_remote": false,
  "job_posted_at_timestamp": 1691443200,
  "job_posted_at_datetime_utc": "2026-08-08T00:00:00Z",
  "job_description": "Full job description text...",
  "job_apply_link": "https://...",
  "job_apply_is_direct": true,
  "job_required_skills": ["AWS", "Docker", "Kubernetes"],
  "job_benefits": ["Health Insurance", "401k", "PTO"]
}
```

---

## Integration with Matching Pipeline

### Step 1: Fetch Jobs

```python
import requests
from databricks.sdk.runtime import dbutils

# Get API key from Databricks Secrets
RAPIDAPI_KEY = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")

def fetch_jsearch_jobs(query, max_pages=5):
    """Fetch jobs from JSearch API with pagination."""
    all_jobs = []
    
    for page in range(1, max_pages + 1):
        params = {
            "query": query,
            "page": str(page),
            "num_pages": "1",
            "date_posted": "month"
        }
        
        response = requests.get(
            f"https://jsearch.p.rapidapi.com/search",
            headers={
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            },
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('data', [])
            all_jobs.extend(jobs)
            
            # Stop if no more results
            if len(jobs) == 0:
                break
        else:
            print(f"Error on page {page}: {response.status_code}")
            break
    
    return all_jobs
```

### Step 2: Transform to Standard Schema

```python
def transform_jsearch_to_standard(jsearch_job):
    """Convert JSearch format to For-Your-Service schema."""
    return {
        "job_id": jsearch_job.get("job_id"),
        "source": "jsearch",
        "title": jsearch_job.get("job_title"),
        "company": jsearch_job.get("employer_name"),
        "location_city": jsearch_job.get("job_city"),
        "location_state": jsearch_job.get("job_state"),
        "location_display": f"{jsearch_job.get('job_city', '')}, {jsearch_job.get('job_state', '')}",
        "is_remote": jsearch_job.get("job_is_remote", False),
        "salary_min": jsearch_job.get("job_min_salary"),
        "salary_max": jsearch_job.get("job_max_salary"),
        "salary_currency": jsearch_job.get("job_salary_currency", "USD"),
        "description": jsearch_job.get("job_description"),
        "required_skills": jsearch_job.get("job_required_skills", []),
        "employment_type": jsearch_job.get("job_employment_type"),
        "posted_date": jsearch_job.get("job_posted_at_datetime_utc"),
        "apply_url": jsearch_job.get("job_apply_link"),
        "is_direct_apply": jsearch_job.get("job_apply_is_direct", False),
        "benefits": jsearch_job.get("job_benefits", []),
        "scraped_at": datetime.utcnow().isoformat()
    }
```

### Step 3: Load to Bronze Layer

```python
from pyspark.sql import SparkSession

def load_jsearch_to_bronze(jobs_list, veteran_name):
    """Load JSearch jobs to Unity Catalog bronze layer."""
    spark = SparkSession.builder.getOrCreate()
    
    # Transform to standard schema
    standardized = [transform_jsearch_to_standard(job) for job in jobs_list]
    
    # Convert to DataFrame
    df = spark.createDataFrame(standardized)
    
    # Add metadata
    from pyspark.sql.functions import current_timestamp, lit
    df = df.withColumn("ingestion_timestamp", current_timestamp())
    df = df.withColumn("veteran_profile", lit(veteran_name))
    df = df.withColumn("data_source", lit("jsearch_api"))
    
    # Write to bronze
    table_name = "workspace.fys_bronze.job_postings_jsearch"
    df.write.mode("append").saveAsTable(table_name)
    
    return len(standardized)
```

---

## Cost Optimization Strategies

### 1. Request Caching

```python
import json
from datetime import datetime, timedelta

def get_cached_results(query, cache_hours=24):
    """Check for recent cached results before hitting API."""
    cache_path = f"/dbfs/fys/cache/jsearch/{query.replace(' ', '_')}.json"
    
    try:
        with open(cache_path, 'r') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            
            if datetime.utcnow() - cache_time < timedelta(hours=cache_hours):
                return cache['data']
    except FileNotFoundError:
        pass
    
    return None
```

### 2. Batch Processing

- Run scrapes weekly (not daily) to stay under rate limits
- Combine multiple queries in one session
- Store results in Unity Catalog for repeated analysis

### 3. Smart Query Design

```python
# GOOD: Targeted, efficient queries
queries = [
    "Senior DevOps Engineer Greenville SC",
    "Cloud Architect remote South Carolina"
]

# BAD: Too broad, wastes API calls
queries = [
    "engineer",  # Returns millions of irrelevant jobs
    "manager"    # Not specific enough
]
```

---

## Comparison: JSearch vs USAJobs

| Feature | JSearch (RapidAPI) | USAJobs.gov API |
|---------|-------------------|-----------------|
| **Coverage** | Private sector | Federal government |
| **Sources** | Indeed, LinkedIn, etc. | Official USAJobs.gov |
| **Cost** | $0-$50/month | FREE (no limits) |
| **Rate Limits** | 300-10K/month | No documented limit |
| **Best For** | Tech companies, startups | VA, DOD, agencies |
| **Veteran Advantage** | Experience-based | Veteran Preference ★★★ |
| **Clearance Filter** | No | Yes (Secret, TS, TS/SCI) |

**Recommendation:** Use BOTH for comprehensive coverage.

---

## Production Deployment Checklist

- [ ] Store API key in Databricks Secrets (not in code)
- [ ] Implement request caching (24-hour window)
- [ ] Set up error handling and retry logic
- [ ] Configure alerts for rate limit warnings
- [ ] Schedule weekly scraping job (not daily)
- [ ] Monitor API usage via RapidAPI dashboard
- [ ] Validate data quality in bronze layer
- [ ] Document any API changes or deprecations

---

## Error Handling

### Common Error Codes

```python
def handle_jsearch_response(response):
    """Handle JSearch API responses with proper error management."""
    
    if response.status_code == 200:
        return response.json()
    
    elif response.status_code == 429:
        # Rate limit hit
        raise Exception("JSearch rate limit exceeded. Retry after cooldown period.")
    
    elif response.status_code == 401:
        # Authentication failed
        raise Exception("Invalid JSearch API key. Check Databricks Secrets configuration.")
    
    elif response.status_code == 400:
        # Bad request
        raise Exception(f"Invalid JSearch query parameters: {response.text}")
    
    else:
        raise Exception(f"JSearch API error {response.status_code}: {response.text}")
```

---

## Security Best Practices

### ✅ DO

- Store API keys in Databricks Secrets
- Use environment variables for local development
- Implement request logging (without exposing keys)
- Rotate API keys quarterly
- Monitor usage for suspicious activity

### ❌ DON'T

- Hardcode API keys in source code
- Commit credentials to git repositories
- Share API keys in Slack/email
- Use production keys in test environments
- Log full API responses (may contain sensitive data)

---

## Testing

### Validate API Connection

```python
def test_jsearch_connection():
    """Test JSearch API connection and credentials."""
    RAPIDAPI_KEY = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
    
    response = requests.get(
        "https://jsearch.p.rapidapi.com/search",
        headers={
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        },
        params={
            "query": "test",
            "page": "1",
            "num_pages": "1"
        },
        timeout=10
    )
    
    assert response.status_code == 200, f"API test failed: {response.status_code}"
    print("✅ JSearch API connection successful")
    return True
```

---

## Next Steps

1. **Set up Databricks Secrets** - Store JSearch API key securely
2. **Add USAJobs API** - Complement with federal job coverage
3. **Build unified scraper** - Combine JSearch + USAJobs data
4. **Schedule automation** - Weekly job scraping pipeline
5. **Monitor performance** - Track API usage and match quality

---

**Author:** Free Hall (7 Eagle Group)  
**Last Updated:** August 10, 2026  
**Related Docs:** 
- [Job Scraper APIs](JOB_SCRAPER_APIS.md)
- [Deployment Guide](DEPLOYMENT_HUGGINGFACE.md)
- [Matching Algorithm](MATCHING_ALGORITHM.md)
