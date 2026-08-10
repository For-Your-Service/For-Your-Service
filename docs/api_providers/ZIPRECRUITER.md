# ZipRecruiter API Integration

## Overview
AI-powered matching with 2+ million employers.

## API Access
* **Endpoint:** `https://api.ziprecruiter.com/jobs-api`
* **Authentication:** API Key
* **Rate Limit:** 50 requests/minute (strict)
* **Free Tier:** 1,000 calls/month

## Search Parameters
* `api_key` - Your API key
* `search` - Job title or keywords
* `location` - City, state, or zip
* `radius_miles` - Search radius (default: 25)
* `days_ago` - Freshness filter

## Response Format
```json
{
  "jobs": [{
    "id": "abc123",
    "name": "Cloud Architect",
    "hiring_company": {
      "name": "CloudCorp"
    },
    "location": "Greenville, SC",
    "snippet": "...",
    "posted_time": "2026-08-05T10:30:00Z",
    "salary_interval": "yearly",
    "salary_min": "140000",
    "salary_max": "180000"
  }]
}
```

## Smart Matching
ZipRecruiter's AI matches based on:
* Skills and experience
* Location preferences
* Salary expectations
* Work style (remote, hybrid, onsite)

---
**Maintained by:** 7 Eagle Group
**Last Updated:** 2026-08-10
