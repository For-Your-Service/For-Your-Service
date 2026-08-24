# Matching API

## Endpoints

### POST /match/jobs
Match candidate against job database.

**Request:**
```json
{
  "candidate_id": "uuid",
  "location": "Greenville, SC",
  "top_k": 10
}
```

**Response:**
```json
{
  "matches": [
    {
      "job_id": "123",
      "score": 0.92,
      "title": "DevOps Engineer",
      "company": "Tech Corp"
    }
  ]
}
```
