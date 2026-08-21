# Legacy Transactions Sandbox

> **NON-CANONICAL / DEPRECATED**
> Rule: Code that is not on the serving spine is not production.

The PySpark scripts in this directory (`ingest_bronze.py`, `transform_silver.py`, `aggregate_gold.py`) process generic transactions (`record_id`, `raw_content`, `source_system`). They are non-canonical and retained strictly for reference.

For active serving logic, see `workspace.fys_*` catalog targets defined in [ADR 001](../../docs/adr/ADR-001-CODE-CANONICAL-CATALOG-SPINE.md).
