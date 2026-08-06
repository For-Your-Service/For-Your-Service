# For Your Service - Job Market Data Pipeline

## Overview
AI-powered veteran job matching platform using neural networks to match military experience with civilian career opportunities.

## Architecture
* **Bronze Layer**: Raw job postings from multiple APIs
* **Silver Layer**: Feature engineering and MOS mapping
* **Gold Layer**: 384-dimensional tensor embeddings for neural matching

## Data Sources (All FREE Tier)
* **USAJobs API**: Federal government jobs with veteran preferences
* **O*NET API**: Occupational skills and MOS-to-civilian crosswalk
* **BLS API**: Official wage data and employment statistics
* **Adzuna API**: Real-time job postings (1K calls/month free)
* **CareerOneStop API**: DOL veteran employment services

## Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Build Docker image
docker build -t fys-job-pipeline .
```

## API Keys Required
See `src/api/config.py` for configuration.

## Repository
https://github.com/For-Your-Service/For-Your-Service
