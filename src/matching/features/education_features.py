"""Extract education features."""
def extract_degree_level(resume: dict) -> int:
    education = resume.get('education', [])
    if not education:
        return 0
    
    levels = {'phd': 3, 'master': 2, 'bachelor': 1}
    for edu in education:
        degree = edu.get('degree', '').lower()
        for key, level in levels.items():
            if key in degree:
                return level
    return 0
