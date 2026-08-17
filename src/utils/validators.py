"""
Input validation utilities
"""

import re


def validate_mos(mos_code: str) -> bool:
    """
    Validate military MOS code format

    Args:
        mos_code: MOS code string

    Returns:
        True if valid format
    """
    # Army: 2-3 characters + 1 letter (e.g., 25B, 35F)
    army_pattern = r"^\d{2}[A-Z]$|^\d{3}[A-Z]$"

    # Marine Corps: 4 digits (e.g., 0621)
    marine_pattern = r"^\d{4}$"

    return bool(re.match(army_pattern, mos_code) or re.match(marine_pattern, mos_code))


def validate_email(email: str) -> bool:
    """
    Validate email address format

    Args:
        email: Email address string

    Returns:
        True if valid format
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_onet_code(code: str) -> bool:
    """
    Validate O*NET occupation code format

    Args:
        code: O*NET code (e.g., "15-1212.00")

    Returns:
        True if valid format
    """
    pattern = r"^\d{2}-\d{4}\.\d{2}$"
    return bool(re.match(pattern, code))
