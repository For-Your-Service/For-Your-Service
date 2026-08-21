# Hugging Face Spaces Deployment Guide

## Overview
FREE deployment strategy for For Your Service platform using Hugging Face Spaces.

**Cost:** $0/month
**Compute:** 2 vCPU, 16 GB RAM (free tier)
**Uptime:** 48-hour sleep after inactivity

---

## Architecture

```
┌─────────────────────────────────────┐
│   Hugging Face Spaces               │
│   ┌──────────────────────────────┐  │
│   │  Streamlit App               │  │
│   │  - User Interface            │  │
│   │  - Resume Upload             │  │
│   │  - Match Results Display     │  │
│   └──────────────────────────────┘  │
│            ↓                         │
│   ┌──────────────────────────────┐  │
│   │  Inference Engine            │  │
│   │  - SentenceTransformer       │  │
│   │  - Vector Similarity         │  │
│   │  - Match Scoring             │  │
│   └──────────────────────────────┘  │
│            ↓                         │
│   ┌──────────────────────────────┐  │
│   │  Data Storage (Local)        │  │
│   │  - SQLite (embedded)         │  │
│   │  - Job postings cache        │  │
│   │  - Veteran profiles          │  │
│   └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Required Files

### 1. `app.py` (Streamlit Application)
```python
import streamlit as st
from sentence_transformers import SentenceTransformer
import pandas as pd

# Load model (cached)
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

model = load_model()

st.title("For Your Service - Veteran Job Matching")
st.markdown("*Powered by 7 Eagle Group*")

# Veteran profile input
with st.form("veteran_profile"):
    name = st.text_input("Full Name")
    military_branch = st.selectbox("Branch", ["Army", "Navy", "Air Force", "Marines"])
    mos = st.text_input("MOS/AFSC")
    skills = st.text_area("Skills (comma-separated)")
    location = st.text_input("Target Location")

    submitted = st.form_submit_button("Find Matches")

    if submitted:
        # Run matching algorithm
        matches = find_matches(name, skills, location, model)

        # Display results
        st.subheader(f"Top Matches for {name}")
        st.dataframe(matches)
```

### 2. `requirements.txt`
```
streamlit==1.28.0
sentence-transformers==2.2.2
torch==2.0.1
pandas==2.1.0
scikit-learn==1.3.0
numpy==1.24.3
```

### 3. `README.md` (Hugging Face Spaces)
```markdown
---
title: For Your Service
emoji: 🎖️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
---

# For Your Service

AI-powered job matching platform for military veterans.

Partner: 7 Eagle Group
```

### 4. `.gitattributes`
```
*.7z filter=lfs diff=lfs merge=lfs -text
*.arrow filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.bz2 filter=lfs diff=lfs merge=lfs -text
```

---

## Deployment Steps

### Option 1: GitHub Integration (Recommended)
```bash
# 1. Push to GitHub
git add .
git commit -m "Initial Hugging Face Spaces deployment"
git push origin main

# 2. Create Space on Hugging Face
# - Go to https://huggingface.co/spaces
# - Click "Create new Space"
# - Name: for-your-service
# - SDK: Streamlit
# - Link to GitHub repo

# 3. Auto-sync enabled
# Any push to main → automatic deployment
```

### Option 2: Direct Upload
```bash
# 1. Install Hugging Face CLI
pip install huggingface_hub

# 2. Login
huggingface-cli login

# 3. Create space
huggingface-cli repo create for-your-service --type space --space_sdk streamlit

# 4. Upload files
huggingface-cli upload for-your-service ./app.py app.py
huggingface-cli upload for-your-service ./requirements.txt requirements.txt
```

---

## Data Sync Strategy

**Challenge:** Hugging Face Spaces cannot directly access Databricks

**Solution:** Periodic data export from Databricks → GitHub → Hugging Face

### Export Job Data (Daily)
```python
# Run in Databricks notebook
from datetime import datetime

# Get latest job matches
df = spark.table('veteran_intake.gold.job_matches').toPandas()

# Export to CSV
export_file = f"data/jobs_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(export_file, index=False)

# Commit to GitHub
# (Use GitHub Actions or manual git commit)
```

### GitHub Actions Workflow
```yaml
# .github/workflows/sync-data.yml
name: Sync Job Data to Hugging Face

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Download from Databricks
        run: |
          # Databricks API call to export data
          curl -H "Authorization: Bearer ${{ secrets.DATABRICKS_TOKEN }}" \
               "${{ secrets.DATABRICKS_HOST }}/api/2.0/dbfs/read?path=/exports/jobs.csv" \
               -o data/jobs.csv

      - name: Commit to repo
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data/jobs.csv
          git commit -m "Update job data $(date)"
          git push
```

---

## Limitations of FREE Tier

### What Works:
✅ Inference on pre-trained models
✅ Small-scale data (< 100 MB)
✅ Basic web interface
✅ Resume parsing
✅ Vector similarity search

### What Doesn't Work:
❌ Real-time database access
❌ Large-scale training
❌ High-traffic loads
❌ Persistent storage (resets after 48h sleep)
❌ Background jobs

---

## Migration Path to Production

**When to migrate:**
- > 1,000 users
- Need real-time data
- Require 99.9% uptime

**Migration Target:** Google Kubernetes Engine (GKE)

**Estimated Cost:**
```
Small:  $95/month  (2 nodes, n1-standard-1)
Medium: $300/month (3 nodes, n1-standard-2)
Large:  $600/month (5 nodes, n1-standard-2)
```

**Migration Steps:**
1. Containerize application → Docker
2. Deploy to GKE → Kubernetes manifests
3. Connect to Databricks → Direct SQL/API access
4. Set up monitoring → Prometheus + Grafana
5. Configure CI/CD → GitHub Actions → GKE

---

## Testing Locally

```bash
# 1. Clone repo
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit
streamlit run app.py

# 4. Open browser
# http://localhost:8501
```

---

## Monitoring

**Hugging Face Spaces Dashboard:**
- View app logs
- Monitor CPU/RAM usage
- Track user visits (basic analytics)

**Custom Analytics:**
```python
# In app.py
import os

# Log user interactions to file
def log_interaction(veteran_name, num_matches):
    with open('logs/interactions.txt', 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp},{veteran_name},{num_matches}\n")
```

---

**Created:** August 10, 2026
**Author:** William Free Hall <whall4.wh@gmail.com>
**Organization:** 7 Eagle Group
