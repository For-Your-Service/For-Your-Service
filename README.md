# For Your Service 🇺🇸

AI-powered veteran job matching platform using neural networks.

## Mission

Help veterans transition from military to civilian careers by matching their unique skills and experience with the right opportunities.

**Partner:** 7 Eagle Group  
**Developer:** Free Hall (18Z, US Army Special Forces, Ret.)

---

## 🎯 What It Does

- **Multi-Source Ingestion:** Aggregates jobs from USAJOBS, JSearch, and Adzuna APIs
- **Semantic Matching:** Uses sentence-transformers for neural embedding-based matching
- **MOS Crosswalk:** Maps military specialties to civilian job titles
- **Regional Focus:** Greenville-Anderson MSA (expandable)
- **FREE Deployment:** $7-12/month on Databricks + Hugging Face Spaces

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service
```

### 2. Set Up API Keys
Follow [docs/API_QUICKSTART.md](docs/API_QUICKSTART.md) to register for:
- USAJOBS API
- JSearch (RapidAPI)
- Adzuna API

### 3. Configure AWS Infrastructure (Optional)
For production deployment with S3 and DynamoDB:
- See [docs/aws/AWS_IAM_SECURITY_SETUP.md](docs/aws/AWS_IAM_SECURITY_SETUP.md)
- Or use Quick Setup: Open `AWS_Quick_Setup` notebook in Databricks
- Test connection: `scripts/aws/test_aws_connection.py`

### 4. Configure Databricks Secrets
```bash
./scripts/setup_databricks_secrets.sh
```

### 5. Run Ingestion Pipeline
Open `notebooks/03b_Multi_Source_Job_Ingestion` in Databricks

### 5. Test API
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
