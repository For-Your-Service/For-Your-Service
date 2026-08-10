# ❓ Frequently Asked Questions

## General

### Q: What is For Your Service?
A: AI-powered veteran job matching platform using neural networks to match military experience with civilian roles.

### Q: Who developed this?
A: Free Hall (7 Eagle Group) in partnership with veteran placement organizations.

### Q: Is this open source?
A: Yes! GitHub: https://github.com/For-Your-Service/For-Your-Service

## API Keys

### Q: Do I need paid API keys?
A: No! All three APIs have FREE tiers:
- USAJOBS: 1000/day
- JSearch: 1000/month  
- Adzuna: 5000/month

### Q: How do I get API keys?
A: See docs/API_QUICKSTART.md for step-by-step guide

### Q: Where do I store API keys?
A: Use Databricks Secrets (never commit to Git!)

## Data

### Q: How many jobs are ingested daily?
A: Target: 500+ for Greenville MSA

### Q: How fresh is the data?
A: Updated daily (configurable)

### Q: What regions are supported?
A: Currently: Greenville-Anderson, SC (50-mile radius)
Planned: Charlotte, Raleigh, Atlanta

## Deployment

### Q: What infrastructure is required?
A: Databricks (Unity Catalog + Serverless Compute)

### Q: What's the monthly cost?
A: ~$10-15/month (serverless + API costs)

### Q: Can this run on AWS/Azure/GCP?
A: Yes! Databricks supports all three clouds
