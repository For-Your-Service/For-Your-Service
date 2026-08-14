# Issue Specs Catalog — For Your Service

**Organization:** 7 Eagle Group  
**Program:** [PROGRAM.md](PROGRAM.md) · **Research:** [RESEARCH_BRIEF.md](RESEARCH_BRIEF.md) · **Foundry map:** [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md)  
**GitHub:** [GITHUB_ISSUE_MAP.md](GITHUB_ISSUE_MAP.md)  
**Last Updated:** 2026-08-14

Copy any issue block into GitHub. Every acceptance criterion is binary (done / not done).

**Foundry-optimized body standard:** use-case link · object/action · code anchors · stage gate · out of scope · lineage note (see FOUNDRY_ONTOLOGY_MAP).

**Slice 1 plumbing (ship first):** FYS-001, 014, 015, 016, 017, 030, 042, 045, 054, 061, 102, 105, **106, 108, 118, 119**.

**Code is canonical:** Serving/`huggingface/app.py` table names win over docs. See [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md).

---

## Spec Template (all issues)

```
ID / Title / Epic / Priority / Milestone / Estimate
Problem | Goal | In scope | Out of scope
Dependencies | Spec | Acceptance criteria | Test plan | Related docs
```

---

# FYS-E001 — Platform Truth

## FYS-001 — Canonical Unity Catalog schema map
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** S
- **Problem:** Docs and code disagree (`fys_bronze` vs `for_your_service`, etc.).
- **Goal:** Single schema map listing bronze/silver/gold/profile tables and owners.
- **In scope:** Doc + validation script that lists expected tables; ADR note for chosen names.
- **Out of scope:** Migrating historical data volumes (follow-up).
- **Acceptance:**
  - [ ] One table in docs lists every production table name
  - [ ] `PRODUCTION_STATUS.md` and layer specs use the same names
  - [ ] Script fails CI/local check if expected tables missing (optional soft-fail flag)
- **Related:** [PRODUCTION_STATUS.md](../PRODUCTION_STATUS.md), [SILVER_LAYER_SPEC.md](../SILVER_LAYER_SPEC.md), [GOLD_LAYER_SPEC.md](../GOLD_LAYER_SPEC.md)

## FYS-002 — Single production serving path
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** M
- **Problem:** AWS/GCP/HF/Databricks surfaces compete for “the” path.
- **Goal:** Document and implement **Databricks lakehouse + HF FastAPI** as production; demote others to experimental.
- **Acceptance:**
  - [ ] README + DEPLOYMENT_STRATEGY state one primary path
  - [ ] Experimental folders labeled in docs (not deleted without owner OK)
  - [ ] Deploy checklist matches that path only
- **Related:** [DEPLOYMENT_STRATEGY.md](../DEPLOYMENT_STRATEGY.md), [ARCHITECTURE.md](../ARCHITECTURE.md)

## FYS-003 — API credential status truth
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** S
- **Problem:** Credential docs conflict (working vs 401).
- **Goal:** Living status matrix per provider (USAJOBS, JSearch, Adzuna, O*NET).
- **Acceptance:**
  - [ ] Matrix: provider → secret name → last verified date → status
  - [ ] Broken providers cannot silently empty bronze without alert note
- **Related:** [api/API_KEYS_PROGRESS.md](../api/API_KEYS_PROGRESS.md), [SECURE_CREDENTIALS_SETUP.md](../SECURE_CREDENTIALS_SETUP.md)

## FYS-004 — Nested / duplicate tree cleanup plan
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** S
- **Problem:** Nested `For-Your-Service/` confuses contributors.
- **Goal:** Document canonical root; issue PR plan to remove or archive duplicate.
- **Acceptance:**
  - [ ] ROOT_DIRECTORY_GUIDE states canonical paths
  - [ ] Duplicate tree either removed or marked `DEPRECATED` with pointer

---

# FYS-E013 — Data Platform Organization & Pipelines

**Rule:** Code is canonical. See [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md).  
**GitHub epic:** #104

## FYS-106 — Declare code-canonical catalog spine
- **Priority:** P0 · **GitHub #105**
- **Canonical from code:** `workspace.fys_bronze.job_postings`, `workspace.fys_silver.veteran_profiles`
- **Acceptance:** ADR; docs banner on losers (`for_your_service`, `veteran_intake`, `main.fys_*`, lakehouse/transactions)

