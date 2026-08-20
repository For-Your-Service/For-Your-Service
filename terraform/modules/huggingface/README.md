# Hugging Face Module - For Your Service 🇺🇸 ☁️

Terraform module managing Hugging Face Spaces deployment metadata, environment parameters, and Databricks secrets synchronization for **For Your Service**.

---

## 📦 Space Specification

- **SDK:** Docker (Python 3.11-slim, FastAPI)
- **Port:** 7860
- **Hardware:** `cpu-basic` (100% FREE tier, $0/month)
- **Secrets Configured:**
  - `DATABRICKS_SERVER_HOSTNAME`
  - `DATABRICKS_HTTP_PATH`
  - `DATABRICKS_TOKEN`

---

## 🚀 Deployment

The module generates standardized deployment manifests (`dist/README.md`, `dist/.env.space`, `dist/space_secrets.json`) that can be automatically synchronized via GitHub Actions or the Hugging Face Hub CLI.
