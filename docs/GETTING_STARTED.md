# Getting Started with For Your Service

Complete setup guide from zero to running system in 1 hour.

## Prerequisites

- Databricks account (Community or trial)
- GitHub account
- Email address (for API registrations)
- Basic SQL/Python knowledge

---

## Step 1: Set Up Databricks (15 min)

### Create Workspace
1. Go to https://databricks.com/
2. Sign up for Community Edition (FREE)
3. Create workspace

### Enable Unity Catalog
1. Navigate to Data Engineering
2. Enable Unity Catalog
3. Create catalog: `workspace`

---

## Step 2: Clone Repository (5 min)

### Via Databricks Repos
1. Open Databricks workspace
2. Click "Repos" in sidebar
3. "Add Repo"
4. URL: `https://github.com/For-Your-Service/For-Your-Service`

### Via Git CLI
```bash
git clone https://github.com/For-Your-Service/For-Your-Service.git
```

---

## Step 3: Register for APIs (20 min)

### USAJOBS (5 min)
1. Visit https://developer.usajobs.gov/
2. Click "Request API Key"
3. Fill form with email
4. Save key securely

### JSearch via RapidAPI (8 min)
1. Sign up at https://rapidapi.com/
2. Navigate to JSearch API
3. Subscribe to FREE plan (1000 req/month)
4. Copy X-RapidAPI-Key

### Adzuna (7 min)
1. Register at https://developer.adzuna.com/
2. Create app: "For Your Service"
3. Copy App ID and App Key

---

## Step 4: Configure Secrets (10 min)

### Install Databricks CLI
```bash
pip install databricks-cli
databricks configure --token
```

### Create Secrets Scope
```bash
databricks secrets create-scope --scope fys-apis
```

### Add Keys
```bash
databricks secrets put --scope fys-apis --key usajobs-api-key
databricks secrets put --scope fys-apis --key usajobs-user-agent
databricks secrets put --scope fys-apis --key jsearch-rapidapi-key
databricks secrets put --scope fys-apis --key adzuna-app-id
databricks secrets put --scope fys-apis --key adzuna-app-key
```

---

## Step 5: Create Bronze Table (5 min)

Run notebook: `setup/01_Unity_Catalog_Setup.py`

This creates:
- `workspace.fys_bronze.job_postings`

---

## Step 6: Run Test Ingestion (5 min)

Run notebook: `notebooks/03b_Multi_Source_Job_Ingestion`

Should see:
```
✅ USAJOBS: Retrieved 50 jobs
✅ JSearch: Retrieved 120 jobs
✅ Adzuna: Retrieved 80 jobs
📊 Total: 250 jobs
```

---

## Step 7: Verify Data (5 min)

### Check Bronze Table
```sql
SELECT COUNT(*) FROM workspace.fys_bronze.job_postings;
```

Should return: 200-500 jobs (after deduplication)

### Top Companies
```sql
SELECT company, COUNT(*) as job_count
FROM workspace.fys_bronze.job_postings
GROUP BY company
ORDER BY job_count DESC
LIMIT 10;
```

---

## Next Steps

1. **Schedule Daily Job:** See [docs/DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
2. **Build Silver Layer:** See [docs/SILVER_LAYER_SPEC.md](SILVER_LAYER_SPEC.md)
3. **Deploy API:** See [docs/HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md)
4. **Add Monitoring:** See [docs/MONITORING.md](MONITORING.md)

---

## Troubleshooting

See [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

---

## Questions?

- GitHub Issues: https://github.com/For-Your-Service/For-Your-Service/issues
- Email: whall4.wh@gmail.com

---

Welcome to For Your Service! 🇺🇸
