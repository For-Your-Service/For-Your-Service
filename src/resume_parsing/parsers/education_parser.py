"""Education parser."""
import re
def parse_education(text: str) -> list:
    degree_patterns = ['B.S.', 'B.A.', 'M.S.', 'M.A.', 'Ph.D.', 'Bachelor', 'Master']
    education = []
    
    for line in text.split('\n'):
        if any(degree in line for degree in degree_patterns):
            education.append(line.strip())
    
    return education
