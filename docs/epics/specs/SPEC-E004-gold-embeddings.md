# SPEC-E004 — Gold Embeddings

## Problem Statement
The current embedding generator constructs useful job and veteran text strings but returns `np.random.rand(384)` vectors for both. Those vectors are nondeterministic, carry no semantic meaning, and make cosine-based matching invalid. The primary match-serving path is organized around the `workspace.fys_*` catalog spine, so an embedding implementation that writes elsewhere cannot improve the actual service. Veteran embeddings also cannot rely on raw MOS jargon alone: military-to-civilian translation is required before semantic retrieval can accurately represent transferable experience.

## Solution
Replace placeholder vectors with a pinned, real text-embedding model, initially `sentence-transformers/all-MiniLM-L6-v2` unless a documented successor is selected. Generate deterministic normalized 384-dimensional embeddings from canonical silver job text and civilianized veteran profile text; persist model/version metadata and staleness state in canonical gold datasets. Provide an idempotent rebuild path and require match queries to select compatible embedding-model versions.

## User Stories
1. As a transitioning veteran, I want similar jobs to be retrieved because of real semantic overlap with my experience rather than a random score.
2. As a 7 Eagle counselor, I want recommendations to remain stable when the same profile and job data are processed again so that I can trust and explain repeat results.
3. As a matching-service maintainer, I want every gold vector to include its model identifier and dimension so that retrieval only compares compatible representations.
4. As a matching-service maintainer, I want job embeddings to use standardized title, description, and normalized skills so that postings are represented by the enriched evidence users recognize.
5. As a veteran, I want my embedding to use civilianized summary and normalized skills rather than only raw MOS terminology so that civilian roles can be discovered.
6. As a data steward, I want each embedding to retain source identity, input/enrichment version, created time, and stale status so that its lineage can be audited and rebuilt.
7. As a platform operator, I want a model upgrade to mark incompatible old vectors stale and launch a rebuild so that mixed-version vectors do not silently distort retrieval.
8. As a platform operator, I want a failed model load or encoding operation to make the pipeline unhealthy rather than fall back to random vectors.
9. As a release engineer, I want deterministic unit and integration tests for embeddings so that a placeholder or random fallback cannot return to the production path.
10. As a serving maintainer, I want gold embeddings and enrichment to land in the canonical `workspace.fys_*` spine so that the primary match-serving path can consume them.
11. As a matching-service maintainer, I want the selected model version filter applied to retrieval queries so that cosine similarity is computed only among compatible vectors.
12. As a program owner, I want an operational rebuild runbook so that a security, quality, or model-version change has a controlled recovery path.

## Implementation Decisions
- Replace random-vector placeholders with a pinned sentence-transformer model that produces 384-dimensional embeddings, unless a successor is formally approved with a documented compatibility and migration plan.
- Load the model once per execution context, use deterministic inference settings, validate output dimension, and normalize vectors according to the selected retrieval contract.
- Fail closed when model initialization or encoding fails. Production code must not generate random, zero, fabricated, or silently substituted vectors.
- Build job embedding text from canonical silver title, description, and normalized skills with stable field ordering and explicit handling of missing optional values.
- Build veteran embedding text from civilianized summary and normalized skills; use MOS as supplemental contextual evidence only after civilianization is available.
- Persist gold embeddings keyed by the business object identifier plus embedding model/version, with vector, dimension, input/enrichment version, created time, and stale/rebuild metadata.
- Make gold generation idempotent: unchanged canonical input and model version can be reused; changed input or model version produces a controlled replacement or new versioned row.
- Treat a model change as a rebuild event: mark prior-model rows stale, generate the new version, validate coverage, then point compatible serving queries at the new model.
- Keep gold writes and retrieval metadata within the canonical `workspace.fys_*` catalog spine, not a parallel catalog or the non-canonical transaction-domain filesystem lakehouse.
- Do not expose the model as proof of match quality; final rank remains a later multi-factor decision that must use compatible embeddings and explicit factors.

## Testing Decisions
- Unit-test that identical job and veteran input produces identical vectors for the pinned model within defined numeric tolerance.
- Unit-test output shape, dimension 384, finite values, normalization behavior, and cosine similarity of a nonzero vector with itself approximately equal to one.
- Unit-test stable text construction for job and veteran inputs, including missing optional fields, skill order normalization, and civilianized-summary precedence.
- Add a regression test that fails if the production path imports or invokes random-vector generation, including no random fallback after model-load failure.
- Integration-test a fixture bronze/silver-to-gold flow that stores canonical identifiers, vectors, model metadata, input/enrichment version, timestamps, and staleness state in the canonical gold destination.
- Test that a veteran with civilianized text produces an embedding from that text and skills, while MOS alone is not the sole semantic representation.
- Test model-version upgrades: old vectors are marked stale, the rebuild produces new compatible vectors, and a retrieval request filters to one model version.
- Test failure behavior for model download/load/encode errors; the run must fail visibly and must not report successful gold coverage.
- Add a regression assertion that gold tasks do not write to the non-canonical transaction lakehouse path.

## Out of Scope
- Training a custom embedding model, online learning, GPU fleet optimization, or a vector-database migration.
- Hybrid retrieval, hard filters, final multi-factor score weighting, explanation generation, and the neural matching path.
- Declaring MOS alone a sufficient veteran representation or producing match recommendations before civilianization dependencies are available.
- Rewriting the non-canonical transaction-domain medallion pipeline.

## Further Notes
- GitHub epic: **#31**. Child issue IDs: **FYS-030, FYS-031, FYS-032, FYS-033**.
- Lineage: canonical silver job/profile evidence → model-versioned gold Embedding → compatible retrieval/ranking → primary match-serving surface.
- Code is canonical: embeddings and enrichment must feed the `workspace.fys_*` path that primary serving uses. A gold dataset outside that spine cannot satisfy this epic.
- Current reality is intentionally explicit: the generator currently returns random 384-dimensional vectors; it is a placeholder and must never be treated as a valid semantic-embedding implementation.
