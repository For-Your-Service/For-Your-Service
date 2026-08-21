# Import the built-in uuid module to generate random universally unique identifiers for sanitized payloads.
import uuid


def sanitize_payload(raw_payload):
    """Strips personal identifiers (PII) and assigns a unique candidate UUID."""

    # Generate a random version-4 UUID string to uniquely track the anonymized entity without exposing raw PII.
    candidate_uuid = str(uuid.uuid4())

    # Extract the nested 'scores' dictionary from the raw payload, defaulting to an empty dictionary if missing.
    scores = raw_payload.get("scores", {})

    # Construct and return a sanitized dictionary containing only non-sensitive metrics and the generated UUID.
    sanitized = {
        # Assign the generated unique identifier string to the candidate_uuid key.
        "candidate_uuid": candidate_uuid,
        # Extract the temporal score value, defaulting to 0.0 if not present.
        "temporal_score": scores.get("temporal", 0.0),
        # Extract the spatial score value, defaulting to 0.0 if not present.
        "spatial_score": scores.get("spatial", 0.0),
        # Extract the clearance score value, defaulting to 0.0 if not present.
        "clearance_score": scores.get("clearance", 0.0),
        # Extract the preference score value, defaulting to 0.0 if not present.
        "preference_score": scores.get("preference", 0.0),
        # Extract the modifier score value, defaulting to 0.0 if not present.
        "modifier_score": scores.get("modifier", 0.0),
    }

    # Return both the fully sanitized metrics dictionary and the raw candidate UUID string.
    return sanitized, candidate_uuid
