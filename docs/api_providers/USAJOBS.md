# USAJobs API Integration

## Overview
Official federal government job board with exclusive access to federal positions.

## API Access
* **Endpoint:** `https://data.usajobs.gov/api/search`
* **Authentication:** Email-based (no API key)
* **Rate Limit:** 250 requests/hour
* **Registration:** https://developer.usajobs.gov/

## Required Headers
```python
headers = {
    'Host': 'data.usajobs.gov',
    'User-Agent': 'your_email@example.com',
    'Authorization-Key': 'your_authorization_key'
}
```

## Search Parameters
* `Keyword` - Job title or skills
* `LocationName` - City, state, or zip code
* `PostingChannel` - Filter by channel (e.g., "public")
* `SecurityClearanceRequired` - Filter by clearance level
* `TravelPercentage` - 0, 25, 50, 75, 100
* `RemoteIndicator` - True/False

## Veteran Preference
USAJobs supports veteran hiring preferences:
* `VeteranPreference` parameter
* Filter for veteran-only positions
* Preference-eligible indicators in results

## Response Structure
```json
{
  "SearchResult": {
    "SearchResultItems": [{
      "MatchedObjectId": "12345",
      "MatchedObjectDescriptor": {
        "PositionTitle": "IT Specialist",
        "OrganizationName": "Department of Defense",
        "PositionLocation": [{
          "LocationName": "Fort Bragg, NC"
        }],
        "QualificationSummary": "...",
        "SecurityClearanceRequired": "Secret"
      }
    }]
  }
}
```

## Federal Job Grades
* GS-5 to GS-7: Entry-level
* GS-9 to GS-11: Mid-level
* GS-12 to GS-13: Senior-level
* GS-14 to GS-15: Executive-level

## Security Clearance Mapping
* Public Trust
* Confidential
* Secret
* Top Secret
* Top Secret/SCI

---
**Maintained by:** 7 Eagle Group
**Last Updated:** 2026-08-10
