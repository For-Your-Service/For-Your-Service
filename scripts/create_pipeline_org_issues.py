#!/usr/bin/env python3
"""File Foundry org + pipeline issues grounded in canonical code paths."""
from __future__ import annotations

import subprocess
import time

REPO = "For-Your-Service/For-Your-Service"
MAP = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/FOUNDRY_ONTOLOGY_MAP.md"


def run(args, input_text=None):
    return subprocess.run(
        args, input=input_text, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def create(title, body, labels):
    args = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
    for lab in labels:
        args.extend(["--label", lab])
    p = run(args)
    if p.returncode != 0:
        p = run(["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body])
    print(("OK" if p.returncode == 0 else "FAIL"), (p.stdout or p.stderr)[:200])
    time.sleep(0.4)
    return p.stdout.strip() if p.returncode == 0 else None


def comment(n, body):
    run(["gh", "issue", "comment", str(n), "--repo", REPO, "--body", body])
    time.sleep(0.25)


EPIC_BODY = f"""## Epic FYS-E013: Data Platform Organization & Pipelines

**Rule:** Code is canonical. Serving path wins naming conflicts.

**Outcome:** Foundry-style project split + folder spine + one job-domain medallion pipeline with expectations that abort — aligned to what `huggingface/app.py` already queries.

**Doctrine:** {MAP} (Stage 2 organize + pipeline inventory)

### Canonical spine (from code)
```
workspace.fys_bronze.job_postings
workspace.fys_silver.veteran_profiles
workspace.fys_gold.*   # when embeddings real
```

### Child issues
- [ ] FYS-106 — Declare code-canonical catalog spine
- [ ] FYS-107 — Project/folder spine (Datasource / Integration / Ontology / Application)
- [ ] FYS-108 — Wire DQ expectations to fail builds
- [ ] FYS-109 — Health triad: data in / build / data out
- [ ] FYS-118 — Databricks job graph bronze→silver→gold for job_postings
- [ ] FYS-119 — Quarantine non-canonical lakehouse/transactions path
- [ ] FYS-120 — Lineage doc generated from code

### Related epics
- FYS-E001 Platform Truth (#28)
- FYS-E002 Bronze (#29)
- FYS-E003 Silver (#30)
- FYS-E004 Gold (#31)
"""

ISSUES = [
    (
        "[EPIC FYS-E013] Data Platform Organization and Pipelines",
        EPIC_BODY,
        ["epic", "research", "enhancement", "P0", "ops", "bronze"],
    ),
    (
        "[FYS-106] Declare code-canonical catalog spine (workspace.fys_*)",
        f"""## Traceability
- **Issue ID:** `FYS-106` · **Epic:** FYS-E013 · **Also:** FYS-E001 (#28)
- **Foundry Stage:** 2 Organize + 3 Connect
- **Map:** {MAP}
- **Rule:** Code is canonical — docs follow code.

## Problem
Multiple naming schemes in-repo. **Serving code** already queries `workspace.fys_*`. Docs/SQL DDL invent `for_your_service`, `veteran_intake`, `main.fys_*`, and `dbfs:/mnt/lakehouse/.../transactions`.

## Goal
Publish ADR: **canonical = what `huggingface/app.py` reads/writes**. All new work targets that spine. Non-canonical paths marked Experimental/Deprecated.

## Code anchors (winners)
- `huggingface/app.py` → `workspace.fys_silver.veteran_profiles`, `workspace.fys_bronze.job_postings`
- `sql/check_data_quality.sql`, `sql/freshness_report.sql` → `workspace.fys_bronze.job_postings`

## Code anchors (losers until rewritten)
- `docs/PRODUCTION_STATUS.md` → `for_your_service`
- `sql/setup/create_schemas.sql` → `veteran_intake`
- `sql/bronze_schema.sql` → `main.fys_bronze`
- `src/databricks/*/…` → `dbfs:/mnt/lakehouse/.../transactions`

## Foundry gate
A new contributor can name the three UC identifiers the API uses without opening docs that contradict them.

## Acceptance criteria
- [ ] ADR in `docs/` stating code-canonical rule + table list
- [ ] FYS-001 schema map updated to match ADR (not the reverse)
- [ ] Conflicting docs get a one-line “non-canonical; see ADR” banner
""",
        ["enhancement", "research", "P0", "ops", "tech-debt"],
    ),
    (
        "[FYS-107] Foundry project and folder spine in repo + UC",
        f"""## Traceability
- **Issue ID:** `FYS-107` · **Epic:** FYS-E013
- **Foundry Stage:** 2 — Datasource / Integration / Ontology / Application / sandbox
- **Map:** {MAP}

## Problem
Repo mixes ingest, medallion, analytics, and personal Databricks notebook paths (`configs/databricks/databricks_job.json` → `/Users/whall4.wh@gmail.com/...`). Foundry: projects are the permission/ownership unit; folder spine `raw → clean → ontology → output`.

## Goal
Document and lightly reorganize **ownership map** (no big-bang move required) so each area has a named owner path:

| Foundry project | Code-canonical path |
|-----------------|---------------------|
| Datasource | `src/api/`, `src/ingestion/`, `src/integration/` |
| Integration | UC `workspace.fys_*` + `sql/` that queries it |
| Ontology | `src/profile/`, `src/pipeline/job_matcher.py` |
| Application | `huggingface/` |
| Sandbox | `results/`, nested duplicate tree |

## Code anchors
- `configs/databricks/databricks_job.json` (user-home notebook paths)
- Repo layout under `src/`, `sql/`, `huggingface/`, `notebooks/`

## Foundry gate
New teammate finds raw→clean→ontology→app without being told.

## Acceptance criteria
- [ ] Ownership table in FOUNDRY_ONTOLOGY_MAP / ROOT_DIRECTORY_GUIDE matches real dirs
- [ ] Job JSON paths plan to leave personal home folders (tracked in FYS-118)
- [ ] Sandbox trees labeled (nested `For-Your-Service/` → FYS-004)
""",
        ["enhancement", "research", "P0", "ops"],
    ),
    (
        "[FYS-108] Wire data expectations to abort bad bronze builds",
        f"""## Traceability
- **Issue ID:** `FYS-108` · **Epic:** FYS-E013 / E002
- **Foundry Stage:** 4 Clean — expectations fail the build
- **Map:** {MAP}
- **Object:** JobPosting

## Problem
`sql/check_data_quality.sql` already encodes Foundry-style expectations (duplicate `job_id`, missing title/company) against **canonical** `workspace.fys_bronze.job_postings`, but nothing fails the pipeline when counts > 0.

## Goal
Run DQ as a Databricks task (or CI step) after bronze write; **non-zero issue_count aborts** or quarantines batch.

## Code anchors
- `sql/check_data_quality.sql` (canonical table)
- `src/ingestion/bronze_writer.py` (must write before DQ matters — FYS-014)
- `src/ingestion/validator.py` (today score-intake only — extend or call SQL)

## Foundry gate
Bad batch cannot silently become match input.

## Acceptance criteria
- [ ] DQ task wired after bronze land
- [ ] Failure mode documented (abort vs quarantine table)
- [ ] Fixture test: missing titles → fail
""",
        ["enhancement", "research", "P0", "bronze", "ingestion"],
    ),
    (
        "[FYS-109] Pipeline health triad — in / build / out",
        f"""## Traceability
- **Issue ID:** `FYS-109` · **Epic:** FYS-E013 / E012
- **Foundry Stage:** 8 Operate — only three health questions
- **Map:** {MAP}

## Problem
Foundry: health answers (1) does data get in (2) does it get built (3) does it get out. FYS has SQL for freshness/monitor but no single ops checklist tied to schedule.

## Goal
One runbook + optional job alerts using existing SQL:

| Question | Code anchor |
|----------|-------------|
| In | `src/ingestion/scheduler.py` 06:00 + per-source counts (FYS-010) |
| Build | Bronze→Silver→Gold job success (FYS-118) + FYS-108 expectations |
| Out | HF `/ready` + row freshness `sql/freshness_report.sql` / `sql/monitor_ingestion.sql` |

## Foundry gate
Someone other than the builder can say whether today's jobs are usable for match.

## Acceptance criteria
- [ ] DAILY_OPERATIONS lists the triad with commands
- [ ] Freshness query uses canonical `workspace.fys_bronze.job_postings`
- [ ] Alert owner named (even if email/manual at first)
""",
        ["enhancement", "research", "P1", "ops"],
    ),
    (
        "[FYS-118] Databricks job graph for job_postings medallion",
        f"""## Traceability
- **Issue ID:** `FYS-118` · **Epic:** FYS-E013
- **Foundry Stage:** 3–4 Pipeline Builder analog (Databricks Jobs)
- **Map:** {MAP}

## Problem
`configs/databricks/databricks_job.json` only chains analytics notebooks under a **personal** workspace path (`/Users/whall4.wh@gmail.com/...`). It is not a bronze→silver→gold job for **job_postings**. Meanwhile `src/databricks/*` writes **transactions** to DBFS lakehouse — wrong domain.

## Goal
One Databricks Job definition (repo-tracked) that:

1. Ingest/land bronze `workspace.fys_bronze.job_postings`
2. Run DQ expectations (FYS-108)
3. Silver enrich (when FYS-024 ready)
4. Gold embeddings (when FYS-031 ready)

Paths are **repo/UC canonical**, not `/Users/...`.

## Code anchors
- `configs/databricks/databricks_job.json` (replace or add sibling `fys_medallion_job.json`)
- `notebooks/03b_Multi_Source_Job_Ingestion.py`, `src/ingestion/*`
- Serving contract: `huggingface/app.py`

## Foundry gate
Scheduled job builds green on the same tables the API reads.

## Acceptance criteria
- [ ] Job JSON in repo without personal home paths
- [ ] Task graph documented
- [ ] Depends on FYS-014 + FYS-106 naming
""",
        ["enhancement", "research", "P0", "bronze", "ops"],
    ),
    (
        "[FYS-119] Quarantine non-canonical lakehouse/transactions pipeline",
        f"""## Traceability
- **Issue ID:** `FYS-119` · **Epic:** FYS-E013
- **Map:** {MAP}
- **Rule:** Code that is not on the serving spine is not production.

## Problem
`src/databricks/bronze/ingest_bronze.py`, `silver/transform_silver.py`, `gold/aggregate_gold.py` implement a **transactions** medallion on `dbfs:/mnt/lakehouse/...` (`record_id`, `raw_content`, `source_system`). That is not the job-matching domain and conflicts with Foundry “one lineage to ontology.”

## Goal
Label these modules Experimental/Deprecated; either rewrite to `workspace.fys_*` job_postings or move under `sandbox/` with README pointing to canonical spine.

## Code anchors
- `src/databricks/bronze/ingest_bronze.py`
- `src/databricks/silver/transform_silver.py`
- `src/databricks/gold/aggregate_gold.py`

## Foundry gate
No contributor mistakes transactions lakehouse for production job bronze.

## Acceptance criteria
- [ ] README or module docstring: NON-CANONICAL
- [ ] ROADMAP/PROGRAM do not list this path as production
- [ ] Rewrite ticket linked OR sandbox move done
""",
        ["enhancement", "research", "P0", "ops", "tech-debt"],
    ),
    (
        "[FYS-120] Data lineage doc generated from code paths",
        f"""## Traceability
- **Issue ID:** `FYS-120` · **Epic:** FYS-E013
- **Foundry Stage:** 8 — data lineage (source → ontology → surface)
- **Map:** {MAP}

## Problem
Foundry lineage answers “where did this number come from?” FYS has competing stories; need one diagram/table **sourced from code imports and SQL strings**, not aspirational architecture slides.

## Goal
`docs/LINEAGE.md` (or section in FOUNDRY_ONTOLOGY_MAP) listing:

```
USAJOBS/Adzuna/JSearch clients
  → orchestrator.collect_job_postings
  → BronzeWriter → workspace.fys_bronze.job_postings
  → [silver enrich]
  → huggingface get_jobs / match
```

Plus veteran path: profile API → `workspace.fys_silver.veteran_profiles` → match.

## Code anchors
- Grep-backed list of `workspace.fys_` references in `src/` + `huggingface/` + `sql/`
- Explicit “not in lineage” list: transactions lakehouse, `veteran_intake`, nested tree

## Foundry gate
Someone other than the builder traces a match result field to a bronze column.

## Acceptance criteria
- [ ] LINEAGE.md committed
- [ ] Regenerated/updated when FYS-106 ADR lands
- [ ] Linked from README / epics README
""",
        ["enhancement", "research", "P1", "ops", "documentation"],
    ),
]


def main():
    urls = []
    for title, body, labels in ISSUES:
        u = create(title, body, labels)
        if u:
            urls.append(u)

    # Point existing platform/bronze epics at new work
    note = f"""### Organization & pipelines (code-canonical)

New epic **FYS-E013** covers Foundry Stage 2 project/folder split and Stage 3–4/8 pipeline practices, grounded in what serving code already uses (`workspace.fys_*`).

See {MAP} § Stage 2 + § Data pipelines inventory.

Child issues: FYS-106 … FYS-109, FYS-118 … FYS-120.
"""
    for n in (28, 29, 30, 31, 39):
        comment(n, note)

    # Strengthen FYS-001 with code-canonical rule
    comment(
        40,
        f"""**Code is canonical:** Prefer `huggingface/app.py` tables (`workspace.fys_bronze.job_postings`, `workspace.fys_silver.veteran_profiles`) over PRODUCTION_STATUS / `veteran_intake` / `main.fys_*` / lakehouse transactions. Sibling: FYS-106. Map: {MAP}""",
    )

    print("URLs:")
    for u in urls:
        print(u)


if __name__ == "__main__":
    main()
