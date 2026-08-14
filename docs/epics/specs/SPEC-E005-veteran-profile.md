# SPEC-E005 — Veteran Profile System

## Problem Statement

Transitioning veterans cannot receive trustworthy recommendations from an incomplete profile. The Slice 1 model layer already captures identity, military background, constraints, and self-understanding, but package imports are currently broken and the serving profile shape does not yet enforce the same completion contract. Matching must not begin until the veteran has supplied the information needed to judge fit rather than merely MOS similarity.

## Solution

Make the veteran profile the canonical ontology object for Slice 1 and expose a clean package boundary around it. Preserve the required self-understanding sequence—Five Elements, career archetype, and complete Operator Compass—alongside military facts and preferences. Evaluate completeness into an explicit `ready_for_matching` gate with a machine-readable list of missing fields. The serving API must persist and return this gate state, and match serving must reject profiles that are not ready.

The canonical operational record is the Veteran object in `workspace.fys_silver.veteran_profiles`; matching receives an anonymized feature projection rather than direct contact information.

## User Stories

1. As a transitioning veteran, I can enter exactly three Five Elements so the service understands the conditions that make work sustainable for me.
2. As a transitioning veteran, I cannot submit duplicate Five Elements because repeated priorities do not describe three distinct needs.
3. As a transitioning veteran, I can choose a primary career archetype and, optionally, a secondary archetype to express how I prefer to create value.
4. As a transitioning veteran, I can answer all four Operator Compass prompts—energy, environment, mission, and family needs—before I am told that matching is available.
5. As a transitioning veteran, I can record positive and negative preferences so recommendations can avoid known no-go conditions.
6. As a transitioning veteran, I can provide a WHY statement and the problems I want to solve without either becoming a hard requirement for Slice 1 matching.
7. As a transitioning veteran, I can supply branch, MOS/AFSC/rating, rank, years of service, clearance status, and separation timing so the service has accurate military context.
8. As a transitioning veteran, I can set location, remote preference, relocation willingness, commute radius, salary bounds, skills, certifications, and target roles.
9. As a transitioning veteran, I receive a precise missing-field list instead of a vague “profile incomplete” message.
10. As a transitioning veteran, I cannot run matching while any required identity, military, self-understanding, or preference section is incomplete.
11. As a counselor, I can inspect the same readiness result as the veteran and help close specific intake gaps.
12. As a counselor, I can use the veteran identifier and matching features without receiving unnecessary contact PII in analytics or matching payloads.
13. As a serving client, I can import the profile package successfully and construct the canonical profile model without hidden missing-module failures.
14. As a downstream matching component, I receive a stable, PII-minimized feature projection including military context, constraints, archetype, Five Elements, targets, and preferences.
15. As a platform operator, I can distinguish an incomplete profile from a ready profile deterministically without inferring readiness from row presence or timestamps.

## Implementation Decisions

- Treat the dataclass profile model and its nested value objects as the Slice 1 domain contract; do not introduce a competing profile taxonomy.
- Require exactly three unique Five Elements, one primary archetype, and a complete four-answer Operator Compass for self-understanding readiness.
- Define readiness as the conjunction of identity, military, self-understanding, and preferences completion; retain the missing-field list as the response contract for remediation.
- Keep direct contact data in the operational profile only. Matching and analytics consume the anonymized feature projection.
- Keep clearance level, clearance status, and optional polygraph/expiration separate; an absent clearance must not be represented as an active clearance.
- Preserve optional profile enrichment—secondary archetype, time allocations, WHY statement, civilianized summary, and certifications—without allowing it to silently bypass required intake.
- Restore a slim, import-safe public package surface. FYS-045 is a Slice 1 child and must be complete before API integration depends on it.
- Use the code-canonical `workspace.fys_silver.veteran_profiles` record for serving persistence; do not create a fourth catalog or table name.

## Testing Decisions

- Add model tests for duplicate or non-three Five Elements, incomplete Operator Compass answers, and each false branch of readiness.
- Add a profile-package smoke test that imports the public API in a clean interpreter; this closes the FYS-045 regression rather than masking it with a local import.
- Test the completeness response as data: required sections, `ready_for_matching`, and ordered or explicitly documented missing fields.
- Test that the anonymized matching projection excludes name, email, phone, ZIP code, and other direct contact fields while retaining matching inputs.
- Add API contract tests that verify a persisted incomplete profile cannot be treated as ready by either `POST /veteran` or `POST /match`.
- Use realistic generic fixtures plus the approved partner-demo fixture. Do not use live PII in unit tests.

## Out of Scope

- Authentication and authorization policy for profile writes.
- Full UI intake wizard, therapy/coaching workflows, or counselor case-management UX.
- Automated military-to-civilian translation and embedding generation.
- Campaign creation, outreach, applications, or partner cohort reporting.
- Changing non-canonical lakehouse schemas or backfilling historical profile records.

## Further Notes

- Parent epic: GitHub #32. This specification supports the Slice 1 profile gate before any recommendation is surfaced.
- Relevant children: FYS-045 repairs the import boundary; FYS-015, FYS-016, and FYS-017 complete the dependent matching plumbing.
- The ontology action is `CompleteProfile`; its binary submission criterion is `ready_for_matching == true`.
- Lineage: operational profile → PII-minimized matching features → Match object/factor card → serving response.
