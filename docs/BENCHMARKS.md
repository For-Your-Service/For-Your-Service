# Performance Benchmarks

## Ingestion Pipeline

| Metric | Target | Current |
|--------|--------|---------|
| **Daily job count** | 200-500 | ~350 |
| **Ingestion duration** | <15 min | ~8 min |
| **API calls per run** | <100 | ~75 |
| **Data freshness** | <24 hours | ~6 hours |

---

## API Performance

| Metric | Target | Current |
|--------|--------|---------|
| **Response time (p50)** | <200ms | ~150ms |
| **Response time (p95)** | <500ms | ~380ms |
| **Response time (p99)** | <1000ms | ~720ms |
| **Throughput** | 100 req/s | ~45 req/s |

---

## Matching Engine

| Metric | Target | Current |
|--------|--------|---------|
| **Embedding generation** | <100ms | ~65ms |
| **Match computation** | <200ms | ~140ms |
| **Top-K retrieval (k=20)** | <50ms | ~35ms |
| **Memory per profile** | <1MB | ~650KB |

---

## Data Quality

| Metric | Target | Current |
|--------|--------|---------|
| **Completeness score** | >85% | ~88% |
| **Duplicate rate** | <5% | ~3% |
| **Null rate (salary)** | <30% | ~25% |
| **Schema compliance** | 100% | 100% |

---

## Cost Efficiency

| Metric | Target | Current |
|--------|--------|---------|
| **Cost per match** | <$0.25 | ~$0.18 |
| **Monthly compute cost** | <$10 | ~$7 |
| **Storage cost** | <$2 | ~$1.20 |
| **Total monthly cost** | <$15 | ~$10 |

---

Test environment: Databricks Serverless, S3 storage, 2 vCPU
Last updated: August 10, 2026
