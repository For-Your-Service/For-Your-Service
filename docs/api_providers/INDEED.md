# Indeed API Integration

## Overview
Indeed is the #1 job site worldwide with 250+ million unique visitors monthly.

## API Access
* **Endpoint:** `https://api.indeed.com/ads/apisearch`
* **Authentication:** API Key
* **Rate Limit:** 100 requests/minute
* **Documentation:** https://opensource.indeedeng.io/api-documentation/

## Required Parameters
* `publisher` - Your API publisher key
* `q` - Search query (e.g., "DevOps Engineer")
* `l` - Location (e.g., "Greenville, SC")
* `format` - Response format (json, xml)

## Optional Parameters
* `limit` - Results per page (default: 25, max: 50)
* `start` - Pagination offset
* `radius` - Search radius in miles (default: 25)
* `age` - Days since posting (e.g., 7 for last week)
* `fromage` - Alias for age
* `highlight` - Highlight query terms (0 or 1)
* `filter` - Remove duplicate results (0 or 1)
* `latlong` - Use lat/long instead of location string

## Response Fields
```json
{
  "results": [{
    "jobtitle": "DevOps Engineer",
    "company": "TechCorp",
    "formattedLocation": "Greenville, SC",
    "jobkey": "abc123xyz",
    "snippet": "Job description preview...",
    "date": "Fri, 05 Aug 2026 12:00:00 GMT",
    "url": "https://www.indeed.com/viewjob?jk=abc123xyz"
  }]
}
```

## Example Code
```python
import requests

def fetch_indeed_jobs(query, location, api_key):
    url = "https://api.indeed.com/ads/apisearch"
    params = {
        'publisher': api_key,
        'q': query,
        'l': location,
        'format': 'json',
        'limit': 50,
        'filter': 1
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['results']
```

## Veteran-Specific Tips
* Include "veteran" in query for veteran-friendly postings
* Filter by `company` to target veteran-hiring employers
* Check `snippet` for keywords: clearance, military, veteran
* Use `radius=50` for broader rural area coverage

---
**Maintained by:** 7 Eagle Group  
**Last Updated:** 2026-08-10
