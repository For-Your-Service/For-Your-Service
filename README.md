# For Your Service 🇺🇸

AI-powered veteran job matching platform using neural networks.

## The Mission

The military gives you elite operational experience. Civilian tech applications don't always know how to read it. Raw service records, MOS codes, and leadership tours sit in static PDFs rather than working for you. **For Your Service** learns the patterns in your background, maps your service profile against live industry demand, and surfaces what matters: targeted role matching, resume translation, and automated transition insights.

**Partner:** 7 Eagle Group  
**Lead Architect & Developer:** Free Hall (Cloud Engineer • DevOps Analyst • Data Architect | 18Z / 18F, US Army Special Forces, Ret.)

---

## What For Your Service Does

| Without For Your Service | With For Your Service |
| :--- | :--- |
| Translating your military experience into resume bullet points is manual and frustrating | Automated MOS/AFSC-to-industry role mapping and tensor matching |
| Federal and defense job boards are scattered and hard to track | Live integrated USAJOBS and defense contractor feed ingestion |
| Finding the right technical team or mentor is a guessing game | Data-driven introductions based on peer transition paths |
| Tracking your application pipeline is messy | Unified pipeline tracking through Databricks and a local dashboard |

---

## 🎯 Key Features

- **Streamlit Web Interface:** Production-ready veteran intake portal with real-time job matching across all 6 military branches.
- **Live Impact & Visitor Analytics:** Real-time 4-card metric tracker showing active service members connected and AI matches run.
- **Multi-Source Ingestion:** Aggregates jobs from USAJOBS, JSearch, and Adzuna APIs with sanitized card presentation.
- **Semantic Matching:** Uses sentence-transformers (`all-MiniLM-L6-v2`) for neural embedding-based matching.
- **AI Resume Parsing:** 100% free, local resume parsing (`pypdf`, `python-docx`) extracting technical, combat, and leadership competencies.
- **MOS Crosswalk:** Maps military specialties (Army MOS, Navy Ratings, Air Force AFSC) to civilian career tracks.
- **Regional Focus:** Greenville-Anderson MSA (expandable across national defense corridors).
- **Serverless Cloud Deployment:** Hosted on **Databricks Apps** (`fys-matching-app`) and **Hugging Face Spaces**.

---

## 🚀 Quick Start & Hosting Options

### 1. Clone & Setup (Local Development)
```bash
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service
python3.12 -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -e "."
pip install -r app/requirements.txt
```

### 2. Launch the Streamlit Portal
```bash
streamlit run app/app.py
```
Open **`http://localhost:8501`** (or `http://192.168.50.203:8501` for LAN) in your browser.

---

### 3. Enterprise Cloud Host: Databricks Apps (Serverless)
The production veteran intake portal is deployed serverless on Databricks Apps:
* **Live App URL:** [https://fys-matching-app-7474643734871839.aws.databricksapps.com](https://fys-matching-app-7474643734871839.aws.databricksapps.com)
* **Databricks Workspace:** `https://dbc-3e95d032-684c.cloud.databricks.com`
* **Configuration:** [`app/app.yaml`](app/app.yaml)
* **Automated Deployer:** Run `python scripts/deploy_databricks_app.py`

---

### 4. Deploy 24/7 to Streamlit Community Cloud (100% Free)
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
2. Click **"New app"**.
3. Select `For-Your-Service/For-Your-Service`, branch `main`, and main file path `app/app.py`.
4. Click **"Deploy"** to get a permanent public link (e.g. `https://fys-veterans.streamlit.app`).

See [docs/STREAMLIT_GUIDE.md](docs/STREAMLIT_GUIDE.md) and [app/README.md](app/README.md) for full portal documentation.

---

### 5. Deploy to Hugging Face Spaces (Free CPU Tier)
1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)** → Create new Space (Docker SDK).
2. Uses [`huggingface/Dockerfile`](huggingface/Dockerfile) and [`huggingface/app.py`](huggingface/app.py) (FastAPI backend on port 7860).

---

### 6. Set Up Data Ingestion & API Keys (Databricks / Cloud)
Follow [docs/API_QUICKSTART.md](docs/API_QUICKSTART.md) to register for:
- USAJOBS API
- JSearch (RapidAPI)
- Adzuna API

Configure encrypted secret scopes via:
```bash
./scripts/setup_databricks_secrets.sh
```

---

## 📊 Architecture

```
[Job APIs / USAJOBS] ───► [Bronze Table] ───► [Silver Enrichment] ───► [Gold Embeddings] ───► [Neural Matching]
                                                                                                    │
                                                                                                    ▼
                                                                                   [Streamlit Portal & Databricks Apps]
```

