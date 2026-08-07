# 🔒 API Secrets Setup Guide

## Security Best Practice

**NEVER commit API keys to git!** Use Databricks Secrets instead.

---

## Quick Setup (5 minutes)

### Step 1: Create Secret Scope

```bash
# Via Databricks CLI
databricks secrets create-scope --scope fys-api-keys
```

OR use Databricks UI:
1. Settings → Workspace Admin → Secrets
2. Click "Create Scope"
3. Name: `fys-api-keys`
4. Click "Create"

---

### Step 2: Add Your API Keys

```bash
# Adzuna
databricks secrets put --scope fys-api-keys --key adzuna-app-id
databricks secrets put --scope fys-api-keys --key adzuna-api-key

# USAJobs
databricks secrets put --scope fys-api-keys --key usajobs-api-key

# BLS
databricks secrets put --scope fys-api-keys --key bls-api-key

# CareerOneStop
databricks secrets put --scope fys-api-keys --key careeronestop-user-id
databricks secrets put --scope fys-api-keys --key careeronestop-token
```

---

### Step 3: Use in Code

```python
# The scraper automatically tries to load from secrets:
try:
    ADZUNA_APP_ID = dbutils.secrets.get("fys-api-keys", "adzuna-app-id")
    ADZUNA_API_KEY = dbutils.secrets.get("fys-api-keys", "adzuna-api-key")
except:
    # Fallback to environment variables for local testing
    import os
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")
```

---

## Current Status

✅ Adzuna - Keys registered, working in scraper  
⏸️ USAJobs - Pending registration  
⏸️ BLS - Pending registration  
⏸️ CareerOneStop - Pending registration  

---

## Next Steps

1. **Immediate:** Scraper works with current setup (keys in notebook memory)
2. **Before committing code:** Set up Databricks secrets as shown above
3. **Production:** All keys will be read from secrets only

---

## Verify Setup

```bash
# List all secrets in scope
databricks secrets list --scope fys-api-keys

# Should show:
# - adzuna-app-id
# - adzuna-api-key
# - usajobs-api-key
# - bls-api-key
# - careeronestop-user-id
# - careeronestop-token
```
