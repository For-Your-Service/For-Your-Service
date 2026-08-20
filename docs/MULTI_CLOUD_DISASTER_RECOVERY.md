# Multi-Cloud Disaster Recovery & On-Demand Spin-Up Runbook 🇺🇸 ☁️

**Lead Architect:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group  
**Project:** For Your Service  

---

## ⚡ Overview

With our multi-cloud Terraform configuration, the entire **For Your Service** platform can be spun up from scratch in any clean cloud account in **under 5 minutes**.

---

## 📋 Rapid Spin-Up Procedure

### 1. Prerequisites
- AWS CLI configured or `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` set.
- GCP `gcloud auth application-default login` or Service Account Key.
- Databricks Personal Access Token (`DATABRICKS_TOKEN`).
- Hugging Face Access Token (`HF_TOKEN`).

### 2. Execution Commands
```bash
# 1. Enter the target environment
cd terraform/environments/prod

# 2. Populate credentials
cp terraform.tfvars.example terraform.tfvars
# (Fill in active tokens)

# 3. Initialize & Deploy
terraform init
terraform apply -auto-approve
```

### 3. Verification
Run the verification script to confirm all endpoints and tables are operational:
```bash
python terraform/scripts/test_cloud_connectivity.py
```
