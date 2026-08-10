# Glassdoor API Integration

## Overview
Job board with company reviews and salary transparency.

## API Access
* **Endpoint:** `https://api.glassdoor.com/api/`
* **Authentication:** Partner ID + Key
* **Rate Limit:** 20 requests/minute (very restrictive)
* **Approval Required:** Must apply for partner access

## Job Search
`GET /jobsearch`

### Parameters
* `t.p` - Partner ID
* `t.k` - Partner key
* `q` - Job title
* `l` - Location
* `radius` - Search radius

## Unique Features
* **Company Reviews:** Employee ratings and reviews
* **Salary Data:** Crowdsourced salary ranges
* **Interview Insights:** Interview question previews
* **CEO Approval:** CEO approval ratings

## Response
```json
{
  "response": {
    "jobListings": [{
      "jobTitle": "DevOps Lead",
      "employer": {
        "name": "TechCorp",
        "overallRating": 4.2
      },
      "location": "Greenville, SC",
      "salaryEstimate": "$125K-$165K"
    }]
  }
}
```

## Value for Veterans
* Research company culture before applying
* Verify salary expectations
* Read veteran employee reviews
* Assess work-life balance

---
**Maintained by:** 7 Eagle Group
**Last Updated:** 2026-08-10
