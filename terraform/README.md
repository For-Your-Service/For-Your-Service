# For Your Service - Multi-Cloud Terraform Architecture 🇺🇸 ☁️

Comprehensive Infrastructure as Code (IaC) for **For Your Service** spanning **AWS**, **Google Cloud Platform (GCP)**, **Databricks**, and **Hugging Face Spaces**.

---

## 🏛️ Architecture Overview

The multi-cloud architecture is structured into modular, loosely coupled components designed to allow spinning up, tearing down, and recreating any cloud environment on-demand without affecting running production services.

```
                   ┌────────────────────────────────────────┐
                   │       For Your Service IaC Core        │
                   │        (terraform/main.tf)             │
                   └──────────────────┬─────────────────────┘
                                      │
         ┌──────────────────┬─────────┴─────────┬──────────────────┐
         │                  │                   │                  │
         ▼                  ▼                   ▼                  ▼
┌────────────────┐ ┌────────────────┐ ┌──────────────────┐ ┌────────────────┐
│   AWS Module   │ │   GCP Module   │ │Databricks Module │ │HuggingFace Mod │
│ ────────────── │ │ ────────────── │ │ ──────────────── │ │ ────────────── │
│ • S3 Data Lake │ │ • GCS Archives │ │ • Unity Catalog  │ │ • FastAPI Space│
│ • DynamoDB     │ │ • BigQuery     │ │ • SQL Warehouse  │ │ • Docker App   │
│ • Lambda API   │ │ • Cloud Funcs  │ │ • Secret Scopes  │ │ • Space Secrets│
│ • IAM Security │ │ • Custom Roles │ │ • Ingest Jobs    │ │ • CPU Basic    │
└────────────────┘ └────────────────┘ └──────────────────┘ └────────────────┘
```

---

## 📁 Directory Structure

```
terraform/
├── main.tf                     # Root orchestrator instantiating all cloud modules
├── variables.tf                # Feature flags (enable_aws, enable_gcp, etc.) and global inputs
├── outputs.tf                  # Aggregated outputs (URLs, bucket names, ARNs)
├── versions.tf                 # Provider requirements and version constraints
├── terraform.tfvars.example    # Template variable values
├── DEPLOYMENT_GUIDE.md         # Step-by-step rollout and import guide
├── DEPLOYMENT_CHECKLIST.md     # Production zero-downtime checklist
├── modules/
│   ├── aws/                    # AWS S3, DynamoDB, Lambda, IAM, Secrets Manager
│   ├── gcp/                    # GCP Cloud Storage, BigQuery, IAM Custom Roles, Cloud Functions
│   ├── databricks/             # Databricks Unity Catalog, SQL Warehouses, Secret Scopes, Jobs
│   └── huggingface/            # Hugging Face Space definitions and secrets
├── environments/
│   ├── dev/                    # Development environment configuration
│   ├── staging/                # Staging environment configuration
│   └── prod/                   # Production environment configuration
└── scripts/                    # Validation, deployment, and import automation scripts
```

---

## 🔒 Safe Zero-Downtime Deployment & Existing Resource Adoption

To spin up new infrastructure without impacting the currently running build:
1. **Feature Flags:** Toggle providers on/off using `enable_aws`, `enable_gcp`, `enable_databricks`, and `enable_huggingface`.
2. **Resource Importing:** Existing buckets or schemas can be imported via `terraform import` without downtime.
3. **Isolated State:** State files are separated by environment (`dev`, `staging`, `prod`) to prevent accidental collisions.
4. **Plan Verification:** Always run `terraform plan` to verify the execution graph before `terraform apply`.

---

## 🚀 Quick Start

1. **Initialize Terraform:**
   ```bash
   cd terraform
   terraform init
   ```

2. **Configure Variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your credentials and parameters
   ```

3. **Plan and Validate:**
   ```bash
   terraform plan
   ```

4. **Deploy:**
   ```bash
   terraform apply
   ```
