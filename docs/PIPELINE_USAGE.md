# Job Data Ingestion Pipeline

**Organization:** 7 Eagle Group
**Author:** Free Hall <whall4.wh@gmail.com>

## Overview

End-to-end job data pipeline using **Unity Catalog Volumes** and **Delta Lake** with medallion architecture (Bronze → Silver → Gold).

## Architecture

```
Adzuna API → UC Volume (raw JSON) → Spark DataFrame → Bronze Table → Silver Table → Gold (Matched Jobs)
```

### Data Flow

1. **Fetch:** Pull jobs from Adzuna API (DevOps, Cloud, SRE roles)
2. **Stage:** Save raw JSON to `/Volumes/main/default/job_data/raw`
3. **Load:** Read JSON into Spark DataFrames
4. **Bronze:** Write raw data to `job_matching_bronze` Delta table
5. **Silver:** Transform and normalize to `job_matching_silver`
6. **Gold:** Match with veteran profiles (next phase)

## Quick Start

### 1. Setup UC Volume

```sql
-- Create UC Volume for job data staging
CREATE VOLUME IF NOT EXISTS main.default.job_data;
```

### 2. Run Pipeline in Databricks Notebook

```python
import sys
sys.path.insert(0, '/Workspace/Users/whall4.wh@gmail.com/For-Your-Service')

from src.pipelines.job_ingestion_pipeline import JobDataIngestionPipeline
from config.api_credentials import ADZUNA_APP_ID, ADZUNA_APP_KEY

# Initialize pipeline
pipeline = JobDataIngestionPipeline(
    volume_path="/Volumes/main/default/job_data",
    catalog="main",
    schema="default"
)

# Run full pipeline
summary = pipeline.run_full_pipeline(
    adzuna_app_id=ADZUNA_APP_ID,
    adzuna_app_key=ADZUNA_APP_KEY,
    keywords_list=["DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer"],
    locations=["Greenville, SC", "Remote"]
)

print(f"Jobs fetched: {summary['jobs_fetched']}")
print(f"Status: {summary['pipeline_status']}")
```

### 3. Query Results

```sql
-- Bronze table (raw API responses)
SELECT * FROM main.default.job_matching_bronze LIMIT 10;

-- Silver table (normalized jobs)
SELECT
    title,
    company,
    job_location,
    salary_min,
    salary_max,
    posted_date
FROM main.default.job_matching_silver
WHERE search_location = 'Greenville, SC'
ORDER BY posted_date DESC;
```

## Manual Job Upload (No API Required)

For immediate results, use the manual uploader:

```python
from scripts.manual_job_upload import ManualJobUploader

uploader = ManualJobUploader()

# Add job from Indeed/LinkedIn
job = uploader.add_job(
    title="Senior DevOps Engineer",
    company="TD Bank",
    location="Greenville, SC",
    description="...",
    salary_range="$130K-$160K",
    remote="Hybrid"
)

# Get all jobs for matching
jobs = uploader.get_all_jobs()
```

## Tables Schema

### Bronze Table: `job_matching_bronze`

Raw API responses with metadata:

- `fetched_at` (timestamp)
- `source` (string)
- `keywords` (string)
- `location` (string)
- `count` (int)
- `results` (array of structs)
- `ingested_at` (timestamp)

### Silver Table: `job_matching_silver`

Normalized job records:

- `job_id` (string)
- `title` (string)
- `company` (string)
- `job_location` (string)
- `description` (string)
- `salary_min` (int)
- `salary_max` (int)
- `url` (string)
- `posted_date` (timestamp)
- `processed_at` (timestamp)

## Veteran-Specific Features

- **Location Bonus:** Greenville, SC (10%), Remote (10%), Hybrid (5%)
- **Veteran-Friendly Detection:** Keywords: "veteran", "military", "vets"
- **Clearance Recognition:** TS/SCI, Secret, Public Trust
- **Skill Gap Analysis:** Identifies missing skills for upskilling

## Target Roles

- DevOps Engineer
- Cloud Solutions Architect
- Site Reliability Engineer (SRE)
- Platform Engineer
- Infrastructure Engineer

## Tech Stack Prioritization

**Cloud:** AWS, Azure, GCP
**Container Orchestration:** Kubernetes, Docker
**Infrastructure as Code:** Terraform, Ansible
**CI/CD:** Jenkins, GitHub Actions, GitLab CI
**Monitoring:** Grafana, Prometheus, Datadog
**Languages:** Python, Bash, Go

## API Credentials

Store credentials in `config/api_credentials.py`:

```python
# Adzuna API
ADZUNA_APP_ID = "your_app_id"
ADZUNA_APP_KEY = "your_app_key"

# BLS API
BLS_API_KEY = "your_bls_key"

# O*NET API
ONET_USERNAME = "your_username"
ONET_PASSWORD = "your_password"
```

**Important:** Add to `.gitignore`:
```
config/api_credentials.py
```

## Troubleshooting

### FileNotFoundError

```python
import os
os.makedirs("/Workspace/.../src/pipelines", exist_ok=True)
```

### Spark Session Issues

Pipeline gracefully handles missing Spark session - data still saved to UC Volume.

### API Rate Limits

- **Adzuna:** 50 results per page, rate limited
- **Solution:** Use manual upload or stagger requests

## Next Steps

1. ✅ Bronze/Silver ingestion complete
2. 🔄 Gold layer: Veteran matching with neural network
3. 🔄 Real-time scoring dashboard
4. 🔄 Email alerts for 80%+ matches

## Commit History

**Commits Today:** 40
**Total Project Commits:** 391

## Contact

**Free Hall**
Email: whall4.wh@gmail.com
Organization: 7 Eagle Group
