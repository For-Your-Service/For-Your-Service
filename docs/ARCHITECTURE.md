# Architecture Overview - For Your Service
## AI-Powered Veteran Job Matching Platform

**Organization:** 7 Eagle Group  
**Developer:** Free Hall <whall4.wh@gmail.com>  
**Mission:** Connect veterans with meaningful employment through AI-powered job matching

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Component Breakdown](#component-breakdown)
3. [Data Flow](#data-flow)
4. [Cost Analysis](#cost-analysis)
5. [Deployment Strategy](#deployment-strategy)
6. [Technology Stack](#technology-stack)

---

## System Architecture

### High-Level Design

The For Your Service platform uses a **three-tier architecture** optimized for cost-effectiveness while maintaining enterprise-grade capabilities:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  Base44 Frontend (logic-form-folio.base44.app)                 │
│  • Veteran intake forms                                          │
│  • Job search interface                                          │
│  • Match results dashboard                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS REST API
                         │ (JSON)
┌────────────────────────▼────────────────────────────────────────┐
│                      API LAYER                                   │
│  Hugging Face Spaces (Docker - FREE Tier)                      │
│  • FastAPI Backend (app.py)                                     │
│  • Request routing and validation                               │
│  • CORS handling                                                │
│  • Endpoint: POST /api/v1/veteran/register                     │
│  • Endpoint: POST /api/v1/match                                │
│  • Endpoint: GET /api/v1/jobs                                  │
│  Cost: $0/month                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │ Databricks SQL Connector
                         │ (Python SDK)
┌────────────────────────▼────────────────────────────────────────┐
│                   DATA & COMPUTE LAYER                          │
│  Databricks Lakehouse Platform                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Unity Catalog (Data Storage)                              │ │
│  │ • workspace.fys_silver.veteran_profiles                   │ │
│  │ • workspace.fys_bronze.job_postings                       │ │
│  │ • Delta Lake format (ACID transactions)                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Serverless SQL Warehouse (Compute)                        │ │
│  │ • Query execution                                         │ │
│  │ • Neural network inference                                │ │
│  │ • Auto-scaling (scale to zero when idle)                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│  Cost: ~$5-10/month (usage-based)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend Layer - Base44

**Technology:** No-code form builder (Base44)  
**Responsibility:** User interface and experience  
**Endpoints:** Hosted at `logic-form-folio.base44.app`

**Features:**
* Veteran intake form (personal info, skills, experience)
* Job search and filtering interface
* Match results visualization
* Responsive design (mobile + desktop)

**Communication:** Makes HTTPS POST/GET requests to Hugging Face API backend

---

### 2. API Layer - Hugging Face Spaces

**Technology:** FastAPI + Docker (Python 3.11)  
**Deployment:** Hugging Face Spaces (FREE tier - CPU basic)  
**Source Code:** [`huggingface/app.py`](../huggingface/app.py)

#### Why Hugging Face Spaces?

Hugging Face Spaces replaces traditional cloud compute (GCP Compute Engine, AWS EC2, Azure VMs) with a **FREE managed hosting solution**:

| Traditional Approach | Hugging Face Spaces |
|---------------------|---------------------|
| GCP GKE: $95-600/month | **$0/month** |
| Manual Kubernetes management | Managed Docker hosting |
| Complex CI/CD pipelines | Git push to deploy |
| Load balancer costs | Built-in HTTPS endpoint |

**Key Insight:** Hugging Face Spaces is **NOT a data storage solution** - it's purely an API hosting platform. It runs your Python FastAPI server and proxies requests to Databricks where the actual data lives and processing happens.

#### API Responsibilities

* **Request Validation:** Pydantic models ensure data integrity
* **Authentication Proxy:** Manages Databricks SQL connection with credentials stored as HF Secrets
* **Routing:** Maps HTTP endpoints to Databricks queries
* **CORS Handling:** Allows Base44 frontend cross-origin requests

#### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service info and health status |
| `/health` | GET | Health check (database connectivity) |
| `/api/v1/veteran/register` | POST | Register new veteran profile |
| `/api/v1/veteran/{id}` | GET | Retrieve veteran profile |
| `/api/v1/match` | POST | Get AI-powered job matches |
| `/api/v1/jobs` | GET | Search job postings |

---

### 3. Data & Compute Layer - Databricks

**Technology:** Databricks Lakehouse + Unity Catalog  
**Deployment:** AWS US-East-2 (Serverless)  
**Workspace:** `dbc-3e95d032-684c.cloud.databricks.com`

#### Why Databricks?

Databricks provides **both storage and compute** in a unified lakehouse platform:

**Storage (Unity Catalog):**
* Delta Lake tables with ACID guarantees
* Schema enforcement and evolution
* Built-in data versioning (time travel)
* Governed metadata layer

**Compute (Serverless SQL Warehouse):**
* Auto-scaling compute (scales to zero when idle)
* No cluster management required
* Pay only for query execution time
* Sub-second cold start

#### Data Architecture

**Bronze Layer (Raw Data):**
```sql
workspace.fys_bronze.job_postings
- Source: Indeed, USAJobs, Adzuna scrapers
- Format: Semi-structured JSON
- Update: Daily scraping jobs
- Records: 90+ Houston, TX jobs (growing)
```

**Silver Layer (Curated Data):**
```sql
workspace.fys_silver.veteran_profiles
- Source: Base44 frontend intake forms
- Format: Structured relational
- Schema: 13 columns (skills, experience, salary, location)
- Security: PII tags applied
```

#### Neural Network Matching Engine

**Algorithm:** Siamese Twin Tower Architecture  
**Implementation:** [`notebooks/06_Enhanced_Job_Matching_Engine.py`](../notebooks/06_Enhanced_Job_Matching_Engine.py)

**Pipeline:**
1. **Vectorization:** Transform veteran resume + job descriptions → 384-dim embeddings
2. **Similarity Scoring:** Cosine similarity between veteran/job vectors
3. **Gap Analysis:** Identify missing skills/keywords
4. **Probability Lift:** Simulate resume improvements and show before/after match scores

**Current Status:** Rule-based placeholder in API (neural network integration pending)

---

## Data Flow

### Veteran Registration Flow

```
1. Veteran fills out Base44 intake form
   ↓
2. Frontend POSTs JSON to /api/v1/veteran/register
   ↓
3. Hugging Face API validates data (Pydantic models)
   ↓
4. API generates UUID veteran_id
   ↓
5. API executes INSERT query via Databricks SQL Connector
   ↓
6. Data written to workspace.fys_silver.veteran_profiles
   ↓
7. API returns veteran_id to frontend
```

### Job Matching Flow

```
1. Frontend requests matches: POST /api/v1/match
   Body: {veteran_id, top_n: 10, location_filter: "Houston"}
   ↓
2. API retrieves veteran profile from Unity Catalog
   ↓
3. API queries job_postings with location filter
   ↓
4. [PLACEHOLDER] Rule-based matching (returns top N jobs)
   [TODO] Neural network inference on Databricks
   ↓
5. API returns ranked matches with scores
   Body: {total_matches, matches: [{job_id, title, company, match_score, ...}]}
   ↓
6. Frontend displays results in dashboard
```

---

## Cost Analysis

### Total Cost of Ownership (TCO)

Following 7 Eagle Group's mission to provide cost-effective veteran services, the architecture is optimized for **minimal operational costs**:

| Component | Service | Cost |
|-----------|---------|------|
| **Frontend** | Base44 (No-code) | $0/month (free tier) |
| **API Hosting** | Hugging Face Spaces | **$0/month (FREE tier)** |
| **Data Storage** | Databricks Unity Catalog | ~$2-3/month (Delta storage) |
| **Compute** | Databricks Serverless SQL | ~$3-7/month (query execution) |
| **Total** | | **~$5-10/month** |

### Cost Comparison

| Architecture | Monthly Cost | Annual Cost |
|--------------|--------------|-------------|
| **Current (HF + Databricks)** | **$5-10** | **$60-120** |
| GCP GKE + Cloud SQL | $95-200 | $1,140-2,400 |
| AWS ECS + RDS | $120-250 | $1,440-3,000 |
| Azure AKS + PostgreSQL | $150-300 | $1,800-3,600 |

**Savings:** 95-98% cost reduction vs. traditional cloud deployments

### Why This Is Sustainable

1. **Serverless Databricks:** Compute scales to zero when idle (no overnight/weekend costs)
2. **FREE API Hosting:** Hugging Face Spaces provides unlimited CPU basic tier
3. **Low Data Volume:** <100GB of job/veteran data = minimal storage costs
4. **Pay-per-query:** Only charged for actual SQL execution time

---

## Deployment Strategy

### Development → Production Pipeline

**Phase 1: Development (Current)**
* Manual deployment to Hugging Face Spaces
* Test environment: HF Space with Databricks dev workspace
* No CI/CD pipeline (single developer)

**Phase 2: Production (Next)**
* Automated deployment: Git push to HF Space (auto-rebuild)
* Monitoring: HF Space logs + Databricks query history
* Secrets management: HF Space environment variables

**Phase 3: Scale (Future)**
* Multi-region job scraping (expand beyond Houston)
* Production-grade monitoring (alerts, uptime tracking)
* A/B testing for matching algorithm improvements

### Deployment Files

```
For-Your-Service/
├── huggingface/
│   ├── Dockerfile               # Python 3.11-slim container
│   ├── app.py                   # FastAPI backend (262 lines)
│   ├── requirements.txt         # 5 dependencies
│   └── README.md                # Deployment instructions
├── setup/
│   ├── 01_Unity_Catalog_Setup.py      # Automated table creation
│   ├── 02_Generate_Databricks_Token.md # Token generation guide
│   └── 03_Test_API.py                 # API test suite (6 tests)
└── notebooks/
    ├── 06_Enhanced_Job_Matching_Engine.py  # Neural network matching
    └── 08_Base44_API_Backend.py            # API development notebook
```

---

## Technology Stack

### Frontend
* **Framework:** Base44 (No-code form builder)
* **Styling:** Built-in responsive templates
* **Hosting:** Base44 managed hosting

### API Layer
* **Language:** Python 3.11
* **Framework:** FastAPI 0.104.1
* **Validation:** Pydantic 2.5.0
* **Database Client:** databricks-sql-connector 3.0.0
* **Server:** Uvicorn (ASGI)
* **Container:** Docker (Python 3.11-slim base image)
* **Hosting:** Hugging Face Spaces (FREE tier)

### Data Layer
* **Platform:** Databricks Lakehouse
* **Catalog:** Unity Catalog (multi-catalog namespace)
* **Storage Format:** Delta Lake (open-source)
* **Compute:** Serverless SQL Warehouse
* **Orchestration:** Databricks Jobs (scheduled scrapers)

### Machine Learning
* **Algorithm:** Siamese Twin Tower Neural Network
* **Framework:** PySpark ML + pandas
* **Embeddings:** 384-dimensional semantic vectors
* **Similarity Metric:** Cosine similarity

---

## Security & Compliance

### Data Protection

**PII Handling:**
* Veteran profiles contain PII (name, email, location)
* Unity Catalog tags applied: `pii=true`
* Access control via Databricks permissions

**Authentication:**
* Databricks Personal Access Token (90-day rotation)
* Stored as Hugging Face Space secret (not in code)
* Token never committed to Git

**Network Security:**
* HTTPS only (HF Spaces + Databricks)
* CORS restricted to Base44 frontend domain
* No public database access (API proxy layer)

---

## Future Enhancements

### Short-term (Q3 2026)
1. **Integrate Neural Network:** Replace rule-based matching with Siamese model
2. **Expand Job Sources:** Scrape LinkedIn, Dice, ClearanceJobs
3. **Add Resume Optimization UI:** Show veterans how to improve match scores

### Medium-term (Q4 2026)
4. **Multi-city Support:** Expand beyond Houston to Greenville, SC and nationwide
5. **Authentication:** Add veteran login and saved searches
6. **Email Notifications:** Weekly job match updates

### Long-term (2027)
7. **Mobile App:** Native iOS/Android with push notifications
8. **Employer Portal:** Allow companies to post jobs directly
9. **Success Metrics:** Track placements and veteran outcomes

---

## Developer Information

**Primary Developer:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group  
**GitHub:** https://github.com/For-Your-Service/For-Your-Service  
**Architecture Document Version:** 1.0  
**Last Updated:** 2026-08-09

---

## Questions or Issues?

For questions about this architecture or deployment, please:
1. Review the [Deployment Status](../DEPLOYMENT_STATUS.md)
2. Check the [Setup Documentation](../setup/)
3. Open an issue on GitHub
4. Contact: whall4.wh@gmail.com

---

**Built with ❤️ for veterans by 7 Eagle Group**
