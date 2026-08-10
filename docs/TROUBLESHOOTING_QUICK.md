# Quick Troubleshooting

## Common Issues

### ❌ "Table not found"
**Fix:** Run `databricks sql execute --statement "USE CATALOG workspace"`

### ❌ "API rate limit exceeded"
**Fix:** Wait 1 hour or switch to different API key

### ❌ "Permission denied"
**Fix:** Check Unity Catalog grants: `GRANT SELECT ON TABLE ...`

### ❌ "Import error"
**Fix:** `pip install -r requirements.txt`

### ❌ "Databricks CLI not found"
**Fix:** `pip install databricks-cli && databricks configure`

### ❌ "Notebook cell fails"
**Fix:** Restart compute: `Cmd/Ctrl + Shift + F`

### ❌ "Git push rejected"
**Fix:** `git pull --rebase && git push`

### ❌ "Test failures"
**Fix:** Clear cache: `pytest --cache-clear tests/`

---

## Quick Commands

```bash
# Check job status
databricks jobs list

# View table data
databricks sql execute --statement "SELECT * FROM workspace.fys_bronze.job_postings LIMIT 5"

# Test connectivity
curl -X GET https://api.usajobs.gov/search/jobs -H "Authorization-Key: $USAJOBS_API_KEY"

# Restart job
databricks jobs run-now --job-id 12345
```

---

Still stuck? Check full TROUBLESHOOTING.md or email whall4.wh@gmail.com
