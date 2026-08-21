# Job Scraper API Documentation

**Last Updated:** August 10, 2026
**Author:** Free Hall (7 Eagle Group)
**Purpose:** Multi-source job data aggregation for veteran matching

---

## Overview

For-Your-Service integrates with multiple job APIs to provide comprehensive coverage:

| API Source | Coverage | Status | Priority |
|------------|----------|--------|----------|
| **JSearch** | Private sector | ✅ Configured | High |
| **USAJobs.gov** | Federal government | ⚠️ Pending setup | Critical |
| **Adzuna** | General aggregation | ✅ Configured | Medium |
| **LinkedIn** | Professional network | 🔄 Future | Low |

**Current State:** JSearch + Adzuna operational; USAJobs registration needed

---

## 1. JSearch API (RapidAPI)

**Status:** ✅ Credentials configured, production-ready
**Coverage:** Private sector tech roles
**Best For:** DevOps, Cloud, SRE positions at tech companies

### Quick Start

```python
import requests
from databricks.sdk.runtime import dbutils

RAPIDAPI_KEY = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(
    "https://jsearch.p.rapidapi.com/search",
    headers=headers,
    params={
        "query": "DevOps Engineer in Greenville SC",
        "page": "1",
        "date_posted": "month"
    }
)

jobs = response.json()['data']
```

### Key Features

- **Sources:** Indeed, LinkedIn, ZipRecruiter, Glassdoor, Monster
- **Rate Limits:** 300 requests/month (free), 10K/month (pro)
- **Salary Data:** Available for most postings
- **Remote Filter:** Built-in remote job filtering
- **Geolocation:** Latitude/longitude included

### Limitations

- ❌ No federal government jobs (use USAJobs for this)
- ❌ No veteran preference tracking
- ❌ No security clearance filters
- ⚠️ Rate limits on free tier

**Full Documentation:** [JSEARCH_API_INTEGRATION.md](JSEARCH_API_INTEGRATION.md)

---

## 2. USAJobs.gov API

**Status:** ⚠️ Requires registration
**Coverage:** Federal government positions
**Best For:** VA, DOD, DHS roles with veteran preference

### Registration (5 minutes)

1. Visit: https://developer.usajobs.gov/APIRequest/Index
2. Fill form:
   - Name: William Free Hall
   - Email: whall4.wh@gmail.com
   - Organization: 7 Eagle Group
   - Purpose: Veteran job matching platform
3. Receive API key via email (instant)

### Why This Matters for Veterans

- ✅ **Veteran Preference** - 5-10 points added to scores
- ✅ **Clearance Advantage** - TS/SCI reinstatement saves agencies $10K-30K
- ✅ **SF-50 Priority** - Former military get preference
- ✅ **Remote Options** - Many federal DevOps roles now remote

### Quick Start (Once Registered)

```python
headers = {
    'Host': 'data.usajobs.gov',
    'User-Agent': 'whall4.wh@gmail.com',
    'Authorization-Key': '<YOUR_KEY>'  # From Databricks Secrets
}

params = {
    'Keyword': 'DevOps Engineer',
    'LocationName': 'Greenville, South Carolina',
    'SecurityClearanceRequired': 'Secret;Top Secret',
    'ResultsPerPage': 100
}

response = requests.get(
    'https://data.usajobs.gov/api/search',
    headers=headers,
    params=params
)
```

### Expected Results for Free Hall Profile

- 50-75 DevOps/Cloud Engineer roles (GS-13/14, $120K-$170K)
- 20-30 Solutions Architect roles (GS-14/15, $140K-$180K)
- 30-50 Infrastructure roles at defense contractors

### Key Features

- **Veteran Filters:** Search by veteran status
- **Clearance Levels:** Filter by Secret, TS, TS/SCI
- **Pay Grade:** GS scale + contractor ranges
- **Agency Filter:** VA, DOD, DHS, NASA, etc.
- **No Rate Limits:** Free, unlimited requests

---

## 3. Adzuna API

**Status:** ✅ Previously configured
**Coverage:** General job aggregation (UK/US)
**Best For:** Broad market coverage

### Configuration

```python
ADZUNA_APP_ID = dbutils.secrets.get(scope="api-keys", key="adzuna-app-id")
ADZUNA_API_KEY = dbutils.secrets.get(scope="api-keys", key="adzuna-api-key")

url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
params = {
    'app_id': ADZUNA_APP_ID,
    'app_key': ADZUNA_API_KEY,
    'results_per_page': 50,
    'what': 'DevOps Engineer',
    'where': 'Greenville, SC',
    'salary_min': 120000
}
```

### Notes

- Used in Aug 7, 2026 scrape (71 jobs analyzed)
- Good for UK market coverage
- Similar to JSearch but less U.S. focused
- Free tier: 1,000 calls/month

---

## 4. LinkedIn Jobs API

**Status:** 🔄 Future consideration
**Coverage:** Professional network jobs
**Cost:** Enterprise pricing required

### Why Not Now?

