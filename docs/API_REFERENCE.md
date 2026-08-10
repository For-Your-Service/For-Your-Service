# API Reference

## FastAPI Endpoints

### Base URL
```
https://huggingface.co/spaces/7eaglegroup/for-your-service
```

---

## Veteran Endpoints

### Register Veteran
```http
POST /veteran/register
Content-Type: application/json

{
  "personal_info": {
    "name": "string",
    "email": "string",
    "location": {"city": "string", "state": "string"}
  },
  "military_experience": {
    "branch": "string",
    "mos": "string",
    "years_of_service": int
  },
  "skills": ["string"],
  "preferences": {
    "target_roles": ["string"],
    "desired_salary": {"min": int, "max": int}
  }
}
```

**Response:** 201 Created
```json
{
  "veteran_id": "vet_xxxxx",
  "status": "registered",
  "created_at": "2026-08-10T14:30:00Z"
}
```

---

### Get Veteran Profile
```http
GET /veteran/{veteran_id}
```

**Response:** 200 OK
```json
{
  "veteran_id": "vet_xxxxx",
  "profile": { ... }
}
```

---

## Job Matching Endpoints

### Get Job Matches
```http
POST /match
Content-Type: application/json

{
  "veteran_id": "vet_xxxxx",
  "top_k": 10,
  "min_score": 0.7
}
```

**Response:** 200 OK
```json
{
  "veteran_id": "vet_xxxxx",
  "matches": [
    {
      "job_id": "job_xxxxx",
      "match_score": 0.92,
      "title": "DevOps Engineer",
      "company": "Acme Corp"
    }
  ]
}
```

---

### Search Jobs
```http
GET /jobs/search?keywords=devops&location=Greenville,SC&radius=50
```

**Query Parameters:**
- `keywords` (required): Search terms
- `location` (optional): City, State
- `radius` (optional): Miles from location
- `min_salary` (optional): Minimum salary
- `max_salary` (optional): Maximum salary

**Response:** 200 OK
```json
{
  "total": 150,
  "jobs": [ ... ]
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 429 | Rate Limit Exceeded |
| 500 | Server Error |

---

## Rate Limiting

- **Free tier:** 100 requests/hour
- **Pro tier:** 1000 requests/hour

---

## Authentication

Currently open API. Authentication coming in v1.1.

---

## SDKs

### Python
```python
from fys_client import ForYourServiceClient

client = ForYourServiceClient(api_key="your-key")
matches = client.get_matches("vet_12345")
```

### JavaScript
```javascript
import { FYSClient } from 'fys-sdk';

const client = new FYSClient({ apiKey: 'your-key' });
const matches = await client.getMatches('vet_12345');
```

Coming soon!
