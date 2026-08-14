#!/usr/bin/env python3
"""Organize remaining GitHub issues: remove/close obsolete, link sub-issues, attach SPECs."""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

REPO = "For-Your-Service/For-Your-Service"

# Old pre-architecture backlog — close as superseded by MASTER #112 program
# Keep DONE ones closed with pointer; close open duplicates/backlog that map to FYS
CLOSE_AS_SUPERSEDED = {
    # Early GCP/Databricks local_ops era — superseded by E001/E002/E013 code-canonical path
    1: "Superseded by FYS-E002/E013 (bronze land on workspace.fys_*). See MASTER #112.",
    2: "Superseded by FYS-E002 + FYS-E001 single production path (Databricks+HF). See #112.",
    3: "Superseded by FYS-E002/E013 medallion job graph (FYS-118). See #112.",
    4: "Superseded by FYS-E012/E002 E2E path via Slice 1. See #112 / SPEC #114.",
    7: "Duplicate of GCP ingest work; superseded by FYS-E002. See #112.",
    8: "Superseded by Slice 1 plumbing + FYS-110 tests. See #112.",
    13: "Duplicate IN PROGRESS GCP CF; superseded by FYS-E001/E002 (HF+Databricks canonical). See #112.",
    14: "Duplicate E2E backlog; superseded by FYS-E012/E002. See #112.",
    15: "Duplicate PII backlog; superseded by FYS-E011 / SPEC #123 (FYS-100). See #112.",
    16: "Duplicate PII backlog; superseded by FYS-E011 / SPEC #123. See #112.",
    21: "IN PROGRESS GCP CF — demoted; production path is Databricks+HF (FYS-002). See #112.",
    22: "Local Task Scheduler daemon — out of Slice 1 scope; reopen only if still needed after FYS-013.",
    23: "Duplicate E2E payload; superseded by FYS-E002/E012. See #112.",
    24: "Duplicate PII; superseded by FYS-E011 SPEC #123. See #112.",
}

# Already [DONE] but still OPEN — close as completed historical
CLOSE_AS_DONE = {
    5: "Historical [DONE] — closing; architecture program continues under #112.",
    6: "Historical [DONE] — closing; see FYS-E004/E006 for next matching work (#112).",
    9: "Historical [DONE] — closing; see #112.",
    10: "Historical [DONE] — closing; vector path continues under E004/E006 (#112).",
    11: "Historical [DONE] — closing; job graph work continues as FYS-118 (#109).",
    12: "Historical [DONE] — closing; ingest continues under E002 (#112).",
}

# Epic -> children (FYS ids mapped later via title parse)
EPIC_CHILDREN_FYS = {
    28: ["FYS-001", "FYS-002", "FYS-003", "FYS-004"],
    29: ["FYS-010", "FYS-011", "FYS-012", "FYS-013", "FYS-014"],
    30: ["FYS-020", "FYS-021", "FYS-022", "FYS-023", "FYS-024"],
    31: ["FYS-030", "FYS-031", "FYS-032", "FYS-033"],
    32: ["FYS-040", "FYS-041", "FYS-042", "FYS-043", "FYS-044", "FYS-045"],
    33: ["FYS-015", "FYS-016", "FYS-017", "FYS-050", "FYS-051", "FYS-052", "FYS-053", "FYS-054", "FYS-055"],
    34: ["FYS-060", "FYS-061", "FYS-062", "FYS-063", "FYS-064"],
    35: ["FYS-070", "FYS-071", "FYS-072", "FYS-073", "FYS-074"],
    36: ["FYS-080", "FYS-081", "FYS-082", "FYS-083", "FYS-084", "FYS-085"],
    37: ["FYS-090", "FYS-091", "FYS-092", "FYS-093"],
    38: ["FYS-100", "FYS-101", "FYS-102", "FYS-103", "FYS-104", "FYS-105"],
    39: ["FYS-110", "FYS-111", "FYS-112", "FYS-113", "FYS-114"],
    104: ["FYS-106", "FYS-107", "FYS-108", "FYS-109", "FYS-118", "FYS-119", "FYS-120"],
}

