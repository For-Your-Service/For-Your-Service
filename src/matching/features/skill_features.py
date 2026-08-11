"""Extract skill features."""
def extract_skill_count(resume: dict) -> int:
    return len(resume.get('skills', []))

def extract_skill_diversity(resume: dict) -> int:
    skills = resume.get('skills', [])
    categories = set(s.get('category') for s in skills)
    return len(categories)
