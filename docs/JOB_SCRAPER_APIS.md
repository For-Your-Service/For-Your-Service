# Job Scraper API Configuration

## Overview
Configuration and integration guide for real-time job scraping APIs used in For Your Service platform.

## Supported Job Boards

### 1. USAJobs (Federal Government Jobs)
**Best for:** Veterans with security clearances, federal employment

**API Endpoint:** `https://data.usajobs.gov/api/search`

**Authentication:** API Key (free registration required)
- Register at: https://developer.usajobs.gov/
- Store credentials in Databricks Secrets

**Request Example:**
```python
import requests

headers = {
    'Host': 'data.usajobs.gov',
    'User-Agent': 'whall4.wh@gmail.com',
    'Authorization-Key': '<API_KEY>'
}

params = {
    'Keyword': 'DevOps Engineer',
    'LocationName': 'Greenville, SC',
    'SecurityClearanceRequired': 'Secret',
    'ResultsPerPage': 100
}

response = requests.get('https://data.usajobs.gov/api/search', 
                       headers=headers, 
                       params=params)
```

**Rate Limits:** 
- 250 requests per day (free tier)
- 1 request per second

---

### 2. Adzuna API
**Best for:** Aggregated job postings from multiple sources

**API Endpoint:** `https://api.adzuna.com/v1/api/jobs/us/search`

**Authentication:** App ID + App Key (free registration)
- Register at: https://developer.adzuna.com/

**Request Example:**
```python
url = f'https://api.adzuna.com/v1/api/jobs/us/search/1'
params = {
    'app_id': '<APP_ID>',
    'app_key': '<APP_KEY>',
    'what': 'Cloud Engineer',
    'where': 'Greenville, SC',
    'results_per_page': 50,
    'content-type': 'application/json'
}

response = requests.get(url, params=params)
```

**Rate Limits:**
- Free: 250 calls/month
- Developer: 500 calls/month ($50)
- Production: Custom pricing

---

### 3. Indeed Scraper (via RapidAPI)
**Best for:** Largest job board, comprehensive coverage

**API Endpoint:** `https://indeed-indeed.p.rapidapi.com/apisearch`

**Authentication:** RapidAPI Key
- Subscribe at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/indeed-indeed

**Request Example:**
```python
headers = {
    'X-RapidAPI-Key': '<RAPIDAPI_KEY>',
    'X-RapidAPI-Host': 'indeed-indeed.p.rapidapi.com'
}

params = {
    'query': 'Solutions Architect',
    'location': 'Greenville, SC',
    'page_id': '1',
    'locality': 'us',
    'fromage': '7'  # Last 7 days
}

response = requests.get('https://indeed-indeed.p.rapidapi.com/apisearch',
                       headers=headers,
                       params=params)
```

**Rate Limits:**
- Basic: 100 requests/month (free)
- Pro: 10,000 requests/month ($29.99)

---

### 4. LinkedIn Job Search (via RapidAPI)
**Best for:** Professional network, high-quality roles

**API Endpoint:** `https://linkedin-data-api.p.rapidapi.com/search-jobs`

**Authentication:** RapidAPI Key

**Request Example:**
```python
headers = {
    'X-RapidAPI-Key': '<RAPIDAPI_KEY>',
    'X-RapidAPI-Host': 'linkedin-data-api.p.rapidapi.com'
}

params = {
    'keywords': 'Kubernetes DevOps',
    'locationId': '103644278',  # United States
    'datePosted': 'pastWeek',
    'sort': 'mostRelevant'
}
```

**Rate Limits:**
- Basic: 500 requests/month ($9.99)
- Pro: 5,000 requests/month ($49.99)

---

## Search Strategy for William Free Hall

### Target Keywords
```python
SEARCH_KEYWORDS = [
    # Primary roles
    "DevOps Engineer",
    "Solutions Architect",
    "Cloud Engineer",
    "Site Reliability Engineer",
    "Platform Engineer",
    
    # Technology-specific
    "AWS Architect",
    "Kubernetes Engineer",
    "Terraform Engineer",
    "Infrastructure Engineer",
    
    # Leadership roles
    "Engineering Manager",
    "Technical Lead",
    "VP Engineering"
]
```

### Target Locations
```python
LOCATIONS = [
    "Greenville, SC",
    "Spartanburg, SC",
    "Anderson, SC",
    "Remote",
    "Charlotte, NC",  # 1.5 hours
    "Atlanta, GA"      # 2 hours
]
```

### Filters
```python
FILTERS = {
    'salary_min': 120000,
    'salary_max': 180000,
    'remote_preference': ['Remote', 'Hybrid', 'On-site'],
    'posted_within_days': 14,
    'security_clearance': ['Secret', 'Top Secret', 'TS/SCI', 'None']
}
```

---

## Scraping Schedule

**Bronze Layer (Raw Data Ingestion):**
- Run: Every 6 hours
- Retention: 30 days
- De-duplication: By job_id

**Silver Layer (Cleaned/Normalized):**
- Run: Every 6 hours (triggered by Bronze)
- Retention: 90 days
- Transformations: Salary parsing, location standardization

**Gold Layer (Match Scores):**
- Run: Daily at 6 AM UTC
- Retention: 365 days
- ML Model: Siamese neural network

---

## Cost Optimization

**FREE Tier Strategy:**
```python
# Prioritize free APIs
API_PRIORITY = [
    ('USAJobs', 'free', 250),      # 250 requests/day
    ('Adzuna', 'free', 8),          # 250/month = ~8/day
]

# Total daily scrapes: ~258 job postings
# Monthly cost: $0
```

**Paid Tier (Production):**
```python
API_PRIORITY = [
    ('USAJobs', 'free', 250),
    ('Adzuna', 'dev', 16),          # 500/month
    ('Indeed', 'pro', 333),         # 10,000/month
    ('LinkedIn', 'pro', 166)        # 5,000/month
]

# Total daily scrapes: ~765 job postings
# Monthly cost: ~$90
```

---

## Error Handling

```python
def scrape_with_retry(api_name, params, max_retries=3):
    """
    Retry logic for API failures
    """
    for attempt in range(max_retries):
        try:
            response = call_api(api_name, params)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                wait_time = int(response.headers.get('Retry-After', 60))
                time.sleep(wait_time)
            else:
                log_error(api_name, response.status_code)
        except Exception as e:
            log_error(api_name, str(e))
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return None
```

---

**Created:** August 10, 2026  
**Author:** William Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group
