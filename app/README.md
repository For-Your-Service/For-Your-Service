# 🎖️ For Your Service - Veteran Intake Portal

**Streamlit Application for AI-Powered Veteran Job Matching**

*Powered by 7 Eagle Group*

---

## 📋 Overview

This Streamlit application provides a production-ready web interface for the For Your Service veteran job matching platform. Service members can:

* Register their profile with contact information
* Specify target job location and salary preferences
* Submit their resume text for AI-powered parsing
* Receive real-time job matches from 670+ active postings
* Apply directly to matching opportunities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│  Streamlit Frontend (app.py)                    │
├─────────────────────────────────────────────────┤
│  • Veteran intake form                          │
│  • Resume text parsing                          │
│  • Real-time validation                         │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  Databricks Unity Catalog                       │
├─────────────────────────────────────────────────┤
│  • workspace.fys_silver.veteran_profiles        │
│    (stores veteran registration data)           │
│  • workspace.fys_bronze.job_postings            │
│    (670+ jobs from Adzuna + USAJobs APIs)       │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  AI Matching Engine                             │
├─────────────────────────────────────────────────┤
│  • Keyword-based skill extraction               │
│  • Salary range filtering                       │
│  • Location-based matching                      │
│  • Scoring algorithm (0-100 scale)              │
└─────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
app/
├── __init__.py         # Package initialization
├── app.py              # Main Streamlit patriotic application
├── app.yaml            # Databricks App configuration
├── mos_data.py         # Military MOS/AFSC/Rating database & crosswalk
├── sample_data.py      # Zero-cost local fallback dataset & demo profile
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

---

## 🚀 Deployment Instructions

### Option 1: Databricks Apps (Recommended - FREE)

1. **Navigate to Apps**:
   - In your Databricks workspace, click **Compute** → **Apps**
   - Click **Create App**

2. **Configure App**:
   - **Name**: `fys-veteran-intake`
   - **Framework**: Streamlit
   - **Source**: `/Users/whall4.wh@gmail.com/For-Your-Service/app`

3. **Deploy**:
   - Click **Deploy**
   - Databricks serverless compute will auto-provision
   - App URL will be generated (e.g., `https://<workspace>.cloud.databricks.com/apps/fys-veteran-intake`)

4. **Share**:
   - Share the app URL with 7 Eagle Group coordinators
   - Veterans can access directly without Databricks accounts

### Option 2: Streamlit Community Cloud (100% Free - Recommended)

Deploy permanently 24/7 in 60 seconds directly from GitHub:

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New app"**.
3. Set **Repository**: `For-Your-Service/For-Your-Service`
4. Set **Branch**: `main`
5. Set **Main file path**: `app/app.py`
6. Click **"Deploy"**.

### Option 3: Local Development (100% Free & Offline)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (runs in local fallback mode if Databricks is not configured)
streamlit run app.py
```

---

## 🔧 Configuration

### Unity Catalog Tables

The app requires access to:

**Input Table**: `workspace.fys_silver.veteran_profiles`
```sql
CREATE TABLE IF NOT EXISTS workspace.fys_silver.veteran_profiles (
    veteran_id STRING PRIMARY KEY,
    name STRING NOT NULL,
    email STRING NOT NULL,
    target_city STRING,
    target_state STRING,
    total_years INT,
    seniority_level STRING,
    technical_skills STRING,  -- JSON string
    target_roles STRING,      -- JSON string
    salary_min INT,
    salary_max INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Job Postings Table**: `workspace.fys_bronze.job_postings`
- Contains 670+ active job listings
- Sourced from Adzuna and USAJobs APIs
- Refreshed daily

---

## 📊 Features

### 1. **Veteran Intake Form**
- **Personal Info**: Name, email
- **Location**: Target city and state (2-letter code)
- **Salary**: Min/max range sliders ($40K-$200K)
- **Resume**: Text area for resume paste (no file upload required)

### 2. **AI Resume Parsing**
- Automatic skill extraction (AWS, Kubernetes, Python, etc.)
- Years of experience calculation
- Seniority level determination (Entry/Mid/Senior)
- JSON-formatted skill storage

### 3. **Job Matching Engine**
- **Skills Match**: 40 points (keyword overlap)
- **Salary Alignment**: 30 points (range overlap)
- **Title Match**: 20 points (target role keywords)
- **Location Bonus**: 10 points (exact city match)

### 4. **Results Display**
- Top 10 matches sorted by score
- Expandable job cards with details
- Direct "Apply Now" links
- CSV export of all results

---

## 🛠️ Technical Stack

- **Frontend**: Streamlit 1.28+
- **Backend**: Databricks Unity Catalog (Delta Lake)
- **Compute**: Databricks Serverless (FREE tier)
- **Data Processing**: PySpark 3.4+
- **APIs**: Adzuna, USAJobs (job data ingestion)

---

## 📈 Data Flow

1. **Veteran Submission**:
   ```python
   veteran_id = generate_uuid()
   profile_data.write.saveAsTable("workspace.fys_silver.veteran_profiles")
   ```

2. **Job Query**:
   ```sql
   SELECT * FROM workspace.fys_bronze.job_postings
   WHERE location.state = 'SC'
     AND salary.max >= 75000
     AND salary.min <= 120000
   ```

3. **Matching Algorithm**:
   ```python
   score = skills_match(40) + salary_match(30) + title_match(20) + location_bonus(10)
   ```

4. **Results Display**:
   - Top 10 jobs ranked by score
   - Clickable application links
   - Downloadable CSV export

---

## 🔐 Security & Privacy

- **Data Encryption**: All data stored in Unity Catalog with Delta Lake encryption
- **PII Protection**: Email and personal data are access-controlled
- **Resume Privacy**: Resume text is parsed on-the-fly, not permanently stored
- **Access Control**: Unity Catalog RBAC enforced

---

## 📞 Support

**Developer**: Free Hall (whall4.wh@gmail.com)  
**Organization**: 7 Eagle Group  
**Project**: For Your Service - AI-Powered Veteran Placement  
**GitHub**: https://github.com/For-Your-Service/For-Your-Service

---

## 📝 License

Copyright © 2026 7 Eagle Group. All rights reserved.

---

## 🎖️ Mission Statement

*"Serving Those Who Served"*

For Your Service leverages AI to bridge the gap between military experience and civilian career opportunities, helping veterans find meaningful employment that honors their skills and service.