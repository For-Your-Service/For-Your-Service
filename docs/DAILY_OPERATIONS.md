# 📅 Daily Operations Guide

## Morning Routine (5 minutes)

1. **Check Ingestion Status**
   - Open Databricks SQL
   - Run: `sql/monitor_ingestion.sql`
   - Verify yesterday's data loaded

2. **Review Data Quality**
   - Run: `sql/check_data_quality.sql`
   - Flag any issues >5% failure rate

3. **Monitor API Health**
   - Run: `scripts/check_api_rate_limits.py`
   - Ensure quota not exhausted

## Weekly Tasks (15 minutes)

### Monday
- Review 7-day ingestion trends
- Check for new high-volume companies
- Verify regional coverage

### Wednesday
- Run salary analysis
- Compare with market benchmarks
- Update compensation insights

### Friday
- Generate weekly summary report
- Archive old partition files
- Plan next week's improvements

## Monthly Tasks (1 hour)

- Review API costs vs. budget
- Analyze source quality metrics
- Update documentation
- Plan Silver layer enhancements

## Incident Response

### Job Failed
1. Check Databricks job logs
2. Test API connectivity
3. Verify secrets not expired
4. Re-run manually
5. Document root cause

### Zero Jobs Returned
1. Check API rate limits
2. Verify location parameters
3. Test each API individually
4. Check for service outages

### Data Quality Issues
1. Run validation script
2. Identify affected source
3. Backfill if needed
4. Update quality rules
