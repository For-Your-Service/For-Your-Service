# Dice API Integration

## Overview
Tech-focused job board specializing in IT and engineering roles.

## API Access
* **Endpoint:** `https://api.dice.com/v1/`
* **Authentication:** OAuth 2.0
* **Rate Limit:** 30 requests/minute
* **Focus:** Technology jobs only

## Job Search
`GET /jobs`

### Parameters
* `q` - Search query (job title, skills)
* `location` - City, state, or zip
* `radius` - Search radius (miles)
* `postedDate` - Posting date filter
* `employmentType` - Full-time, contract, etc.

## Response
```json
{
  "data": [{
    "id": "DICE123",
    "title": "Senior SRE",
    "employer": "TechGiant",
    "jobLocation": {
      "displayName": "Greenville, SC"
    },
    "employment": "FULL_TIME",
    "salary": "$130K - $170K",
    "postedDate": "2026-08-05"
  }]
}
```

## Tech Skills Focus
Perfect for veterans with technical MOS:
* 25B (IT Specialist)
* 17C (Cyber Operations)
* 35T (Military Intelligence)
* 25N (Network Engineer)

---
**Maintained by:** 7 Eagle Group
**Last Updated:** 2026-08-10
