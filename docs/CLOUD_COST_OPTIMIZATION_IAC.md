# Multi-Cloud Cost Optimization & Free-Tier Guardrails in IaC 🇺🇸 💰

**Lead Architect:** Free Hall <whall4.wh@gmail.com>
**Organization:** 7 Eagle Group
**Project:** For Your Service

---

## 💰 Target Monthly Budget: $5.00 – $12.00 / Month

This document details the cost optimization mechanisms built directly into the Terraform code to ensure **For Your Service** remains 100% free-tier compliant where possible and low-cost on serverless compute.

---

## 🛡️ Cloud-by-Cloud Cost Controls

| Cloud Provider | Component | Optimization Mechanism | Monthly Cost Impact |
|----------------|-----------|------------------------|---------------------|
| **AWS** | S3 Staging | 14-day auto-expiration lifecycle rule | $0.00 (within 5 GB limit) |
| **AWS** | DynamoDB | `PAY_PER_REQUEST` on-demand billing mode | $0.00 (under 25 GB limit) |
| **AWS** | Lambda | Memory sized to 256MB, 30s timeout | $0.00 (under 1M calls/mo) |
| **AWS** | AWS Budgets | Zero-spend email notification threshold ($5) | Prevents runaway costs |
| **GCP** | Cloud Storage | Nearline (30d) and Coldline (90d) transitions | < $0.50 / month |
| **GCP** | BigQuery | Partitioned tables by date to reduce scan volume | $0.00 (under 10 GB limit) |
| **GCP** | Cloud Functions | 256MB RAM with 60s timeout | $0.00 (under 2M calls/mo) |
| **Databricks** | SQL Warehouse | `auto_stop_mins = 10` & `2X-Small` Serverless | ~$5.00 - $10.00 / month |
| **Hugging Face** | Spaces | `cpu-basic` hardware tier | **$0.00 / month** (100% FREE) |
| **Total** | | | **~$5.00 – $10.50 / month** |

---

## 🔍 Code Enforcement Examples

### Databricks Auto-Stop
```hcl
resource "databricks_sql_endpoint" "serverless_warehouse" {
  cluster_size              = "2X-Small"
  auto_stop_mins            = 10
  enable_serverless_compute = true
}
```

### AWS S3 Auto-Expire
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "staging_lifecycle" {
  rule {
    id     = "expire-temporary-staging-data"
    status = "Enabled"
    expiration {
      days = 14
    }
  }
}
```
