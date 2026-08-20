# For Your Service 🇺🇸

AI-powered veteran job matching platform using neural networks.

## Mission

Help veterans transition from military to civilian careers by matching their unique skills and experience with the right opportunities.

**Partner:** 7 Eagle Group  
**Lead Architect & Developer:** Free Hall (Cloud Engineer • DevOps Analyst • Data Architect | 18Z / 18F, US Army Special Forces, Ret.)

---

## 🎯 What It Does

- **Streamlit Web Interface:** Production-ready veteran intake portal with real-time job matching
- **Multi-Source Ingestion:** Aggregates jobs from USAJOBS, JSearch, and Adzuna APIs
- **Semantic Matching:** Uses sentence-transformers for neural embedding-based matching
- **AI Resume Parsing:** Automatic skill extraction and experience analysis
- **MOS Crosswalk:** Maps military specialties to civilian job titles
- **Regional Focus:** Greenville-Anderson MSA (expandable)
- **FREE Deployment:** $7-12/month on Databricks + Hugging Face Spaces

---

## 🚀 Quick Start

### 1. Run the Streamlit Veteran Portal (100% Free & Local)
The fastest way to test the platform:
```bash
# Clone and enter repo
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service

# Install app dependencies
pip install -r app/requirements.txt

# Launch the Streamlit Portal
streamlit run app/app.py
```
Open **`http://localhost:8501`** in your browser.

---

### 2. Deploy 24/7 to Streamlit Community Cloud (100% Free)
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
2. Click **"New app"**.
3. Select `For-Your-Service/For-Your-Service`, branch `main`, and main file path `app/app.py`.
4. Click **"Deploy"** to get a permanent public link (e.g. `https://fys-veterans.streamlit.app`).

See [docs/STREAMLIT_GUIDE.md](docs/STREAMLIT_GUIDE.md) and [app/README.md](app/README.md) for full portal documentation.

---

### 3. Set Up Data Ingestion & API Keys (Databricks / Cloud)
Follow [docs/API_QUICKSTART.md](docs/API_QUICKSTART.md) to register for:
- USAJOBS API
- JSearch (RapidAPI)
- Adzuna API

### 4. Configure AWS Infrastructure (Optional)
For production deployment with S3 and DynamoDB:
- See [docs/aws/AWS_IAM_SECURITY_SETUP.md](docs/aws/AWS_IAM_SECURITY_SETUP.md)
- Or use Quick Setup: Open `AWS_Quick_Setup` notebook in Databricks
- Test connection: `scripts/aws/test_aws_connection.py`

### 5. Configure Databricks Secrets
```bash
./scripts/setup_databricks_secrets.sh
```

### 6. Run Ingestion Pipeline
Open `notebooks/03b_Multi_Source_Job_Ingestion` in Databricks

### 7. Test API
```bash
python setup/03_Test_API.py
```

---

## 📊 Architecture

```
[Job APIs] → [Bronze Table] → [Silver Enrichment] → [Gold Embeddings] → [Neural Matching] → [FastAPI]
```

- **Bronze:** Raw job data from 3 sources
- **Silver:** O*NET skills + MOS crosswalk
- **Gold:** 384-dim semantic embeddings
- **Matching:** Siamese twin tower network

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

---

## 📁 Project Structure

```
For-Your-Service/
├── notebooks/          # Databricks notebooks
├── docs/              # Comprehensive documentation
├── scripts/           # Utility scripts
├── tests/             # Unit + integration tests
├── config/            # Deployment configurations
├── examples/          # Code examples
├── sql/               # Monitoring queries
└── huggingface/       # Hugging Face Spaces deployment
```

---

## 🔧 Technology Stack

- **Data Platform:** Databricks (Unity Catalog + Serverless)
- **APIs:** USAJOBS, JSearch, Adzuna
- **ML:** sentence-transformers (all-MiniLM-L6-v2)
- **Backend:** FastAPI
- **Deployment:** Hugging Face Spaces (FREE) or Kubernetes (Production)
- **Testing:** pytest

---

## 💰 Cost Breakdown

| Component | Monthly Cost |
|-----------|--------------|
| API Keys (3 sources) | $0 (FREE tiers) |
| Databricks Serverless | $5-10 |
| Unity Catalog Storage | $0.50 |
| Hugging Face Spaces | $0 (FREE tier) |
| **Total** | **$7-12/month** |

Cost per veteran matched: **$0.14-0.24**

---

## 📚 Documentation

- [API Quickstart](docs/API_QUICKSTART.md) - 15-minute setup
- [Multi-Cloud Terraform Guide](terraform/README.md) - Automated IaC across AWS, GCP, Databricks & HF
- [Terraform Architecture Whitepaper](docs/TERRAFORM_ARCHITECTURE.md) - Complete multi-cloud infrastructure blueprint
- [Zero-Downtime Migration Guide](docs/ZERO_DOWNTIME_MIGRATION.md) - Non-destructive resource adoption runbook
- [Cloud Cost Optimization in IaC](docs/CLOUD_COST_OPTIMIZATION_IAC.md) - Free tier guardrails & budget controls
- [AWS IAM Security Setup](docs/aws/AWS_IAM_SECURITY_SETUP.md) - AWS infrastructure configuration
- [Multi-Source Ingestion Spec](docs/MULTI_SOURCE_INGESTION_SPEC.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [FAQ](docs/FAQ.md)
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md)
- [Security Best Practices](docs/SECURITY_BEST_PRACTICES.md)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

