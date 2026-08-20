# GCP Module - For Your Service 🇺🇸 ☁️

Terraform module managing Google Cloud Platform (GCP) infrastructure for **For Your Service**.

---

## 📦 Provisioned Resources

| Resource | Service | Purpose | Free Tier / Cost Guardrails |
|----------|---------|---------|-----------------------------|
| `google_storage_bucket.archive` | Cloud Storage | Long-term cold storage archive | Lifecycle: Nearline (30d) → Coldline (90d) |
| `google_storage_bucket.raw_ingestion` | Cloud Storage | Temporary raw API dumps | Auto-deletion after 14 days |
| `google_bigquery_dataset.fys_analytics` | BigQuery | Crosswalk and matching analytics | 10 GB free storage/month, 1 TB queries |
| `google_bigquery_table.ingested_jobs` | BigQuery | Ingested jobs partitioned by timestamp | Day-partitioned for query cost reduction |
| `google_cloudfunctions_function.veteran_intake` | Cloud Functions | Serverless intake endpoint | 2M free invocations/month |
| `google_project_iam_custom_role.fys_pipeline_operator` | Cloud IAM | Least-privilege role for ingestion | Scoped to storage & BigQuery only |
| `google_service_account.pipeline_sa` | Cloud IAM | Non-human identity for pipeline jobs | Keyless workload identity ready |

---

## 🔒 Security & Access

- Uniform bucket-level access enforced on all GCS buckets.
- Custom IAM role grants minimal permissions to BigQuery and GCS.
- Cloud Functions run under dedicated `foryourservice-sa-*` service account.
