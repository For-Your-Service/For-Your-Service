"""FastAPI application."""
from fastapi import FastAPI, File, UploadFile
from src.resume_parsing import ResumeParser
from src.matching.two_stage import TwoStageMatcher

app = FastAPI(title="For Your Service API")

parser = ResumeParser()
matcher = TwoStageMatcher()

@app.post("/parse/resume")
async def parse_resume(file: UploadFile = File(...)):
    """Parse uploaded resume."""
    content = await file.read()
    resume = parser.parse_bytes(content)
    
    return {
        "candidate_id": resume.candidate_id,
        "skills": resume.get_skill_names(),
        "experience_years": resume.total_years_experience,
        "clearance": resume.clearance_level
    }

@app.post("/match/jobs")
async def match_jobs(resume_text: str, top_k: int = 10):
    """Match resume to jobs."""
    # TODO: Load job database
    job_descriptions = []
    
    results = matcher.match(resume_text, job_descriptions, top_k=top_k)
    
    return {"matches": results}
