# SPEC-E010 — Partner Placement

## Problem Statement

7 Eagle and future placement partners need a governed view of a cohort’s progress from profile readiness through interview and offer, without turning partner reporting into an uncontrolled view of veteran PII. A partner, cohort relationship, aggregate funnel, and outcome contract do not yet have source owners. Building the dashboard before the profile, match, and campaign writeback foundations are reliable would create metrics detached from the actual workflow.

This epic is a later-milestone partner surface over the existing Veteran, Match, and Campaign boundaries. It must consume approved operational records and aggregate them; it must not create its own placement flow or rerun matching.

## Solution

Establish a Partner object, a governed Veteran-to-Partner cohort membership, controlled batch intake, and a placement SITREP:

1. Partner administrators can define a partner and approved cohort scope.
2. Authorized users can ingest a cohort through a validated file or API contract, receive a per-row result, and correct failures without partially obscuring what occurred.
3. Partner users can see policy-appropriate aggregate funnel health, response rates, interview activity, offers, and trend periods, with tightly controlled drill-down.
4. Authorized veteran or partner workflows record verified placement milestones through `RecordOutcome`.
5. The SITREP derives its metrics from profile, match, campaign, outreach, and outcome records with explicit denominator and time-window definitions.

## User Stories (LONG)

- As a 7 Eagle program administrator, I can create a partner organization and define authorized users, so cohort data is associated with the organization responsible for supporting it.
- As a placement counselor, I can assign a veteran to the correct partner cohort through an approved process, so the veteran appears in the right support program without duplicating their profile.
- As a partner administrator, I can upload a cohort file or submit a batch request and receive row-level validation results, so I can fix missing or invalid records before they affect reporting.
- As a counselor, I can distinguish created, updated, rejected, and skipped batch rows with a reason, so a retry does not silently duplicate veterans or overwrite information unexpectedly.
- As a partner user, I can view a funnel SITREP for my permitted cohort—profile-ready, matched, campaign-active, applied, outreach activity, interviews, and offers—so I can direct staff attention to the stage with the greatest blockage.
- As a partner user, I can compare a current reporting period with a defined baseline, so an apparent improvement or decline has a meaningful denominator and time window.
- As a counselor, I can drill into a permitted veteran’s current stage and next action when policy allows, so aggregate reporting leads to productive placement support rather than surveillance.
- As a partner executive, I can export a PII-minimized weekly SITREP, so I can discuss program performance without distributing personal contact details or unnecessary sensitive information.
- As an authorized veteran or partner representative, I can record interview and offer milestones with dates and attribution, so offer-before-ETS and time-to-first-interview are calculated from actual events.
- As a program analyst, I can see data-quality indicators for unknown ETs, missing campaign links, incomplete profiles, and unverified outcomes, so the dashboard does not present weak data as a definitive placement rate.
- As a veteran, I can trust that a partner sees only the cohort and fields permitted by policy, so participation in a placement program does not expose unrelated personal information.

## Implementation Decisions (no file paths)

- Introduce Partner as a first-class object with a stable string identifier. Represent cohort membership as an explicit Veteran-to-Partner relationship with effective dates and policy context; do not copy the Veteran object into partner storage.
- Establish an explicit source owner for Partner and Campaign domain contracts before implementation begins. No existing production source module owns either object today.
- Require authenticated, authorized actions for partner administration, cohort intake, drill-down, export, and outcome recording. Default partner reporting to aggregate, PII-minimized views.
- Make batch intake idempotent using a documented external row key or validated identity resolution process. Return an auditable per-row result and avoid blind upserts.
- Derive funnel stages from canonical profile, Match, Campaign, outreach, and outcome records. Do not create a partner-only match runner, alternative campaign stage, or copied analytics score.
- Use `RecordOutcome` for interview and offer timestamps and retain outcome source, recorder, and verification status. Define correction/audit semantics rather than destructive history edits.
- Publish metric definitions with numerator, denominator, inclusion/exclusion rules, reporting window, partner/cohort scope, and missing-data behavior.
- Support export only from the permitted aggregate projection, with explicit column selection and export audit metadata.

## Testing Decisions

- Test partner and cohort access boundaries for administrator, counselor, veteran, and unauthorized users, including cross-partner isolation.
- Test cohort batch validation, idempotent retry, per-row error reporting, and behavior when only part of a batch is valid.
- Test that aggregate SITREP counts reconcile to canonical source events across profile, match, campaign, outreach, interview, and offer fixtures.
- Test metric formulas for offer-before-ETS and time-to-first-interview, including missing ETS dates, multiple interviews, corrections, and excluded/unverified outcomes.
- Test aggregate-first rendering, permitted drill-down, export column minimization, and absence of restricted PII in partner-facing payloads.
- Test `RecordOutcome` authorization, immutable audit history, and downstream SITREP refresh behavior.

## Out of Scope (explicitly: before Slice 1 done)

- Before Slice 1 plumbing is done, this epic does not introduce a Partner-owned profile store, parallel matching/ranking path, copied Campaign workflow, or dashboard metrics based on fake match results.
- Billing, contracts, partner marketplace features, cross-organization data sharing, and automated eligibility decisions are out of scope.
- Full CRM case management and broad data-warehouse reporting are out of scope; the first delivery is a governed placement SITREP.

## Further Notes

- GitHub epic: **#37**. FYS children: **FYS-090** Partner organization object, **FYS-091** cohort/batch veteran ingest, **FYS-092** funnel SITREP dashboard, and **FYS-093** placement outcome metrics.
- Ontology links: Veteran `belongs_to` Partner; Campaign targets opportunities; verified outcomes provide the proof layer. E010 is the “Prove” stage and deliberately depends on upstream truth.
- Foundry actions: `RecordOutcome` is E010’s core writeback. `CompleteProfile`, `RunMatch`, `StartCampaign`, and `LogOutreach` are upstream action records consumed for funnel visibility, not recreated by partner tooling.