## FYS-107 — Foundry project and folder spine
- **Priority:** P0 · **GitHub #106**
- **Map:** Datasource=`src/api|ingestion|integration` · Integration=`workspace.fys_*`+`sql/` · Ontology=`profile`+`pipeline/job_matcher` · Application=`huggingface/` · Sandbox=`results/`

## FYS-108 — Wire DQ expectations to abort bad bronze
- **Priority:** P0 · **GitHub #107**
- **Code:** `sql/check_data_quality.sql` already targets canonical bronze — wire to fail builds

## FYS-109 — Pipeline health triad (in / build / out)
- **Priority:** P1 · **GitHub #108**
- **Code:** `scheduler.py`, `freshness_report.sql`, `monitor_ingestion.sql`, HF `/ready`

## FYS-118 — Databricks job graph for job_postings medallion
- **Priority:** P0 · **GitHub #109**
- **Replace/extend:** `configs/databricks/databricks_job.json` (no `/Users/...` paths)

## FYS-119 — Quarantine lakehouse/transactions pipeline
- **Priority:** P0 · **GitHub #110**
- **Code:** `src/databricks/bronze|silver|gold/*.py` → NON-CANONICAL

## FYS-120 — Lineage doc from code paths
- **Priority:** P1 · **GitHub #111**
- **Output:** `docs/LINEAGE.md` grep-backed from `workspace.fys_` references

---

# FYS-E002 — Bronze Ingestion

## FYS-010 — Harden multi-source orchestrator
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Problem:** Partial failures / stubs undermine general job supply.
- **Goal:** Orchestrator runs USAJOBS + JSearch + Adzuna with per-source success/fail.
- **Acceptance:**
  - [ ] One source failure does not abort others
  - [ ] Run report: counts per source + errors
  - [ ] Bronze rows carry `source`, `ingested_at`, raw payload ref
- **Related:** `src/ingestion/`, `src/pipelines/job_ingestion_pipeline.py`

## FYS-011 — Bronze schema + validation
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Pydantic/validator rejects incomplete jobs before write.
- **Acceptance:**
  - [ ] Required: title, company or agency, location or remote flag, source id
  - [ ] Invalid rows quarantined with reason
- **Related:** `src/ingestion/validator.py`, [DATA_VALIDATION.md](../DATA_VALIDATION.md)

## FYS-012 — Regional config (MSA packs)
- **Priority:** P1 · **Milestone:** M2 · **Estimate:** S
- **Goal:** Config-driven regions (Greenville first; packs for Charlotte/Raleigh/Atlanta later).
- **Acceptance:**
  - [ ] Region pack YAML/JSON: geo query params per source
  - [ ] Default region documented in README

## FYS-013 — Ingestion schedule + idempotency
- **Priority:** P1 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Daily job (e.g. 6 AM) with idempotent keys (`source` + external job id).
- **Acceptance:**
  - [ ] Re-run same day does not duplicate active postings
  - [ ] Schedule documented in DAILY_OPERATIONS

## FYS-014 — Fix BronzeWriter stub path
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Problem:** Stub writer blocks production landings.
- **Goal:** Working write path to Unity Catalog bronze table.
- **Acceptance:**
  - [ ] Integration test or notebook run writes ≥1 real/fixture batch
  - [ ] No “NotImplemented” on primary path
- **Related:** `src/ingestion/bronze_writer.py`

## FYS-015 — Unify SiameseMatchingModel public API
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** S · **GitHub follow-on**
- **Problem:** `matcher.py` imports `SiameseNetwork`; module exports `SiameseMatchingModel` → ImportError.
- **Goal:** One canonical public API; package imports cleanly.
- **Code:** `src/matching/matcher.py`, `siamese_network.py`, `__init__.py`
- **Acceptance:**
  - [ ] Import succeeds
  - [ ] Tests aligned or deferred to FYS-016

## FYS-016 — Repair or delete lying matching/ingestion tests
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** S
- **Problem:** Tests import missing symbols — false green / ImportError.
- **Goal:** Pass or remove with pointer; keep `tests/pipeline/test_job_matcher.py`.
- **Acceptance:**
  - [ ] Zero ImportError on listed test paths

