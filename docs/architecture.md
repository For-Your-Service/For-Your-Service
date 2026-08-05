# For Your Service - Architecture

## System Components

### 1. Counselor Intake
- **Interface:** Wizard-based web form
- **Data:** Veteran profile (15 sections)
- **Output:** JSON payload
- **Partner:** 7 Eagle Group counselor network

### 2. GCP Ingestion Layer
- **Component:** Cloud Function (Gen2)
- **Function:** PII anonymization + schema validation
- **Storage:** GCS bucket (gs://fys-veteran-intake-raw)
- **Lifecycle:** 30-day retention (raw data)

### 3. Databricks Bronze Layer
- **Table:** main.fys_bronze.veteran_profiles
- **Format:** Delta Lake
- **Ingestion:** Auto Loader (incremental)
- **Schema:** JSON with nested structs

### 4. Databricks Silver Layer
- **Table:** main.fys_silver.veteran_features
- **Transformations:**
  - MOS code → civilian skill mapping
  - Certification standardization
  - Feature vector creation
  - Location normalization

### 5. Databricks Gold Layer
- **Table:** main.fys_gold.job_matches
- **Engine:** Tensor computations (PySpark MLlib)
- **Algorithm:** Multi-dimensional vector dot products
- **Output:** Placement probability matrix

### 6. Output Layer
- **Dashboard:** Counselor action dashboard
- **Reports:** Ranked job match lists
- **Analytics:** Skill gap identifiers

---

## Data Privacy Architecture

### PII Removal Strategy

**Removed at Ingestion:**
- Full name → Anonymous veteran_id (VET_<hash>)
- Email → SHA-256 hash (deduplication only)
- Phone → Deleted
- Date of birth → Birth year only
- SSN → Deleted
- Street address → Deleted
- Full ZIP → ZIP3 (first 3 digits)

**Retained Data:**
- Military service (MOS, rank, branch, years, deployments)
- Security clearance (type, active status)
- Skills (technical, soft, languages, tools)
- Education (degrees, fields, institutions, years)
- Certifications (names, issuers, dates)
- Job preferences (roles, industries, locations, salary)
- Transition info (counselor, urgency, notes)

### Security Measures
1. No PII stored in Databricks
2. Anonymous veteran_id for all tracking
3. GCS bucket with IAM restrictions
4. Cloud Function enforces schema validation
5. 30-day data retention on raw intake

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|----------|
| Intake API | GCP Cloud Functions Gen2 | Serverless HTTP endpoint |
| Data Lake | Google Cloud Storage | Raw JSON storage |
| Processing | Databricks (PySpark) | ETL and ML pipelines |
| Storage | Delta Lake (Unity Catalog) | ACID transactions, time travel |
| ML Engine | PySpark MLlib | Vector computations |
| Orchestration | Databricks Workflows | Pipeline scheduling |

---

## Integration Points

### 7 Eagle Group Integration
- Counselor intake wizard submits to Cloud Function
- Counselor dashboard reads from Gold layer
- Action items and notifications via API

### Job Posting Sources (Future)
- Indeed API
- LinkedIn Jobs API
- USAJobs (federal positions)
- Defense contractor job boards
- Direct employer feeds

---

## Deployment Architecture

### GCP Project: uap-scraper-lab-2026
- Region: us-central1
- Cloud Function: veteran-intake-processor
- GCS Bucket: fys-veteran-intake-raw

### Databricks Workspace
- Catalog: main
- Schemas: fys_bronze, fys_silver, fys_gold
- Compute: Serverless (no dedicated cluster required)

---

## Scalability

- **Ingestion:** Cloud Functions auto-scale (0-1000 instances)
- **Storage:** GCS (unlimited)
- **Processing:** Databricks serverless (auto-scaling)
- **Concurrency:** Event-driven (parallel intake processing)

---

## Future Enhancements

1. **Real-time matching:** Streaming pipeline for instant job matches
2. **Mobile intake:** Native iOS/Android apps
3. **AI recommendations:** LLM-powered career guidance
4. **Skill gap training:** Integration with online learning platforms
5. **Veteran dashboard:** Self-service portal for veterans
