# Deployment Strategy - For Your Service
## Cost-Optimized Architecture for Veteran Services

**Organization:** 7 Eagle Group  
**Developer:** Free Hall <whall4.wh@gmail.com>  
**Date:** 2026-08-09

---

## Executive Summary

The For Your Service platform uses a **hybrid deployment strategy** that separates API hosting from data processing to achieve **95%+ cost savings** compared to traditional cloud architectures.

**Key Decision:** Use Hugging Face Spaces (FREE) for API hosting, while maintaining Databricks as the data and compute layer.

---

## The Three-Component Model

### Component 1: API Hosting (Hugging Face Spaces)

**What It Does:**
* Runs the FastAPI backend server
* Handles HTTP requests from Base44 frontend
* Routes queries to Databricks
* Validates data with Pydantic models

**What It Does NOT Do:**
* ❌ Store any data
* ❌ Perform heavy computation
* ❌ Run machine learning inference
* ❌ Replace Databricks

**Cost:** $0/month (FREE tier - CPU basic)

**Why Hugging Face?**
* Provides managed Docker hosting at no cost
* Auto-deploys on git push
* Built-in HTTPS endpoint
* Replaces GCP Compute Engine ($95-600/month)

---

### Component 2: Data Storage (Databricks Unity Catalog)

**What It Does:**
* Stores veteran profiles permanently
* Stores job postings from scrapers
* Provides ACID transactions (Delta Lake)
* Enforces schema and governance

**What It Does NOT Do:**
* ❌ Run the API server
* ❌ Host the frontend

**Cost:** ~$2-3/month (storage only)

**Why Databricks?**
* Unified lakehouse for analytics + transactional data
* Built-in versioning and time travel
* Scalable from 100 rows to 1 billion rows
* No separate database costs

---

### Component 3: Compute (Databricks Serverless SQL)

**What It Does:**
* Executes SQL queries on demand
* Runs neural network matching inference
* Scales to zero when idle
* Auto-scales for query load

**What It Does NOT Do:**
* ❌ Store data (data lives in Unity Catalog)
* ❌ Run 24/7 (only when queries execute)

**Cost:** ~$3-7/month (usage-based)

**Why Serverless?**
* Pay only for execution time (no idle costs)
* Cold start < 1 second
* No cluster management overhead
* Automatically stops after 10 minutes of inactivity

---

## Architecture Decision Records

### ADR-001: Why Not GCP for Everything?

**Problem:** Need API hosting, database, and compute for veteran job matching.

**Options Considered:**

| Option | Monthly Cost | Pros | Cons |
|--------|--------------|------|------|
| **GCP GKE + Cloud SQL** | $95-200 | Full control, mature ecosystem | High cost, complex management |
| **AWS ECS + RDS** | $120-250 | AWS ecosystem | Similar costs to GCP |
| **Heroku** | $25-50 | Simple deployment | Limited free tier |
| **HF + Databricks (CHOSEN)** | **$5-10** | **95% cost savings**, leverages existing Databricks investment | Split architecture |

**Decision:** Use Hugging Face Spaces for FREE API hosting + Databricks for data/compute.

**Rationale:**
* 7 Eagle Group is a nonprofit → cost optimization critical
* Already using Databricks for data engineering
* Hugging Face provides production-grade hosting at $0
* No data lock-in (Delta Lake is open-source)

---

### ADR-002: Why Not Run Everything on Databricks?

**Problem:** Could we run the FastAPI server on Databricks too?

**Analysis:**

**Option A: Databricks Apps (All-in-One)**
* **Cost:** $10-30/month (dedicated compute for app server)
* **Pros:** Single platform, no external dependencies
* **Cons:** More expensive, overkill for simple API

**Option B: HF Spaces + Databricks (Chosen)**
* **Cost:** $5-10/month ($0 API + $5-10 Databricks queries)
* **Pros:** FREE API hosting, pay only for data queries
* **Cons:** Two platforms to manage

**Decision:** Split architecture (HF + Databricks)

**Rationale:**
* Hugging Face excels at hosting lightweight Python apps
* Databricks excels at data processing
* Let each platform do what it does best
* Total cost is lower than unified approach

---

### ADR-003: Why Not Use Databricks for Storage AND Use GCP for API?

**Problem:** Could we use GCP for API and keep Databricks for data?

**Answer:** That was the original plan, but Hugging Face is **free** vs. GCP's $95-600/month.

**Cost Breakdown:**

| Architecture | API Hosting | Data/Compute | Total |
|--------------|-------------|--------------|-------|
| **GCP + Databricks** | $95-200 | $10-20 | **$105-220/month** |
| **HF + Databricks (Chosen)** | $0 | $5-10 | **$5-10/month** |

**Savings:** $95-210/month ($1,140-2,520/year)

---

## Data Flow Clarification

### What Happens When a Veteran Registers

```
Step 1: Veteran submits form on Base44
        ↓
Step 2: Base44 sends HTTPS POST to Hugging Face API
        Request: {name, email, skills, location, salary, ...}
        ↓
Step 3: Hugging Face API validates the JSON (Pydantic)
        ↓
Step 4: API connects to Databricks SQL Warehouse
        Using: databricks-sql-connector library
        ↓
Step 5: API executes INSERT query
        INSERT INTO workspace.fys_silver.veteran_profiles VALUES (...)
        ↓
Step 6: Data is written to Unity Catalog (Delta Lake table)
        Stored in: AWS S3 (managed by Databricks)
        ↓
Step 7: API returns veteran_id to Base44
        Response: {veteran_id: "uuid-123", status: "registered"}
        ↓
Step 8: Base44 shows confirmation to veteran
```

