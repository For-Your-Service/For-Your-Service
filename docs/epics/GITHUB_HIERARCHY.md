# GitHub Issue Hierarchy — For Your Service

**Best practice used:** Master → Epic → Task via GitHub **task-list tracked issues** (`- [ ] #N`).

- **Master:** [#112](https://github.com/For-Your-Service/For-Your-Service/issues/112)
- **Project board:** https://github.com/users/parthalon025/projects/2
- **Doctrine:** [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md)

## Permission note

This contributor can create/edit issues and a **user** Project, but org **labels / milestones / issue types / addSubIssue / org projects** require Admin.
Org admin should run `scripts/github_admin_setup.ps1`, then optionally convert task-lists to native Sub-issues.

## Tree

- [MASTER #112](https://github.com/For-Your-Service/For-Your-Service/issues/112)
  - [EPIC FYS-E001 #28](https://github.com/For-Your-Service/For-Your-Service/issues/28)
    - [#40](https://github.com/For-Your-Service/For-Your-Service/issues/40) [FYS-001] Canonical Unity Catalog schema map
    - [#41](https://github.com/For-Your-Service/For-Your-Service/issues/41) [FYS-002] Single production serving path
    - [#42](https://github.com/For-Your-Service/For-Your-Service/issues/42) [FYS-003] API credential status truth
    - [#43](https://github.com/For-Your-Service/For-Your-Service/issues/43) [FYS-004] Nested/duplicate tree cleanup plan
  - [EPIC FYS-E002 #29](https://github.com/For-Your-Service/For-Your-Service/issues/29)
    - [#44](https://github.com/For-Your-Service/For-Your-Service/issues/44) [FYS-010] Harden multi-source orchestrator
    - [#45](https://github.com/For-Your-Service/For-Your-Service/issues/45) [FYS-011] Bronze schema and validation
    - [#46](https://github.com/For-Your-Service/For-Your-Service/issues/46) [FYS-012] Regional config MSA packs
    - [#47](https://github.com/For-Your-Service/For-Your-Service/issues/47) [FYS-013] Ingestion schedule and idempotency
    - [#48](https://github.com/For-Your-Service/For-Your-Service/issues/48) [FYS-014] Fix BronzeWriter stub path
  - [EPIC FYS-E003 #30](https://github.com/For-Your-Service/For-Your-Service/issues/30)
    - [#49](https://github.com/For-Your-Service/For-Your-Service/issues/49) [FYS-020] O*NET client production path
    - [#50](https://github.com/For-Your-Service/For-Your-Service/issues/50) [FYS-021] MOS to O*NET soft prior
    - [#51](https://github.com/For-Your-Service/For-Your-Service/issues/51) [FYS-022] Skill extraction to O*NET taxonomy
    - [#52](https://github.com/For-Your-Service/For-Your-Service/issues/52) [FYS-023] Standardized titles and industry
    - [#53](https://github.com/For-Your-Service/For-Your-Service/issues/53) [FYS-024] Silver transform job
  - [EPIC FYS-E004 #31](https://github.com/For-Your-Service/For-Your-Service/issues/31)
    - [#54](https://github.com/For-Your-Service/For-Your-Service/issues/54) [FYS-030] Replace placeholder embeddings
    - [#55](https://github.com/For-Your-Service/For-Your-Service/issues/55) [FYS-031] Job embedding pipeline
    - [#56](https://github.com/For-Your-Service/For-Your-Service/issues/56) [FYS-032] Veteran embedding from civilianized text
    - [#57](https://github.com/For-Your-Service/For-Your-Service/issues/57) [FYS-033] Embedding versioning and rebuild
  - [EPIC FYS-E005 #32](https://github.com/For-Your-Service/For-Your-Service/issues/32)
    - [#58](https://github.com/For-Your-Service/For-Your-Service/issues/58) [FYS-040] Self-understanding intake schema
    - [#59](https://github.com/For-Your-Service/For-Your-Service/issues/59) [FYS-041] Core veteran profile
    - [#60](https://github.com/For-Your-Service/For-Your-Service/issues/60) [FYS-042] Profile completeness gate
    - [#61](https://github.com/For-Your-Service/For-Your-Service/issues/61) [FYS-043] Military to civilian translation fields
    - [#62](https://github.com/For-Your-Service/For-Your-Service/issues/62) [FYS-044] Profile context loader hot summary
    - [#102](https://github.com/For-Your-Service/For-Your-Service/issues/102) [FYS-045] Fix profile package imports (intake/summary missing)
  - [EPIC FYS-E006 #33](https://github.com/For-Your-Service/For-Your-Service/issues/33)
    - [#63](https://github.com/For-Your-Service/For-Your-Service/issues/63) [FYS-050] Hard filters before rank
    - [#64](https://github.com/For-Your-Service/For-Your-Service/issues/64) [FYS-051] Hybrid retrieval BM25 plus dense
    - [#65](https://github.com/For-Your-Service/For-Your-Service/issues/65) [FYS-052] Multi-factor white-box score
    - [#66](https://github.com/For-Your-Service/For-Your-Service/issues/66) [FYS-053] Grounded match explanations
    - [#67](https://github.com/For-Your-Service/For-Your-Service/issues/67) [FYS-054] Remove stub match scores in HF paths
    - [#68](https://github.com/For-Your-Service/For-Your-Service/issues/68) [FYS-055] MOS prior integration in ranker
    - [#99](https://github.com/For-Your-Service/For-Your-Service/issues/99) [FYS-015] Unify SiameseMatchingModel public API (ImportError)
    - [#100](https://github.com/For-Your-Service/For-Your-Service/issues/100) [FYS-016] Repair or delete lying matching/ingestion tests
    - [#101](https://github.com/For-Your-Service/For-Your-Service/issues/101) [FYS-017] Choose single JobMatcher path for Slice 1
  - [EPIC FYS-E007 #34](https://github.com/For-Your-Service/For-Your-Service/issues/34)
    - [#69](https://github.com/For-Your-Service/For-Your-Service/issues/69) [FYS-060] Veteran profile API
    - [#70](https://github.com/For-Your-Service/For-Your-Service/issues/70) [FYS-061] Match API with profile gate
    - [#71](https://github.com/For-Your-Service/For-Your-Service/issues/71) [FYS-062] Jobs query API
    - [#72](https://github.com/For-Your-Service/For-Your-Service/issues/72) [FYS-063] Health and readiness endpoints
    - [#73](https://github.com/For-Your-Service/For-Your-Service/issues/73) [FYS-064] Rate limiting and caching
  - [EPIC FYS-E008 #35](https://github.com/For-Your-Service/For-Your-Service/issues/35)
    - [#74](https://github.com/For-Your-Service/For-Your-Service/issues/74) [FYS-070] Profile creation wizard
    - [#75](https://github.com/For-Your-Service/For-Your-Service/issues/75) [FYS-071] Recommendation dashboard
    - [#76](https://github.com/For-Your-Service/For-Your-Service/issues/76) [FYS-072] Match explanation UI
    - [#77](https://github.com/For-Your-Service/For-Your-Service/issues/77) [FYS-073] Email notifications
    - [#78](https://github.com/For-Your-Service/For-Your-Service/issues/78) [FYS-074] Accessibility pass
  - [EPIC FYS-E009 #36](https://github.com/For-Your-Service/For-Your-Service/issues/36)
    - [#79](https://github.com/For-Your-Service/For-Your-Service/issues/79) [FYS-080] Bidirectional employer Go/No-Go
    - [#80](https://github.com/For-Your-Service/For-Your-Service/issues/80) [FYS-081] Campaign entity and funnel
    - [#81](https://github.com/For-Your-Service/For-Your-Service/issues/81) [FYS-082] Side Door warm outreach hooks
    - [#82](https://github.com/For-Your-Service/For-Your-Service/issues/82) [FYS-083] SkillBridge CSP pathway tags
    - [#83](https://github.com/For-Your-Service/For-Your-Service/issues/83) [FYS-084] Federal USAJOBS preference path
    - [#84](https://github.com/For-Your-Service/For-Your-Service/issues/84) [FYS-085] HoH fellowship channel tags
  - [EPIC FYS-E010 #37](https://github.com/For-Your-Service/For-Your-Service/issues/37)
    - [#85](https://github.com/For-Your-Service/For-Your-Service/issues/85) [FYS-090] Partner organization object
    - [#86](https://github.com/For-Your-Service/For-Your-Service/issues/86) [FYS-091] Cohort batch veteran ingest
    - [#87](https://github.com/For-Your-Service/For-Your-Service/issues/87) [FYS-092] Funnel SITREP dashboard
    - [#88](https://github.com/For-Your-Service/For-Your-Service/issues/88) [FYS-093] Placement outcome metrics
  - [EPIC FYS-E011 #38](https://github.com/For-Your-Service/For-Your-Service/issues/38)
    - [#89](https://github.com/For-Your-Service/For-Your-Service/issues/89) [FYS-100] Ops vs analytics PII split
    - [#90](https://github.com/For-Your-Service/For-Your-Service/issues/90) [FYS-101] Secrets only in scopes
    - [#91](https://github.com/For-Your-Service/For-Your-Service/issues/91) [FYS-102] CORS lockdown
    - [#92](https://github.com/For-Your-Service/For-Your-Service/issues/92) [FYS-103] AuthN for write APIs
    - [#93](https://github.com/For-Your-Service/For-Your-Service/issues/93) [FYS-104] Retention alignment
    - [#103](https://github.com/For-Your-Service/For-Your-Service/issues/103) [FYS-105] Remove hardcoded API credential defaults from config
  - [EPIC FYS-E012 #39](https://github.com/For-Your-Service/For-Your-Service/issues/39)
    - [#94](https://github.com/For-Your-Service/For-Your-Service/issues/94) [FYS-110] Match path unit and integration tests
    - [#95](https://github.com/For-Your-Service/For-Your-Service/issues/95) [FYS-111] Precision at k and NDCG harness
    - [#96](https://github.com/For-Your-Service/For-Your-Service/issues/96) [FYS-112] Monitoring hooks
    - [#97](https://github.com/For-Your-Service/For-Your-Service/issues/97) [FYS-113] Daily operations runbook update
    - [#98](https://github.com/For-Your-Service/For-Your-Service/issues/98) [FYS-114] Placement success instrumentation
  - [EPIC FYS-E013 #104](https://github.com/For-Your-Service/For-Your-Service/issues/104)
    - [#105](https://github.com/For-Your-Service/For-Your-Service/issues/105) [FYS-106] Declare code-canonical catalog spine (workspace.fys_*)
    - [#106](https://github.com/For-Your-Service/For-Your-Service/issues/106) [FYS-107] Foundry project and folder spine in repo + UC
    - [#107](https://github.com/For-Your-Service/For-Your-Service/issues/107) [FYS-108] Wire data expectations to abort bad bronze builds
    - [#108](https://github.com/For-Your-Service/For-Your-Service/issues/108) [FYS-109] Pipeline health triad — in / build / out
    - [#109](https://github.com/For-Your-Service/For-Your-Service/issues/109) [FYS-118] Databricks job graph for job_postings medallion
    - [#110](https://github.com/For-Your-Service/For-Your-Service/issues/110) [FYS-119] Quarantine non-canonical lakehouse/transactions pipeline
    - [#111](https://github.com/For-Your-Service/For-Your-Service/issues/111) [FYS-120] Data lineage doc generated from code paths
