# For Your Service - Veteran Job Placement Platform

## 🚀 **START HERE: [Deployment Progress Log](./DEPLOYMENT_LOG.md)**

**👉 New to the project?** Read the [DEPLOYMENT_LOG.md](./DEPLOYMENT_LOG.md) first!

It contains:
- ✅ **What we've built so far** - Complete work summary
- 🔄 **Current deployment status** - What's live, what's in progress
- 📋 **Next steps** - Detailed checklist
- 🏗️ **Simple architecture explanation** - How everything works
- 🔐 **Privacy & security details** - How we protect veteran data
- 🛠️ **Troubleshooting guide** - Common issues and fixes

**Last Updated:** August 5, 2026

---

## 🔐 **Privacy & PII Protection**

We take veteran privacy seriously. Read our comprehensive documentation:

### 👉 [PII Protection Documentation](./PII_PROTECTION.md)

**What you'll learn:**
- ✅ How we remove ALL personal identifying information
- ✅ Simple explanation for non-technical readers
- ✅ Technical implementation details
- ✅ Complete data flow showing where PII is removed
- ✅ What data we keep vs. remove
- ✅ Security guarantees and compliance (GDPR, CCPA, HIPAA)

**Quick Summary:**
Before storing any veteran data, our system automatically removes names, emails, phone numbers, addresses, SSNs, and birthdates. We replace them with anonymous IDs. This means veteran identities are protected even if our database is compromised.

---

# 🎖️ For Your Service - Veteran Job Placement Platform

## Mission
For Your Service (FYS) is an AI-powered platform that matches transitioning military veterans with civilian job opportunities using multi-dimensional tensor analysis and machine learning.

**Partner:** 7 Eagle Group (Veteran Placement Organization)

---

## Architecture Overview

```
Counselor Intake Wizard
        ↓
    JSON Payload (Veteran Profile)
        ↓
GCP Cloud Function (PII Anonymization)
        ↓
GCS Raw Bucket (gs://fys-veteran-intake-raw)
        ↓
Databricks Bronze Layer (Raw Anonymized Data)
        ↓
Databricks Silver Layer (Feature Engineering)
        ↓
Databricks Gold Layer (Tensor Engine - Vector Dot Products)
        ↓
Placement Probability Matrix
        ↓
Counselor Dashboard + Ranked Job Matches
```

---

## Repository Structure

### `/cloud-functions/`
GCP Cloud Functions for intake processing
- `veteran-intake/` - PII anonymization and GCS storage

### `/databricks/`
Databricks notebooks for data pipeline
- `01_intake_schema_definition.py` - Veteran profile schema
- `03_bronze_ingestion.py` - Raw data ingestion from GCS
- `04_silver_feature_engineering.py` - MOS-to-skill mapping, feature extraction
- `05_gold_tensor_engine.py` - Tensor computations for job matching

### `/docs/`
Architecture and technical documentation

### `/terraform/`
(Future) Infrastructure as Code for GCP resources

### `/scripts/`
(Future) Deployment and utility scripts

---

## Quick Start

### 1. Deploy GCP Infrastructure

```bash
# Create GCS bucket
gsutil mb -p uap-scraper-lab-2026 -c STANDARD -l us-central1 gs://fys-veteran-intake-raw

# Deploy Cloud Function
cd cloud-functions/veteran-intake
gcloud functions deploy veteran-intake-processor \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=veteran_intake \
  --trigger-http \
  --allow-unauthenticated \
  --memory=1GB \
  --timeout=60s
```

### 2. Configure Databricks

1. Import notebooks from `/databricks/` to your Databricks workspace
2. Configure GCS access in cluster settings:
   ```
   spark.hadoop.google.cloud.auth.service.account.json.keyfile /path/to/keyfile.json
   ```
3. Create Unity Catalog schemas:
   ```sql
   CREATE SCHEMA IF NOT EXISTS main.fys_bronze;
   CREATE SCHEMA IF NOT EXISTS main.fys_silver;
   CREATE SCHEMA IF NOT EXISTS main.fys_gold;
   ```

### 3. Run Pipeline

1. Test Cloud Function with sample veteran profile
2. Run Bronze ingestion notebook
3. Run Silver feature engineering
4. Run Gold tensor engine

---

## Data Privacy & Security

### PII Protection
- All personally identifiable information (PII) is anonymized before storage
- Anonymous `veteran_id` generated for tracking
- Only aggregated location data (ZIP3) retained
- Email hashed for deduplication only

### Anonymized Data

✅ **Kept:**
- Military service data (MOS, rank, branch, deployments)
- Skills, certifications, education
- Job preferences (roles, industries, salary range)
- General location (city, state, ZIP3)
- Birth year (for age-based matching)

❌ **Removed:**
- Full name
- Email address
- Phone number
- Full date of birth
- SSN/Last 4
- Street address

---

## Technology Stack

- **GCP Cloud Functions** - Serverless intake processing
- **Google Cloud Storage** - Raw data lake
- **Databricks** - Data engineering and ML platform
- **Delta Lake** - ACID transactions and time travel
- **PySpark** - Distributed data processing
- **Unity Catalog** - Data governance

---

## Roadmap

### Phase 1: Core Pipeline (In Progress)
- [x] Intake schema definition
- [x] PII anonymization Cloud Function
- [x] Bronze layer ingestion
- [ ] Silver layer feature engineering
- [ ] Gold layer tensor engine

### Phase 2: Job Matching
- [ ] Job posting data ingestion
- [ ] MOS-to-civilian skill mapping
- [ ] Real-time probability matrix computation
- [ ] Counselor dashboard

### Phase 3: Operations
- [ ] Counselor intake wizard UI
- [ ] Local task scheduler
- [ ] Status sync system
- [ ] Public branding and case studies

---

## Contributing

This project is in active development. Contributors:
- Will Hall (whall4.wh@gmail.com)
- Donavan Marcus (Donavanmarcus@gmail.com)
- Josh Shalack (Josh.shalack@gmail.com)
- Leroy (leroy@ironin.com)

---

## License

Proprietary - For Your Service Organization

---

## Contact

For questions or partnership inquiries:
- **Email:** whall4.wh@gmail.com
- **Organization:** For Your Service
- **Partner:** 7 Eagle Group
