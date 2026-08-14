# FYS-E013 — Data Platform Organization & Pipelines

## Problem Statement
The production serving surface consumes `workspace.fys_bronze.job_postings` and `workspace.fys_silver.veteran_profiles`, but the current BronzeWriter does not persist records, data-quality SQL is not a build gate, and Spark medallion prototypes write an unrelated transactions lakehouse path. Personal notebook paths and competing catalogs prevent a reliable, discoverable JobPosting pipeline from raw landing through Match serving.

## Solution
Deliver one observable JobPosting pipeline organized around the code-canonical workspace spine: ingest raw source payloads into bronze, abort the run when required quality expectations fail, transform only the job domain through silver and gold, and make lineage and ownership discoverable. Explicitly quarantine the unrelated transactions prototype until it is rewritten against the production JobPosting contract.

## User Stories
1. As a data engineer, I want a documented catalog spine for JobPosting data, so that every pipeline stage targets the relations used by Match serving.
2. As an ingestion operator, I want source batches to land durably in canonical bronze, so that a successful collection run produces JobPosting records the API can read.
3. As a data-quality owner, I want duplicate IDs, missing titles, and missing companies to stop a bad bronze build, so that corrupted JobPosting data cannot reach matching.
4. As a platform operator, I want clear inbound, build, and outbound health signals, so that I can distinguish source failure, transform failure, and serving-readiness failure.
5. As a scheduler owner, I want idempotent ingestion and a visible run history, so that retries do not create duplicate active JobPosting records.
6. As a new contributor, I want datasource, integration, ontology, application, and sandbox ownership clearly mapped, so that I can find the correct change location without relying on personal paths.
7. As a Databricks administrator, I want a portable job graph with repository-relative or managed workspace references, so that production runs do not depend on one user home directory.
8. As a Match service, I want only data that passed bronze expectations to become candidate JobPostings, so that serving reads reliable inventory.
9. As a security and governance owner, I want raw, clean, ontology, and output lineage recorded, so that data movement from source to Match response is auditable.
10. As a maintainer, I want the transactions-domain prototype visibly quarantined, so that it cannot be mistaken for the JobPosting medallion path.
11. As a release reviewer, I want a generated code-backed lineage report, so that changes to `workspace.fys_*` references are visible before deployment.
12. As a transitioning Veteran, I want current and valid JobPosting supply behind Match results, so that my recommendations are based on usable opportunities.

## Implementation Decisions
- FYS-106: Declare the code-canonical workspace contract as `workspace.fys_bronze.job_postings`, `workspace.fys_silver.veteran_profiles`, and future `workspace.fys_gold.*`. Label conflicting `main`, `veteran_intake`, `for_your_service`, and transactions references as non-canonical until migrated.
- FYS-107: Organize responsibilities as datasource (source integrations and raw collection), integration (workspace tables and quality checks), ontology (Veteran, JobPosting, Match semantics), application (FastAPI serving), and sandbox (experiments with no business-of-record writes).
- FYS-108: Make bronze quality checks executable expectations immediately after landing. A nonzero duplicate-ID, missing-title, or missing-company result for the evaluated run must mark the pipeline failed and prevent downstream silver/gold execution; failures retain run diagnostics and quarantined evidence.
- FYS-109: Report the health triad: inbound source availability and row counts, build status and DQ result, and outbound readiness for the serving dependency. Health must distinguish stale data from an unavailable warehouse or model.
- FYS-118: Define one job-domain graph: source collection → canonical bronze JobPosting land → DQ abort gate → silver enrichment → gold embeddings/Match artifacts when available → serving-readiness publication. Use portable managed paths and explicit task dependencies.
- FYS-119: Quarantine the transactions-domain Spark prototype with a prominent non-canonical status. It may not write or advertise itself as the JobPosting production pipeline until it targets the workspace contract and passes the same DQ gate.
- FYS-120: Generate a lineage artifact from code and SQL references to `workspace.fys_*`, including source, bronze, silver, gold, and FastAPI serving reads. Review generation output in pull requests affecting pipeline references.
- Bronze landing must preserve source provenance, external source identifier, ingestion timestamp, and raw-payload traceability. The stable JobPosting key derives from source plus external job identifier; replays must be idempotent.
- This epic supplies the supporting data seam for Match serving. It does not define the E005 `ready_for_matching` profile gate; it only ensures the JobPosting side of the Match boundary is trustworthy.

## Testing Decisions
- Run a fixture ingestion batch and assert durable records are available in canonical bronze with source provenance and ingestion timestamp.
- Run the quality expectation task with duplicate IDs, missing titles, and missing companies independently; assert each failure blocks all downstream tasks and preserves diagnostics.
- Test a clean batch proceeds from bronze to the next allowed transform task and exposes row counts in the run record.
- Test idempotent replay of the same source/external-job pair and verify it does not create a duplicate active JobPosting.
- Contract-test the job graph has the required dependency order and contains no user-home execution paths.
- Test health reporting for source outage, DQ failure, stale bronze data, warehouse unavailability, and healthy serving readiness.
- Test that non-canonical transactions output cannot satisfy the serving-readiness check.
- Generate lineage from a fixture reference set and assert all published nodes use the `workspace.fys_*` names.

## Out of Scope
- Rebuilding the unrelated transactions prototype as a general-purpose medallion framework.
- Implementing full silver enrichment, real embeddings, ranking logic, or Match factor cards.
- Replacing the FastAPI serving contract or fully specifying the E005 Veteran profile gate.
- Historical migration of every legacy catalog and notebook in the same delivery slice.

## Further Notes
- Code-canonical spine: `workspace.fys_bronze.job_postings` → `workspace.fys_silver.veteran_profiles` → `workspace.fys_gold.*`; the JobPosting bronze relation is the pipeline's required serving input.
- GitHub parent epic: E013 = #104. Child FYS IDs: FYS-106, FYS-107, FYS-108, FYS-109, FYS-118, FYS-119, FYS-120.
- Slice 1 relevance: bronze landing plus a DQ abort gate are direct Slice 1 plumbing prerequisites; without them, FastAPI Match requests can only read empty, stale, or untrusted JobPosting candidates.
