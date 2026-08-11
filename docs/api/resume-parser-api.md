# Resume Parser API

## Endpoints

### POST /parse/resume
Upload and parse a resume file.

**Request:**
```json
{
  "file": "<PDF or DOCX file>",
  "options": {
    "extract_skills": true,
    "normalize": true
  }
}
```

**Response:**
```json
{
  "candidate_id": "uuid",
  "skills": ["python", "kubernetes", "aws"],
  "experience_years": 8,
  "clearance": "ts/sci"
}
```
