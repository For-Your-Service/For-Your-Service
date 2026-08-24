"""Expand acronyms."""
ACRONYMS = {
    'AI': 'artificial intelligence',
    'ML': 'machine learning',
    'CI/CD': 'continuous integration continuous deployment',
    'IaC': 'infrastructure as code',
}

def expand_acronym(text: str) -> str:
    for acronym, expansion in ACRONYMS.items():
        text = text.replace(acronym, expansion)
    return text
