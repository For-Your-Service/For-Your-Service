"""Normalize whitespace."""
import re
def normalize_whitespace(text: str) -> str:
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
