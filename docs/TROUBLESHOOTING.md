# 🔧 Troubleshooting Guide

## API Issues

### 403 Forbidden
**Cause:** Invalid API credentials
**Fix:**
- Verify no extra spaces in API key
- Check key hasn't expired
- Regenerate key if needed

### 429 Rate Limit Exceeded
**Cause:** Too many requests
**Fix:**
- Wait for quota reset
- Implement exponential backoff
- Consider paid tier

### Zero Jobs Returned
**Cause:** Location parameter mismatch
**Fix:**
- Use exact format: "Greenville, SC"
- Check radius parameter
- Verify API is searching correct region

## Databricks Issues

### Secrets Not Found
**Cause:** Secrets scope not created
**Fix:**
```bash
databricks secrets create-scope --scope fys-apis
```

### Table Not Found
**Cause:** Bronze table doesn't exist
**Fix:** Run `setup/01_Unity_Catalog_Setup.py`

### Permission Denied
**Cause:** Missing Unity Catalog permissions
**Fix:** Contact workspace admin for CREATE TABLE

## Data Quality Issues

### Duplicate Jobs
**Cause:** job_id collision
**Fix:** Add timestamp to hash input

### Missing Salary Data
**Cause:** Not all APIs provide salary
**Expected:** 70% coverage rate

### Wrong Location
**Cause:** Regional filter too broad
**Fix:** Tighten MSA keywords list
