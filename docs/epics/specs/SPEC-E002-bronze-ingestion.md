# SPEC-E002 — Bronze Ingestion

## Problem Statement
Transitioning veterans and their counselors cannot receive trustworthy job recommendations unless the system first lands a complete, traceable, and repeatable supply of job postings. The current multi-source collector can continue after USAJOBS or Adzuna failures, but it does not yet run JSearch, does not emit a per-source run report, and depends on a `BronzeWriter` that only adds an `ingestion_timestamp` and logs a would-write message. The existing validator validates a veteran-intake score payload rather than job postings. As a result, the primary serving path can query the canonical bronze table, but the ingestion path cannot populate it.

## Solution
Deliver a job-domain bronze ingestion pipeline that collects configured provider results, preserves the source payload and source identity, validates each normalized JobPosting, quarantines invalid records, and idempotently lands valid records in `workspace.fys_bronze.job_postings`. Schedule the pipeline daily at 06:00 UTC through a durable job runner, with an observable run report that exposes counts, failures, duplicates, and quarantines. Make data-quality expectations an abort gate before downstream processing.

## User Stories
1. As a transitioning veteran, I want current jobs from more than one source so that my recommendations are not limited by a single job board.
2. As a 7 Eagle counselor, I want each job to show its source and source-specific identifier so that I can verify the original listing before advising an applicant.
3. As a pipeline operator, I want a failure from one provider to be isolated so that the remaining providers can still deliver usable jobs.
4. As a pipeline operator, I want a run report with per-source attempted, received, accepted, duplicate, quarantined, and failed counts so that I can identify an empty or degraded source run.
5. As a data steward, I want every accepted JobPosting to retain its raw payload reference and ingestion time so that normalized fields remain auditable.
6. As a data steward, I want postings missing a title, source identifier, or both company/agency and location/remote information quarantined with a reason so that malformed records never silently enter the serving corpus.
7. As a data steward, I want the canonical natural key to use source plus external job identifier so that a retry or same-day re-run does not create duplicate active listings.
8. As a regional program manager, I want provider-specific location packs with Greenville as the initial default so that geographic coverage is intentional and repeatable.
9. As a platform operator, I want the daily collection to be scheduled at 06:00 UTC and observable for freshness so that I know when recommendations may be stale.
10. As a matching-service maintainer, I want valid Bronze JobPosting rows in the canonical workspace catalog so that the primary match-serving query has a real job supply.
11. As a release engineer, I want duplicate, missing-title, and missing-company quality checks to abort the downstream build when thresholds are violated so that bad bronze data cannot flow into enrichment.
12. As a contributor, I want non-job `dbfs:/mnt/lakehouse/.../transactions` work explicitly quarantined so that it cannot be mistaken for the production job-posting ingestion path.

## Implementation Decisions
- Treat JobPosting as the bronze business object; preserve source-native payload information as-is alongside normalized identity and operational metadata.
- Use `source + external_job_id` as the stable business key and make ingestion idempotent with an upsert/merge policy for active postings.
- Add USAJOBS, JSearch, and Adzuna adapters behind a common result contract; retain per-source error isolation and rate-limit behavior.
- Validate normalized jobs before the write: title; company or agency; location or remote indicator; source; and external identifier are mandatory.
- Send invalid records to a dedicated canonical quarantine dataset with rejection reason, source identity, raw payload reference, and run identifier. Do not discard them.
- Implement the bronze writer as the production Unity Catalog landing boundary; it must write to `workspace.fys_bronze.job_postings`, not log-only, a new catalog name, or a filesystem lakehouse path.
- Record a run identifier, started/completed timestamps, source-level outcomes, accepted-row count, quarantine count, duplicate count, and errors for every execution.
- Drive region selection from versioned configuration rather than hard-coded scheduler arrays; begin with Greenville and allow future Charlotte, Raleigh, and Atlanta packs.
- Run the collection through a durable scheduled job at 06:00 UTC; retain a callable one-run entry point for tests and manual recovery.
- Gate bronze completion on data-quality expectations. A failing quality gate prevents the bronze run from advertising success or releasing data to silver.
- Mark the transaction-domain filesystem medallion modules as non-canonical and exclude them from the job-postings job graph.

## Testing Decisions
- Unit-test each source adapter's normalization, credential-missing behavior, rate-limit integration, and exception isolation using mocked provider responses.
- Unit-test job validation with valid fixtures and each required-field failure; assert quarantined records include the exact reason and original source identity.
- Unit-test idempotency by ingesting the same source/external identifier repeatedly and asserting one active bronze row with deterministic update behavior.
- Integration-test the production writer against the canonical bronze table with a fixture batch; assert rows, raw-payload reference, source, run metadata, and ingestion timestamp are persisted.
- Integration-test a mixed batch containing valid, invalid, duplicate, and one failed source; assert the run report counts and continued successful writes.
- Execute the canonical data-quality SQL against fixture data and assert duplicate, missing-title, and missing-company violations fail the pipeline gate.
- Test the scheduled job definition and one-run command without relying on an infinite in-process scheduler loop.
- Add a regression assertion that no production job-posting task reads or writes the non-canonical transaction lakehouse path.

## Out of Scope
- Silver enrichment, title standardization, skill extraction, O*NET classification, and embedding generation.
- Ranking, matching, candidate profile writes, or campaign workflows.
- Historical migration from conflicting catalogs or bulk backfill of every past provider response.
- Building an ingestion implementation for the non-canonical transaction-domain lakehouse pipeline.

## Further Notes
- GitHub epic: **#29**. Child issue IDs: **FYS-010, FYS-011, FYS-012, FYS-013, FYS-014**.
- Lineage: external job APIs → raw/validated JobPosting → canonical bronze landing → later silver enrichment → match-serving surface.
- Code is canonical: the primary serving path and quality checks establish `workspace.fys_bronze.job_postings` as the bronze target. Conflicting documentation, `main`/`veteran_intake` names, and `dbfs:/mnt/lakehouse/.../transactions` do not define the production job domain.
- Current reality is intentionally explicit: the collector has partial-failure handling, but JSearch/reporting/validation are incomplete and the BronzeWriter is a no-op stub until this epic lands.
