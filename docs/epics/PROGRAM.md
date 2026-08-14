# Architecture Program — For Your Service

**Organization:** 7 Eagle Group  
**Based on:** [RESEARCH_BRIEF.md](RESEARCH_BRIEF.md)  
**Roadmap:** [../ROADMAP.md](../ROADMAP.md)  
**Issue specs:** [ISSUE_SPECS.md](ISSUE_SPECS.md)  
**Last Updated:** 2026-08-14

---

## System Target (general use)

```
[Job APIs + Pathways] → Bronze → Silver (O*NET/MOS/skills) → Gold (real embeddings)
                              ↓
[Veteran Profile + Self-Understanding] → Translation → Hard Filters → Hybrid Match → Factor Card
                              ↓
                    Campaign (ATS + Side Door) → Partner SITREP
                              ↓
              FastAPI (HF Spaces) ←→ Databricks Unity Catalog
```

Audience: **any transitioning service member / veteran**, plus **placement partners** (starting with 7 Eagle). Not a single-person tool.

---

## Capability Epics (entire architecture)

| Epic | Name | Outcome | Priority | Issues |
|------|------|---------|----------|--------|
| **FYS-E001** | Platform Truth | One production path; schema + credential docs match runtime | P0 | FYS-001 … 004 |
| **FYS-E002** | Bronze Ingestion | Reliable multi-source job landings, validated, scheduled | P0 | FYS-010 … 014 |
| **FYS-E003** | Silver Enrichment | O*NET skills + MOS soft prior + titles/industry | P0 | FYS-020 … 024 |
| **FYS-E004** | Gold Embeddings | Real 384-dim vectors for jobs + veterans | P0 | FYS-030 … 033 |
| **FYS-E005** | Veteran Profile System | Self-understanding + profile gate + context loader | P0 | FYS-040 … 044 |
| **FYS-E006** | Matching Engine | Hard filters → hybrid → white-box → grounded explain | P0 | FYS-050 … 055 |
| **FYS-E007** | Serving API | FastAPI contracts for profile, match, jobs, health | P0 | FYS-060 … 064 |
| **FYS-E008** | Veteran Experience | Wizard + match dashboard (general UX) | P1 | FYS-070 … 074 |
| **FYS-E009** | Campaign & Pathways | Bidirectional fit, Side Door, SkillBridge/federal tags | P1 | FYS-080 … 085 |
| **FYS-E010** | Partner Placement | 7 Eagle batch + SITREP + conversion metrics | P1 | FYS-090 … 093 |
| **FYS-E011** | Security & Privacy | Secrets, CORS, PII split ops vs analytics | P0 | FYS-100 … 104 |
| **FYS-E012** | Quality & Observability | Tests, Precision@k, monitoring, runbooks | P1 | FYS-110 … 114 |
| **FYS-E013** | Data Platform Org & Pipelines | Foundry Stage 2 folders + medallion job graph; **code-canonical** `workspace.fys_*` | P0 | FYS-106…109, 118…120 |

---

## Dependency Graph

```
E001 Platform Truth ──┐
E013 Org & Pipelines ─┼──► catalog spine workspace.fys_* (code-canonical)
E011 Security ────────┘
        │
        ▼
E002 Bronze ──► E003 Silver ──► E004 Gold ──┐
   FYS-108/118                               ▼
E005 Profile ──► Translation ──► E006 Match ◄─┘
                                   │
                                   ▼
                         E007 Serving API
                                   │
              ┌────────────────────┼────────────────┐
              ▼                    ▼                ▼
        E008 Veteran UX     E009 Campaign     E010 Partner
              └────────────────────┴────────────────┘
                                   │
                                   ▼
                         E012 Quality (cross-cuts)
```

**Critical path:** E001 + E013 + E011 → E005 → E002/E003/E004 → E006 → E007 → (E008 ∥ E009) → E010

**Code-canonical rule:** `huggingface/app.py` table names beat docs. See [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md).

---

## Epic Briefs

### FYS-E001 — Platform Truth
**Problem:** Nested trees, `fys_*` vs `for_your_service`, conflicting API credential status, unused cloud surfaces confuse operators.  
**Outcome:** One canonical Unity Catalog schema + one serving path (Databricks + HF) documented and enforced — **names taken from serving code**, not PRODUCTION_STATUS.  
**Related:** [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md), [DEPLOYMENT_STRATEGY.md](../DEPLOYMENT_STRATEGY.md), sibling **E013**

### FYS-E013 — Data Platform Organization & Pipelines
**Problem:** Foundry Stage 2/3/4/8 practices missing; competing pipeline implementations (API spine vs lakehouse/transactions vs personal notebook jobs).  
**Outcome:** Project/folder ownership map; DQ expectations that abort; health triad; one medallion job graph for `job_postings` on `workspace.fys_*`; quarantine non-canonical paths.  
**Related:** [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md), GitHub #104  

### FYS-E002 — Bronze Ingestion
**Problem:** Ingestion must be production-reliable for general job supply (USAJOBS, JSearch, Adzuna; regional + expandable).  
**Outcome:** Scheduled, validated bronze landings; failed sources isolated; provenance on every row.  
**Related:** [PIPELINE_USAGE.md](../PIPELINE_USAGE.md), `src/ingestion/`, `src/api/`