**Where does data live at each step?**
* **Steps 1-2:** In-memory (frontend JSON)
* **Step 3:** In-memory (Hugging Face API process)
* **Step 4-5:** In-memory (SQL connection)
* **Step 6:** **Permanently stored in Unity Catalog (Delta Lake on S3)**
* **Steps 7-8:** In-memory (API response)

**Key Insight:** Hugging Face never stores data. It's just a proxy/router.

---

## Cost Optimization Strategies

### 1. Serverless Compute (Current)

**How it works:**
* SQL Warehouse spins up on first query
* Executes query in < 1 second
* Automatically stops after 10 minutes of inactivity

**Example:**
* Veteran registers at 9:00 AM → Warehouse starts, runs INSERT, stops at 9:10 AM
* No queries 9:10 AM - 5:00 PM → **No compute costs**
* Next veteran registers at 5:15 PM → Warehouse starts again

**Savings:** Pay for ~10 minutes of compute per registration batch, not 24/7.

---

### 2. Hugging Face FREE Tier (Current)

**Limits:**
* CPU basic (no GPU)
* Container sleeps after 48 hours of inactivity
* Cold start: ~30 seconds after sleep

**Optimization:**
* Accept 30-second cold start (veteran registration is not latency-sensitive)
* Most registrations will hit warm container (sleep timer resets on each request)

**Savings:** $95-200/month vs. GCP Compute Engine

---

### 3. Delta Lake Storage (Current)

**How it works:**
* Data stored in compressed Parquet files
* Only changed data written (not full table)
* Automatic data compaction

**Example:**
* 1,000 veteran profiles ≈ 5 MB compressed
* 10,000 job postings ≈ 50 MB compressed
* Total: 55 MB → **Negligible storage cost**

**Savings:** No separate database license fees ($100-500/month for PostgreSQL/MySQL on GCP)

---

## Scalability Path

### Phase 1: MVP (Current - 100 veterans, 1,000 jobs)
* **Infrastructure:** HF Spaces (FREE) + Databricks Serverless
* **Cost:** $5-10/month
* **Bottleneck:** None (over-provisioned)

### Phase 2: Growth (1,000 veterans, 10,000 jobs)
* **Infrastructure:** Same (auto-scaling handles load)
* **Cost:** $10-20/month (more query volume)
* **Bottleneck:** None

### Phase 3: Scale (10,000 veterans, 100,000 jobs)
* **Infrastructure:** Add Databricks cluster for batch matching jobs
* **Cost:** $50-100/month
* **Bottleneck:** HF Spaces (may need upgrade to paid tier or move to dedicated hosting)

### Phase 4: Enterprise (100,000+ veterans)
* **Infrastructure:** Migrate API to Databricks Apps or GCP GKE with load balancer
* **Cost:** $200-500/month
* **Bottleneck:** Database (may need partitioning and optimization)

**Key Insight:** Current architecture supports 10,000 veterans before any upgrades needed.

---

## Risk Analysis

### Risk 1: Hugging Face Space Goes Down

**Probability:** Low (HF has 99%+ uptime)  
**Impact:** High (API unavailable)  
**Mitigation:**
* Health check endpoint (monitor uptime)
* Backup deployment to Databricks Apps (can be activated in < 1 hour)
* No data loss (data lives in Databricks, not HF)

### Risk 2: Databricks Costs Spike

**Probability:** Medium (if query patterns change)  
**Impact:** Medium (could go from $10 → $50/month)  
**Mitigation:**
* Query result caching (reduce redundant queries)
* Scheduled job matching (batch instead of real-time)
* Set Databricks budget alerts

### Risk 3: Hugging Face Removes FREE Tier

**Probability:** Low (HF committed to free tier for community projects)  
**Impact:** Medium (need to migrate to paid tier or alternative)  
**Mitigation:**
* Containerized application (portable to any Docker host)
* Can deploy to Railway.app, Render.com, or Fly.io as alternatives
* Migration time: < 4 hours

---

## Deployment Checklist

### Prerequisites (Completed ✅)
- [x] Databricks workspace configured
- [x] Unity Catalog schemas created
- [x] Tables created and populated
- [x] FastAPI backend written and tested
- [x] Dockerfile created
- [x] GitHub repository set up

### Manual Steps (Pending 🔄)
- [ ] Generate Databricks Personal Access Token
- [ ] Create Hugging Face Space
- [ ] Upload deployment files (Dockerfile, app.py, requirements.txt)
- [ ] Configure HF Secrets (DATABRICKS_TOKEN, DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH)
- [ ] Test API endpoints
- [ ] Update Base44 frontend with API URL

### Post-Deployment (Future 📅)
- [ ] Set up monitoring (HF logs + Databricks query history)
- [ ] Configure budget alerts
- [ ] Document runbook for common issues
- [ ] Schedule monthly cost review

---

## Conclusion

The For Your Service platform achieves **95% cost savings** by strategically splitting API hosting (Hugging Face Spaces - FREE) from data processing (Databricks - $5-10/month).

**Key Principles:**
1. **Use FREE tiers aggressively** (Hugging Face, Base44)
2. **Pay only for what you use** (Databricks serverless)
3. **Let each platform do what it does best** (HF for APIs, Databricks for data)
4. **Maintain portability** (Docker, open-source Delta Lake)

This architecture supports **7 Eagle Group's mission** of providing cost-effective veteran services while maintaining production-grade reliability and scalability.

---

**Developer:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group  
**Document Version:** 1.0  
**Last Updated:** 2026-08-09

**Built with ❤️ for veterans**
