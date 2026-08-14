# Issue organization report

## Hierarchy (live on GitHub)

```
MASTER #112
  ├── EPICs #28–39, #104   ← task-list tracks FYS children + SPEC
  │     └── FYS tasks (~#40–111)
  └── SPECs #113–125       ← ready-for-agent (title-tagged)
```

Board: https://github.com/users/parthalon025/projects/2

## Done this pass

| Action | Result |
|--------|--------|
| Epic bodies | Each epic tracks its SPEC + child FYS issues |
| Task bodies | `Part of #<epic> · Spec #<n> · Master #112` |
| SPEC bodies | `Part of #<epic> · ready-for-agent` |
| MASTER #112 | Epic + SPEC + Slice 1 checklists |
| Legacy #1–16, #21–24 | SUPERSEDED comments pointing at replacements |

## Could not remove (permission)

Your GitHub user **cannot close or edit** issues #1–24 (created by others / needs triage+).  

**Org admin (Free Hall) should run:**

```powershell
.\scripts\github_admin_close_superseded.ps1
.\scripts\github_admin_setup.ps1
```

That closes the legacy set and applies the `ready-for-agent` label to SPECs #113–125.

## Legacy → replacement map

| Legacy | Replacement |
|--------|-------------|
| #1–4, #7, #13, #21 GCP/E2E | #112 / E002 / SPEC #114 / FYS-118 |
| #5, #6, #9–12 DONE historical | Archive under #112 |
| #8, #14, #23 E2E | SPEC #114 / FYS-110 |
| #15, #16, #24 PII dupes | SPEC #123 / FYS-100 |
| #22 Task Scheduler | Defer (not Slice 1) |