### FYS-E003 — Silver Enrichment
**Problem:** Static MOS tables alone are not enough; research says O*NET is the substrate.  
**Outcome:** Enriched jobs with O*NET codes/skills, MOS soft-prior links, standardized titles.  
**Related:** [SILVER_LAYER_SPEC.md](../SILVER_LAYER_SPEC.md), [ONET_INTEGRATION.md](../ONET_INTEGRATION.md), [MOS_CROSSWALK.md](../MOS_CROSSWALK.md)

### FYS-E004 — Gold Embeddings
**Problem:** Random embeddings invalidate all match claims.  
**Outcome:** Real MiniLM (or successor) embeddings for job + civilianized veteran text; versioned model id on every vector.  
**Related:** [GOLD_LAYER_SPEC.md](../GOLD_LAYER_SPEC.md), [MATCHING_ALGORITHM.md](../MATCHING_ALGORITHM.md)

### FYS-E005 — Veteran Profile System
**Problem:** Research: matching without self-understanding produces wrong-channel noise.  
**Outcome:** Guided intake (Five Elements ×3, Compass, archetype), core profile, completeness gate, hot context loader, military→civilian translation fields.  
**Related:** [VETERAN_PROFILE_SCHEMA.md](../VETERAN_PROFILE_SCHEMA.md)

### FYS-E006 — Matching Engine
**Problem:** Cosine-only ranking ignores clearance/geo/salary and cannot explain itself.  
**Outcome:** Hard filters → BM25+dense retrieve → multi-factor score (skills, MOS prior, values, clearance, salary) → grounded explanations.  
**Related:** [NEURAL_MATCHING_ARCHITECTURE.md](../NEURAL_MATCHING_ARCHITECTURE.md), `src/matching/`, `src/pipeline/`

### FYS-E007 — Serving API
**Problem:** Frontend/partners need stable contracts; `/match` must enforce profile gate.  
**Outcome:** Versioned FastAPI on HF Spaces: health, veteran CRUD, match, jobs; rate limits; Databricks SQL behind.  
**Related:** [API.md](../API.md), `huggingface/app.py`

### FYS-E008 — Veteran Experience
**Problem:** Architecture includes Base44/UI; veterans need wizard + factor cards, not raw JSON.  
**Outcome:** Profile wizard, recommendation dashboard, mobile-responsive basics.  
**Related:** Phase 5 in roadmap

### FYS-E009 — Campaign & Pathways
**Problem:** White space is campaign OS + right channel, not more listings.  
**Outcome:** Bidirectional Go/No-Go, campaign entity, Side Door outreach stages, SkillBridge/federal/HoH badges + ETS clocks.  

### FYS-E010 — Partner Placement
**Problem:** 7 Eagle needs batch outcomes, not one-off demos.  
**Outcome:** Partner org object, cohort ingest, funnel SITREP, conversion metrics without excess PII.  

### FYS-E011 — Security & Privacy
**Problem:** PII in ops APIs vs analytics anonymization must be explicit; secrets out of git.  
**Outcome:** Documented split, tight CORS, secret scopes, retention alignment.  
**Related:** [guides/PII_PROTECTION.md](../guides/PII_PROTECTION.md), [SECURITY.md](../SECURITY.md)

### FYS-E012 — Quality & Observability
**Problem:** Placement claims need measurement.  
**Outcome:** Unit/integration tests for match path, Precision@k harness, monitoring + daily ops hooks.  
**Related:** [TESTING_STRATEGY.md](../TESTING_STRATEGY.md), [METRICS.md](../METRICS.md), [MONITORING.md](../MONITORING.md)

---

## Milestone Mapping

| Milestone | Epics | Window |
|-----------|-------|--------|
| **M0 — Truth & Safety** | E001, E011 | Immediate |
| **M1 — Know Yourself** | E005 (intake + profile + loader) | Q3 2026 |
| **M2 — Real Match Substrate** | E002, E003, E004, E006 core | Q3–Q4 2026 |
| **M3 — Serve & UX** | E007, E008 | Q4 2026 |
| **M4 — Campaign Differentiator** | E009 | Q4 2026 |
| **M5 — Partner Scale** | E010, E012 | Q4 2026–2027 |

---

## Now / Next / Later

### Now (P0)
- Platform schema truth + kill nested confusion (E001)  
- Security/PII baseline (E011)  
- Profile gate + self-understanding (E005)  
- Replace placeholder embeddings (E004)  
- Hard filters + hybrid white-box match (E006)  
- O*NET-backed MOS prior (E003)  

### Next (P1)
- Serving API completeness (E007)  
- Veteran wizard/dashboard (E008)  
- Campaign + pathways (E009)  
- Partner SITREP (E010)  
- Match quality harness (E012)  

### Later (P2 / 2027)
- Multi-region scale, more sources (ClearanceJobs, Dice)  
- Salary prediction, skill-gap, success scoring  
- Community / mentor matching  
- White-label  

---

## Filing GitHub Issues

1. Create one Issue per `FYS-0xx` from [ISSUE_SPECS.md](ISSUE_SPECS.md).  
2. Title: `[FYS-0xx] Short name`  
3. Body: paste **Problem / Spec / Acceptance / Dependencies** from the catalog.  
4. Labels: priority + area + `research` when derived from this program.  
5. Milestone: M0–M5 as above.  
6. Parent: comment `Parent: FYS-E0xx`.

Optional: one tracking Issue per epic titled `[EPIC FYS-E0xx] …` with checklist of child IDs.

---

Built with ❤️ for those who served. 🇺🇸
