# SPEC-E008 — Veteran Experience

## Problem Statement

A transitioning veteran needs a trustworthy way to move from a complete profile to a decision about a real opportunity. Today, the intended experience is fragmented: the profile gate, match response, explanations, and practical career advice do not form one usable decision flow. A score by itself is not enough; the veteran must be able to see why an opportunity fits, what constraints were applied, and what action to take next without being asked to interpret opaque model behavior.

This epic is the **surface** over the canonical Match serving boundary. It must consume the gated match result and its factor card; it must not create a browser-only scoring, retrieval, or profile-read path.

## Solution

Deliver a responsive veteran-facing experience with four connected moments:

1. A profile-creation wizard that captures the required self-understanding, military, and preference information, makes incompleteness visible, and invokes `CompleteProfile`.
2. A recommendation dashboard that invokes `RunMatch` only for a match-ready veteran and displays the returned ranked opportunities, pathway indicators, and grounded next actions.
3. A match-detail view that renders the returned factor card, hard-filter context, and explanation as evidence for the displayed score.
4. Actionable, clearly labelled career tips drawn from the existing recommendation capability—resume improvements, job-search tips, networking advice, and skill-development steps—without presenting generic advice as match evidence.

The experience should guide “find → decide → act.” Starting a campaign is a handoff to E009 rather than a second match system.

## User Stories (LONG)

- As a transitioning veteran, I can begin a guided profile instead of facing one large form, so I understand why self-understanding, military experience, and job constraints are all needed before recommendations can be trusted.
- As a veteran completing my profile, I can see which required answers remain and why they block matching, so I can correct missing information rather than receiving a vague failure after submitting.
- As a veteran, I can review the information that will be used for matching before completing my profile, so I retain control over how my military background, civilianized strengths, location, salary, clearance, and preferences are represented.
- As a veteran whose profile is not ready, I receive an actionable incomplete-profile state rather than empty or fabricated recommendations, with a direct route back to the missing section.
- As a match-ready veteran, I can run a match and see a ranked list of opportunities sourced from the serving boundary, so every displayed opportunity is governed by the same hard filters and scoring rules.
- As a veteran considering an opportunity, I can open its factor breakdown and see the applied constraints, positive fit factors, and limitations, so I can decide whether to apply without treating a percentage as a black box.
- As a veteran, I can distinguish “good match,” “prepare,” and “not currently viable” guidance from the evidence that produced the match, so helpful advice never disguises itself as a model fact.
- As a veteran, I can receive resume, job-search, networking, and skill-development suggestions tailored to the available profile, gap, and target-job information, so the dashboard helps me improve my readiness as well as browse opportunities.
- As a veteran with no eligible results, I receive a clear explanation that filters or available jobs produced no results and a safe next action, so the product does not imply that I am unplaceable.
- As a keyboard-only, screen-reader, or mobile user, I can complete the wizard, inspect a match explanation, and choose the next action without losing context or relying on color alone.
- As a counselor assisting a veteran, I can recognize the same profile-ready and match-result states used by the veteran, so guidance during a session is consistent with the serving response.

## Implementation Decisions (no file paths)

- Treat `CompleteProfile` as the only transition to match-ready status; the UI validates for usability, but the server remains authoritative for the gate.
- Treat `RunMatch` as the only recommendation source. Preserve returned job identifiers, factor cards, explanations, model/version metadata, and empty-result semantics instead of recalculating scores or fetching a parallel job list.
- Render explanations from returned factors. Narrative or tip content must be labelled separately and must not claim a skill, preference, clearance, or employer fact absent from the factor card.
- Keep career tips as a supplementary readiness panel based on the existing recommendation contract: resume improvements, job-search tips, networking advice, skill-development plan, and estimated timeline.
- Keep profile editing, match execution, and campaign initiation as explicit user actions with loading, retry, and error states. Do not auto-run writes on page load.
- Use accessible semantic controls, visible focus, error summaries, non-color status cues, and responsive layouts as baseline experience requirements.
- Handoff a selected or manually targeted job to `StartCampaign`; do not persist campaign state in the veteran-experience surface.

## Testing Decisions

- Cover each wizard step, review state, incomplete-profile state, and server-returned missing-field error.
- Verify a ready profile invokes the canonical match action once and renders returned ordering, factor data, explanation, and empty-result response without client-side score changes.
- Verify that factor cards and explanations never render claims not present in the supplied response fixture.
- Test tip panels against representative recommendation fixtures, including no tips and partial gap-analysis data.
- Run keyboard navigation, screen-reader-label, focus-management, color-contrast, and narrow-screen checks for wizard and match-detail flows.
- Add integration coverage for the complete profile → match → select opportunity handoff, with campaign creation represented only as the E009 action boundary.

## Out of Scope (explicitly: before Slice 1 done)

- Before Slice 1 plumbing is done, this epic does not build a replacement profile API, client-side eligibility gate, browser-side matching/ranking path, or fake recommendation cards.
- Email notifications, a full messaging center, autonomous application submission, and a native mobile application are out of scope.
- Campaign workflow, outreach logging, partner visibility, and placement outcomes belong to E009/E010 actions after the Slice 1 match foundation is reliable.

## Further Notes

- GitHub epic: **#35**. FYS children: **FYS-070** profile creation wizard, **FYS-071** recommendation dashboard, **FYS-072** match explanation UI, **FYS-073** notifications, and **FYS-074** accessibility pass.
- Ontology surface: Veteran → Match → JobPosting, with Match factor-card evidence. This is the “Surface” stage of the FYS pipeline.
- Foundry actions: `CompleteProfile` prepares the Veteran; `RunMatch` produces the served Match; `StartCampaign` is the deliberate writeback handoff. `LogOutreach` and `RecordOutcome` are not veteran-experience writes.
