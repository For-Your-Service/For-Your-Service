# SPEC-E003 — Silver Enrichment

## Problem Statement
Raw job postings are not yet suitable for transparent veteran-to-job matching. The repository contains two O*NET client implementations with different authentication, rate-limit, timeout, cache, and error-handling behavior. It also contains a small static MOS-to-O*NET mapping, a broader branch-aware military-role map, and a skill normalizer based mostly on local aliases. None currently establishes a durable job-domain silver contract. Treating a MOS as the answer would overfit military jargon; treating an unknown crosswalk as a failed match would hide valid civilian opportunities.

## Solution
Create an idempotent bronze-to-silver job enrichment flow in the canonical workspace catalog. It will normalize job text, extract and normalize skills with importance/provenance, assign standardized titles and industry sectors, and attach O*NET occupation candidates. It will also produce provenance-bearing MOS/AFSC/rating occupation-prior records that improve later ranking without becoming a hard eligibility filter. Use one production O*NET access boundary with deterministic caching, explicit rate limiting, and observable failures.

## User Stories
1. As a transitioning veteran, I want job descriptions translated into recognizable skills so that I can understand why a role fits my experience.
2. As a 7 Eagle counselor, I want standardized titles and industry sectors so that I can compare similarly named roles across providers.
3. As a matching-service maintainer, I want silver job records with structured skill importance and provenance so that ranking can use explainable evidence instead of opaque text.
4. As a veteran with MOS, AFSC, or rating history, I want likely civilian occupations represented as a soft prior so that military experience informs discovery without overriding my current skills and preferences.
5. As a veteran with a less-common military occupation, I want an empty or weak crosswalk to remain a valid profile state so that the system can still surface jobs through skills and text similarity.
6. As a data steward, I want each MOS occupation candidate to store its source, confidence, and mapping version so that counselors can distinguish a seed-table suggestion from an API-derived result.
7. As a platform operator, I want one O*NET client policy with credentials in secrets, bounded retries, timeouts, cache behavior, and rate limiting so that enrichment does not overload the provider or silently degrade.
8. As a platform operator, I want cached O*NET occupation and skill data to be reusable across runs so that repeat enrichment is fast, predictable, and respectful of provider limits.
9. As a data steward, I want every silver record to record its enrichment version and enriched date so that stale outputs can be identified and rebuilt.
10. As a release engineer, I want bronze-to-silver processing to be idempotent and partition-aware so that safe retries do not multiply enriched records.
11. As a quality owner, I want fixture-corpus coverage checks for standardized title and industry values so that generic enrichment rules have measurable quality.
12. As a serving maintainer, I want job enrichments to feed the canonical `workspace.fys_*` serving spine so that later embeddings and match retrieval use the same dataset the API serves.

## Implementation Decisions
- Establish one production O*NET access boundary and retire duplicate client behavior from the runtime path; preserve compatibility adapters only where needed during migration.
- Resolve O*NET credentials from managed secrets, apply explicit request timeouts and bounded retry policy, and enforce the selected documented rate-limit policy.
- Cache occupation profiles, skills, and normalized taxonomy results with TTL and metadata sufficient to refresh or invalidate stale entries.
- Preserve raw job text in bronze; produce clean, versioned silver properties for standardized title, industry sector, extracted skills, and occupation candidates.
- Represent skills as a structured collection containing raw term, canonical term, category, importance when available, confidence, extraction method, and taxonomy provenance.
- Use deterministic rules and taxonomy normalization before adding any probabilistic extraction; retain the evidence that produced each skill.
- Model MOS/AFSC/rating mappings as ranked occupation-prior candidates with branch, occupation code, confidence, source, and mapping version.
- Treat crosswalk results as a ranking feature only. No mapping, or a low-confidence mapping, must not exclude a veteran or job from later retrieval.
- Seed common Army 11/18/25 series mappings and support extension to other branches through the existing branch-aware map rather than assuming Army-only semantics.
- Make the silver transform an idempotent merge keyed by canonical job identity and enrichment version, with an enriched date and controlled partition strategy.
- Land all production silver output in the `workspace.fys_*` catalog spine; do not use a parallel catalog or the non-canonical transaction-domain filesystem pipeline.

## Testing Decisions
- Contract-test the selected O*NET client with mocked occupation, skills, knowledge, abilities, timeout, authentication, and rate-limit responses.
- Test cache hit, expiry, invalidation, and provider-error behavior; confirm a cache miss failure is observable rather than converted to fabricated taxonomy data.
- Unit-test skill normalization aliases, deduplication, fuzzy matching thresholds, categories, and structured provenance.
- Unit-test MOS, AFSC, and Navy rating mappings for common seed examples, including 11-, 18-, and 25-series Army records.
- Test that an unknown MOS or empty candidate set returns an explicit empty soft-prior result and does not cause an eligibility failure.
- Integration-test bronze-to-silver fixtures for deterministic standardized titles, industry sectors, skills, occupation candidates, enrichment version, enriched date, and idempotent reruns.
- Measure standardized-title and industry-sector fill rate on the fixture corpus; enforce the stated 80% target as a release criterion once the corpus is approved.
- Assert silver writes occur only on the canonical workspace catalog path and add a regression guard against the transaction lakehouse path.

## Out of Scope
- Replacing O*NET with a proprietary ontology or promising full coverage for every military specialty in the first release.
- Embedding generation, vector indexing, hybrid retrieval, final match scoring, and generated explanations.
- Using a MOS crosswalk as a hard filter, qualification determination, or civilian credential equivalency decision.
- Migrating unrelated transaction-domain medallion modules into the job-posting pipeline.

## Further Notes
- GitHub epic: **#30**. Child issue IDs: **FYS-020, FYS-021, FYS-022, FYS-023, FYS-024**.
- Lineage: canonical bronze JobPosting → clean/enriched job and occupation-prior data → canonical silver → gold embeddings and matching surface.
- Code is canonical: production enrichment must feed the `workspace.fys_*` serving spine. Existing duplicate O*NET clients and static maps are implementation evidence, not competing production contracts.
- Current reality is intentionally explicit: O*NET access is split across two clients, mapping data is thin/static, local caches exist, and no complete canonical silver job transform is wired today.
