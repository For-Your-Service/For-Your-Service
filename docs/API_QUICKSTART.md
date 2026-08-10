# 🚀 API Setup Quickstart

Get your For Your Service API credentials configured in under 15 minutes.

## Prerequisites
- Databricks account with Unity Catalog access
- GitHub account
- Email address for API registrations

## Step 1: Register for API Keys (10 minutes)

### USAJOBS (2 min)
1. Visit https://developer.usajobs.gov/
2. Request API Key
3. Save key securely

### JSearch via RapidAPI (3 min)
1. Sign up at https://rapidapi.com/
2. Subscribe to JSearch API (FREE tier)
3. Copy X-RapidAPI-Key

### Adzuna (5 min)
1. Register at https://developer.adzuna.com/
2. Create app: "For Your Service"
3. Copy App ID and App Key

## Step 2: Configure Databricks Secrets
```bash
./scripts/setup_databricks_secrets.sh
```

## Step 3: Test Pipeline
Run `notebooks/03b_Multi_Source_Job_Ingestion`
