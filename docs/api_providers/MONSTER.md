# Monster API Integration

## Overview
One of the oldest job boards with 50+ years of recruitment experience.

## API Access
* **Endpoint:** `https://api.monster.com/v2/`
* **Authentication:** API Key
* **Rate Limit:** 120 requests/minute
* **Documentation:** https://partner.monster.com/

## Job Search
`GET /jobs/search`

### Parameters
* `q` - Search query
* `location` - City, state, or zip
* `country` - Country code (US, CA, UK)
* `radius` - Search radius in miles
* `page` - Pagination

## Response Format
```json
{
  "jobs": [{
    "id": "ABC123",
    "title": "Platform Engineer",
    "company": {
      "name": "TechCorp"
    },
    "location": {
      "city": "Greenville",
      "state": "SC"
    },
    "salary": {
      "min": 120000,
      "max": 160000
    },
    "datePosted": "2026-08-05"
  }]
}
```

## Best Practices
* Use specific job titles over broad keywords
* Set radius to 50+ miles for rural areas
* Filter by `datePosted` for fresh listings
* Parse salary ranges for accurate matching

---
**Maintained by:** 7 Eagle Group  
**Last Updated:** 2026-08-10
