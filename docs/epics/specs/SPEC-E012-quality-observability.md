# SPEC-E012 — Quality & Observability

## Problem Statement

For Your Service cannot prove trustworthiness with a passing UI alone. The profile gate, canonical Match serving boundary, data quality checks, explanation contract, campaign writes, and placement outcomes require tests and operational signals that reveal whether the system is fresh, correct, safe, and useful. Existing quality checks and health concepts are incomplete as a delivery gate, while later placement metrics must not be interpreted before their upstream event lineage is dependable.

This epic validates and observes the canonical path. It must not add a test-only match algorithm, synthetic production score, alternate pipeline, or monitoring data store that becomes a parallel business-of-record.

## Solution

Create a layered quality and observability program:

1. Unit and integration tests protect deterministic profile readiness, hard filters, ranking-factor behavior, response contracts, and grounded explanations.
2. An offline evaluation harness measures Precision@k and NDCG on versioned, consented/labeled veteran-to-job fixtures with documented relevance and slice definitions.
3. Monitoring tracks the pipeline health triad—input freshness, build/data-quality health, and output/serving health—plus match gate outcomes, latency, empty results, error rates, and explanation/factor-card coverage.
4. A daily operations runbook ties each alert or failed check to an owner, threshold, diagnostic step, and safe recovery action.
5. Placement instrumentation records lifecycle events as the result of action writebacks, allowing outcome measures to reconcile to the campaign funnel instead of relying on client-only analytics.

## User Stories (LONG)

- As a veteran, I can rely on a match result not being produced from a placeholder embedding, hardcoded score, or unready profile, so the product does not create false confidence at a critical transition point.
- As an engineer, I can run focused tests for the profile gate, filters, factor scoring, explanation contract, and empty-result behavior, so a regression is diagnosed near the rule that broke.
- As an engineer, I can run an integration scenario from completed profile through canonical match response and campaign handoff, so separate components are proven to preserve identifiers, factors, and action eligibility.
- As a product owner, I can review offline Precision@k and NDCG by documented cohort and job slice, so changes to matching are evaluated against relevance rather than only code coverage.
- As a product owner, I can see evaluation data version, match-model version, labeling guidance, and exclusions, so a headline metric cannot be mistaken for a general guarantee.
- As an operator, I can tell whether source input arrived, whether the build passed quality gates, and whether serving is ready, so “healthy” is not reduced to a running web process.
- As an operator, I can see match latency, request failures, gate rejections, empty-result rates, and factor-card coverage, so I can distinguish an infrastructure incident from an overly strict user constraint or a data-supply problem.
- As an operator, I receive an actionable alert with a named owner and runbook step when freshness, data quality, serving readiness, or error thresholds are breached, so alerts lead to recovery rather than dashboard noise.
- As a counselor or program lead, I can see whether profile completions, match views, campaign starts, outreach, interviews, and offers reconcile, so placement success is measured as a workflow rather than a page-view count.
- As a privacy-conscious veteran, I can expect monitoring and evaluation to use minimized, pseudonymous, or aggregate data where possible, so observability does not become an uncontrolled copy of my profile.
- As a release manager, I can compare a change against a baseline and block promotion when critical canonical-path checks regress, so new experience work cannot silently bypass the quality gate.

## Implementation Decisions (no file paths)

- Define a canonical-path test matrix covering `CompleteProfile`, `RunMatch`, `StartCampaign`, `LogOutreach`, and `RecordOutcome`; test action contracts and state transitions rather than duplicating their business logic in fixtures.
- Treat serving response identifiers, factor cards, explanation fields, model/version metadata, and empty-result semantics as compatibility contracts.
- Include explicit regression tests that reject random/placeholder embeddings and hardcoded successful match scores on the production path.
- Use deterministic fixture data for unit and integration tests. Keep separately governed, versioned labeled data for offline relevance evaluation; prohibit production PII in default test runs.
- Calculate Precision@k and NDCG with documented relevance labels, candidate-set rules, k values, segment definitions, and a stored baseline. Report uncertainty or insufficient sample size rather than overclaiming.
- Instrument the in/build/out health triad: source freshness and counts; data-quality/build outcomes; and serving readiness plus request behavior. A process liveness signal alone is insufficient.
- Emit lifecycle events from successful action writebacks, deduplicate by action/event identifier, and reconcile them to authoritative campaign/outcome records. Client telemetry may supplement usability analysis but cannot be the source of placement truth.
- Define alert thresholds, ownership, severity, retention, PII minimization, and runbook links before enabling paging or automated escalation.

## Testing Decisions

- Add unit coverage for profile completeness, match preconditions, hard filters, scoring-factor bounds, grounded-explanation rendering, and no-result behavior.
- Add integration coverage for canonical profile → match → campaign → outreach → outcome flows, including rejected writes, retries, and idempotent event emission.
- Add contract tests for serving response shape and version fields, including graceful handling when embeddings or downstream dependencies are unavailable.
- Add data-quality and freshness test fixtures that exercise successful, stale, malformed, duplicate, and partial-source inputs.
- Add offline-evaluation tests that validate label schema, metric calculations, segment filtering, and baseline comparison; use a small deterministic fixture for continuous runs.
- Add observability tests for metric/event emission, cardinality/PII safeguards, alert threshold evaluation, and runbook references.
- Perform periodic accessibility and security regression checks for surfaced quality states, while keeping dedicated authorization and privacy controls in their owning epic.

## Out of Scope (explicitly: before Slice 1 done)

- Before Slice 1 plumbing is done, this epic does not certify match quality, publish placement-success claims, or build dashboards on random embeddings, hardcoded scores, broken profile imports, or a parallel match path.
- Online learning-to-rank, autonomous score tuning, production A/B experimentation on veterans, and an enterprise-wide observability platform are out of scope.
- Partner-facing cohort dashboards are E010 work; this epic provides the trustworthy test, event, and operational foundations they consume.

## Further Notes

- GitHub epic: **#39**. FYS children: **FYS-110** match-path tests, **FYS-111** Precision@k/NDCG harness, **FYS-112** monitoring hooks, **FYS-113** daily operations runbook update, and **FYS-114** placement-success instrumentation.
- Ontology focus: Match evidence, pipeline health, and outcome lineage. The epic spans “Operate” and supports “Prove”; it validates the serving boundary rather than replacing it.
- Foundry actions: `CompleteProfile`, `RunMatch`, `StartCampaign`, `LogOutreach`, and `RecordOutcome` define the event lineage. The action write is authoritative; instrumentation observes it and never invents a second writeback.
