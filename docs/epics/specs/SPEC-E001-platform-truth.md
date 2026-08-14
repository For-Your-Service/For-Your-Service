# FYS-E001 — Platform Truth

## Problem Statement
For Your Service has competing names, deployment descriptions, credential claims, and repository roots. The running serving path is the authority: the Hugging Face FastAPI service reads JobPosting records from `workspace.fys_bronze.job_postings`, stores and retrieves Veteran profiles in `workspace.fys_silver.veteran_profiles`, and exposes Veteran registration, Veteran retrieval, and Match endpoints. Conflicting documents and prototypes create a risk that a contributor validates, deploys, or writes data to a system the service does not use.

## Solution
Establish one code-derived platform contract: Databricks Unity Catalog is the data system of record and Hugging Face FastAPI is the primary serving boundary for Veteran and Match requests. Publish a machine-checkable catalog map, a credential-status matrix, and a canonical-root guide. Demote alternate clouds, catalogs, and duplicate trees to explicitly labeled experiments until their code is wired into the production path.

## User Stories
1. As a platform engineer, I want one canonical `workspace.fys_*` catalog map, so that every data producer and consumer uses the same JobPosting, Veteran, and future Match namespaces.
2. As a FastAPI maintainer, I want the service boundary declared as the production surface, so that endpoint behavior is not confused with prototype deployments.
3. As a transitioning Veteran, I want Match results to come from the documented JobPosting store, so that the jobs I review are traceable to the operational pipeline.
4. As a 7 Eagle counselor, I want Veteran lookup and Match requests to use the same platform contract, so that I can trust the data shown to a Veteran.
5. As a data engineer, I want bronze, silver, and gold ownership documented, so that raw JobPosting ingestion, cleaned enrichment, and Match outputs have unambiguous destinations.
6. As a security owner, I want a current provider credential-status matrix, so that an expired source credential cannot silently make the bronze JobPosting supply empty.
7. As an operator, I want a deployment checklist that names one supported production path, so that releases exercise the same workspace and serving surface used by clients.
8. As a contributor, I want alternate AWS, GCP, local, and experimental paths visibly demoted, so that I do not mistake an unconnected prototype for production.
9. As a repository maintainer, I want a canonical root and a disposition for duplicate trees, so that fixes land in the codebase actually built and served.
10. As a reviewer, I want validation to detect missing expected workspace tables, so that documentation drift becomes a failing check rather than an incident.

## Implementation Decisions
- FYS-001: Define `workspace.fys_bronze.job_postings` as the canonical raw JobPosting relation and `workspace.fys_silver.veteran_profiles` as the canonical operational Veteran relation. Reserve `workspace.fys_gold.*` for versioned embeddings and persisted Match outputs when implemented.
- FYS-001: Represent object identity with stable string IDs: `veteran_id`, `job_id`, `partner_id`, and a Match identity derived from Veteran, JobPosting, and model version. Do not derive identity from row order or parsed identifiers.
- FYS-001: Provide a catalog-contract validator that checks the expected relations and reports a concise missing/extra/drift result. It must support a non-production soft-fail mode only when explicitly selected.
- FYS-002: Declare the production request boundary as the Hugging Face FastAPI Veteran and Match surface backed by the workspace catalog. The Match request reads the registered Veteran and JobPosting candidates; the response remains the contract for future real Match factors.
- FYS-002: Treat alternate deployment surfaces as experimental until they use the same workspace contract and pass the same readiness and deploy checks.
- FYS-003: Maintain a provider matrix containing provider, secret-name reference only, owner, verification timestamp, status, and degraded-mode behavior. Never place secret values in the matrix.
- FYS-003: Source failures must be visible in operational status and cannot be represented as a successful empty bronze run without an alert annotation.
- FYS-004: Declare one repository root, label nested or duplicate copies as deprecated or archive them through an approved migration plan, and ensure contributor instructions point only to the canonical root.
- The profile completeness gate, including `ready_for_matching`, is a dependency owned by E005. This epic defines the platform contract it will use but does not specify profile fields or gate rules.

## Testing Decisions
- Run the catalog-contract validator against a fixture workspace and verify that a missing bronze or silver relation fails with an actionable message.
- Contract-test Veteran registration and retrieval against the canonical silver relation, and Match requests against canonical JobPosting reads.
- Verify the documentation and deployment checklist name only the approved serving boundary and catalog spine.
- Test credential-status rendering with configured, missing, invalid, and degraded providers; assert no secret value is emitted.
- Test the canonical-root guidance by checking that duplicate-tree references either redirect or carry a deprecation label.

## Out of Scope
- Historical data migration between competing catalogs.
- Replacing the current Match algorithm, embeddings, or factor-card implementation.
- Building the E005 profile schema and `ready_for_matching` rules.
- Removing experimental cloud code without a separately approved retention or archival decision.

## Further Notes
- Code-canonical spine: `workspace.fys_bronze.job_postings` → `workspace.fys_silver.veteran_profiles` → `workspace.fys_gold.*`; serving behavior is authoritative over conflicting documentation.
- GitHub parent epic: E001 = #28. Child FYS IDs: FYS-001, FYS-002, FYS-003, FYS-004.
- Slice 1 relevance: this is a prerequisite for the plumbing slice because real Match serving cannot be trusted while producers, consumers, and deployment guidance disagree about the workspace contract.
