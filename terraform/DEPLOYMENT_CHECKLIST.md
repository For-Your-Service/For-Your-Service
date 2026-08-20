# Multi-Cloud Terraform Deployment Checklist 🇺🇸 ☁️

Use this checklist before applying any Terraform changes in production to guarantee zero downtime.

---

## 📋 Pre-Flight Checklist (Before Plan)

- [ ] **Git State Clean:** Working branch is up-to-date with `main`.
- [ ] **Formatting Verified:** `powershell -ExecutionPolicy Bypass -File terraform\scripts\tf_validate.ps1` returns green.
- [ ] **Credential Security:** Ensure no sensitive tokens (`dapi...`, `hf_...`, AWS secrets) are committed to git.
- [ ] **Connectivity Validated:** `python terraform\scripts\test_cloud_connectivity.py` confirms access to all required providers.
- [ ] **Target Environment Confirmed:** Double check that you are in the intended directory (`dev`, `staging`, or `prod`).

---

## 🔍 In-Flight Verification (During Plan)

- [ ] Run `terraform plan -out=execution.tfplan`.
- [ ] Inspect the plan summary:
  - **Plan: X to add, Y to change, 0 to destroy.**
- [ ] Ensure no active databases, S3 buckets, or Unity Catalog schemas are marked for destruction or replacement.
- [ ] Verify resource naming matches project prefix (`foryourservice-*` or `fys-*`).

---

## 🚀 Post-Flight Verification (After Apply)

- [ ] `terraform apply execution.tfplan` completed with exit code 0.
- [ ] **AWS Check:** Verify S3 buckets and DynamoDB tables are accessible.
- [ ] **Databricks Check:** Verify Unity Catalog schemas (`fys_bronze`, `fys_silver`, `fys_gold`) and SQL Warehouse status.
- [ ] **GCP Check:** Verify BigQuery dataset `fys_analytics` and GCS archive buckets.
- [ ] **Hugging Face Check:** Verify Space container status is `Running` on port 7860.
- [ ] **Streamlit App Check:** Launch `streamlit run app/app.py` and test candidate intake & job matching.
