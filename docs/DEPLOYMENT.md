# Deployment Guide

## Local Development

### Prerequisites
* Python 3.11+
* Docker (optional)
* Databricks workspace access

### Setup
```bash
# Clone repository
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run tests
pytest tests/ -v
```

## Docker Deployment

```bash
# Build image
docker build -t fys-job-pipeline .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## Databricks Deployment

### Unity Catalog Tables
```bash
# Initialize tables
python scripts/init_db.py
```

### Databricks Jobs
1. Navigate to Workflows → Jobs
2. Create new job
3. Add Python wheel task
4. Configure schedule (daily 6 AM UTC)
5. Add compute cluster

## Cloud Function (GCP)

```bash
# Deploy to Cloud Functions
gcloud functions deploy fys-job-collector \
  --runtime python311 \
  --trigger-topic daily-collection \
  --entry-point main \
  --memory 512MB
```

## Monitoring

* **Logs**: CloudWatch / Stackdriver
* **Metrics**: Track API calls, match quality
* **Alerts**: Rate limit warnings, errors
