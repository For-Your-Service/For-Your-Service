"""Example: Match candidate to jobs."""
from src.matching.two_stage import TwoStageMatcher

# Initialize matcher
matcher = TwoStageMatcher()

# Load resume and jobs
resume_text = open('resume.txt').read()
job_descriptions = [open(f'job_{i}.txt').read() for i in range(100)]

# Match
results = matcher.match(resume_text, job_descriptions, top_k=10)

# Print top matches
for job_idx, score in results[:5]:
    print(f"Job {job_idx}: {score:.2f}")
