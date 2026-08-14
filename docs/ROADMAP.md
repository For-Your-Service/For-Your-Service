# Product Roadmap — For Your Service

**Organization:** 7 Eagle Group  
**Repo:** [For-Your-Service/For-Your-Service](https://github.com/For-Your-Service/For-Your-Service)  
**Last Updated:** 2026-08-14  
**Based on:** [epics/RESEARCH_BRIEF.md](epics/RESEARCH_BRIEF.md) · [epics/PROGRAM.md](epics/PROGRAM.md)

---

## BLUF (from research)

For Your Service is a **profile-gated, explainable veteran→civilian matching and placement campaign platform** on Databricks medallion + FastAPI — **not** another national job board.

| Build | Do not build |
|-------|----------------|
| Self-understanding + profile gate | Matching on empty / MOS-only profiles |
| O*NET MOS as **soft prior** | MOS table as sole ranker |
| Hard filters → hybrid → white-box scores | Cosine-only / placeholder embeddings |
| Campaign + Side Door + pathway tags | Listings without funnel |
| Partner SITREP (7 Eagle) | Employer-only vanity metrics |

**Full issue specs:** [epics/ISSUE_SPECS.md](epics/ISSUE_SPECS.md)  
**Capability epics:** [epics/PROGRAM.md](epics/PROGRAM.md)

---

## Architecture target

```
[Job APIs + Pathways] → Bronze → Silver (O*NET/MOS) → Gold (real embeddings)
                              ↓
[Profile + Self-Understanding] → Translation → Filters → Hybrid Match → Factor Card
                              ↓
              Campaign (ATS + Side Door) → Partner SITREP
                              ↓
         FastAPI (HF Spaces) ←→ Databricks Unity Catalog
```

See [ARCHITECTURE.md](ARCHITECTURE.md) and [DEPLOYMENT_STRATEGY.md](DEPLOYMENT_STRATEGY.md).

---

## How planning is organized

| Layer | Doc | Role |
|-------|-----|------|
| Research | [epics/RESEARCH_BRIEF.md](epics/RESEARCH_BRIEF.md) | Why / white space / non-goals |
| Program | [epics/PROGRAM.md](epics/PROGRAM.md) | 12 capability epics + dependencies |
| Issues | [epics/ISSUE_SPECS.md](epics/ISSUE_SPECS.md) | Acceptance-ready tickets |
| Roadmap | **This file** | Quarters + milestones |
| Layer specs | `SILVER_*`, `GOLD_*`, profile schema | Contracts |

---

## Milestones (research program)

| ID | Theme | Epics | Window |
|----|-------|-------|--------|
| **M0** | Truth & safety | E001 Platform, E011 Security | Immediate |
| **M1** | Know yourself | E005 Profile | Q3 2026 |
| **M2** | Real match substrate | E002 Bronze, E003 Silver, E004 Gold, E006 Match | Q3–Q4 2026 |
| **M3** | Serve & UX | E007 API, E008 UX | Q4 2026 |
| **M4** | Campaign differentiator | E009 Campaign & pathways | Q4 2026 |
| **M5** | Partner scale | E010 Partner, E012 Quality | Q4 2026–2027 |

```
M0 ──► M1 ──► M2 ──► M3 ──► M4 ──► M5
              ▲
         E003/E004 feed E006
```

---

## Q3 2026 (July – September)

### ✅ Phase 1: Foundation (Complete)
- [x] Bronze layer multi-source ingestion (initial)
- [x] Databricks Unity Catalog setup
- [x] API integrations (USAJOBS, JSearch, Adzuna)
- [x] Regional filtering (Greenville MSA)
- [x] Comprehensive documentation

### 🔧 Phase 1.5: Platform Truth & Safety (M0 — NEW from research)
- [ ] Canonical schema map — **FYS-001** (**code wins:** `workspace.fys_*` from `huggingface/app.py`)
- [ ] Declare code-canonical spine ADR — **FYS-106**
- [ ] Foundry project/folder spine — **FYS-107**
- [ ] Quarantine lakehouse/transactions path — **FYS-119**
- [ ] Wire DQ expectations — **FYS-108**
- [ ] Medallion Databricks job for job_postings — **FYS-118**
- [ ] Single production path (Databricks + HF) — **FYS-002**
- [ ] API credential status matrix — **FYS-003**
- [ ] Nested tree cleanup plan — **FYS-004**
- [ ] Ops vs analytics PII split — **FYS-100**
- [ ] Secrets-only scopes — **FYS-101** / **FYS-105**
- [ ] CORS allowlist — **FYS-102**
- Epic: [FYS-E013](https://github.com/For-Your-Service/For-Your-Service/issues/104) · Map: [epics/FOUNDRY_ONTOLOGY_MAP.md](epics/FOUNDRY_ONTOLOGY_MAP.md)

### 🔄 Phase 2: Enrichment (In Progress → M2 / E003)
- [ ] O*NET client production path — **FYS-020**
- [ ] MOS → O*NET soft prior — **FYS-021**
- [ ] Skill extraction → taxonomy — **FYS-022**
- [ ] Standardized titles + industry — **FYS-023**
- [ ] Silver transform job — **FYS-024**
- [ ] Harden bronze orchestrator + writer — **FYS-010**, **FYS-014**

### 🆕 Phase 2.5: Profile Gate (M1 / E005 — research P0)
- [ ] Self-understanding intake — **FYS-040**
- [ ] Core veteran profile — **FYS-041**
- [ ] Completeness / `ready_for_matching` — **FYS-042**
- [ ] Military → civilian translation fields — **FYS-043**
- [ ] Profile context loader — **FYS-044**
- [ ] Extend [VETERAN_PROFILE_SCHEMA.md](VETERAN_PROFILE_SCHEMA.md)

### 📅 Phase 3: ML Matching (M2 / E004 + E006)
- [ ] Replace placeholder embeddings — **FYS-030**
- [ ] Job + veteran embedding pipelines — **FYS-031**, **FYS-032**
- [ ] Hard filters before rank — **FYS-050**
- [ ] Hybrid BM25 + dense retrieval — **FYS-051**
- [ ] Multi-factor white-box scores — **FYS-052**
- [ ] Grounded explanations — **FYS-053**
- [ ] Remove hardcoded HF match scores — **FYS-054**
- [ ] MOS prior in ranker — **FYS-055**

---

## Q4 2026 (October – December)

### Phase 4: API & Deployment (M3 / E007)
- [ ] Veteran profile API — **FYS-060**
- [ ] Match API with profile gate — **FYS-061**
- [ ] Jobs query API — **FYS-062**
- [ ] Health + readiness — **FYS-063**
- [ ] Rate limiting & caching — **FYS-064**
- [ ] Hugging Face Spaces production deploy
- [ ] AuthN for write APIs — **FYS-103**

### Phase 5: User Experience (M3 / E008)
- [ ] Profile creation wizard — **FYS-070**
- [ ] Recommendation dashboard — **FYS-071**
- [ ] Match explanation UI — **FYS-072**
- [ ] Accessibility pass — **FYS-074**
- [ ] Email notifications — **FYS-073** (P2)

### Phase 5.5: Campaign & Pathways (M4 / E009 — research white space)
- [ ] Bidirectional Go/No-Go (fit weights) — **FYS-080**
- [ ] Campaign entity + funnel — **FYS-081**
- [ ] Side Door warm outreach — **FYS-082**
- [ ] SkillBridge / CSP tags + ETS clocks — **FYS-083**
- [ ] Federal / USAJOBS preference path — **FYS-084**
- [ ] HoH / fellowship tags — **FYS-085**

---

## 2027

### Phase 6: Partner Scale (M5 / E010)
- [ ] Partner org object — **FYS-090**
- [ ] Cohort batch ingest — **FYS-091**
- [ ] Funnel SITREP dashboard — **FYS-092**
- [ ] Placement outcome metrics — **FYS-093**
- [ ] Additional regions (Charlotte, Raleigh, Atlanta)
- [ ] More job sources (ClearanceJobs, Dice)
- [ ] White-label option for partners

### Phase 7: Intelligence
- [ ] Salary prediction model
- [ ] Career path recommendations
- [ ] Skill gap analysis (extends pipeline gap analyzer)
- [ ] Market trend forecasting
- [ ] Success prediction scoring
- [ ] Precision@k / NDCG harness — **FYS-111**

### Phase 8: Community
- [ ] Veteran success stories
- [ ] Mentor matching
- [ ] Peer networking
- [ ] Company veteran-friendly ratings
- [ ] Extended placement org dashboard

### Cross-cut Quality (E012 — ongoing)
- [ ] Match path tests — **FYS-110**
- [ ] Monitoring hooks — **FYS-112**
- [ ] Daily ops runbook — **FYS-113**
- [ ] Placement event instrumentation — **FYS-114**

---

## Now / Next / Later

### Now
M0 truth/safety + M1 profile gate + kill placeholder embeddings + O*NET MOS prior + hard-filter hybrid match.

### Next
Serving API, veteran wizard/dashboard, campaign + pathways, partner SITREP.

### Later
Multi-region, more sources, predictive intelligence, community.

---

## Priority legend

| Priority | Meaning |
|----------|---------|
| **P0** | Trustworthy general-use matching; ship before polish |
| **P1** | Campaign / UX / partner differentiation |
| **P2** | Scale & intelligence (2027+) |

---

## Filing work

1. Open [epics/ISSUE_SPECS.md](epics/ISSUE_SPECS.md) → copy issue block.  
2. GitHub Issue via [`.github/ISSUE_TEMPLATE/epic_child.md`](../.github/ISSUE_TEMPLATE/epic_child.md).  
3. Labels: `P0|P1|P2` + area + `research`.  
4. Milestone M0–M5; parent epic `FYS-E0xx`.

---

## Long-term vision

- **10,000+ veterans matched** per year  
- **Nationwide coverage** (all 50 states)  
- **99.9% uptime** for API  
- **&lt;2 second** median match latency  
- **80%+ placement** success rate (partner-reported)  
- **Warm-path response ≥10%** on Side Door campaigns  

---

Built with ❤️ for those who served. 🇺🇸
