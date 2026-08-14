# SPEC-E006 — Matching Engine

## Problem Statement

The repository has two incompatible matching implementations: a usable cosine-based pipeline matcher and an experimental neural matcher that imports a class name the model does not export. Current embeddings are not production-real, and the serving path manufactures a `0.75` score instead of calculating one. This makes ranking, explanations, and user trust invalid.

## Solution

Adopt the pipeline cosine matcher as the sole Slice 1 ranking path for supplied fixture or real embeddings. It must calculate, threshold, filter, rank, and summarize actual vectors; it must never fabricate a score. Apply deterministic job constraints before ranking, then return each selected match with its calculated score, matching-skill metadata, applied filters, and factor data that can support grounded explanations.

The Siamese model remains experimental until real feature/embedding generation, an import-safe public API, trained weights, and evaluation evidence exist. Its `SiameseMatchingModel` versus `SiameseNetwork` name drift is resolved as a compatibility/API decision, not by silently selecting the neural path for Slice 1.

## User Stories

1. As a ready veteran, I receive jobs ordered by a score calculated from my embedding and each job embedding.
2. As a veteran, I never see a fixed score merely because a job was returned by the API.
3. As a veteran, I can set a minimum score and receive only matches whose calculated score meets it.
4. As a veteran, I can request a bounded number of top results and receive no more than that number.
5. As a veteran with a location constraint, I see local jobs and eligible remote jobs, but not unrelated on-site jobs.
6. As a veteran with a salary floor, I do not receive jobs whose known minimum compensation is below that floor.
7. As a veteran, I receive an honest empty result when no jobs meet the hard filters or similarity threshold.
8. As a counselor, I can see which matching skills, location rule, salary rule, and veteran-friendly status contributed to the returned result.
9. As a counselor, I can distinguish a calculated Slice 1 cosine score from a future multi-factor production score.
10. As a platform operator, I can tell whether matches were unavailable because no job data existed, no embeddings were supplied, filters excluded all jobs, or no jobs met threshold.
11. As a platform operator, I can run batch matching and preserve the correct candidate identifier in each result.
12. As a developer, I have one declared public matcher path for Slice 1 rather than two implementations with ambiguous selection.
13. As a developer, importing the experimental neural matcher does not fail because its public model class has a different name from the consumer expectation.
14. As a quality engineer, I can prove that identical vectors score 1.0, orthogonal vectors score 0.5 after normalization, opposite vectors score 0.0, and zero vectors score 0.0.
15. As a quality engineer, I can prove returned scores arise from fixture vectors and differ when fixture vectors differ.
16. As a future model owner, I can replace the Slice 1 embedding source with real versioned embeddings without changing the profile gate or serving response semantics.

## Implementation Decisions

- Slice 1 has one canonical matching path: the deterministic pipeline cosine matcher.
- Accept embeddings as explicit input to the matching boundary. If embeddings are absent, report matching as unavailable; do not generate random vectors or a fallback confidence.
- Normalize cosine similarity from `[-1, 1]` to `[0, 1]` and use the calculated value unchanged as the Slice 1 similarity score.
- Apply deterministic eligibility checks before ranking: location/remote eligibility, salary floor where parseable, and clearance eligibility when job metadata supports it.
- Treat unparseable or unavailable salary data as unknown, not evidence that a job satisfies a salary floor; document the selected product behavior in the factor payload.
- Preserve the searched-job count separately from returned matches so empty results remain explainable.
- Return matching-skill metadata only when it exists in the job record; it is not evidence of actual semantic overlap until the future factor model computes that overlap.
- Keep veteran-friendly prioritization explicit and bounded. If enabled, expose both the base similarity and applied boost/factor rather than presenting the boosted value as pure semantic similarity.
- Resolve the `SiameseMatchingModel` versus `SiameseNetwork` name drift under FYS-015, but retain the neural model as Experimental through Slice 1. FYS-017 records this routing decision.
- Do not claim hybrid retrieval, MOS priors, white-box multi-factor weighting, or LLM explanations are delivered by the cosine-only Slice 1 path.

## Testing Decisions

- Retain `tests/pipeline/test_job_matcher.py` as the prior-art baseline and extend it rather than replacing a working pipeline contract with neural tests.
- Test cosine normalization, zero-vector safety, descending rank order, threshold behavior, top-k, batch candidate IDs, salary parsing, location/remote filtering, and veteran-friendly ordering.
- Add deterministic fixture-vector tests that assert no returned score is a constant across distinguishable jobs.
- Add hard-filter tests for unavailable salary, active/inactive/no clearance metadata, and no-results reasons once those inputs are represented.
- Add a regression test that the chosen Slice 1 matcher imports and executes without importing the experimental neural path.
- Repair or delete tests that import nonexistent neural symbols or obsolete ingestion helpers; retain a pointer explaining any deliberately deferred neural coverage. This is FYS-016, not a reason to accept false-green tests.
- Add contract tests for the factor payload so explanation code cannot claim a skill or constraint absent from the matching input.

## Out of Scope

- Training, tuning, or serving the Siamese neural model.
- Random or placeholder embedding generation.
- Hybrid BM25+dense retrieval, MOS/O*NET priors, learned ranking, and calibrated outcomes.
- Full values, culture, mission, clearance, and compensation white-box weighting beyond the Slice 1 deterministic inputs.
- Natural-language explanations generated from model intuition.
- Persistent Match history, campaigns, and counselor action workflows.

## Further Notes

- Parent epic: GitHub #33. This is Slice 1 plumbing, not a claim that the long-term matching model is complete.
- Related children: FYS-015 unifies the neural public API; FYS-016 removes or repairs lying tests; FYS-017 records the single matcher path.
- The ontology object is `Match`, keyed by veteran, job, and model version. Its Slice 1 factor card must state that the score is cosine similarity from supplied embeddings.
- The Foundry sequencing remains: hard filters → ranked candidate set → factors → grounded narrative. Slice 1 supplies the first two pieces honestly and prepares the factor boundary.
