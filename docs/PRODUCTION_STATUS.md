> **DEPRECATED / NON-CANONICAL:** This document/script contains legacy schema references. The code-canonical production spine is defined in [ADR 001](adr/ADR-001-CODE-CANONICAL-CATALOG-SPINE.md) (workspace.fys_*).

# Production Data Pipeline Status

**Project:** For Your Service
**Organization:** 7 Eagle Group
**Author:** Free Hall <whall4.wh@gmail.com>

---

## 🟢 Production Infrastructure - READY

### Unity Catalog Assets Created

✅ **Volume:** `workspace.for_your_service.job_data`
   - Path: `/Volumes/workspace/for_your_service/job_data`
   - Purpose: Raw JSON staging from APIs/manual scraping
   - Owner: whall4.wh@gmail.com

✅ **Schema:** `workspace.for_your_service`
   - Comment: "7 Eagle Group - For Your Service veteran job matching pipeline"

✅ **Bronze Table:** `workspace.for_your_service.job_matching_bronze` (awaiting first ingestion)

---

## 🔴 Production Data Ingestion - BLOCKED

### Current Status: NO REAL DATA

**Root Cause:** Invalid Adzuna API credentials

```
❌ API Response: 401 Unauthorized
   "Authorisation failed"
```

---

## ✅ Solutions Implemented

### Option 1: Fix Adzuna API Credentials

**Steps:**
1. Go to https://developer.adzuna.com/member
2. Sign up / log in
3. Create application
4. Copy App ID and App Key
5. Update `config/api_credentials.py`:

```python
ADZUNA_APP_ID = "your_real_app_id"
ADZUNA_APP_KEY = "your_real_app_key"
```

6. Re-run production ingestion script

### Option 2: Manual Job Scraping (Immediate Solution)

**Steps:**
1. Visit Indeed: https://www.indeed.com/jobs?q=DevOps+Engineer&l=Greenville%2C+SC
2. Visit LinkedIn: https://www.linkedin.com/jobs/devops-engineer-greenville-sc
3. Copy job details from 5-10 real postings
4. Run manual uploader:

```python
import sys
sys.path.insert(0, '/Workspace/Users/whall4.wh@gmail.com/For-Your-Service')

from scripts.manual_real_job_uploader import ManualRealJobUploader

uploader = ManualRealJobUploader()

real_jobs = []

# Add REAL job from Indeed
real_jobs.append(uploader.add_real_job_from_indeed(
    job_url="https://www.indeed.com/viewjob?jk=ACTUAL_JOB_ID",
    title="ACTUAL TITLE",
    company="ACTUAL COMPANY",
    location="Greenville, SC",
    description="FULL DESCRIPTION",
    salary_text="$120K-$150K",
    posted_date="3 days ago"
))

# Save to UC Volume
filepath = uploader.save_jobs_to_volume(real_jobs, source_name="indeed_manual")
```

5. Run production ingestion:

```python
from src.pipelines.job_ingestion_pipeline import ingest_from_uc_volume_files

result = ingest_from_uc_volume_files()
```

---

## 📊 Pipeline Flow (Production Mode)

```
┌─────────────────┐
│  Adzuna API     │ ─── 401 Error ──> BLOCKED
└─────────────────┘

           ↓ FALLBACK

┌─────────────────────────────────┐
│  UC Volume Manual Upload        │ ─── READY
│  /Volumes/.../job_data/raw      │
└─────────────────────────────────┘

           ↓

┌─────────────────────────────────┐
│  Spark DataFrame                │ ─── READY
│  spark.read.json()              │
└─────────────────────────────────┘

           ↓

┌─────────────────────────────────┐
│  Bronze Delta Table             │ ─── READY (empty)
│  job_matching_bronze            │
└─────────────────────────────────┘

           ↓

┌─────────────────────────────────┐
│  Silver Table                   │ ─── READY (empty)
│  job_matching_silver            │
└─────────────────────────────────┘
```

---

## 🚫 Strict Production Rules

**NO MOCK DATA POLICY:**
- ❌ No synthetic job records
- ❌ No hardcoded test data
- ❌ No DataFrame creation with fake jobs
- ✅ ONLY real API responses
- ✅ ONLY manually scraped real jobs
- ✅ Graceful error handling when no data available

---

## 📈 Progress Metrics

**Commits Today:** 41
**Total Commits:** 392
**Production Assets:** 3 (Volume, Schema, Pipeline)
**Real Jobs Ingested:** 0 (awaiting credentials or manual upload)

---

## 🎯 Next Action Required

**Choose ONE:**

### A. Get Adzuna API Credentials (30 minutes)
- Free tier: 10,000 requests/month
- Real-time data
- Automated ingestion

### B. Manual Scrape Indeed/LinkedIn (15 minutes)
- Scrape 5-10 real jobs
- Immediate pipeline validation
- Demonstrates full Bronze → Silver flow

---

## 📞 Contact

**Free Hall**
Email: whall4.wh@gmail.com
Organization: 7 Eagle Group
Role: Army Special Forces (Ret.) → DevOps/Cloud Engineer

