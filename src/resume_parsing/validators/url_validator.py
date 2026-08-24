"""URL validation."""
import re
def validate_url(url: str) -> bool:
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))
