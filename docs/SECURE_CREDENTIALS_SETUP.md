# Secure API Credential Storage Guide

**Author:** Free Hall (7 Eagle Group)  
**Last Updated:** August 10, 2026  
**Purpose:** Store and access API keys securely without git exposure

---

## Overview

**Problem:** API keys hardcoded in code = security risk + git exposure  
**Solution:** Databricks Secrets for encrypted credential storage

### APIs We're Securing

| API | Purpose | Status |
|-----|---------|--------|
| **JSearch (RapidAPI)** | Private sector jobs | ✅ Have credentials |
| **USAJobs.gov** | Federal government jobs | ⚠️ Pending registration |

---

## Quick Start: Store Your JSearch API Key (2 minutes)

### Using Databricks UI (Recommended)

1. **Navigate to Secrets:**
   ```
   User Profile → Settings → Admin Console → Secrets
   Direct URL: https://dbc-3e95d032-684c.cloud.databricks.com/#secrets
   ```

2. **Create Secret Scope:**
   - Click "Create Scope"
   - Name: `api-keys`
   - Managed Principal: All Users (or restrict)
   - Click "Create"

3. **Add Your JSearch Credentials:**
   
   Secret #1:
   - Key: `jsearch-rapidapi-key`
   - Value: [paste your RapidAPI key]
   
   Secret #2:
   - Key: `jsearch-rapidapi-host`
   - Value: `jsearch.p.rapidapi.com`

✅ **Done!** Credentials are now encrypted and secure.

---

## Access Secrets in Code

### Basic Usage

```python
from databricks.sdk.runtime import dbutils
import requests

# Fetch credentials (always shows [REDACTED] if printed)
API_KEY = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
API_HOST = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")

# Use in API calls
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

response = requests.get(
    f"https://{API_HOST}/search",
    headers=headers,
    params={"query": "DevOps Engineer Greenville SC", "page": "1"}
)

print(f"Status: {response.status_code}")
```

### Complete Secure Scraper

```python
def fetch_jsearch_jobs_secure(query, max_results=100):
    """
    Fetch jobs from JSearch using Databricks Secrets.
    No API keys exposed in code or logs.
    """
    from databricks.sdk.runtime import dbutils
    import requests
    
    # Securely fetch credentials
    api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
    api_host = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    
    all_jobs = []
    page = 1
    
    while len(all_jobs) < max_results:
        params = {
            "query": query,
            "page": str(page),
            "date_posted": "month"
        }
        
        try:
            response = requests.get(
                f"https://{api_host}/search",
                headers=headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                if not jobs:
                    break
                all_jobs.extend(jobs)
                page += 1
            elif response.status_code == 429:
                print("⚠️  Rate limit reached")
                break
            else:
                print(f"API error: {response.status_code}")
                break
                
        except requests.exceptions.Timeout:
            print("Request timeout")
            break
    
    return all_jobs[:max_results]

# Usage
jobs = fetch_jsearch_jobs_secure(
    query="DevOps Engineer Greenville SC",
    max_results=50
)
print(f"✅ Securely fetched {len(jobs)} jobs")
```

---

## Add USAJobs API (After Registration)

### Step 1: Register (5 minutes)

1. Visit: https://developer.usajobs.gov/APIRequest/Index
2. Fill out form:
   - Name: William Free Hall
   - Email: whall4.wh@gmail.com
   - Organization: 7 Eagle Group
   - Purpose: Veteran job matching platform
3. Receive API key via email (instant)

### Step 2: Store Credentials

In Databricks Secrets UI:
- Add secret: `usajobs-api-key` → [your key from email]
- Add secret: `usajobs-email` → `whall4.wh@gmail.com`

### Step 3: Use in Code

```python
def fetch_usajobs_secure(keyword, location, clearance_levels=None):
    """Fetch federal jobs using secure credentials."""
    from databricks.sdk.runtime import dbutils
    import requests
    
    # Securely fetch credentials
    api_key = dbutils.secrets.get(scope="api-keys", key="usajobs-api-key")
    user_email = dbutils.secrets.get(scope="api-keys", key="usajobs-email")
    
    headers = {
        'Host': 'data.usajobs.gov',
        'User-Agent': user_email,
        'Authorization-Key': api_key
    }
    
    params = {
        'Keyword': keyword,
        'LocationName': location,
        'ResultsPerPage': 100
    }
    
    if clearance_levels:
        params['SecurityClearanceRequired'] = ';'.join(clearance_levels)
    
    response = requests.get(
        'https://data.usajobs.gov/api/search',
        headers=headers,
        params=params,
        timeout=20
    )
    
    if response.status_code == 200:
        data = response.json()
        jobs = data['SearchResult']['SearchResultItems']
        return [job['MatchedObjectDescriptor'] for job in jobs]
    return []

# Usage
federal_jobs = fetch_usajobs_secure(
    keyword="DevOps Engineer",
    location="Greenville, South Carolina",
    clearance_levels=["Secret", "Top Secret"]
)
print(f"✅ Found {len(federal_jobs)} federal jobs")
```

