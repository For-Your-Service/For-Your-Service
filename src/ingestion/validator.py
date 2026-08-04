def validate_intake_schema(payload):
    """Validates presence of required vector scoring metrics."""
    required_keys = ["scores"]
    for key in required_keys:
        if key not in payload:
            return False, f"Missing required payload key: '{key}'"
            
    scores = payload.get("scores", {})
    required_scores = ["temporal", "spatial", "clearance", "preference", "modifier"]
    for s_key in required_scores:
        if s_key not in scores:
            return False, f"Missing score metric: '{s_key}'"
            
    return True, "Valid"