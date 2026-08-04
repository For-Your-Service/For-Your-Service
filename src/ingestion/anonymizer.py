import uuid

def sanitize_payload(raw_payload):
    """Strips personal identifiers (PII) and assigns a unique candidate UUID."""
    candidate_uuid = str(uuid.uuid4())
    
    # Extract numerical scoring attributes for vector conversion
    scores = raw_payload.get("scores", {})
    
    sanitized = {
        "candidate_uuid": candidate_uuid,
        "temporal_score": scores.get("temporal", 0.0),
        "spatial_score": scores.get("spatial", 0.0),
        "clearance_score": scores.get("clearance", 0.0),
        "preference_score": scores.get("preference", 0.0),
        "modifier_score": scores.get("modifier", 0.0)
    }
    
    return sanitized, candidate_uuid