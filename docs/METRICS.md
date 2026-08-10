# Key Metrics & KPIs

## System Health Metrics

### Ingestion Pipeline
- **Daily Job Count:** 200-500 (target)
- **Source Availability:** >99% uptime
- **Ingestion Duration:** <15 minutes
- **Data Quality Score:** >80%

### API Performance
- **Response Time (p95):** <500ms
- **Match Accuracy:** >85%
- **Uptime:** >99.5%
- **Error Rate:** <1%

---

## Business Metrics

### Veteran Engagement
- **Active Veterans:** Users in last 30 days
- **Profile Completion Rate:** % with full profiles
- **Average Matches per Veteran:** 25-50
- **Match Click-Through Rate:** >30%

### Job Market Coverage
- **Total Active Jobs:** ~500 (Greenville MSA)
- **Companies Tracked:** 100+
- **Average Salary Range:** $80K-$140K
- **Remote Jobs %:** 40-60%

### Placement Success
- **Interview Rate:** % veterans getting interviews
- **Offer Rate:** % veterans receiving offers
- **Placement Rate:** % veterans accepting jobs
- **Time to Placement:** Days from registration to hire

---

## Data Quality Metrics

### Completeness
- **Title:** 100% (required)
- **Company:** 95%+
- **Salary:** 70%+
- **Description:** 90%+
- **Location:** 98%+

### Accuracy
- **Duplicate Rate:** <5%
- **Stale Job Rate:** <20% (>30 days old)
- **Salary Prediction Accuracy:** ±10K

---

## ML Model Metrics

### Matching Engine
- **Precision@10:** >80%
- **Recall@10:** >70%
- **MRR (Mean Reciprocal Rank):** >0.75
- **Embedding Generation Time:** <100ms per profile

---

## Cost Metrics

- **Cost per Match:** $0.14-0.24
- **Cost per Veteran (monthly):** $0.70-1.20
- **Total Monthly Cost:** $7-12
- **Cost per Placement:** <$5

---

## Dashboard Queries

See `sql/` directory for metric calculation queries.