## FYS-017 — Choose single JobMatcher path for Slice 1
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** S
- **Problem:** Dual JobMatchers; pipeline cosine works, neural broken; HF fakes scores.
- **Goal:** ADR — Slice 1 uses pipeline matcher; neural Experimental until embeddings real.
- **Acceptance:**
  - [ ] ADR in docs/
  - [ ] HF wires chosen path only

---

# FYS-E003 — Silver Enrichment

## FYS-020 — O*NET client production path
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Live O*NET Web Services client with key in secrets; rate limit 50/min respected.
- **Acceptance:**
  - [ ] Occupations + skills fetch for sample codes
  - [ ] Cache layer to avoid hammering API
- **Related:** [ONET_INTEGRATION.md](../ONET_INTEGRATION.md), `src/api/onet/`, `src/skill_taxonomy/`

## FYS-021 — MOS → O*NET soft prior
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** L
- **Problem:** Research: MOS is prior, not sole ranker; static tables insufficient.
- **Goal:** Map MOS/AFSC/rating → SOC/O*NET set with provenance; empty crosswalk ≠ empty match.
- **Acceptance:**
  - [ ] API or table returns ranked SOC candidates for common MOS (11/18/25 series + extensible)
  - [ ] Similarity/confidence stored for silver `mos_matches`
  - [ ] Docs update MOS_CROSSWALK to “static seed + API prior”
- **Related:** [MOS_CROSSWALK.md](../MOS_CROSSWALK.md), `src/features/mos_mapper.py`

## FYS-022 — Skill extraction → O*NET taxonomy
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** L
- **Goal:** Job description → skills array with importance scores.
- **Acceptance:**
  - [ ] Silver rows include `skills` struct array
  - [ ] Version field `enrichment_version`
- **Related:** [SILVER_LAYER_SPEC.md](../SILVER_LAYER_SPEC.md), `src/features/skill_extractor.py`

## FYS-023 — Standardized titles + industry
- **Priority:** P1 · **Milestone:** M2 · **Estimate:** M
- **Goal:** `standardized_title`, `industry_sector` on silver.
- **Acceptance:**
  - [ ] Mapping rules documented
  - [ ] ≥80% fill rate on fixture corpus

## FYS-024 — Silver transform job
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Bronze→Silver notebook/job aligns with SILVER_LAYER_SPEC.
- **Acceptance:**
  - [ ] Idempotent enrich
  - [ ] Partition + enriched_date set
- **Related:** `src/databricks/silver/transform_silver.py`

---

# FYS-E004 — Gold Embeddings

## FYS-030 — Replace placeholder embeddings
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Problem:** `np.random.rand` invalidates matching.
- **Goal:** Load `sentence-transformers/all-MiniLM-L6-v2` (or documented successor); encode real text.
- **Acceptance:**
  - [ ] Same text → same vector (determinism within model)
  - [ ] No random fallback in production code path
  - [ ] Unit test asserts cosine(self,self) ≈ 1
- **Related:** `src/features/embedding_generator.py`, [GOLD_LAYER_SPEC.md](../GOLD_LAYER_SPEC.md)

## FYS-031 — Job embedding pipeline
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Title + description + skills → 384-dim gold table with `embedding_model`.
- **Acceptance:**
  - [ ] Gold schema matches GOLD_LAYER_SPEC
  - [ ] Model name stored per row

## FYS-032 — Veteran embedding from civilianized text
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Embed translated profile text (not raw MOS jargon only) — depends on FYS-043.
- **Acceptance:**
  - [ ] Veteran gold/profile embedding uses civilianized_summary + skills
  - [ ] Documented in MATCHING_ALGORITHM

## FYS-033 — Embedding versioning & rebuild
- **Priority:** P1 · **Milestone:** M2 · **Estimate:** S
- **Goal:** Model bump triggers rebuild job; old vectors marked stale.
- **Acceptance:**
  - [ ] Runbook: rebuild gold embeddings
  - [ ] `embedding_model` filter on match queries

---

# FYS-E005 — Veteran Profile System

