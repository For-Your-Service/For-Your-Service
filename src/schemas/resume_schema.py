"""Resume JSON schema."""
RESUME_SCHEMA = {
    "type": "object",
    "properties": {
        "candidate_id": {"type": "string"},
        "skills": {"type": "array"},
        "experience_years": {"type": "integer"},
        "clearance": {"type": "string"}
    },
    "required": ["candidate_id"]
}
