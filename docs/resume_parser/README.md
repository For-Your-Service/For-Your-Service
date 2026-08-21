# Resume Parser

Extracts structured data from unstructured resume formats (PDF, DOCX) for the For Your Service veteran job matching platform.

## Features

- **PDF Parsing**: PyPDF2-based extraction (free tier)
- **DOCX Parsing**: python-docx support for Microsoft Word
- **Structured Schema**: Dataclass-based models with JSON serialization
- **Veteran Fields**: Military branch, MOS, security clearance, service years
- **Contact Extraction**: Email, phone, LinkedIn, GitHub via regex
- **Skills Detection**: Tech stack keyword identification

## Installation

```bash
pip install -r src/resume_parser/requirements.txt
```

## Usage

### Parse PDF Resume

```python
from src.resume_parser import PDFResumeParser

parser = PDFResumeParser()
resume = parser.parse("path/to/resume.pdf")

print(f"Name: {resume.full_name}")
print(f"Email: {resume.email}")
print(f"Skills: {[s.name for s in resume.skills]}")
print(f"Military: {resume.military_branch} {resume.military_mos}")
```

### Parse DOCX Resume

```python
from src.resume_parser import DOCXResumeParser

parser = DOCXResumeParser()
resume = parser.parse("path/to/resume.docx")

# Serialize to JSON
resume_dict = resume.to_dict()
```

## Schema

### ResumeSchema

Main structured resume data:

- **Contact**: full_name, email, phone, location, linkedin_url, github_url
- **Skills**: List[SkillEntry] with categories and proficiency
- **Experience**: List[ExperienceEntry] with duration calculation
- **Education**: List[EducationEntry] with GPA and honors
- **Military**: branch, mos, clearance, years_of_service
- **Certifications**: List[str] of professional certifications

### SkillEntry

- name: Skill name
- category: "Technical", "Leadership", etc.
- proficiency: "Expert", "Intermediate", "Beginner"
- years_experience: Float duration

### ExperienceEntry

- title: Job title
- company: Organization name
- start_date / end_date: Date range (None = current)
- duration_years: Auto-calculated from dates
- achievements: List[str] of bullet points

## Author

**Free Hall** <whall4.wh@gmail.com>
7 Eagle Group