### Areas for Contribution
- Additional job sources (ClearanceJobs, Dice, GitHub Jobs)
- More MOS codes → civilian crosswalks
- Regional expansion (Charlotte, Raleigh, Atlanta)
- ML model improvements
- Bug fixes and documentation

---

## 📧 Contact

**Free Hall**  
Email: whall4.wh@gmail.com  
Organization: 7 Eagle Group  
GitHub: https://github.com/For-Your-Service

---

## ⭐ Star This Repo

If this project helps you or a veteran you know, please star it!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---


## 📋 Changelog

---

* See [PRODUCTION_STATUS.md](docs/PRODUCTION_STATUS.md) for current deployment status

* See [LINEAGE.md](docs/LINEAGE.md) for complete data flow documentation
* See [ADR-001](docs/adr/ADR-001-CODE-CANONICAL-CATALOG-SPINE.md) for Unity Catalog spine details
**Related Documentation:**
* **Net Change:** -2,610 lines (improved code quality through consolidation)

* **Deletions:** 11,006 lines removed (code cleanup and refactoring)
* **Insertions:** 8,396 lines of new code and documentation
* **Files Changed:** 275 files across the codebase
#### 🔧 Technical Details

* **Option B:** Manually scrape 5-10 real jobs from Indeed/LinkedIn for immediate validation

* **Option A:** Get Adzuna API credentials (free tier: 10K requests/month)
**Recommended Actions:**
* 🔴 Data ingestion **BLOCKED** on invalid Adzuna API credentials (401 Unauthorized)

* ✅ Unity Catalog infrastructure is **READY**
**Infrastructure Status:**
#### 🔴 Production Status

* Automated dependency remediation

* Add automated CI workflows (Black, Flake8, Vulture)
* Deploy FastAPI ingestion backend with GCS integration
* Add consumer packaging documentation
* Resolve flake8 linting issues (config BOM + test suite)
* Add system architecture documentation for Hugging Face
* Fix unit test failures across matching/validation/ingestion
#### 📊 Commit Highlights

* PowerShell automation scripts for GitHub admin and issue resolution

* `pipeline_config.json` - Centralized pipeline configuration
* `resume_cheatsheet.md` - Resume parsing reference guide
* `ingest_resume.py` - Resume ingestion pipeline
**6. New Utilities**

* Legacy code migration: Moved deprecated transaction lakehouse code to `sandbox/legacy_transactions/`

* Script improvements: Enhanced error handling across API clients, data quality scripts, and production scrapers
  * Example: `notebooks/04_Job_Market_Data_Sources.py` reduced from 2,578 lines
* Massive notebook cleanup: Reduced bloat in notebooks
**5. Code Refactoring**

* `automated/vulture-dead-code-sweep` - Dead code cleanup automation

* `feature/system-architecture-docs` - Architecture documentation
* `feature/consumer-packaging-options` - Consumer distribution strategy
* `feature/add-pipeline-ingestion` - Pipeline ingestion enhancements
* `feature/huggingface-deployment` - Hugging Face Space deployment work
**4. New Feature Branches**

  * Gold: `src/databricks/gold/aggregate_fys_job_postings.py`

  * Silver: `src/databricks/silver/transform_fys_job_postings.py`
  * Bronze: `src/databricks/bronze/ingest_fys_job_postings.py`
* Established canonical pipeline paths:
* Added comprehensive deployment documentation
**3. System Architecture for Hugging Face Deployment**

* **PRODUCTION_STATUS.md:** Current state showing infrastructure ready but blocked on Adzuna API credentials

* **LINEAGE.md:** Documents data flow from APIs → Bronze → Silver → Gold → Hugging Face matching
  * Deprecated legacy namespaces (`for_your_service`, `veteran_intake`, `main.fys_*`)
    * `workspace.fys_gold.job_embeddings`
    * `workspace.fys_gold.match_results`
    * `workspace.fys_silver.veteran_profiles`
    * `workspace.fys_silver.enriched_jobs`
    * `workspace.fys_bronze.job_postings`
  * Declared official production tables:
* **ADR-001:** Established code-canonical Unity Catalog spine (`workspace.fys_*`)
**2. Production Architecture Documentation**

* Generated `flake8_errors.md` documenting 1,844 lint errors for systematic cleanup

* Resolved unit test failures across neural matching, validation, ingestion, and pipeline orchestration
* Added `dead-code-analysis.yml` - Automated detection of unused code using Vulture
* Added `flake8-linter.yml` - Automated linting for code quality
* Added `black-formatter.yml` - Automated Python code formatting workflow
**1. Code Quality & CI/CD Automation**

#### 🎯 Major Updates

**Repository Update:** 275 files changed | 8,396 insertions | 11,006 deletions

### August 18, 2026

---

Built with ❤️ by veterans, for veterans.
### Production Canonical Path
For production job pipeline logic, reference:
- `src/databricks/bronze/` -> `ingest_fys_job_postings.py`
- `src/databricks/silver/` -> `transform_fys_job_postings.py`
- `src/databricks/gold/` -> `aggregate_fys_job_postings.py`
### Production Canonical Path
- `src/databricks/bronze/` -> `ingest_fys_job_postings.py`
- `src/databricks/silver/` -> `transform_fys_job_postings.py`
- `src/databricks/gold/` -> `aggregate_fys_job_postings.py`