- ❌ Expensive ($5K+/month for API access)
- ❌ Requires LinkedIn partnership
- ✅ Already covered by JSearch aggregation
- ✅ Can scrape public LinkedIn via JSearch

**Decision:** Not cost-effective; JSearch already indexes LinkedIn

---

## Unified Scraping Strategy

### Multi-Source Pipeline

```python
def scrape_all_sources(veteran_profile):
    """Scrape from all configured APIs."""

    all_jobs = []

    # 1. JSearch (private sector)
    jsearch_jobs = fetch_jsearch_jobs(
        query=f"{veteran_profile['target_role']} in {veteran_profile['location']}",
        max_pages=5
    )
    all_jobs.extend(transform_jsearch(jsearch_jobs))

    # 2. USAJobs (federal - if configured)
    if usajobs_key_exists():
        usajobs = fetch_usajobs(
            keyword=veteran_profile['target_role'],
            location=veteran_profile['location'],
            clearance=veteran_profile['clearance_level']
        )
        all_jobs.extend(transform_usajobs(usajobs))

    # 3. Adzuna (supplemental)
    adzuna_jobs = fetch_adzuna_jobs(
        what=veteran_profile['target_role'],
        where=veteran_profile['location']
    )
    all_jobs.extend(transform_adzuna(adzuna_jobs))

    return deduplicate_jobs(all_jobs)
```

### Deduplication Logic

```python
def deduplicate_jobs(jobs_list):
    """Remove duplicate postings across sources."""
    seen = set()
    unique_jobs = []

    for job in jobs_list:
        # Create fingerprint
        fingerprint = (
            job['title'].lower(),
            job['company'].lower(),
            job['location_city'].lower()
        )

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_jobs.append(job)

    return unique_jobs
```

---

## Cost Analysis

### Monthly API Costs (Free Tier)

| API | Free Tier | Requests Needed | Cost |
|-----|-----------|----------------|------|
| JSearch | 300/month | ~50/week | $0 |
| USAJobs | Unlimited | ~100/week | $0 |
| Adzuna | 1,000/month | ~50/week | $0 |
| **TOTAL** | - | ~200/week | **$0/month** |

### Cost Optimization

1. **Weekly Scraping** - Not daily (saves 75% of API calls)
2. **Result Caching** - 24-hour cache reduces redundant calls
3. **Smart Queries** - Targeted searches, not broad sweeps
4. **Deduplication** - Avoid re-processing same jobs

**Result:** Entire job scraping infrastructure runs FREE

---

## Error Handling

### Retry Logic with Exponential Backoff

```python
import time

def fetch_with_retry(api_function, max_retries=3):
    """Retry API calls with exponential backoff."""

    for attempt in range(max_retries):
        try:
            return api_function()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait)
            else:
                raise
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                print("Rate limit hit - pausing scrape")
                return None
            else:
                raise
```

---

## Monitoring & Alerts

### API Usage Tracking

```python
def log_api_usage(api_name, requests_made, requests_remaining):
    """Track API usage for monitoring."""

    usage_data = {
        'api': api_name,
        'timestamp': datetime.utcnow().isoformat(),
        'requests_made': requests_made,
        'requests_remaining': requests_remaining,
        'usage_percent': (requests_made / (requests_made + requests_remaining)) * 100
    }

    # Write to monitoring table
    spark.createDataFrame([usage_data]).write.mode('append').saveAsTable(
        'workspace.fys_monitoring.api_usage'
    )

    # Alert if > 80% usage
    if usage_data['usage_percent'] > 80:
        send_alert(f"⚠️ {api_name} at {usage_data['usage_percent']:.1f}% capacity")
```

---

## Security Checklist

- [x] JSearch API key stored in Databricks Secrets
- [ ] USAJobs API key stored in Databricks Secrets (pending registration)
- [x] No credentials in source code
- [x] No credentials in git commits
- [x] Request logging without exposing keys
- [ ] Quarterly credential rotation policy
- [ ] Usage monitoring dashboard

---

## Next Steps

1. **Register USAJobs API** (5 minutes)
   - Visit https://developer.usajobs.gov
   - Complete registration form
   - Add key to Databricks Secrets

2. **Run Initial Multi-Source Scrape** (20 minutes)
   - JSearch: ~100 private sector jobs
   - USAJobs: ~100 federal jobs
   - Adzuna: ~50 supplemental jobs
   - **Total: 200-250 unique matches**

3. **Schedule Weekly Automation** (15 minutes)
   - Databricks Job for weekly scraping
   - Automatic matching pipeline
   - Email reports to veterans

4. **Monitor Performance** (Ongoing)
   - Track API usage
   - Measure match quality
   - Refine queries based on results

---

## Related Documentation

- [JSearch Integration Guide](JSEARCH_API_INTEGRATION.md) - Detailed JSearch setup
- [Veteran Profile Schema](VETERAN_PROFILE_SCHEMA.md) - Data model
- [Matching Algorithm](MATCHING_ALGORITHM.md) - Scoring logic
- [Deployment Guide](DEPLOYMENT_HUGGINGFACE.md) - Production deployment

---

**Questions or Issues?**
Contact: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
