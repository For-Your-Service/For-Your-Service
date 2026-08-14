# SPEC-E009 — Campaign & Pathways

## Problem Statement

Veterans and counselors need more than a ranked job list: they need a lightweight operating system for deciding where to invest effort, applying through the formal channel, pursuing warm outreach, and tracking progress. Without a Campaign object, the relationship among a job, employer research, application, outreach, and outcome is lost. Without pathway context, veterans cannot reliably distinguish a direct application from a SkillBridge, federal-preference, fellowship, or other channel.

Campaign is currently a planned ontology object with no production source owner. This epic must therefore follow, and write back from, the canonical Match serving boundary. It must not introduce a separate match list, campaign score, job store, or profile model.

## Solution

Introduce a campaign workflow around a deliberate target:

1. A veteran or counselor starts a campaign from an existing Match or a documented manual target using `StartCampaign`.
2. The campaign stores its target, research decision, bidirectional Go/No-Go factors, funnel stage, application state, outreach tasks, pathway tags, and response signals.
3. The workflow provides a clear next action: Apply Now, Prepare, Monitor, or Bypass; same-day ATS application and a warm-path task list can coexist.
4. `LogOutreach` records outreach activity and responses against the campaign rather than in free-form, disconnected notes.
5. Existing match evidence remains immutable provenance for the decision. Campaign research adds decision context; it does not alter the Match score.

## User Stories (LONG)

- As a transitioning veteran, I can start a campaign from a recommendation I selected, so the opportunity, its match evidence, and my next steps remain connected.
- As a veteran, I can create a manual campaign target when I find an opportunity outside the current result set, so I can organize my search without pretending that the job received a canonical match score.
- As a veteran, I can record a Go/No-Go decision with explicit factors such as location, compensation, clearance, mission, readiness, and employer research, so I know why I should apply now, prepare, monitor, or bypass.
- As a veteran, I see location and other non-negotiable constraints called out as hard blockers, so a promising employer does not override conditions that make the role infeasible.
- As a veteran, I can keep an ATS application task and warm outreach tasks in the same campaign, so I can pursue the Side Door without losing the formal application path.
- As a veteran, I can log whom I contacted, the purpose, date, response status, and follow-up step, so outreach is a measurable sequence rather than a memory-dependent activity.
- As a veteran, I can see a campaign move through Target, Research, Apply, Outreach, Interview, and Offer (or a documented equivalent), so I can immediately identify stalled opportunities and decide what to do next.
- As a veteran close to ETS, I can see eligibility-sensitive pathways and time warnings for SkillBridge/CSP opportunities, so I do not learn about a deadline after it has passed.
- As a veteran eligible for federal preference, I can recognize relevant USAJOBS opportunities and receive clearly scoped guidance, so I can use the appropriate channel without making unsupported eligibility claims.
- As a counselor, I can help prioritize multiple campaigns using visible decision factors and stages, so coaching focuses on the next highest-value action rather than an undifferentiated job list.
- As a veteran, I can preserve a bypassed or monitored campaign with a stated reason, so later decisions and counselor conversations have context without polluting active work.

## Implementation Decisions (no file paths)

- Define Campaign with a stable string identifier and explicit foreign keys for veteran, optional partner, linked job, and optional originating match. Do not encode business meaning in identifiers.
- Start campaigns through `StartCampaign` only after validating an existing Match or recording a manual-target provenance flag. A manual target must never manufacture a match score, factor card, or explanation.
- Use a controlled campaign stage model: Target → Research → Apply → Outreach → Interview → Offer, with terminal/reopen semantics documented for Bypass, Closed, or Withdrawn states.
- Store Go/No-Go factors separately from Match factors. Reuse canonical match evidence as read-only context and preserve a timestamped campaign research decision with configurable weights.
- Treat location, clearance, work authorization, and other declared non-negotiables as capable of hard-failing the campaign decision; do not average them away.
- Create outreach tasks and response tracking through `LogOutreach`; keep the scope CRM-lite and require explicit user submission for every write.
- Model SkillBridge/CSP, federal/USAJOBS preference, Hire Our Heroes, and fellowship information as transparent channel/pathway tags with source and eligibility/date context.
- Expose stalled-stage health using documented time thresholds and accessible text labels in addition to color.

## Testing Decisions

- Test campaign creation from a Match, campaign creation from a manual target, and rejection of an unproven target that claims match provenance.
- Test every stage transition, terminal state, reopen rule, and stalled-stage calculation.
- Test Go/No-Go factor evaluation, including a hard location failure and an otherwise strong candidate/employer fit.
- Test linked application and outreach task creation, outreach logging, response updates, and preservation of an immutable originating match reference.
- Test pathway tag display and date/eligibility warning behavior with sourced fixtures; never infer veteran eligibility solely from a tag.
- Run authorization and PII-focused tests once write authorization is available, including that one veteran/counselor cannot alter another veteran’s campaign without policy permission.

## Out of Scope (explicitly: before Slice 1 done)

- Before Slice 1 plumbing is done, this epic does not build Campaign on fake scores, a parallel job-search or match-serving path, a separate profile store, or browser-only writes to analytics data.
- Full CRM functionality, contact scraping, LinkedIn automation, automatic ATS submission, and bulk unsolicited messaging are out of scope.
- Partner cohort administration, aggregate SITREP reporting, and formal outcome metrics belong to E010; production evaluation/operations instrumentation belongs to E012.

## Further Notes

- GitHub epic: **#36**. FYS children: **FYS-080** bidirectional employer Go/No-Go, **FYS-081** Campaign entity, **FYS-082** Side Door/warm outreach hooks, **FYS-083** SkillBridge/CSP tags, **FYS-084** federal/USAJOBS path, and **FYS-085** HoH/fellowship tags.
- Ontology links: Campaign `targets` JobPosting and Company; a Match remains the provenance for a recommended target. Campaign is the primary writeback object for the “Verbs” stage.
- Foundry actions: `StartCampaign` creates the Target-stage campaign; `LogOutreach` records outreach and response tracking. `CompleteProfile` and `RunMatch` remain upstream prerequisites where a campaign originates from a recommendation; `RecordOutcome` is the downstream placement write.
