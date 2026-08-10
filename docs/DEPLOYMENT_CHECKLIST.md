# ✅ Deployment Checklist

## Pre-Deployment

- [ ] All API keys obtained and tested
- [ ] Databricks Secrets configured
- [ ] Bronze table created in Unity Catalog
- [ ] Test ingestion run completed successfully
- [ ] Data quality validation passed

## Deployment Steps

### 1. Create Databricks Job

```yaml
name: FYS Multi-Source Job Ingestion
schedule: "0 0 6 * * ?" # 6 AM daily
notebook: /notebooks/03b_Multi_Source_Job_Ingestion
cluster: Serverless (auto)
timeout: 1800 seconds (30 min)
```

### 2. Configure Alerts

- Email on job failure
- Slack webhook for completion
- PagerDuty for critical errors

### 3. Enable Monitoring

- Add to daily health check dashboard
- Set up weekly summary email
- Configure data quality alerts

### 4. Document Handoff

- Share API keys with ops team (via secrets)
- Train team on troubleshooting
- Document escalation procedures

## Post-Deployment

- [ ] Monitor first 3 runs closely
- [ ] Verify Bronze table growth
- [ ] Check data quality metrics
- [ ] Confirm API rate limits not exceeded
- [ ] Review ingestion duration trends

## Rollback Procedure

If issues occur:
1. Pause Databricks Job
2. Check error logs
3. Validate API connectivity
4. Test locally first
5. Re-enable after fix confirmed