## FYS-040 — Self-understanding intake schema
- **Priority:** P0 · **Milestone:** M1 · **Estimate:** M
- **Problem:** Research: Five Elements + Compass gate fit; missing → wrong matches.
- **Goal:** Structured fields: exactly 3 Five Elements, Operator Compass (4), primary/secondary archetype, prefer/avoid, WHY, problems-to-solve.
- **Acceptance:**
  - [ ] Schema in VETERAN_PROFILE_SCHEMA
  - [ ] Validation: exactly 3 elements; required compass answers
  - [ ] Cannot set `ready_for_matching=true` without this block
- **Out of scope:** Full therapy product; keep intake concise

## FYS-041 — Core veteran profile
- **Priority:** P0 · **Milestone:** M1 · **Estimate:** M
- **Goal:** Identity + military + constraints for general users (MOS/AFSC/rating, branch, rank, YOS, clearance, geo/remote/radius, relocate, salary, ETS, targets).
- **Acceptance:**
  - [ ] Aligns with existing schema sections + clearance status/poly optional
  - [ ] Completeness checker lists missing fields
  - [ ] Example profile remains William Free Hall–style fixture (partner demo), plus generic fixture
- **Related:** [VETERAN_PROFILE_SCHEMA.md](../VETERAN_PROFILE_SCHEMA.md)

## FYS-042 — Profile completeness gate
- **Priority:** P0 · **Milestone:** M1 · **Estimate:** S
- **Goal:** `ready_for_matching` boolean; match API rejects false.
- **Acceptance:**
  - [ ] Gate rules documented
  - [ ] API returns 400/422 with missing-field list

## FYS-043 — Military → civilian translation fields
- **Priority:** P0 · **Milestone:** M1–M2 · **Estimate:** L
- **Goal:** `civilianized_summary`, skill vocabulary, quantified bullets for embeddings + explanations.
- **Acceptance:**
  - [ ] Translator module or pipeline step
  - [ ] Stored on profile; used by FYS-032 / FYS-052
- **Related:** research Military Experience Translator pattern

## FYS-044 — Profile context loader (hot summary)
- **Priority:** P0 · **Milestone:** M1 · **Estimate:** M
- **Goal:** Token-efficient hot summary for API/agents; deep slices on demand.
- **Acceptance:**
  - [ ] Default payload = summary (WHY, USP, non-negotiables, targets, MOS prior)
  - [ ] Expand flags for military / behavioral / preferences
- **Related:** hub-and-spoke profile pattern from research

## FYS-045 — Fix profile package imports
- **Priority:** P0 · **Milestone:** M1 · **Estimate:** S · **GitHub #102**
- **Problem:** `__init__.py` imports missing `intake`/`summary` — package unimportable despite good `models.py`.
- **Goal:** Clean `import src.profile`; slim exports or minimal modules.
- **Code:** `src/profile/__init__.py`, `models.py`
- **Acceptance:**
  - [ ] Package import smoke test passes

---

# FYS-E006 — Matching Engine

## FYS-050 — Hard filters before rank
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Problem:** Research: location often hard No-Go; clearance must not soft-drop.
- **Goal:** Pre-filter geo/remote/radius, clearance, salary overlap, work auth.
- **Acceptance:**
  - [ ] Cleared-required jobs excluded when veteran lacks clearance
  - [ ] Empty result returns soft-fail message (filters too tight)
  - [ ] Factor card lists applied filters
- **Related:** Company Research Go/No-Go pattern

## FYS-051 — Hybrid retrieval (BM25 + dense)
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** L
- **Goal:** Candidate set from lexical + vector before scoring.
- **Acceptance:**
  - [ ] Configurable k from each channel
  - [ ] Union/dedupe by job_id
- **Out of scope:** Learned learning-to-rank v1

## FYS-052 — Multi-factor white-box score
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** L
- **Goal:** Score = weighted skills + MOS prior + values/Five Elements + clearance + salary (+ optional culture/mission when employer package exists).
- **Acceptance:**
  - [ ] Weights documented and configurable
  - [ ] Per-match factor breakdown JSON
  - [ ] No hardcoded constant score (e.g. 0.75) on primary path
- **Related:** [MATCHING_ALGORITHM.md](../MATCHING_ALGORITHM.md)

