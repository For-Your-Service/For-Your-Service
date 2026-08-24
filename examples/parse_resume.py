"""Example: Parse a resume file."""
from src.resume_parsing import ResumeParser

# Initialize parser
parser = ResumeParser()

# Parse resume
resume = parser.parse('path/to/resume.pdf')

# Access structured data
print(f"Skills: {resume.get_skill_names()}")
print(f"Experience: {resume.total_years_experience} years")
print(f"Clearance: {resume.clearance_level}")
