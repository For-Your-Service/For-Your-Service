# Epics & Issues — For Your Service

**Organization:** 7 Eagle Group  
**Purpose:** Turn research into implementable work without losing architecture intent.  
**Last Updated:** 2026-08-14

---

## How to Use This Folder

| File | When to open |
|------|----------------|
| [../ROADMAP.md](../ROADMAP.md) | Phases, quarters, milestone order |
| [PROGRAM.md](PROGRAM.md) | Full architecture program from research — all capability epics |
| [RESEARCH_BRIEF.md](RESEARCH_BRIEF.md) | Why we build this (white space, competitors, non-goals) |
| [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md) | Palantir/Foundry doctrine → FYS objects, actions, Slice 1 gates |
| [ISSUE_SPECS.md](ISSUE_SPECS.md) | Copy/paste specs for every issue (acceptance criteria) |
| [specs/README.md](specs/README.md) | AFK **to-spec** documents per epic (`ready-for-agent`) |
| [GITHUB_ISSUE_MAP.md](GITHUB_ISSUE_MAP.md) | Filed GitHub issue links |
| Layer specs (`SILVER_LAYER_SPEC`, `GOLD_LAYER_SPEC`, …) | Data/ML contracts |

**Workflow**
1. Open the [MASTER issue](https://github.com/For-Your-Service/For-Your-Service/issues/112) or [Project board](https://github.com/users/parthalon025/projects/2).
2. Pick an epic from [PROGRAM.md](PROGRAM.md) / [GITHUB_HIERARCHY.md](GITHUB_HIERARCHY.md).
3. Work a tracked child (`- [ ] #N` on the epic).
4. Org admin: run [`scripts/github_admin_setup.ps1`](../../scripts/github_admin_setup.ps1) for labels, milestones, issue types.

**Hierarchy (GitHub best practice)**
```
[MASTER] #112
  └── [EPIC] (task-list trackedIssues)
        └── [FYS-xxx] Task (task-list on epic)
Project v2 fields: Status · Kind · Priority · Area · Milestone
```


---

## ID Scheme

| Prefix | Meaning | Example |
|--------|---------|---------|
| `FYS-E0xx` | Epic (capability outcome) | `FYS-E005` Veteran Profile System |
| `FYS-0xx` | Issue (shippable slice) | `FYS-021` Hard filters before rank |

---

## Labels (GitHub)

| Label | Use |
|-------|-----|
| `epic` | Parent tracking issue |
| `P0` / `P1` / `P2` | Priority |
| `bronze` `silver` `gold` | Medallion layer |
| `profile` `matching` `ingestion` `api` `ux` `campaign` `partner` `security` `ops` | Area |
| `tech-debt` | Fix stubs / drift / placeholders |
| `research` | Derived from competitive / domain research |

---

## Definition of Done (every issue)

- [ ] Acceptance criteria checked
- [ ] Related docs updated (`VETERAN_PROFILE_SCHEMA`, layer specs, `API.md` as needed)
- [ ] Tests added under `tests/` for the touched module
- [ ] No new placeholder embeddings / hardcoded match scores
- [ ] PII rules followed ([guides/PII_PROTECTION.md](../guides/PII_PROTECTION.md))

---

Built with ❤️ for those who served. 🇺🇸
