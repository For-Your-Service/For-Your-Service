# Foundry → For Your Service Ontology Map

**Organization:** 7 Eagle Group  
**Sources:** [Ontology core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts/) · [Use case lifecycle](https://www.palantir.com/docs/foundry/use-case-life-cycle/overview) · [Pipeline Builder](https://www.palantir.com/docs/foundry/pipeline-builder/overview/) · [Developer hub](https://www.palantir.com/docs/foundry/developers/)  
**Code audit date:** 2026-08-14  
**Purpose:** Optimize FYS issues using Foundry best practices **without requiring Foundry deploy** — map doctrine onto Databricks medallion + FastAPI.

---

## Rule: Code is canonical

| Prefer | Demote until code changes |
|--------|---------------------------|
| What **serving and runnable modules** actually query/write | Docs, ROADMAP, PRODUCTION_STATUS, ADRs that disagree |
| `huggingface/app.py` table names | `docs/PRODUCTION_STATUS.md` (`for_your_service`) |
| `sql/check_data_quality.sql` / `freshness_report.sql` on `workspace.fys_bronze.job_postings` | `sql/setup/create_schemas.sql` (`veteran_intake`) |
| Job-domain medallion | `src/databricks/*/…` `dbfs:/mnt/lakehouse/.../transactions` (wrong domain) |

**Canonical catalog spine (from serving code today):**

```
workspace.fys_bronze.job_postings
workspace.fys_silver.veteran_profiles   (+ job enrich tables when wired)
workspace.fys_gold.*                    (embeddings / match outputs — when real)
```

Evidence: `huggingface/app.py` INSERT/SELECT on `workspace.fys_silver.veteran_profiles` and SELECT on `workspace.fys_bronze.job_postings`.

When code paths conflict, **pick the path the API uses**, then make notebooks/SQL/DDL/docs match that path (FYS-001 / FYS-106). Do not invent a fourth naming scheme in docs.

---

## Stage 0 — Use case (Mad Libs)

> Once upon a time, a **transitioning veteran (and their 7 Eagle counselor)** searched jobs using LinkedIn/USAJOBS and MOS guesswork.  
> Due to **jargon mismatch, wrong channel, and opaque “match %”**, they struggled to **pick roles worth applying to and running a warm path**.  
> If FYS provided a **gated profile → hard-filtered hybrid match → factor card → campaign writeback**, they could **apply with confidence before ETS**, which matters because **placement outcomes are the mission**.

| Field | Value |
|-------|-------|
| Named primary user | Transitioning service member + 7 Eagle placement counselor |
| Decision improved | Which jobs to pursue / apply / Side Door this week |
| Trigger | Profile complete (`ready_for_matching`) or counselor opens cohort |
| Success metric | Offer-before-ETS rate; warm-path response ≥10%; % matches with factor cards |
| Out of scope | National social network; Foundry enrollment dependency for MVP |

**Gate:** One sentence a veteran recognizes as their problem.

---

## Stage 1 — Plumbing slice (ship first)

| Slice | User can… | Issues | Code reality |
|-------|-----------|--------|--------------|
| **Slice 1 — plumbing** | Complete profile gate → get **non-fake** top-k matches with factors → counselor sees same payload | FYS-001, 014, 030, 042, 045, 050, 054, 061, 015, 017 | Embeddings random; HF score 0.75; BronzeWriter no-op; matching import broken; pipeline cosine **works** |
| Slice 2 | O*NET/MOS prior + silver enrich + real MiniLM | FYS-020–024, 031–032, 051–055 | Dual O*NET clients; thin MOS map |
| Slice 3 | Campaign actions write back + partner SITREP | FYS-080–093 | **No `src/` owners yet** |

**Rule (Foundry):** Narrow slice fully delivered > ambitious half-finished. Prefer wiring **`src/pipeline/job_matcher.py`** for Slice 1 over fixing broken Siamese import path first — then replace with neural once embeddings are real.

---

## Object types (nouns) → FYS owners

| Object type | Primary key | Backing today | Maturity | Owner files |
|-------------|-------------|---------------|----------|-------------|
| **Veteran** | `veteran_id` (string UUID) | `src/profile/models.py`; HF Pydantic; UC `veteran_profiles` | Experimental — package `__init__` broken | FYS-E005 |
| **JobPosting** | `source` + `external_job_id` → `job_id` | Bronze tables; API models | Experimental — BronzeWriter stub | FYS-E002 |
| **Skill / OccupationPrior** | `onet_code` / MOS code | `mos_mapper`, `skill_taxonomy` | Experimental — dual clients | FYS-E003 |
| **Embedding** | `job_id` / `veteran_id` + `embedding_model` | Gold spec; generator **random** | Broken | FYS-E004 |
| **Match** | `match_id` = `veteran_id`+`job_id`+`model_version` | `pipeline/job_matcher.JobMatch`; HF fake | Partial | FYS-E006 |
| **Campaign** | `campaign_id` | Docs only | Missing | FYS-E009 |
| **Partner** | `partner_id` | Docs only | Missing | FYS-E010 |
| **AnonymizedCandidate** | hashed id | `anonymizer.py` (scores-only) | Thin | FYS-E011 |

**Foundry PK rules applied:** string `id`; never row-order; never infer properties by parsing id; FKs as `veteran_id`, `job_id`, `partner_id`.

---

## Link types (workflow traversals)

| Link | From → To | Enables |
|------|-----------|---------|
| `served_as` | Veteran → MOS/OccupationPrior | Soft prior boost |
| `matches` | Veteran → JobPosting (via Match) | Recommendation list |
| `explains` | Match → FactorCard properties | Trust UI |
| `targets` | Campaign → JobPosting + Company | Funnel |
| `belongs_to` | Veteran → Partner | SITREP cohort |

---

## Action types (verbs) — writeback loop

| Action | Object edits | Submission criteria | Side effects |
|--------|--------------|---------------------|--------------|
| `CompleteProfile` | Veteran properties + `ready_for_matching` | Self-understanding + military + prefs complete | Emit `profile_complete` |
| `RunMatch` | Creates Match objects | `ready_for_matching == true` | Persist factor card; never invent skills |
| `StartCampaign` | Campaign Target stage | Match exists or manual target | Tasks for apply + Side Door |
| `LogOutreach` | Campaign outreach fields | Campaign open | Response tracking |
| `RecordOutcome` | Interview/Offer timestamps | Partner or veteran auth | SITREP metrics |

**Foundry rule:** Deterministic filters/scores in functions; LLM only narrates **existing** factors (FYS-053). Actions are the write path — UI must not raw-UPDATE analytics tables with PII.

---

## Pipeline spine (Foundry layers ↔ FYS)

```
SOURCE (APIs)     CLEAN              ONTOLOGY              LOGIC                SURFACE
USAJOBS/…    →    Bronze→Silver  →   Veteran/Job/Match →  Match fn + Actions → FastAPI/HF + UI
as-is land        expectations        string ids            no LLM math          Workshop-class UX later
```

| Foundry stage | FYS epic | Gate |
|---------------|----------|------|
| 2 Organize projects/folders | E001 + **E013** | New teammate finds raw→clean→ontology→app without asking |
| 3 Connect as-is | E002 | Successful sync + row counts per source |
| 4 Clean + expectations | E002/E003 | PK unique; **abort** on bad schema |
| 5 Ontology | E005/E006 objects | User answers “why this job?” via factors without code |
| 6 Verbs | E007/E009 actions | Gate + writeback |
| 7 Surface | E008 | Find → decide → act |
| 8 Operate | E001/E011/E012 | Freshness, build success, markings (PII) |
| 9 Prove | E010/E012 | Metric vs baseline |

---

## Stage 2 — Organization (Foundry projects → FYS repo + UC)

Foundry splits **Datasource / Integration / Ontology / Application / sandbox**. Map onto **this repo’s real trees** (not aspirational folders):

| Foundry project | FYS ownership (code-canonical) | Purpose |
|-----------------|--------------------------------|---------|
| **Datasource – job APIs** | `src/api/{usajobs,adzuna,onet,…}/`, `src/ingestion/`, `src/integration/` | Ingest as-is; mark PII at boundary (`anonymizer.py`) |
| **Integration – job domain** | Target: UC `workspace.fys_*` tables + `sql/*` that already query them; **not** `src/databricks/*/transactions` until rewritten | Combine, PKs, restricted columns |
| **Ontology – placement** | `src/profile/`, `src/pipeline/job_matcher.py`, Match factor JSON | Semantic objects: Veteran, JobPosting, Match |
| **Application – serving** | `huggingface/app.py`, future UX | Surface + actions |
| **Sandbox** | `results/`, nested `For-Your-Service/`, experiments | No business-of-record writes |

**Folder spine (Foundry `raw/ → clean/ → ontology/ → output/`):**

| Spine | Code-canonical location |
|-------|-------------------------|
| raw | Landing from orchestrator → bronze write (`BronzeWriter` → `workspace.fys_bronze.job_postings`) |
| clean | Silver transforms / SQL enrich touching `workspace.fys_silver.*` |
| ontology | Profile models + Match objects in Python/API payloads |
| output | HF responses, `results/` exports, partner SITREP |

**Issue:** FYS-106 (declare + document this map from code), FYS-107 (repo/UC folder alignment).

---

## Data pipelines inventory (code as-is)

| Pipeline | Entry | Writes / reads | Status vs canonical |
|----------|-------|----------------|---------------------|
| Multi-source collect | `src/ingestion/orchestrator.py` + `scheduler.py` (06:00) | Calls `BronzeWriter` | Collect works; **write stub** |
| BronzeWriter | `src/ingestion/bronze_writer.py` | Should land bronze jobs | **No-op** |
| Serving read path | `huggingface/app.py` | `workspace.fys_bronze.job_postings`, `workspace.fys_silver.veteran_profiles` | **Canonical consumer** |
| DQ checks | `sql/check_data_quality.sql`, `sql/freshness_report.sql`, `sql/monitor_ingestion.sql` | Query `workspace.fys_bronze.job_postings` | Canonical checks; **not wired to fail builds** |
| Analytics job JSON | `configs/databricks/databricks_job.json` | User-home notebooks `src/analytics/01…03` | Separate vector/tensor path — not bronze→silver jobs |
| Medallion Spark modules | `src/databricks/bronze|silver|gold/*.py` | `dbfs:/mnt/lakehouse/.../transactions` | **Non-canonical** (transactions domain, not job_postings) |
| SQL DDL | `sql/bronze_schema.sql` → `main.fys_bronze`; `sql/setup/create_schemas.sql` → `veteran_intake` | Conflicts with HF | Align to `workspace.fys_*` |
| Notebooks | `notebooks/03*`, `databricks/03*` | Mix `main.fys_*` / `workspace.fys_*` | Follow HF |

**Foundry pipeline checklist → FYS issues:**

| Foundry practice | Issue |
|------------------|-------|
| Ingest as-is; clean inside platform | FYS-010, FYS-014 |
| Data expectations abort bad builds | **FYS-108** (wire `check_data_quality.sql`) |
| Schedules + health (in / build / out) | FYS-013 + **FYS-109** |
| Incremental where append-style | FYS-013 idempotency |
| Branch/PR; don’t develop only in personal folders | **FYS-107**; fix `databricks_job.json` user-home paths |
| One job graph bronze→silver→gold for **jobs** | **FYS-110b** job def (avoid clash with test issue FYS-110) → use **FYS-118** |
| Retire wrong-domain lakehouse path | **FYS-119** |
| Lineage doc generated from code | **FYS-120** |

---

## Code-grounded blockers (must appear on issues)

| Finding | Issue |
|---------|-------|
| `EmbeddingGenerator` uses `np.random.rand` | FYS-030 |
| HF `match_score=0.75` hardcoded | FYS-054 |
| `BronzeWriter` no-op | FYS-014 |
| `SiameseNetwork` vs `SiameseMatchingModel` ImportError | **FYS-015** (new) |
| Two `JobMatcher` classes; pipeline one works | **FYS-017** (new) |
| `src/profile/__init__` imports missing modules | **FYS-045** (new) |
| Lying tests (neural, ingestion Indeed helpers) | **FYS-016** (new) |
| Schema `fys_*` vs `for_your_service` vs `main` | FYS-001 |
| CORS `*` + credentials | FYS-102 |
| Hardcoded API defaults in `src/api/config.py` | **FYS-105** (new) |
| Dual O*NET / MOS mappers | FYS-020, FYS-021 |
| Campaign/Partner no `src/` | E009/E010 — do not schedule before Slice 1 plumbing |
| Competing catalogs (`main`, `veteran_intake`, `for_your_service`, lakehouse/transactions) | **FYS-106**, FYS-001, **FYS-119** |
| DQ SQL exists but does not gate builds | **FYS-108** |
| No single bronze→silver→gold **job** graph for job_postings | **FYS-118** |
| Job JSON points at personal `/Users/whall4…` paths | **FYS-107**, **FYS-118** |

---

## Issue writing standard (Foundry-optimized)

Every FYS GitHub issue body must include:

1. **Use-case link** — which Stage 0 decision it serves  
2. **Object / Action** — noun or verb touched  
3. **Code anchors** — file paths from this audit (**code is canonical**)  
4. **Gate** — binary done condition (Foundry stage gate language)  
5. **Out of scope** — prevent ocean-boiling  
6. **Lineage note** — raw / clean / ontology / surface  
7. **Canonical conflict** — if docs disagree with code, say which code wins and what to update

---

Built with ❤️ for those who served. 🇺🇸
