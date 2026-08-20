# AWS Module - For Your Service 🇺🇸 ☁️

Terraform module managing AWS infrastructure for **For Your Service**.

---

## 📦 Provisioned Resources

| Resource | Service | Purpose | Free Tier Limit |
|----------|---------|---------|-----------------|
| `aws_s3_bucket.data_prod` | Amazon S3 | Primary data lake & historical resumes | 5 GB storage |
| `aws_s3_bucket.staging` | Amazon S3 | Short-lived staging bucket for Databricks | 14-day auto-expiry |
| `aws_s3_bucket.resumes` | Amazon S3 | Ingested PDF/DOCX veteran resumes | Encrypted AES-256 |
| `aws_s3_bucket.models` | Amazon S3 | Neural network model weights & checkpoints | Encrypted AES-256 |
| `aws_dynamodb_table.veterans` | DynamoDB | Candidate profiles & career preferences | 25 GB storage (PAY_PER_REQUEST) |
| `aws_dynamodb_table.jobs` | DynamoDB | Ingested job postings & matching vectors | 25 GB storage (PAY_PER_REQUEST) |
| `aws_lambda_function.match_api` | AWS Lambda | Serverless real-time matching API | 1M free requests/month |
| `aws_iam_role.databricks_s3_role` | AWS IAM | Cross-account assume role for Unity Catalog | STS external ID secured |
| `aws_secretsmanager_secret.fys_secrets` | Secrets Manager | Secure storage for job board API keys | Auto-ignored in git |
| `aws_budgets_budget.zero_spend_budget` | AWS Budgets | Zero-spend notification threshold | Prevents unexpected charges |

---

## 🔒 Security & Least Privilege

- All S3 buckets block 100% of public access by default.
- Server-side AES-256 encryption enabled on all storage.
- IAM policy is scoped strictly to `foryourservice-*` and `fys-*` ARNs.
- Databricks cross-account assume role enforces `sts:ExternalId`.
