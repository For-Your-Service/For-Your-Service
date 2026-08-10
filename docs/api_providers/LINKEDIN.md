# LinkedIn API Integration

## Overview
LinkedIn has 900+ million professionals and extensive job posting data.

## API Access
* **Endpoint:** `https://api.linkedin.com/v2/`
* **Authentication:** OAuth 2.0
* **Rate Limit:** 60 requests/minute
* **Token Lifespan:** 60 days

## OAuth Setup
1. Create LinkedIn App at https://www.linkedin.com/developers/
2. Request scopes: `r_liteprofile`, `r_basicprofile`, `w_member_social`
3. Implement OAuth flow to get access token

## Job Search Endpoint
`GET /jobs/search`

### Parameters
* `keywords` - Job title or keywords
* `location` - Location name or ID
* `listedAt` - Unix timestamp for recent jobs
* `sortBy` - Relevance or date

## Response Example
```json
{
  "elements": [{
    "id": "123456789",
    "title": "Senior Cloud Engineer",
    "company": {
      "name": "CloudTech Inc"
    },
    "location": "Greenville, SC",
    "description": "...",
    "applyUrl": "https://..."
  }]
}
```

## Rate Limiting
```python
from requests_oauthlib import OAuth2Session

oauth = OAuth2Session(client_id, token=access_token)
response = oauth.get('https://api.linkedin.com/v2/jobs/search', params=params)

if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    time.sleep(retry_after)
```

## Veteran Features
* Target military skills: "cleared", "security clearance", "DoD"
* Company filters for defense contractors
* Alumni filters for service academies

---
**Maintained by:** 7 Eagle Group  
**Last Updated:** 2026-08-10
