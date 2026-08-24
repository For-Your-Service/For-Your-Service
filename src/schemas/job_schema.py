"""Job JSON schema."""
JOB_SCHEMA = {
    "type": "object",
    "properties": {
        "job_id": {"type": "string"},
        "title": {"type": "string"},
        "required_skills": {"type": "array"},
        "years_required": {"type": "integer"}
    },
    "required": ["job_id", "title"]
}
