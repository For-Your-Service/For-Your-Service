# Multi-Cloud Terraform Architecture Whitepaper 🇺🇸 ☁️

**Lead Architect:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group  
**Project:** For Your Service - AI Veteran Job Matching Platform  

---

## 1. Executive Summary

**For Your Service** operates a mission-critical AI platform connecting transitioning military veterans with civilian careers. The infrastructure spans four distinct cloud environments:
- **Amazon Web Services (AWS):** Object storage (S3), NoSQL fast lookups (DynamoDB), Serverless APIs (Lambda), Secrets Manager, and IAM security.
- **Google Cloud Platform (GCP):** Cold archives (GCS), Analytics & ML reporting (BigQuery), Serverless Webhooks (Cloud Functions), and Custom IAM.
- **Databricks:** Unity Catalog data lakehouse (Bronze, Silver, Gold Delta layers), Serverless SQL Warehouses, and Automated ETL Pipelines.
- **Hugging Face Spaces:** Containerized production FastAPI backend and neural network matching endpoints.

This document describes the unified Infrastructure as Code (IaC) architecture built with Terraform to ensure fast, repeatable, and non-destructive deployments.

---

## 2. Multi-Cloud Topology

```
                                  ┌────────────────────────┐
                                  │   Streamlit Web UI     │
                                  │   (Local / Cloud)      │
                                  └───────────┬────────────┘
                                              │
                                  ┌───────────▼────────────┐
                                  │ Hugging Face Spaces    │
                                  │ FastAPI Backend (7860) │
                                  └─────┬────────────┬─────┘
                                        │            │
             ┌──────────────────────────┘            └─────────────────────────┐
             ▼                                                                 ▼
┌─────────────────────────┐                                       ┌─────────────────────────┐
│       Databricks        │                                       │           AWS           │
│ ─────────────────────── │                                       │ ─────────────────────── │
│ • Unity Catalog         │◄─────── STS Cross-Account Trust ─────►│ • S3 Staging & Data     │
│   - fys_bronze          │                                       │ • DynamoDB Veterans     │
│   - fys_silver          │                                       │ • DynamoDB Jobs         │
│   - fys_gold            │                                       │ • Lambda Matching API   │
│ • Serverless SQL Whse   │                                       │ • Secrets Manager       │
└────────────┬────────────┘                                       └─────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│           GCP           │
│ ─────────────────────── │
│ • GCS Archive Bucket    │
│ • BigQuery Analytics    │
│ • Cloud Functions       │
│ • Custom Role Operator  │
└─────────────────────────┘
```

---

## 3. Module Hierarchy & Separation of Concerns

```
terraform/
├── main.tf                 # Top-level composition & provider instances
├── variables.tf            # Global flags (enable_aws, enable_gcp, etc.)
├── outputs.tf              # Aggregated resource URIs and ARNs
├── versions.tf             # HashiCorp & Databricks provider constraints
│
├── modules/
│   ├── aws/                # AWS resource bundle
│   ├── gcp/                # GCP resource bundle
│   ├── databricks/         # Databricks lakehouse bundle
│   └── huggingface/        # Hugging Face deployment bundle
│
└── environments/
    ├── dev/                # Development configuration
    ├── staging/            # Staging configuration
    └── prod/               # Production configuration
```

---

## 4. Cost Optimization & Free-Tier Guardrails

1. **AWS:**
   - S3 Lifecycle: Auto-expires staging data after 14 days.
   - DynamoDB: `PAY_PER_REQUEST` on-demand billing (zero idle charges).
   - AWS Budgets: $5.00/month threshold with early email warning alerts.
2. **GCP:**
   - GCS: Transitions archive files from Standard → Nearline (30d) → Coldline (90d).
   - BigQuery: Day-partitioned tables to minimize scanned byte volume.
3. **Databricks:**
   - Serverless SQL Warehouse: Configured with `auto_stop_mins = 10` to eliminate idle compute spend.
4. **Hugging Face:**
   - Spaces: Utilizes `cpu-basic` hardware tier ($0/month).

**Total Estimated Monthly Infrastructure Cost:** **$5 – $12 / month**
