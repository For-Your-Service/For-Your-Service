"""Hugging Face Spaces deployment."""
import gradio as gr
from src.resume_parsing import ResumeParser
from src.matching.two_stage import TwoStageMatcher

parser = ResumeParser()
matcher = TwoStageMatcher()

def match_jobs(resume_file, location):
    """Match uploaded resume to jobs."""
    # Parse resume
    resume = parser.parse(resume_file.name)
    
    # TODO: Load job database
    job_descriptions = []  # Load from database
    
    # Match
    results = matcher.match(resume.raw_text, job_descriptions, top_k=10)
    
    return f"Found {len(results)} matching jobs"

demo = gr.Interface(
    fn=match_jobs,
    inputs=[
        gr.File(label="Upload Resume (PDF/DOCX)"),
        gr.Textbox(label="Preferred Location")
    ],
    outputs="text"
)

if __name__ == "__main__":
    demo.launch()
