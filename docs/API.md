# API Documentation

## Overview
For Your Service API for veteran job matching.

## Endpoints

### POST /match
Match a veteran profile to jobs.

**Request:**
```json
{
  "veteran_id": "v12345",
  "mos": "25B",
  "skills": ["python", "aws", "docker"],
  "location": "San Diego, CA",
  "clearance": "Secret",
  "top_k": 10
}
```

**Response:**
```json
{
  "matches": [
    {
      "job_id": "j67890",
      "title": "DevOps Engineer",
      "company": "Tech Corp",
      "similarity_score": 0.89,
      "explanation": {
        "mos_match": true,
        "skill_overlap": 7,
        "location_match": true
      }
    }
  ]
}
```

### GET /jobs/{job_id}
Get job details.

### GET /veteran/{veteran_id}/profile
Get veteran profile.

## Authentication
API key required in header:
```
Authorization: Bearer YOUR_API_KEY
```
