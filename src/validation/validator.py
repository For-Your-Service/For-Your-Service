"""
Veteran Profile Validation
"""

import re


class ValidationError(Exception):
    """Raised when profile validation fails"""
    pass


VALID_CLEARANCES = {
    "NONE",
    "CONFIDENTIAL",
    "SECRET",
    "TOP SECRET",
    "TS/SCI",
    "TS-SCI",
    "PUBLIC TRUST",
}

REQUIRED_FIELDS = [
    "name",
    "military_branch",
    "mos",
    "clearance_level",
    "years_service",
    "target_location",
]


def validate_veteran_profile(profile: dict) -> bool:
    """Validate veteran profile dictionary"""
    if not profile or not isinstance(profile, dict):
        raise ValidationError("Invalid profile format")

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in profile or profile[field] is None:
            raise ValidationError(f"Missing required field: {field}")

    # Validate clearance level
    clearance = str(profile.get("clearance_level", "")).strip().upper()
    if clearance not in VALID_CLEARANCES:
        raise ValidationError(f"Invalid clearance_level: {profile.get('clearance_level')}")

    # Validate years of service
    years = profile.get("years_service")
    if not isinstance(years, (int, float)) or years < 0:
        raise ValidationError("years_service must be positive")

    # Validate target location format: 'City, STATE'
    location = str(profile.get("target_location", "")).strip()
    if not re.match(r"^.+,\s*[A-Z]{2}$", location):
        raise ValidationError("location must be in format 'City, STATE'")

    return True
