# Pipeline Orchestration

End-to-end veteran job matching pipeline coordinating resume parsing, skill normalization, gap analysis, job matching, and personalized recommendations.

## Architecture

```
Resume Upload
    ↓
Resume Parser (PDF/DOCX)
    ↓
Skill Normalization + Military Enrichment
    ↓
Gap Analyzer (Skills Comparison)
    ↓
Job Matcher (Vector Similarity)
    ↓
Recommendation Engine (Tailored Advice)
    ↓
Match Results + Action Plan
```

## Components

### Gap Analyzer
Compares candidate skills against job requirements and identifies:
- Matching skills (strengths)
- Missing skills (gaps)
- Weak skills (needs improvement)
- Match score (0-1)
- Learning resources and timelines

### Job Matcher
Vector-based similarity matching:
- Cosine similarity between skill embeddings
- Location and salary filtering
- Veteran-friendly employer boosting
- Security clearance handling
- Batch processing support

### Recommendation Engine
Generates personalized advice:
- Resume improvement suggestions
- Job search strategy tips
- Networking recommendations
- Skill development plans
- Timeline to readiness

### Orchestrator
Coordinates full pipeline:
- Resume parsing (PDF/DOCX)
- Skill normalization
- Military skill enrichment
- Gap analysis per job
- Match scoring
- Recommendation generation

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:
- numpy (vector operations)
- PyPDF2, python-docx (resume parsing)
- requests (O*NET API)

## Usage

### End-to-End Matching

```python
from src.pipeline import MatchingOrchestrator

# Initialize orchestrator
orchestrator = MatchingOrchestrator(
    similarity_threshold=0.6,
    enable_military_mapping=True
)

# Define job requirements
jobs = [
    {
        "id": "job1",
        "title": "DevOps Engineer",
        "company": "Tech Corp",
        "location": "Greenville, SC",
        "salary_range": "$120K-$180K",
        "required_skills": [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Kubernetes", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Terraform", "importance": "Important", "required_level": "Proficient"},
            {"skill": "Python", "importance": "Important", "required_level": "Proficient"}
        ]
    }
]

# Process resume and match
results = orchestrator.end_to_end_match(
    resume_path="path/to/resume.pdf",
    job_requirements=jobs,
    location_filter="Greenville, SC",
    salary_min=120000
)

# Access results
print(f"Best match score: {results['summary']['best_match_score']:.2f}")
print(f"Candidate: {results['candidate']['name']}")
print(f"Matching skills: {results['candidate']['skills']}")
```

### Gap Analysis Only

```python
from src.pipeline import GapAnalyzer

analyzer = GapAnalyzer()

# Candidate skills
skills = ["AWS", "Python", "Docker"]

# Job requirements
requirements = [
    {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
    {"skill": "Kubernetes", "importance": "Critical", "required_level": "Proficient"},
    {"skill": "Python", "importance": "Important", "required_level": "Proficient"}
]

# Analyze gap
gap = analyzer.analyze(
    candidate_skills=skills,
    job_requirements=requirements,
    candidate_experience_years=10
)

print(f"Match score: {gap.match_score:.2f}")
print(f"Missing skills: {[g.skill_name for g in gap.missing_skills]}")
print(f"Recommendations: {gap.recommendations}")
print(f"Readiness: {gap.estimated_readiness}")
```

### Job Matching Only

```python
import numpy as np
from src.pipeline import JobMatcher

matcher = JobMatcher(similarity_threshold=0.6)

# Candidate embedding (from neural network)
candidate_emb = np.array([0.8, 0.5, 0.9, 0.3])

# Job embeddings with metadata
jobs = [
    (
        "job1",
        np.array([0.9, 0.6, 0.8, 0.4]),
        {
            "title": "DevOps Engineer",
            "company": "Tech Corp",
            "location": "Remote",
            "salary_range": "$150K-$180K",
            "skills": ["AWS", "Kubernetes"],
            "veteran_friendly": True
        }
    )
]

# Find matches
results = matcher.find_matches(
    candidate_embedding=candidate_emb,
    job_embeddings=jobs,
    top_k=10,
    location_filter="Greenville, SC",
    salary_min=120000
)

for match in results.matches:
    print(f"{match.job_title} at {match.company}")
    print(f"  Similarity: {match.similarity_score:.2f}")
    print(f"  Location: {match.location}")
    print(f"  Veteran-friendly: {match.veteran_friendly}")
```

### Personalized Recommendations

```python
from src.pipeline import RecommendationEngine

engine = RecommendationEngine()

# Resume data
resume = {
    "full_name": "John Doe",
    "military_branch": "Army",
    "military_mos": "18Z",
    "skills": ["Leadership", "AWS", "Python"],
    "total_years_experience": 15,
    "location": "Greenville, SC"
}

# Gap analysis results
gap_data = {
    "match_score": 0.7,
    "missing_skills": [
        {
            "skill_name": "Kubernetes",
            "importance": "Critical",
            "estimated_time": "6-10 weeks",
            "learning_resources": ["CKA Certification", "KodeKloud"]
        }
    ]
}

# Generate recommendations
recommendations = engine.generate_recommendations(
    resume_data=resume,
    gap_analysis=gap_data,
    target_jobs=[]
)

# Access advice
for improvement in recommendations.resume_improvements:
    print(f"{improvement.section}: {improvement.suggestion}")

for tip in recommendations.job_search_tips:
    print(f"  • {tip}")
```

### Batch Processing

```python
orchestrator = MatchingOrchestrator()

# Multiple resumes
resumes = [
    "path/to/resume1.pdf",
    "path/to/resume2.docx",
    "path/to/resume3.pdf"
]

# Process all
results = orchestrator.batch_process(resumes, jobs)

for path, result in results.items():
    print(f"{path}: Best match {result['summary']['best_match_score']:.2f}")
```

## Veteran-Specific Features

### Military Skill Enrichment
Automatically enriches resumes with civilian-equivalent skills:
- Army 18 Series → Leadership, Strategic Planning, Foreign Languages
- 18E → Network Administration, Telecommunications, Cybersecurity
- 35F → Intelligence Analysis, Report Writing, Critical Thinking

### Veteran-Friendly Employer Boosting
Prioritizes employers participating in veteran hiring programs:
- 10% similarity score boost
- Filtering by veteran preference

### Security Clearance Handling
- Highlights active clearances
- Filters clearance-required roles for non-cleared candidates
- Recommends defense contractor opportunities

### Military-to-Civilian Resume Tips
- Translate MOS codes to job titles
- Remove military acronyms
- Quantify achievements with metrics
- Emphasize leadership and team management

## Match Scoring

Weighted by importance:
- Critical skills: 3x weight
- Important skills: 2x weight
- Nice-to-have: 1x weight

```
match_score = earned_score / max_possible_score
```

Readiness estimates:
- ≥ 0.8: "Ready Now - Apply immediately"
- ≥ 0.6: "1-2 months - Upskill on nice-to-haves"
- < 0.6: "3-6 months - Comprehensive development needed"

## Testing

Run full test suite:

```bash
python -m pytest tests/pipeline/
```

Individual component tests:

```bash
python -m pytest tests/pipeline/test_gap_analyzer.py
python -m pytest tests/pipeline/test_job_matcher.py
```

## Author

**Free Hall** <whall4.wh@gmail.com>  
7 Eagle Group  
Army Green Beret (18Z), 1999-2017
