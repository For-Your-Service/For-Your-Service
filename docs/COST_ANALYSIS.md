# Cost Analysis - For Your Service

## Monthly Operating Costs

### API Costs (FREE Tier)
- **USAJOBS:** $0/month (1000 requests/day)
- **JSearch:** $0/month (1000 requests/month)
- **Adzuna:** $0/month (5000 requests/month)
- **O*NET:** $0/month (unlimited with free key)

**Total API Costs:** $0/month

### Databricks Costs
- **Serverless Compute:** ~$5-10/month
  - 30 min/day ingestion = $3-5
  - SQL queries for matching = $2-5
- **Unity Catalog Storage:** ~$0.50/month
  - Bronze: 100MB/day × 30 days = 3GB
  - $0.023/GB/month = $0.07
- **Delta Table Storage:** ~$2/month
  - Compressed Delta with partitioning

**Total Databricks:** $7-12/month

### Optional Costs
- **Hugging Face Spaces:** $0/month (FREE tier)
- **GitHub:** $0/month (public repo)
- **O*NET API:** $0/month (free tier)

## Total Monthly Cost: $7-12/month

## Cost per Veteran Matched
Assuming 50 veterans/month:
- **Cost per match:** $0.14-0.24
- **Extremely cost-effective!**

## Scaling Costs

| Monthly Matches | Est. Cost |
|----------------|-----------|
| 50 | $7-12 |
| 200 | $15-25 |
| 500 | $30-50 |
| 1000 | $50-100 |

## Cost Optimizations
- Use Serverless (pay per use)
- Partition tables by date
- Compress with ZSTD
- Cache frequent queries
- Batch API calls
