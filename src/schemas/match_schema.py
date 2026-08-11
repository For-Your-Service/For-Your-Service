"""Match JSON schema."""
MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "candidate_id": {"type": "string"},
        "job_id": {"type": "string"},
        "score": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["candidate_id", "job_id", "score"]
}
