# Data Dictionary

## Bronze Layer: job_postings

Raw job data from API sources.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| job_id | STRING | Unique job identifier | "usa-123456" |
| source | STRING | API source | "usajobs", "adzuna" |
| raw_json | STRING | Full API response | {...} |
| title | STRING | Job title | "Cybersecurity Specialist" |
| company | STRING | Company name | "Department of Defense" |
| description | STRING | Full job description | "Looking for..." |
| location | STRING | Job location | "San Diego, CA" |
| salary_min | DOUBLE | Minimum salary | 75000 |
| salary_max | DOUBLE | Maximum salary | 125000 |
| posted_date | TIMESTAMP | When job was posted | 2026-08-01 |
| fetched_at | TIMESTAMP | When we fetched it | 2026-08-06 |
| ingestion_date | DATE | Partition date | 2026-08-06 |

## Silver Layer: job_features

Normalized and enriched job data.

| Column | Type | Description |
|--------|------|-------------|
| job_id | STRING | Primary key |
| technical_skills | ARRAY<STRING> | ["python", "aws", "docker"] |
| soft_skills | ARRAY<STRING> | ["leadership", "communication"] |
| relevant_mos_codes | ARRAY<STRING> | ["25B", "17C"] |
| onet_codes | ARRAY<STRING> | ["15-1212.00"] |
| is_remote | BOOLEAN | Remote work available |
| veteran_preference | BOOLEAN | Veteran hiring preference |
| clearance_required | STRING | "Secret", "Top Secret" |

## Gold Layer: job_embeddings

384-dimensional embeddings for neural matching.

| Column | Type | Description |
|--------|------|-------------|
| job_id | STRING | Primary key |
| embedding | ARRAY<DOUBLE> | 384-dim vector |
| embedding_version | STRING | Model version "v1.0" |