- **Bronze:** Raw job data from USAJOBS, JSearch, and Adzuna APIs
- **Silver:** O*NET skills + MOS crosswalk (`workspace.fys_silver.veteran_profiles`)
- **Gold:** 384-dim semantic embeddings (`workspace.fys_gold.job_embeddings`)
- **Matching:** Siamese twin tower network + sentence-transformers

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

---

## 📁 Project Structure

```
For-Your-Service/
├── app/                # Streamlit Web Application & Databricks App spec
│   ├── app.py          # Main portal application
│   ├── app.yaml        # Databricks App proxy & environment configuration
│   ├── mos_data.py     # Universal military MOS / Rating / AFSC crosswalk
│   ├── sample_data.py  # Zero-cost local cached datasets & demo profiles
│   └── requirements.txt# Streamlit app dependencies
├── data/               # Analytics & live job cache
│   ├── analytics/      # Live visitor & usage metrics tracking
│   └── jobs_cache/     # Sanitized federal & defense job cache
├── notebooks/          # Databricks notebooks
├── docs/               # Comprehensive documentation & daily notes
├── scripts/            # Deployment and utility automation scripts
├── tests/              # Full unit & integration test suite (126 tests)
├── config/             # Deployment configurations & schemas
├── terraform/          # Multi-cloud IaC (AWS, GCP, Databricks, Hugging Face)
└── huggingface/        # Hugging Face Spaces deployment
```

---

## 🔧 Technology Stack

- **Frontend & App:** Streamlit (1.62+), Uvicorn, FastAPI
- **Data Platform:** Databricks (Unity Catalog `workspace.fys_*` + Serverless Compute)
- **Hosting:** Databricks Apps (`fys-matching-app`), Hugging Face Spaces, Streamlit Community Cloud
- **Job Feeds:** USAJOBS API, JSearch, Adzuna
- **ML / AI:** sentence-transformers (`all-MiniLM-L6-v2`), PyTorch
- **Testing:** pytest (126 passed tests)

---

## 💰 Cost Breakdown

| Component | Monthly Cost |
|-----------|--------------|
| API Keys (3 sources) | $0 (FREE tiers) |
| Databricks Serverless Apps | $5-10 |
| Unity Catalog Storage | $0.50 |
| Hugging Face Spaces | $0 (FREE tier) |
| **Total** | **$7-12/month** |

Cost per veteran matched: **$0.14-0.24**

---

## 📚 Documentation

- [Daily Notes August 20, 2026](DAILY_NOTES_2026_08_20.md) - Databricks Apps hosting, live metrics & USAJOBS ingestion
- [Daily Notes August 13, 2026](DAILY_NOTES_2026_08_13.md) - AWS IAM security architecture & Terraform IaC
- [Streamlit Portal Guide](docs/STREAMLIT_GUIDE.md) - Comprehensive portal guide & rank crosswalks
- [API Quickstart](docs/API_QUICKSTART.md) - 15-minute setup
- [Multi-Cloud Terraform Guide](terraform/README.md) - Automated IaC across AWS, GCP, Databricks & HF
- [Terraform Architecture Whitepaper](docs/TERRAFORM_ARCHITECTURE.md) - Multi-cloud blueprint
- [Zero-Downtime Migration Guide](docs/ZERO_DOWNTIME_MIGRATION.md) - Non-destructive adoption runbook
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📧 Contact

**Free Hall**  
Email: whall4.wh@gmail.com  
Organization: 7 Eagle Group  
GitHub: https://github.com/For-Your-Service

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 📋 Changelog

### August 20, 2026
* **Databricks Apps Serverless Deployment:** Deployed `fys-matching-app` on Databricks Apps with proxy routing and `$DATABRICKS_APP_PORT` support.
* **Live Visitor & Impact Metrics Bar:** Integrated atomic 4-card live counter for visitors, matches run, and 7 Eagle recruiter intros.
* **USAJOBS Search Ingestor & Sanitizer:** Added production federal search ingestion with official application referral routing.
* **Security & Secret Scope:** Created automated Databricks KMS Secret Scope manager script.
* **Live Job Cache Update:** Updated sanitized listings for aerospace, defense, and cyber roles.

### August 18, 2026
* **Code Quality & CI/CD:** Consolidated codebase (-2,610 net lines), resolved unit test failures across 126 test cases.
* **ADR-001 Canonical Catalog Spine:** Standardized on `workspace.fys_*` Unity Catalog tables.

---

Built with ❤️ by veterans, for veterans.
