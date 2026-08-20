# Databricks Module - For Your Service 🇺🇸 ☁️

Terraform module managing Databricks Unity Catalog, Serverless SQL Warehouses, Secret Scopes, and Ingestion Jobs for **For Your Service**.

---

## 📦 Provisioned Resources

| Resource | Type | Purpose | Cost Optimization |
|----------|------|---------|-------------------|
| `databricks_schema.bronze` | Unity Catalog | Ingestion layer for raw job postings | Delta auto-optimize & compact |
| `databricks_schema.silver` | Unity Catalog | Cleaned veteran profiles & MOS taxonomy | Optimized partitioning |
| `databricks_schema.gold` | Unity Catalog | 384-dim neural embeddings & match metrics | Production serving |
| `databricks_sql_endpoint.serverless_warehouse` | SQL Warehouse | Query engine for FastAPI and Streamlit | Auto-stop in 10 minutes |
| `databricks_secret_scope.aws_credentials` | Secrets | Secure AWS IAM credential access | Role-based STS access |
| `databricks_secret_scope.api_keys` | Secrets | Secure USAJOBS, JSearch, Adzuna keys | Keyless in code |
| `databricks_storage_credential.aws_s3_cred` | Credential | Unity Catalog IAM trust credential | Zero hardcoded keys |
| `databricks_external_location.s3_staging` | Location | External S3 staging bucket mapping | Read/write restricted |
| `databricks_job.daily_ingestion_pipeline` | Workflow | Automated multi-source job ingestion | Scheduled off-peak |

---

## 🔒 Unity Catalog Integration

- Schemas are scoped by environment (`fys_bronze` for prod, `fys_dev_bronze` for dev).
- Serverless SQL Warehouse automatically stops when idle, keeping compute costs below $5-10/month.
