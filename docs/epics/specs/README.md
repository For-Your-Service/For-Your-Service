# Spec Index — For Your Service (AFK-ready)

**Master:** [#112](https://github.com/For-Your-Service/For-Your-Service/issues/112)  
**Rule:** Code is canonical (`workspace.fys_*` from serving).  
**Seams:**
1. Match serving boundary (HF `/match` + `/veteran`)
2. Bronze land + DQ abort
3. Profile `ready_for_matching` gate

| Spec | Epic | GitHub epic | Milestone |
|------|------|-------------|-----------|
| [SPEC-E001](SPEC-E001-platform-truth.md) | Platform Truth | #28 | M0 |
| [SPEC-E011](SPEC-E011-security-privacy.md) | Security & Privacy | #38 | M0 |
| [SPEC-E013](SPEC-E013-org-pipelines.md) | Org & Pipelines | #104 | M0 |
| [SPEC-E005](SPEC-E005-veteran-profile.md) | Veteran Profile | #32 | M1 |
| [SPEC-E002](SPEC-E002-bronze-ingestion.md) | Bronze Ingestion | #29 | M2 |
| [SPEC-E003](SPEC-E003-silver-enrichment.md) | Silver Enrichment | #30 | M2 |
| [SPEC-E004](SPEC-E004-gold-embeddings.md) | Gold Embeddings | #31 | M2 |
| [SPEC-E006](SPEC-E006-matching-engine.md) | Matching Engine | #33 | M2 |
| [SPEC-E007](SPEC-E007-serving-api.md) | Serving API | #34 | M3 |
| [SPEC-E008](SPEC-E008-veteran-experience.md) | Veteran Experience | #35 | M3 |
| [SPEC-E009](SPEC-E009-campaign-pathways.md) | Campaign & Pathways | #36 | M4 |
| [SPEC-E010](SPEC-E010-partner-placement.md) | Partner Placement | #37 | M5 |
| [SPEC-E012](SPEC-E012-quality-observability.md) | Quality & Observability | #39 | M5 |

**Triage:** Spec issues are published as `[SPEC][ready-for-agent]`. Org admin should create the `ready-for-agent` label via `scripts/github_admin_setup.ps1`.

**Slice 1 order:** E001 → E013 → E011 → E005 → E002 → E004/E006 → E007 (then later epics).