## FYS-053 — Grounded explanations
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Narrative from factor card only (no invented skills).
- **Acceptance:**
  - [ ] Explanation cites only present factors
  - [ ] Test: scrubbed factors → no hallucinated claims in template mode

## FYS-054 — Remove stub match scores in HF/app paths
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** S
- **Goal:** HF `/match` uses real matcher or returns “embeddings unavailable”.
- **Acceptance:**
  - [ ] Grep-clean of hardcoded confidence on match success path
  - [ ] Integration test with fixture embeddings

## FYS-055 — MOS prior integration in ranker
- **Priority:** P0 · **Milestone:** M2 · **Estimate:** M
- **Goal:** Silver `mos_matches` boosts, does not sole-rank.
- **Acceptance:**
  - [ ] Ablation: with/without prior changes order but non-prior jobs can still surface

---

# FYS-E007 — Serving API

## FYS-060 — Veteran profile API
- **Priority:** P0 · **Milestone:** M3 · **Estimate:** M
- **Goal:** CRUD/upsert + get summary (FYS-044) on FastAPI.
- **Acceptance:**
  - [ ] OpenAPI documents schema
  - [ ] PII fields only on authenticated ops paths (see E011)

## FYS-061 — Match API with gate
- **Priority:** P0 · **Milestone:** M3 · **Estimate:** M
- **Goal:** `POST /match` requires `ready_for_matching`; returns jobs + factors + explanation.
- **Acceptance:**
  - [ ] Gate enforced
  - [ ] Latency target documented; p50 tracked when monitoring exists

## FYS-062 — Jobs query API
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** S
- **Goal:** Filtered job list from silver/gold for debugging and UI.

## FYS-063 — Health + readiness
- **Priority:** P0 · **Milestone:** M3 · **Estimate:** S
- **Goal:** `/health` (process) + `/ready` (Databricks reachable, model loaded flag).

## FYS-064 — Rate limiting & caching
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** M
- **Related:** [RATE_LIMITING.md](../RATE_LIMITING.md)

---

# FYS-E008 — Veteran Experience

## FYS-070 — Profile creation wizard
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** L
- **Goal:** Multi-step UI: self-understanding → military → preferences → review gate.
- **Acceptance:**
  - [ ] Cannot finish without gate fields
  - [ ] Mobile-responsive basics

## FYS-071 — Recommendation dashboard
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** L
- **Goal:** Cards with score, factors, pathway badges, CTA apply/campaign.

## FYS-072 — Match explanation UI
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** M
- **Goal:** Factor breakdown visible; no black-box-only score.

## FYS-073 — Notifications (email)
- **Priority:** P2 · **Milestone:** Later · **Estimate:** M

## FYS-074 — Accessibility pass
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** S
- **Related:** [ACCESSIBILITY.md](../ACCESSIBILITY.md)

---

# FYS-E009 — Campaign & Pathways

## FYS-080 — Bidirectional employer Go/No-Go
- **Priority:** P1 · **Milestone:** M4 · **Estimate:** L
- **Goal:** Company↔candidate scores with research weights; tiers Apply Now / Prepare / Monitor / Bypass.
- **Acceptance:**
  - [ ] Weights configurable; location can hard-fail
  - [ ] Tier stored on campaign/job package

## FYS-081 — Campaign entity
- **Priority:** P1 · **Milestone:** M4 · **Estimate:** M
- **Goal:** company + role + application + outreach + funnel stage.
- **Acceptance:**
  - [ ] Stages: Target → Research → Apply → Outreach → Interview → Offer (or equivalent)
  - [ ] Health color on stalled stages

## FYS-082 — Side Door / warm outreach hooks
- **Priority:** P1 · **Milestone:** M4 · **Estimate:** L
- **Goal:** Same-day ATS apply + warm-path task list (templates; CRM-lite).
- **Acceptance:**
  - [ ] Outreach tasks linked to campaign
  - [ ] Response tracking field
- **Out of scope:** Full LinkedIn automation bot

## FYS-083 — SkillBridge / CSP pathway tags
- **Priority:** P1 · **Milestone:** M4 · **Estimate:** M
- **Goal:** Tag employers/jobs; ETS eligibility clock warnings.

## FYS-084 — Federal / USAJOBS preference path
- **Priority:** P1 · **Milestone:** M4 · **Estimate:** M
- **Goal:** Badge + guidance for veterans’ preference eligible roles from USAJOBS silver rows.

