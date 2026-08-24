"""Example: Analyze skill gaps."""
from src.advice import GapAnalyzer
from src.resume_parsing import ResumeParser

# Parse resume
parser = ResumeParser()
candidate = parser.parse('resume.pdf')

# Analyze gaps
analyzer = GapAnalyzer()
job_skills = ['kubernetes', 'terraform', 'python', 'prometheus']

analysis = analyzer.analyze(
    candidate,
    job_skills,
    job_required_years=5
)

# Print gaps
print("Missing Skills:")
for gap in analysis.missing_skills:
    print(f"  - {gap.skill_name} (importance: {gap.importance})")
