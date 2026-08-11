"""Extract experience features."""
def extract_total_experience(resume: dict) -> int:
    return resume.get('total_years_experience', 0)

def extract_role_count(resume: dict) -> int:
    return len(resume.get('work_history', []))
