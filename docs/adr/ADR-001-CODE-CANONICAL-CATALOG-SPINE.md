# ADR 001: Code-Canonical Unity Catalog Spine

* **Status:** Accepted
* **Date:** 2026-08-14
* **Deciders:** FYS Engineering Lead
* **Related Issues:** FYS-106 (#105), FYS-E013 (#104), FYS-E001 (#28)

## Context
Multiple naming schemes exist across documentation, SQL DDL scripts, and runtime code. Serving components (`huggingface/app.py`) query the `workspace.fys_*` catalog structure, whereas legacy scripts and documentation reference `for_your_service`, `veteran_intake`, `main.fys_*`, and `dbfs:/mnt/lakehouse/.../transactions`.

## Decision
Code is canonical. The production Unity Catalog spine is strictly anchored to what active runtime code reads and writes:

### Canonical Unity Catalog Objects (`workspace.fys_*`)
1. `workspace.fys_bronze.job_postings`
2. `workspace.fys_silver.veteran_profiles`
3. `workspace.fys_silver.enriched_jobs`
4. `workspace.fys_gold.job_embeddings`
5. `workspace.fys_gold.match_results`

### Deprecated / Non-Canonical Schemas
The following namespaces are marked **Deprecated/Experimental** and must not be targeted for production pipelines:
* `for_your_service` (Legacy docs)
* `veteran_intake` (`sql/setup/create_schemas.sql`)
* `main.fys_*` (`sql/bronze_schema.sql`)
* `dbfs:/mnt/lakehouse/.../transactions` (Legacy lakehouse mounts)

## Consequences
* All new development, DDL modifications, and Databricks jobs must target `workspace.fys_*`.
* Any documentation or DDL specifying alternative namespaces must carry a non-canonical warning banner pointing to this ADR.
