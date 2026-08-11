"""Date validation."""
from datetime import datetime
def validate_date(date_str: str) -> bool:
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%Y']
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    return False
