#!/usr/bin/env python3
"""Organize FYS GitHub issues: master + epic tracked lists, project board, admin assets."""
from __future__ import annotations

import json
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

REPO = "For-Your-Service/For-Your-Service"
OWNER, NAME = REPO.split("/")
PROJECT_OWNER = "parthalon025"
PROJECT_NUMBER = 2
MAP_URL = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/FOUNDRY_ONTOLOGY_MAP.md"

# Epic ID -> child FYS IDs (from ISSUE_SPECS + follow-ons)
EPIC_CHILDREN: dict[str, list[str]] = {
    "FYS-E001": ["FYS-001", "FYS-002", "FYS-003", "FYS-004"],
    "FYS-E002": ["FYS-010", "FYS-011", "FYS-012", "FYS-013", "FYS-014"],
    "FYS-E003": ["FYS-020", "FYS-021", "FYS-022", "FYS-023", "FYS-024"],
    "FYS-E004": ["FYS-030", "FYS-031", "FYS-032", "FYS-033"],
    "FYS-E005": ["FYS-040", "FYS-041", "FYS-042", "FYS-043", "FYS-044", "FYS-045"],
    "FYS-E006": ["FYS-015", "FYS-016", "FYS-017", "FYS-050", "FYS-051", "FYS-052", "FYS-053", "FYS-054", "FYS-055"],
    "FYS-E007": ["FYS-060", "FYS-061", "FYS-062", "FYS-063", "FYS-064"],
    "FYS-E008": ["FYS-070", "FYS-071", "FYS-072", "FYS-073", "FYS-074"],
    "FYS-E009": ["FYS-080", "FYS-081", "FYS-082", "FYS-083", "FYS-084", "FYS-085"],
    "FYS-E010": ["FYS-090", "FYS-091", "FYS-092", "FYS-093"],
    "FYS-E011": ["FYS-100", "FYS-101", "FYS-102", "FYS-103", "FYS-104", "FYS-105"],
    "FYS-E012": ["FYS-110", "FYS-111", "FYS-112", "FYS-113", "FYS-114"],
    "FYS-E013": ["FYS-106", "FYS-107", "FYS-108", "FYS-109", "FYS-118", "FYS-119", "FYS-120"],
}

# Milestone assignment by FYS id prefix / specific
MILESTONE_BY_ID: dict[str, str] = {}
for eid in ["FYS-001", "FYS-002", "FYS-003", "FYS-004", "FYS-100", "FYS-101", "FYS-102", "FYS-105", "FYS-106", "FYS-107", "FYS-108", "FYS-118", "FYS-119"]:
    MILESTONE_BY_ID[eid] = "M0"
for eid in ["FYS-040", "FYS-041", "FYS-042", "FYS-043", "FYS-044", "FYS-045"]:
    MILESTONE_BY_ID[eid] = "M1"
for eid in [
    "FYS-010", "FYS-011", "FYS-012", "FYS-013", "FYS-014", "FYS-015", "FYS-016", "FYS-017",
    "FYS-020", "FYS-021", "FYS-022", "FYS-023", "FYS-024",
    "FYS-030", "FYS-031", "FYS-032", "FYS-033",
    "FYS-050", "FYS-051", "FYS-052", "FYS-053", "FYS-054", "FYS-055",
    "FYS-109", "FYS-110", "FYS-113",
]:
    MILESTONE_BY_ID[eid] = "M2"
for eid in ["FYS-060", "FYS-061", "FYS-062", "FYS-063", "FYS-064", "FYS-070", "FYS-071", "FYS-072", "FYS-074", "FYS-103", "FYS-112"]:
    MILESTONE_BY_ID[eid] = "M3"
for eid in ["FYS-080", "FYS-081", "FYS-082", "FYS-083", "FYS-084", "FYS-085"]:
    MILESTONE_BY_ID[eid] = "M4"
for eid in ["FYS-073", "FYS-090", "FYS-091", "FYS-092", "FYS-093", "FYS-104", "FYS-111", "FYS-114", "FYS-120"]:
    MILESTONE_BY_ID[eid] = "M5"

