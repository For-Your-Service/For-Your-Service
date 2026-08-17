# Skill Taxonomy

Normalizes and canonicalizes skills using O*NET taxonomy with military-to-civilian translation for the For Your Service platform.

## Features

- **O*NET Integration**: Free tier API client with rate limiting
- **Skill Normalization**: 40+ tech skill aliases (aws→Amazon Web Services)
- **Military Mapper**: MOS/AFSC/Rating to civilian skills translation
- **Taxonomy Cache**: File-based persistence to minimize API calls
- **Fuzzy Matching**: Handle skill variations and typos
- **Category Grouping**: Organize skills by Cloud, DevOps, Programming, etc.

## Installation

```bash
pip install requests  # For O*NET API client
```

## Usage

### Normalize Skills

```python
from src.skill_taxonomy import SkillNormalizer

normalizer = SkillNormalizer()

# Normalize single skill
skill = normalizer.normalize_skill("k8s")
print(skill)
# {'original': 'k8s', 'canonical_name': 'Kubernetes', 
#  'category': 'DevOps', 'confidence': 1.0}

# Normalize multiple skills
raw_skills = ["aws", "terraform", "python", "docker"]
normalized = normalizer.normalize_skills(raw_skills)

# Group by category
tech_stack = normalizer.extract_tech_stack(normalized)
print(tech_stack)
# {'Cloud': ['Amazon Web Services'], 
#  'DevOps': ['Terraform', 'Docker'],
#  'Programming': ['Python']}
```

### Military-to-Civilian Translation

```python
from src.skill_taxonomy import MilitarySkillMapper

mapper = MilitarySkillMapper()

# Get civilian skills for Army 18Z (Team Sergeant)
skills = mapper.extract_civilian_skills("18Z", "Army")
print(skills)
# ['Senior Leadership', 'Strategic Planning', ...]

# Get recommended certifications
certs = mapper.get_recommended_certifications("18E", "Army")
print(certs)
# ['Network+', 'CCNA', 'Security+', 'CEH']

# Get civilian job equivalent
title = mapper.get_civilian_equivalent("18D", "Army")
print(title)
# 'Paramedic / Emergency Medical Technician'

# Enrich resume with military-derived skills
resume_data = {
    "full_name": "John Doe",
    "military_branch": "Army",
    "military_mos": "18E",
    "skills": ["Leadership"]
}

enriched = mapper.enrich_resume_with_military_skills(resume_data)
# Adds: Network Administration, Telecommunications, Cybersecurity, etc.
```

### O*NET API Client

```python
from src.skill_taxonomy import ONetClient

client = ONetClient()  # Free tier, no auth required

# Search occupations
results = client.search_occupations("software engineer", limit=5)

# Get occupation skills
skills = client.get_skills("15-1252.00")  # Software Developer code

# Get complete profile
profile = client.get_occupation_profile("15-1252.00")
```

### Taxonomy Cache

```python
from src.skill_taxonomy import TaxonomyCache

cache = TaxonomyCache(ttl_days=30)

# Cache O*NET data
cache.set_onet_occupation("15-1252.00", occupation_data)

# Retrieve cached data
data = cache.get_onet_occupation("15-1252.00")

# Cache stats
stats = cache.get_cache_stats()

# Clean expired entries
removed_count = cache.clear_expired()
```

## Supported Military Codes

### Army MOS
- **18 Series (Special Forces)**: 18A, 18B, 18C, 18D, 18E, 18F, 18Z
- **11 Series (Infantry)**: 11B
- **35 Series (Intelligence)**: 35F
- **25 Series (Signal)**: 25B, 25D

### Air Force AFSC
- 1N0X1: All-Source Intelligence Analyst
- 3D0X2: Cyber Systems Operations

### Navy Ratings
- IT: Information Systems Technician
- CTN: Cryptologic Technician Networks

## Skill Aliases

Common variations automatically mapped to canonical forms:

- aws, amazon web services → Amazon Web Services
- k8s, kube → Kubernetes
- tf, terraform → Terraform
- py, python3 → Python
- postgres → PostgreSQL
- cicd, ci/cd → CI/CD

## Author

**Free Hall** <whall4.wh@gmail.com>  
7 Eagle Group  
Army Special Forces (18Z), 1999-2017
