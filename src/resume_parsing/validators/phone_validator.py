"""Phone validation."""
import re
def validate_phone(phone: str) -> bool:
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))
