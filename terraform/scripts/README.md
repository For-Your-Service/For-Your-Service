# Terraform Automation & Tooling Scripts 🇺🇸 ☁️

Automation scripts for managing the multi-cloud infrastructure of **For Your Service**.

---

## 🛠️ Scripts Inventory

| Script | Runtime | Purpose |
|--------|---------|---------|
| `tf_validate.ps1` | PowerShell | Lints, formats, and verifies syntax across all modules and environments |
| `tf_plan_all.sh` | Bash | Generates dry-run execution plan (`.tfplan`) with environment selection |
| `tf_apply_all.sh` | Bash | Safely applies verified `.tfplan` files |
| `tf_import_existing.sh` | Bash | Zero-downtime resource import helper (AWS, Databricks, GCP) |
| `tf_import_existing.ps1` | PowerShell | Windows-compatible resource import helper |
| `test_cloud_connectivity.py` | Python 3 | Verifies authentication and network connectivity to AWS, GCP, Databricks, and HF |

---

## 🔒 Safe Zero-Downtime Adoption Workflow

To link existing live cloud assets into Terraform state without tearing down or breaking the current build:

```powershell
# 1. Validate Terraform formatting
powershell -ExecutionPolicy Bypass -File terraform\scripts\tf_validate.ps1

# 2. Check multi-cloud connectivity
python terraform\scripts\test_cloud_connectivity.py

# 3. Import existing live resources into state
powershell -ExecutionPolicy Bypass -File terraform\scripts\tf_import_existing.ps1 -Environment prod
```