## FYS-085 — HoH / fellowship channel tags
- **Priority:** P2 · **Milestone:** M4 · **Estimate:** S

---

# FYS-E010 — Partner Placement

## FYS-090 — Partner organization object
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** S
- **Goal:** Partner id (e.g. 7 Eagle), users, cohort permissions.

## FYS-091 — Cohort / batch veteran ingest
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** M
- **Goal:** CSV/API batch create profiles under partner.

## FYS-092 — Funnel SITREP dashboard
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** L
- **Goal:** Aggregate stages, response rates, interviews, offers; PII-minimized.
- **Acceptance:**
  - [ ] Partner sees aggregates + drill-down under policy
  - [ ] Export for weekly SITREP

## FYS-093 — Placement outcome metrics
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** M
- **Goal:** Offer-before-ETS, time-to-first-interview; align METRICS.md.

---

# FYS-E011 — Security & Privacy

## FYS-100 — Ops vs analytics PII split
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** M
- **Goal:** Ops API may hold contact; analytics/match features use anonymized projection.
- **Acceptance:**
  - [ ] Anonymizer on analytics path
  - [ ] Docs match code
- **Related:** [guides/PII_PROTECTION.md](../guides/PII_PROTECTION.md), `src/ingestion/anonymizer.py`

## FYS-101 — Secrets only in scopes
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** S
- **Acceptance:**
  - [ ] No secrets in tracked config samples
  - [ ] Databricks + HF secret names documented

## FYS-102 — CORS lockdown
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** S
- **Goal:** Replace `*` with allowlist for known frontends.

## FYS-103 — AuthN for write APIs
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** M
- **Goal:** Token/API key for profile write + partner routes.
- **Related:** [API_AUTHENTICATION.md](../API_AUTHENTICATION.md)

## FYS-104 — Retention alignment
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** S
- **Related:** [DATA_RETENTION_POLICY.md](../DATA_RETENTION_POLICY.md)

## FYS-105 — Remove hardcoded API credential defaults
- **Priority:** P0 · **Milestone:** M0 · **Estimate:** S · **GitHub #103**
- **Problem:** `src/api/config.py` hardcoded defaults; O*NET orchestrator ctor mismatch.
- **Goal:** Env/secrets only; fail fast in prod.
- **Acceptance:**
  - [ ] No live-looking secrets in config
  - [ ] `.env.example` names only

---

# FYS-E012 — Quality & Observability

## FYS-110 — Match path unit/integration tests
- **Priority:** P1 · **Milestone:** M2–M5 · **Estimate:** M
- **Acceptance:**
  - [ ] Tests for filters, scoring, gate, no-random-embeddings

## FYS-111 — Precision@k / NDCG harness
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** L
- **Goal:** Labeled veteran↔job pairs; offline eval job.
- **Related:** [BENCHMARKS.md](../BENCHMARKS.md)

## FYS-112 — Monitoring hooks
- **Priority:** P1 · **Milestone:** M3 · **Estimate:** M
- **Related:** [MONITORING.md](../MONITORING.md)

## FYS-113 — Daily operations runbook update
- **Priority:** P1 · **Milestone:** M2 · **Estimate:** S
- **Related:** [DAILY_OPERATIONS.md](../DAILY_OPERATIONS.md)

## FYS-114 — Placement success instrumentation
- **Priority:** P1 · **Milestone:** M5 · **Estimate:** M
- **Goal:** Events: profile_complete, match_view, apply, outreach_sent, interview, offer.

---

## Traceability (research → epic)

| Research finding | Epics |
|------------------|-------|
| Not another job board; campaign OS | E009, E010 |
| Profile / self-understanding gates match | E005, E006, E007 |
| O*NET MOS soft prior | E003, E006 |
| Hard filters → hybrid → white-box → explain | E006 |
| Fit weights / Go/No-Go tiers | E009 |
| SkillBridge / federal / HoH channels | E009 |
| Partner SITREP / seekers free | E010 |
| Placeholder embeddings / stub scores | E004, E006 |
| Schema / path / credential drift | E001 |
| PII / CORS | E011 |

---

Built with ❤️ for those who served. 🇺🇸