EPIC_MILESTONE = {
    "FYS-E001": "M0", "FYS-E011": "M0", "FYS-E013": "M0",
    "FYS-E005": "M1",
    "FYS-E002": "M2", "FYS-E003": "M2", "FYS-E004": "M2", "FYS-E006": "M2",
    "FYS-E007": "M3", "FYS-E008": "M3",
    "FYS-E009": "M4",
    "FYS-E010": "M5", "FYS-E012": "M5",
}

PRIORITY = {
    "M0": "P0", "M1": "P0", "M2": "P0", "M3": "P0", "M4": "P1", "M5": "P1",
}


def run(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, input=input_text, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def gh_json(args: list[str]) -> object:
    p = run(args)
    if p.returncode != 0:
        raise RuntimeError(p.stderr or p.stdout)
    return json.loads(p.stdout) if p.stdout.strip() else None


def list_issues() -> list[dict]:
    return gh_json([
        "gh", "issue", "list", "--repo", REPO, "--limit", "200", "--state", "all",
        "--json", "number,title,url,body,id",
    ])  # type: ignore


def parse_id(title: str) -> str | None:
    m = re.match(r"\[(EPIC )?(FYS-E?\d+)\]", title)
    if not m:
        return None
    return m.group(2)


def edit_body(number: int, body: str) -> None:
    p = run(["gh", "issue", "edit", str(number), "--repo", REPO, "--body", body])
    if p.returncode != 0:
        print(f"  FAIL edit #{number}: {p.stderr[:200]}")
    else:
        print(f"  OK edit #{number}")
    time.sleep(0.35)


def create_issue(title: str, body: str) -> dict | None:
    p = run(["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body])
    if p.returncode != 0:
        print("FAIL create", p.stderr[:300])
        return None
    url = p.stdout.strip()
    num = int(url.rstrip("/").split("/")[-1])
    print("OK create", url)
    time.sleep(0.4)
    return {"number": num, "url": url}


def project_item_add(url: str) -> None:
    p = run([
        "gh", "project", "item-add", str(PROJECT_NUMBER),
        "--owner", PROJECT_OWNER, "--url", url,
    ])
    if p.returncode != 0:
        print(f"  project add fail {url}: {p.stderr[:160]}")
    time.sleep(0.2)


def ensure_project_fields(project_id: str) -> None:
    """Create custom single-select fields if missing."""
    # list fields
    p = run(["gh", "project", "field-list", str(PROJECT_NUMBER), "--owner", PROJECT_OWNER, "--format", "json"])
    existing = set()
    if p.returncode == 0 and p.stdout.strip():
        try:
            data = json.loads(p.stdout)
            fields = data if isinstance(data, list) else data.get("fields", data.get("items", []))
            if isinstance(fields, dict):
                fields = fields.get("nodes", [])
            for f in fields or []:
                if isinstance(f, dict) and "name" in f:
                    existing.add(f["name"])
        except json.JSONDecodeError:
            pass

    # Create fields via GraphQL
    defs = [
        ("Priority", ["P0", "P1", "P2"]),
        ("Milestone", ["M0", "M1", "M2", "M3", "M4", "M5"]),
        ("Area", ["ops", "bronze", "silver", "gold", "profile", "matching", "api", "ux", "campaign", "partner", "security", "pipeline"]),
        ("Kind", ["Master", "Epic", "Task"]),
    ]
    for name, options in defs:
        if name in existing:
            print(f"  field exists: {name}")
            continue
        opts = ", ".join(
            '{name: "%s", color: %s, description: "%s"}'
            % (o, "RED" if o == "P0" else "YELLOW" if o == "P1" else "BLUE", o)
            for o in options
        )
        # Simplified colors
        opt_objs = []
        colors = {"P0": "RED", "P1": "YELLOW", "P2": "BLUE", "M0": "PURPLE", "M1": "BLUE", "M2": "GREEN",
                  "M3": "ORANGE", "M4": "PINK", "M5": "GRAY", "Master": "PURPLE", "Epic": "PURPLE", "Task": "BLUE"}
        for o in options:
            c = colors.get(o, "GRAY")
            opt_objs.append(f'{{name: "{o}", color: {c}, description: "{o}"}}')
        mutation = f'''
        mutation {{
          createProjectV2Field(input: {{
            projectId: "{project_id}"
            dataType: SINGLE_SELECT
            name: "{name}"
            singleSelectOptions: [{", ".join(opt_objs)}]
          }}) {{
            projectV2Field {{ ... on ProjectV2SingleSelectField {{ id name }} }}
          }}
        }}'''
        r = run(["gh", "api", "graphql", "-f", f"query={mutation}"])
        print(f"  create field {name}:", "OK" if r.returncode == 0 and "errors" not in (r.stdout or "") else (r.stdout or r.stderr)[:200])
        time.sleep(0.3)


def epic_body(eid: str, title: str, child_nums: list[int], milestone: str) -> str:
    checks = "\n".join(f"- [ ] #{n}" for n in child_nums) or "- [ ] _(none linked yet)_"
    return f"""## Epic `{eid}`

**Kind:** Epic (parent)  
**Milestone:** {milestone}  
**Priority:** {PRIORITY.get(milestone, "P1")}  
**Doctrine:** {MAP_URL}

### Sub-issues (tracked)
{checks}

### Definition of done
- [ ] All sub-issues closed or explicitly deferred with comment
- [ ] Related docs match **code-canonical** spine (`workspace.fys_*` from serving code)
- [ ] No new placeholder embeddings / hardcoded match scores

### How this is organized
This issue tracks children via GitHub task-list references (`trackedIssues`).  
Master roadmap issue tracks all epics the same way.
"""


def master_body(epic_nums: list[tuple[int, str]], slice1: list[int]) -> str:
    epic_lines = "\n".join(f"- [ ] #{n} — {name}" for n, name in epic_nums)
    s1 = "\n".join(f"- [ ] #{n}" for n in slice1)
    return f"""## MASTER — For Your Service Architecture Program

**Kind:** Master tracking issue  
**Project:** https://github.com/users/{PROJECT_OWNER}/projects/{PROJECT_NUMBER}  
**Doctrine:** {MAP_URL}  
**Rule:** Code is canonical (`huggingface/app.py` → `workspace.fys_*`).

This is the single top-level tracker. Epics below are parents; each epic tracks its tasks via GitHub sub-issue task lists.

### Epics (tracked)
{epic_lines}

### Slice 1 — plumbing first (ship before campaign/UX polish)
{s1}

### GitHub organization (best practices)
| Layer | Mechanism |
|-------|-----------|
| Master → Epics | Task list on this issue |
| Epic → Tasks | Task list on each `[EPIC]` issue |
| Board | Project v2 (Status, Priority, Milestone, Area, Kind) |
| Labels / Milestones / Issue types / native Sub-issues | Require **repo write/triage** — run `scripts/github_admin_setup.ps1` as org admin |

### Milestones
- **M0** Truth & safety (+ org/pipelines)
- **M1** Know yourself (profile gate)
- **M2** Real match substrate
- **M3** Serve & UX
- **M4** Campaign differentiator
- **M5** Partner scale

### Non-goals
Do not expand Campaign/Partner before Slice 1 plumbing is green.
"""


def write_admin_script(path: Path) -> None:
    path.write_text(
        r'''#Requires -Version 5.1
<#
.SYNOPSIS
  Admin-only: labels, milestones, issue types, org project link for For-Your-Service.
  Run as a user with repo Admin/Maintain (e.g. Free Hall), not triage-only.
#>
$ErrorActionPreference = "Stop"
$Repo = "For-Your-Service/For-Your-Service"
$Org = "For-Your-Service"

Write-Host "== Labels =="
$labels = @(
  @{n='epic';c='B392F0';d='Epic parent issue'},
  @{n='master';c='6F42C1';d='Master program tracker'},
  @{n='research';c='0E8A16';d='From architecture research'},
  @{n='P0';c='D93F0B';d='Blocker / Slice 1'},
  @{n='P1';c='FBCA04';d='Differentiator'},
  @{n='P2';c='C5DEF5';d='Later'},
  @{n='bronze';c='CD7F32';d='Bronze'},
  @{n='silver';c='C0C0C0';d='Silver'},
  @{n='gold';c='FFD700';d='Gold'},
  @{n='profile';c='1D76DB';d='Profile'},
  @{n='matching';c='5319E7';d='Matching'},
  @{n='ingestion';c='BFDADC';d='Ingestion'},
  @{n='api';c='006B75';d='API'},
  @{n='ux';c='E99695';d='UX'},
  @{n='campaign';c='F9D0C4';d='Campaign'},
  @{n='partner';c='D4C5F9';d='Partner'},
  @{n='security';c='B60205';d='Security'},
  @{n='ops';c='FEF2C0';d='Ops'},
  @{n='pipeline';c='1B7F7A';d='Data pipelines'},
  @{n='tech-debt';c='EEEEEE';d='Tech debt'}
)
foreach ($l in $labels) {
  gh label create $l.n --repo $Repo --color $l.c --description $l.d 2>$null
  if ($LASTEXITCODE -ne 0) { gh label edit $l.n --repo $Repo --color $l.c --description $l.d }
}

Write-Host "== Milestones =="
$ms = @(
  @{t='M0 Truth and Safety';d='Platform truth, security, org/pipelines'},
  @{t='M1 Know Yourself';d='Profile + self-understanding gate'},
  @{t='M2 Real Match Substrate';d='Bronze/silver/gold + matching'},
  @{t='M3 Serve and UX';d='API + veteran UX'},
  @{t='M4 Campaign Differentiator';d='Campaign + pathways'},
  @{t='M5 Partner Scale';d='7 Eagle SITREP + quality'}
)
foreach ($m in $ms) {
  gh api -X POST "repos/$Repo/milestones" -f title=$m.t -f description=$m.d -f state=open 2>$null | Out-Null
}

Write-Host "== Issue type Epic (org) =="
$orgId = gh api graphql -f query='query { organization(login:"For-Your-Service") { id } }' --jq '.data.organization.id'
gh api graphql -f query="mutation { createIssueType(input:{ ownerId:\"$orgId\", name:\"Epic\", description:\"Outcome parent\", color:PURPLE, isEnabled:true }) { issueType { id name } } }" 2>$null

Write-Host "Done. Then: (1) set issue types Epic/Feature/Task in UI (2) addSubIssue if desired (3) transfer project to org or link repo."
''',
        encoding="utf-8",
    )


def main() -> int:
    issues = list_issues()
    by_fys: dict[str, dict] = {}
    epics: dict[str, dict] = {}
    for i in issues:
        fid = parse_id(i["title"])
        if not fid:
            continue
        if fid.startswith("FYS-E"):
            epics[fid] = i
        else:
            by_fys[fid] = i

    print(f"Found {len(epics)} epics, {len(by_fys)} tasks")

    # Build child number lists
    epic_children_nums: dict[str, list[int]] = {}
    for eid, children in EPIC_CHILDREN.items():
        nums = []
        for cid in children:
            if cid in by_fys:
                nums.append(by_fys[cid]["number"])
            else:
                print(f"  missing child {cid} for {eid}")
        epic_children_nums[eid] = sorted(nums)

    # Update epic bodies with tracked task lists
    print("== Update epic bodies ==")
    for eid, issue in sorted(epics.items()):
        ms = EPIC_MILESTONE.get(eid, "M2")
        # Keep short title after ]
        short = issue["title"].split("]", 1)[-1].strip()
        body = epic_body(eid, short, epic_children_nums.get(eid, []), ms)
        edit_body(issue["number"], body)

    # Create or find master
    print("== Master issue ==")
    master = next((i for i in issues if i["title"].startswith("[MASTER]")), None)
    epic_list = []
    for eid in sorted(epics.keys()):
        epic_list.append((epics[eid]["number"], epics[eid]["title"]))
    epic_list.sort(key=lambda x: x[0])

    slice1_ids = [
        "FYS-001", "FYS-014", "FYS-015", "FYS-016", "FYS-017", "FYS-030",
        "FYS-042", "FYS-045", "FYS-054", "FYS-061", "FYS-102", "FYS-105",
        "FYS-106", "FYS-108", "FYS-118", "FYS-119",
    ]
    slice1_nums = sorted(by_fys[i]["number"] for i in slice1_ids if i in by_fys)

    body = master_body(epic_list, slice1_nums)
    if master:
        edit_body(master["number"], body)
        master_num = master["number"]
        master_url = f"https://github.com/{REPO}/issues/{master_num}"
    else:
        created = create_issue("[MASTER] For Your Service — Architecture Program", body)
        if not created:
            return 1
        master_num = created["number"]
        master_url = created["url"]

    # Project setup
    print("== Project fields ==")
    proj = gh_json([
        "gh", "api", "graphql", "-f",
        f'query=query {{ user(login:"{PROJECT_OWNER}") {{ projectV2(number:{PROJECT_NUMBER}) {{ id title url }} }} }}',
    ])
    project_id = proj["data"]["user"]["projectV2"]["id"]  # type: ignore
    print("Project", proj["data"]["user"]["projectV2"]["url"])  # type: ignore
    ensure_project_fields(project_id)

    print("== Add items to project ==")
    urls = [master_url]
    for i in epics.values():
        urls.append(i["url"] if "url" in i else f"https://github.com/{REPO}/issues/{i['number']}")
    for i in by_fys.values():
        urls.append(i.get("url") or f"https://github.com/{REPO}/issues/{i['number']}")
    # dedupe
    seen = set()
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        project_item_add(u)

    # Write docs
    admin = Path("scripts/github_admin_setup.ps1")
    write_admin_script(admin)
    print("Wrote", admin)

    mapping = {
        "master": master_num,
        "project": f"https://github.com/users/{PROJECT_OWNER}/projects/{PROJECT_NUMBER}",
        "epics": {k: v["number"] for k, v in epics.items()},
        "tasks": {k: v["number"] for k, v in by_fys.items()},
        "epic_children": epic_children_nums,
    }
    Path("docs/epics/GITHUB_HIERARCHY.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")

    # Hierarchy markdown
    lines = [
        "# GitHub Issue Hierarchy — For Your Service",
        "",
        "**Best practice used:** Master → Epic → Task via GitHub **task-list tracked issues** (`- [ ] #N`).",
        "",
        f"- **Master:** [#{master_num}](https://github.com/{REPO}/issues/{master_num})",
        f"- **Project board:** https://github.com/users/{PROJECT_OWNER}/projects/{PROJECT_NUMBER}",
        f"- **Doctrine:** [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md)",
        "",
        "## Permission note",
        "",
        "This contributor can create/edit issues and a **user** Project, but org **labels / milestones / issue types / addSubIssue / org projects** require Admin.",
        "Org admin should run `scripts/github_admin_setup.ps1`, then optionally convert task-lists to native Sub-issues.",
        "",
        "## Tree",
        "",
        f"- [MASTER #{master_num}](https://github.com/{REPO}/issues/{master_num})",
    ]
    for eid in sorted(epics.keys()):
        en = epics[eid]["number"]
        lines.append(f"  - [EPIC {eid} #{en}](https://github.com/{REPO}/issues/{en})")
        for n in epic_children_nums.get(eid, []):
            # find title
            title = next(i["title"] for i in by_fys.values() if i["number"] == n)
            lines.append(f"    - [#{n}](https://github.com/{REPO}/issues/{n}) {title}")
    Path("docs/epics/GITHUB_HIERARCHY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote docs/epics/GITHUB_HIERARCHY.md")
    print(f"\nMASTER: {master_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