---

## Verification Test

```python
def test_secrets_setup():
    """Verify secrets are configured correctly."""
    from databricks.sdk.runtime import dbutils
    
    print("=" * 60)
    print("🔒 TESTING SECURE CREDENTIALS")
    print("=" * 60)
    
    # Test JSearch
    try:
        api_key = dbutils.secrets.get("api-keys", "jsearch-rapidapi-key")
        api_host = dbutils.secrets.get("api-keys", "jsearch-rapidapi-host")
        print("✅ JSearch credentials: CONFIGURED")
    except Exception as e:
        print(f"❌ JSearch credentials: MISSING - {e}")
    
    # Test USAJobs (optional)
    try:
        usajobs_key = dbutils.secrets.get("api-keys", "usajobs-api-key")
        usajobs_email = dbutils.secrets.get("api-keys", "usajobs-email")
        print("✅ USAJobs credentials: CONFIGURED")
    except:
        print("⚠️  USAJobs: NOT CONFIGURED (register first)")
    
    print("=" * 60)

# Run test
test_secrets_setup()
```

---

## Security Comparison

### ❌ INSECURE (Never do this)

```python
# Hardcoded API key
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY_NEVER_HARDCODE"

# Committed to git → public → compromised
headers = {"X-RapidAPI-Key": RAPIDAPI_KEY}
```

### ✅ SECURE (Always do this)

```python
# Fetch from Databricks Secrets
from databricks.sdk.runtime import dbutils
RAPIDAPI_KEY = dbutils.secrets.get("api-keys", "jsearch-rapidapi-key")

# Not in git → encrypted → safe
headers = {"X-RapidAPI-Key": RAPIDAPI_KEY}
```

---

## Security Best Practices

### ✅ DO

- Store ALL API keys in Databricks Secrets
- Use secrets for passwords, tokens, credentials
- Limit secret scope access
- Rotate keys quarterly
- Test secret access before deploying

### ❌ DON'T

- Hardcode API keys in notebooks
- Commit credentials to git
- Print secret values (auto-redacted anyway)
- Share secrets via Slack/email
- Use production keys in test environments

---

## Required Secrets Summary

| Secret Key | Value | Status |
|------------|-------|--------|
| `jsearch-rapidapi-key` | Your RapidAPI key | ✅ Have key |
| `jsearch-rapidapi-host` | `jsearch.p.rapidapi.com` | ✅ Known |
| `usajobs-api-key` | From developer.usajobs.gov | ⚠️ Register |
| `usajobs-email` | `whall4.wh@gmail.com` | ✅ Known |

---

## Troubleshooting

### "Secret scope does not exist"

**Fix:** Create `api-keys` scope in UI:
- Settings → Admin Console → Secrets → Create Scope

### "Secret does not exist"  

**Fix:** Add secret in UI:
- Select `api-keys` scope → Add Secret

### "Access denied"

**Fix:** Check you created the scope or have read access

---

## Next Steps

1. ✅ **Set up `api-keys` scope** (2 min - Databricks UI)
2. ✅ **Store JSearch credentials** (1 min)
3. ✅ **Run verification test** (30 sec)
4. ⚠️ **Register USAJobs** (5 min - https://developer.usajobs.gov)
5. ⚠️ **Store USAJobs credentials** (1 min)
6. 🚀 **Run combined scraper** (15 min → 200+ job matches)

---

**Author:** Free Hall  
**Organization:** 7 Eagle Group  
**Contact:** whall4.wh@gmail.com

**Related Documentation:**
- [JSearch Integration Guide](JSEARCH_API_INTEGRATION.md)
- [Job Scraper APIs Overview](JOB_SCRAPER_APIS.md)
- [Veteran Profile Schema](VETERAN_PROFILE_SCHEMA.md)
