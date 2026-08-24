"""Experience parser."""
import re
def parse_experience(text: str) -> list:
    # Detect job titles (capitalized phrases before dates)
    title_pattern = r'([A-Z][a-zA-Z ]+)\s+[|\-]\s+([A-Z][a-zA-Z ]+)\s+[|\-]\s+(\d{4})'
    
    experiences = []
    for match in re.finditer(title_pattern, text):
        experiences.append({
            'title': match.group(1).strip(),
            'company': match.group(2).strip(),
            'year': match.group(3)
        })
    
    return experiences
