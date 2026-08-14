# SPEC-E007 — Serving API

## Problem Statement

The current FastAPI surface registers and reads a legacy profile shape, then returns job rows with a hardcoded `0.75` match score and invented reasons. It neither evaluates `ready_for_matching` nor uses the working pipeline matcher. It also permits wildcard CORS while credentials are enabled. As the canonical serving consumer, this boundary must report what the system actually knows.

## Solution

Make FastAPI the honest Slice 1 surface for the Veteran and Match ontology objects. Veteran upsert/get flows must materialize the profile completeness result. `POST /match` must load the veteran, reject a profile that is not `ready_for_matching`, obtain eligible job and embedding inputs from the canonical catalog spine, and delegate ranking only to the pipeline matcher. When required embeddings or dependencies are unavailable, return a clear unavailable response instead of fake matches.

Match responses must contain calculated scores and provenance/factors sufficient for a template-based, grounded explanation. Separate process health from readiness, and replace permissive CORS with an explicit frontend allowlist before production exposure.

## User Stories

1. As a veteran, I can create or update my profile and receive my stable veteran identifier, profile status, timestamp, readiness state, and missing-field list.
2. As a veteran, I can retrieve my profile summary and see what remains before matching can start.
3. As a veteran with an incomplete profile, a match request is rejected with a client error that includes the missing fields and does not query or rank jobs.
4. As a ready veteran, a match request returns only calculated results from the selected Slice 1 matcher.
5. As a ready veteran, I receive an empty list with an explicit result state when no eligible jobs meet filters or threshold.
6. As a ready veteran, I receive a service-unavailable response when the job embeddings required for ranking are unavailable; I am not shown synthetic results.
7. As a frontend, I can request top-n results, location filtering, and a minimum score within documented limits.
8. As a frontend, I can render title, company, location, compensation when present, computed score, factors, concerns, and source URL for every returned match.
9. As a counselor, I receive the same gated result contract as the veteran so recommendations cannot diverge by client.
10. As a consumer, I can distinguish not found, profile incomplete, no eligible matches, and matching unavailable through documented status codes and response payloads.
11. As an operator, I can use `/health` to verify process liveness without treating it as evidence that the database or matcher is usable.
12. As an operator, I can use `/ready` to see whether canonical data connectivity and the configured matching inputs are usable.
13. As a security owner, I can identify every browser origin permitted to call the API and confirm that credentialed requests never use a wildcard origin.
14. As a developer, OpenAPI documents the profile gate, match request parameters, success payload, and unavailable/incomplete error payloads.
15. As a developer, all reads and writes use the code-canonical catalog spine: veteran operational records in `workspace.fys_silver.veteran_profiles`, job postings in `workspace.fys_bronze.job_postings`, and gold inputs only once real embeddings are available.
16. As a developer, errors from database access are logged and mapped to intentional API responses without leaking connection details or raw exception strings.

## Implementation Decisions

- Treat FastAPI as the Slice 1 surface, not as an alternate matching engine.
- Evaluate and persist profile completeness during veteran create/update; the match action reads the resulting readiness state rather than reconstructing it ad hoc.
- Enforce `ready_for_matching` before any job retrieval or match calculation.
- Route successful ranking only through the pipeline cosine matcher selected by FYS-017; do not import or instantiate the experimental neural matcher on the serving path.
- Remove the hardcoded `0.75` score and generic “Technical skills match” / “Experience level fit” reasons. Each score and reason must derive from returned matcher data.
- Use an explicit unavailable result when embeddings are not real, not loaded, wrong shape, or otherwise unusable. An unavailable match engine is not a successful empty search.
- Preserve a distinct successful empty result for a ready veteran when data and embeddings are available but filters or threshold yield no matches.
- Return factor/provenance data that labels the Slice 1 score as calculated cosine similarity and identifies filters applied; template explanations may only reference those factors.
- Use `workspace.fys_silver.veteran_profiles` and `workspace.fys_bronze.job_postings` as the code-canonical serving records. Introduce `workspace.fys_gold.*` only with real, versioned embeddings.
- Define `/health` as process liveness and `/ready` as dependency readiness, including catalog reachability and matching-input availability.
- Configure CORS with a maintained explicit frontend allowlist. Never combine `allow_credentials=True` with a wildcard origin.
- Keep authentication, rate limiting, caching, and persistent match writeback outside Slice 1 while shaping errors so those controls can be added without changing gate semantics.

## Testing Decisions

- Start from `tests/pipeline/test_job_matcher.py` as the verified ranking prior art; API tests must use its deterministic fixture embeddings rather than live catalogs or generated vectors.
- Add FastAPI contract tests for profile creation/update, profile retrieval, matching with a missing veteran, and matching with a ready veteran.
- Add a gate test that an incomplete profile returns 400 or 422 with the documented missing-field list and proves the job query/matcher were not called.
- Add an integration test that a ready fixture profile and two distinct job vectors produce ordered, nonconstant scores through the HTTP endpoint.
- Add regression tests that reject a match response containing the old hardcoded score or generic ungrounded reasons.
- Add tests distinguishing empty eligible results from matcher-unavailable responses.
- Add `/health` and `/ready` tests for dependency-ready and dependency-not-ready states.
- Add CORS preflight and credentialed-origin tests for each allowed frontend plus a rejected unlisted origin. The existing wildcard-with-credentials configuration is a security defect and must not be preserved as a compatibility fixture.
- Repair tests that target missing neural symbols or obsolete contracts; do not mark this API complete while such tests merely fail at import time (FYS-016).

## Out of Scope

- UI wizard or recommendation dashboard.
- Authentication/authorization implementation, rate limiting, cache policy, and data-retention controls.
- Persistent Match objects, campaign actions, counselor workflow, and notification delivery.
- Real embedding generation, hybrid retrieval, trained neural inference, MOS priors, and outcome-calibrated scores.
- Broad catalog migrations or a replacement for the canonical Databricks/HF serving path.

## Further Notes

- Parent epic: GitHub #34. This specification delivers the Slice 1 serving seam between a completed Veteran and honest Match results.
- Relevant children: FYS-015 resolves neural naming drift, FYS-016 repairs lying tests, FYS-017 selects the pipeline matcher, and FYS-045 makes the profile package importable.
- The ontology action is `RunMatch`; its submission criterion is `ready_for_matching == true`. It creates a response/factor-card contract now and can persist Match objects later.
- Lineage is canonical job source → serving retrieval → deterministic matcher → factorized API response. No LLM may calculate scores or invent reasons.
