# 🎖️ Streamlit Veteran Portal Guide & Deployment Notes
## For Your Service — 7 Eagle Group
**Lead Architect & Developer:** Free Hall (Cloud Engineer • DevOps Analyst • Data Architect | 18Z / 18F, US Army Special Forces, Ret.)
**Repository:** [https://github.com/For-Your-Service/For-Your-Service](https://github.com/For-Your-Service/For-Your-Service)

---

## 📋 Overview

The **For Your Service** frontend is built with **Streamlit** to provide a fast, patriotic, accessible, and 100% free web portal for transitioning military veterans, active duty personnel, and military spouses.

The portal eliminates the friction of traditional job boards by automatically translating military service, rank, and MOS codes into high-value civilian skills and matching service members with verified opportunities.

---

## 🏗️ Architecture & Component Layout

```
app/
├── __init__.py         # Package initialization
├── app.py              # Main Streamlit patriotic web application
├── app.yaml            # Databricks App serverless configuration
├── mos_data.py         # Military MOS / AFSC / Rating database & crosswalk engine
├── sample_data.py      # Zero-cost local fallback dataset & multi-branch demo profiles
├── requirements.txt    # Application dependencies
└── README.md          # App-specific documentation
```

### Key Frontend Features:

1. **Universal Service Member Intake**:
   - **All 6 Branches:** U.S. Army, U.S. Navy, U.S. Air Force, U.S. Marine Corps, U.S. Coast Guard, U.S. Space Force.
   - **Dynamic Branch Ranks:** Selecting a branch dynamically populates the exact ranks for that service (Enlisted E-1..E-9, Warrant Officers W-1..W-5, Officers O-1..O-10).
   - **Security Clearance Selector:** None, Public Trust, Confidential, Secret, Top Secret, TS/SCI, and Polygraph levels.

2. **Resume & Service Record Parsing (100% Free & Local)**:
   - Supports file uploads in **PDF** (`pypdf`), **Word** (`python-docx`), and **Text** (`.txt`).
   - Zero third-party paid API dependencies for parsing.
   - Real-time extraction of technical tools, trade skills, and military leadership competencies.

3. **MOS / AFSC / Rating Crosswalk Engine** (`app/mos_data.py`):
   - Real-time translation of military occupational specialties into civilian job titles, transferable strengths, and compensation tiers.
   - Dedicated **MOS Career Crosswalk Explorer** tab to search and browse military specialties.

4. **Patriotic Military UI Theme**:
   - Styled with Deep Navy (`#0B2545`), Crimson Red (`#C81D25`), and Military Gold (`#D4AF37`).
   - High-contrast, mobile-friendly cards with visual match score gauges (% Fit).
   - "Why You Match" breakdown explaining how military experience fits the civilian role.
   - 1-click **"🦅 Request 7 Eagle Recruiter Intro"** action button.

5. **Dual Execution Engine (Zero-Cost & Cloud-Scale)**:
   - **Local / Free Tier Mode:** Runs offline using cached scraped jobs and embedded datasets without requiring paid cloud infrastructure.
   - **Databricks Unity Catalog Mode:** Automatically logs veteran profiles to `workspace.fys_silver.veteran_profiles` and queries `workspace.fys_bronze.job_postings` when deployed in Databricks.

---

## 🚀 How to Run & Test Locally

### 1. Install Dependencies
```bash
# From repository root
pip install -r app/requirements.txt
```

### 2. Launch the Streamlit Server
```bash
streamlit run app/app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

### 3. Fast 1-Click Demo Profiles
Use the sidebar buttons to test diverse military backgrounds instantly:
- 🪖 **Army 18F Special Forces Lead** (Cloud Architect / Intelligence)
- 🪖 **Army 11B Infantry Squad Leader** (Operations / Security)
- 🪖 **Army 88M Motor Transport Operator** (Fleet Logistics / CDL)
- ⚓ **Navy IT Specialist** (Systems & Network Administrator)

---

## 🌐 Free Cloud Deployment Options

### Option 1: Streamlit Community Cloud (Recommended — 100% Free 24/7)
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
2. Click **"New app"**.
3. Configure:
   - **Repository:** `For-Your-Service/For-Your-Service`
   - **Branch:** `main`
   - **Main file path:** `app/app.py`
   - **App URL:** `fys-veterans` (creates `https://fys-veterans.streamlit.app`)
4. Click **"Deploy"**.
5. **Continuous Deployment:** Every `git push` to `main` automatically updates the live site.

### Option 2: Databricks Apps (For 7 Eagle Group Workspace)
1. In Databricks workspace, navigate to **Compute** → **Apps** → **Create App**.
2. Set Name: `fys-veteran-intake`.
3. Set Source: `app/`.
4. Deploy using serverless compute.

### Option 3: Hugging Face Spaces (100% Free CPU Tier)
1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)** → **Create new Space**.
2. Select **Streamlit** SDK (Free CPU tier).
3. Connect repository or upload `app/` files.

---

## 🧪 Automated Testing

The Streamlit portal components are verified with automated unit tests:

```bash
pytest tests/test_veteran_app.py -v
```

**Verified Test Cases:**
- `test_all_branches_have_ranks` — Confirms dynamic rank structure for all 6 military branches.
- `test_mos_lookup_across_branches` — Tests crosswalk lookups for Combat, Logistics, Cyber, Intel, and Maritime specialties.
- `test_mos_choices_filtering` — Validates branch-specific specialty filtering.
- `test_parse_veteran_skills_diverse` — Verifies skill extraction across technical, combat, and transportation resumes.
- `test_calculate_veteran_match_score_all_profiles` — Tests scoring algorithm and "Why You Match" generation.
- `test_load_cached_jobs_diversity` — Confirms fallback job dataset covers diverse industry sectors.