SPEC_BY_EPIC = {
    28: 113,
    29: 114,
    30: 115,
    31: 116,
    32: 117,
    33: 118,
    34: 119,
    35: 120,
    36: 121,
    37: 122,
    38: 123,
    39: 124,
    104: 125,
}

EPICS = list(EPIC_CHILDREN_FYS.keys())
MASTER = 112


def run(args, input_text=None):
    return subprocess.run(
        args, input=input_text, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def gh_json(args):
    p = run(args)
    if p.returncode != 0:
        raise RuntimeError(p.stderr or p.stdout)
    return json.loads(p.stdout) if p.stdout.strip() else None


def close_issue(num: int, comment: str):
    p = run(["gh", "issue", "close", str(num), "--repo", REPO, "--comment", comment])
    print(("OK close" if p.returncode == 0 else "FAIL close"), num, (p.stderr or "")[:120])
    time.sleep(0.3)


def edit_body(num: int, body: str):
    p = run(["gh", "issue", "edit", str(num), "--repo", REPO, "--body", body])
    print(("OK edit" if p.returncode == 0 else "FAIL edit"), num, (p.stderr or "")[:120])
    time.sleep(0.35)


def comment(num: int, body: str):
    run(["gh", "issue", "comment", str(num), "--repo", REPO, "--body", body])
    time.sleep(0.25)


def parse_fys(title: str) -> str | None:
    import re
    m = re.match(r"\[(EPIC )?(FYS-E?\d+)\]", title)
    return m.group(2) if m else None


def main():
    issues = gh_json([
        "gh", "issue", "list", "--repo", REPO, "--state", "open", "--limit", "200",
        "--json", "number,title,url",
    ])
    by_num = {i["number"]: i for i in issues}
    print(f"Open issues: {len(issues)}")

    # 1) Close obsolete / duplicates / historical DONE
    print("== Closing superseded/obsolete ==")
    for num, msg in {**CLOSE_AS_SUPERSEDED, **CLOSE_AS_DONE}.items():
        if num in by_num:
            close_issue(num, msg)
        else:
            print(f"  skip {num} (not open)")

    # Refresh open list
    issues = gh_json([
        "gh", "issue", "list", "--repo", REPO, "--state", "open", "--limit", "200",
        "--json", "number,title,url",
    ])
    by_num = {i["number"]: i for i in issues}
    by_fys: dict[str, int] = {}
    for i in issues:
        fid = parse_fys(i["title"])
        if fid and not fid.startswith("FYS-E"):
            by_fys[fid] = i["number"]
        # also map SPEC titles? skip

    # Map FYS-015 etc from titles that aren't EPIC
    import re
    for i in issues:
        m = re.match(r"\[(FYS-\d+)\]", i["title"])
        if m:
            by_fys[m.group(1)] = i["number"]

    print(f"Remaining open: {len(issues)}; FYS tasks mapped: {len(by_fys)}")

    # 2) Rebuild epic bodies: SPEC + children as tracked sub-issues
    print("== Rewriting epic parents with SPEC + children ==")
    for epic_num, child_ids in EPIC_CHILDREN_FYS.items():
        if epic_num not in by_num:
            print(f"  epic {epic_num} closed/missing")
            continue
        title = by_num[epic_num]["title"]
        eid = parse_fys(title) or f"#{epic_num}"
        spec = SPEC_BY_EPIC.get(epic_num)
        child_lines = []
        for cid in child_ids:
            n = by_fys.get(cid)
            if n:
                child_lines.append(f"- [ ] #{n}")
            else:
                child_lines.append(f"- [ ] _{cid} missing_")
        body = f"""## Epic `{eid}`

**Kind:** Epic (parent)  
**Master:** #{MASTER}  
**AFK Spec:** #{spec} (`ready-for-agent`)  

### Spec (implement against this)
- [ ] #{spec}

### Sub-issues (tracked)
{chr(10).join(child_lines)}

### Definition of done
- [ ] Spec acceptance met
- [ ] All sub-issues closed or deferred with comment
- [ ] Code-canonical: serving uses `workspace.fys_*`

### Links
- Master: #{MASTER}
- Spec index: `docs/epics/specs/README.md`
"""
        edit_body(epic_num, body)

    # 3) Tag remaining FYS tasks with Part of epic + Spec pointer
    print("== Annotating task issues with Part of ==")
    epic_for_fys = {}
    for epic_num, child_ids in EPIC_CHILDREN_FYS.items():
        for cid in child_ids:
            epic_for_fys[cid] = epic_num

    for cid, num in by_fys.items():
        epic_num = epic_for_fys.get(cid)
        if not epic_num:
            continue
        spec = SPEC_BY_EPIC.get(epic_num)
        # Prepend Part of if not already — fetch body
        view = gh_json(["gh", "issue", "view", str(num), "--repo", REPO, "--json", "body,title"])
        body = view.get("body") or ""
        if body.lstrip().startswith("Part of #"):
            continue
        header = f"Part of #{epic_num} · Spec #{spec} · Master #{MASTER}\n\n"
        # Don't rewrite huge bodies if already have Traceability
        if "**Parent epic:**" in body or "Parent epic:" in body:
            # still ensure Part of line
            new_body = header + body
        else:
            new_body = header + body
        edit_body(num, new_body)

    # 4) Annotate SPEC issues
    print("== Annotating SPEC issues ==")
    for epic_num, spec_num in SPEC_BY_EPIC.items():
        if spec_num not in by_num:
            continue
        view = gh_json(["gh", "issue", "view", str(spec_num), "--repo", REPO, "--json", "body"])
        body = view.get("body") or ""
        if body.lstrip().startswith("Part of #"):
            continue
        edit_body(spec_num, f"Part of #{epic_num} · Master #{MASTER} · Triage: ready-for-agent\n\n{body}")

    # 5) Rewrite MASTER
    print("== Rewriting MASTER ==")
    epic_checks = "\n".join(f"- [ ] #{n}" for n in sorted(EPICS) if n in by_num)
    spec_checks = "\n".join(
        f"- [ ] #{SPEC_BY_EPIC[n]}" for n in sorted(EPICS) if n in by_num and SPEC_BY_EPIC[n] in by_num
    )
    slice1 = [40, 48, 54, 60, 67, 70, 91, 99, 100, 101, 102, 103, 105, 107, 109, 110]
    slice1_lines = "\n".join(f"| #{n} | Slice 1 |" for n in slice1 if n in by_num)

    master_body = f"""## MASTER — For Your Service Architecture Program

**Kind:** Master  
**Rule:** Code is canonical (`huggingface` serving → `workspace.fys_*`).

### Epics (tracked)
{epic_checks}

### AFK Specs (`ready-for-agent`)
{spec_checks}

### Slice 1 plumbing (do first)
{slice1_lines}

### Cleanup done this pass
- Closed obsolete GCP/local_ops duplicates and historical [DONE] issues in favor of this program.
- Remaining work is FYS epics → tasks, each with a SPEC issue.

### Board
https://github.com/users/parthalon025/projects/2

### Admin
Org admin: `scripts/github_admin_setup.ps1` for labels/milestones/`ready-for-agent`.
"""
    edit_body(MASTER, master_body)

    # 6) Report leftovers
    issues = gh_json([
        "gh", "issue", "list", "--repo", REPO, "--state", "open", "--limit", "200",
        "--json", "number,title",
    ])
    known = set(EPICS) | set(SPEC_BY_EPIC.values()) | {MASTER} | set(by_fys.values())
    leftovers = [i for i in issues if i["number"] not in known]
    print("\n== Leftover open issues (not in FYS tree) ==")
    for i in leftovers:
        print(f"  #{i['number']} {i['title']}")

    Path("docs/epics/ISSUE_CLEANUP_REPORT.md").write_text(
        "# Issue cleanup report\n\n"
        f"Closed superseded/done: {sorted({**CLOSE_AS_SUPERSEDED, **CLOSE_AS_DONE})}\n\n"
        f"Remaining open: {len(issues)}\n\n"
        + "\n".join(f"- #{i['number']} {i['title']}" for i in sorted(issues, key=lambda x: x["number"]))
        + "\n",
        encoding="utf-8",
    )
    print("Wrote docs/epics/ISSUE_CLEANUP_REPORT.md")


if __name__ == "__main__":
    main()
