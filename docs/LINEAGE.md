# Data Lineage & Ontology Map

**Issue ID:** FYS-120 | **Epic:** FYS-E013 | **Foundry Stage:** 8  Data Lineage

---

## Active Pipeline Lineage

```
[ USAJOBS / Adzuna / JSearch APIs ]

                     ?
       orchestrator.collect_job_postings

                     ?
               BronzeWriter

                     ?
      workspace.fys_bronze.job_postings

                     ?
             [ Silver Enrich ]

                     ?
      Hugging Face get_jobs / Match
```

```
[ Veteran Profile API / Ingestion ]

                     ?
    workspace.fys_silver.veteran_profiles

                     ?
             Matching Surface
```

---

## Active Code Anchors (workspace.fys_*)

All active lineage steps are anchored to physical references in the codebase:

| Target Table / Schema | File Location |
| :--- | :--- |
| `workspace.fys_bronze` | `src/databricks/bronze/ingest_bronze.py` |
| `workspace.fys_silver` | `src/databricks/silver/transform_silver.py` |
| `workspace.fys_gold` | `src/databricks/gold/aggregate_gold.py` |

---

## Explicitly Excluded from Active Lineage ("Not in Lineage")

The following schemas, scripts, and tables represent legacy structures, stand-alone analytics, or alternative catalog paradigms and **are not part of the core production match lineage**:

### 1. Legacy Transactions Lakehouse
* **Files:** `src/databricks/bronze/ingest_bronze.py`, `src/databricks/silver/transform_silver.py`, `src/databricks/gold/aggregate_gold.py`, `src/ingestion/db_to_json.py`
* **Reason:** References transaction-level mock/testing lakehouse datasets not consumed by the core match engine.

### 2. veteran_intake Unity Catalog & Schemas
* **Files:** `sql/create_schema.sql`, `sql/example_queries.sql`, `sql/analytics/*`, `sql/setup/*`
* **Reason:** Legacy DDL and analytical query workspace. Active production matching resolves through `workspace.fys_*` namespaces.

### 3. Nested Tree Data Structures
* **Reason:** Experimental hierarchy/taxonomic parsing models not wired into the primary serving layer.

---

## Foundry Gate Verification Protocol

To verify field-level traceability from a match output down to raw bronze storage:

1. Select a target match field (e.g., `job_title`, `required_skills`, `location`).
2. Map backwards from Hugging Face match output to `workspace.fys_silver.job_postings`.
3. Verify origin column in `workspace.fys_bronze.job_postings` via `src/databricks/bronze/ingest_bronze.py`.
