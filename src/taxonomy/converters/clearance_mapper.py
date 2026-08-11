"""Map clearance levels."""
CLEARANCE_HIERARCHY = {
    'top secret/sci': 5,
    'top secret': 4,
    'secret': 3,
    'confidential': 2,
    'public trust': 1,
}

def clearance_level(clearance: str) -> int:
    return CLEARANCE_HIERARCHY.get(clearance.lower(), 0)
