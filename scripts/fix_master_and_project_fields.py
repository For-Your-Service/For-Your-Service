#!/usr/bin/env python3
"""Fix MASTER tracked list (epics only) and set Project Kind/Priority fields."""
from __future__ import annotations

import json
import subprocess
import time

REPO = "For-Your-Service/For-Your-Service"
PROJECT_OWNER = "parthalon025"
PROJECT_NUMBER = 2
MAP = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/FOUNDRY_ONTOLOGY_MAP.md"

EPICS = [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 104]
SLICE1 = [40, 48, 54, 60, 67, 70, 91, 99, 100, 101, 102, 103, 105, 107, 109, 110]

# Epic number -> Kind Epic, Priority
EPIC_PRI = {
    28: "P0", 29: "P0", 30: "P0", 31: "P0", 32: "P0", 33: "P0", 34: "P0",
    35: "P1", 36: "P1", 37: "P1", 38: "P0", 39: "P1", 104: "P0",
}


def run(args, input_text=None):
    return subprocess.run(args, input=input_text, capture_output=True, text=True, encoding="utf-8", errors="replace")


MASTER_BODY = f"""## MASTER — For Your Service Architecture Program

**Kind:** Master  
**Project:** https://github.com/users/{PROJECT_OWNER}/projects/{PROJECT_NUMBER}  
**Doctrine:** {MAP}  
**Rule:** Code is canonical (`huggingface/app.py` → `workspace.fys_*`).

### Epics (tracked sub-issues)
""" + "\n".join(f"- [ ] #{n}" for n in EPICS) + f"""

### Slice 1 rollup (also tracked under their epics — do these first)
| Issue | Focus |
|-------|--------|
""" + "\n".join(f"| #{n} | Slice 1 plumbing |" for n in SLICE1) + f"""

### Board fields
Use Project columns/fields: **Status**, **Kind** (Master/Epic/Task), **Priority** (P0/P1/P2), **Area**, **Milestone**.

### Admin setup (labels, repo milestones, issue types, native Sub-issues)
Requires org **write/admin**. Run: `scripts/github_admin_setup.ps1`

### Milestones
- **M0** Truth & safety + org/pipelines
- **M1** Know yourself
- **M2** Real match substrate
- **M3** Serve & UX
- **M4** Campaign
- **M5** Partner scale

### Hierarchy
```
MASTER #{112 if False else 112}
  └── EPIC (tracked)
        └── Task (tracked on epic)
```
"""


def main():
    # Fix master - need correct master number 112
    body = MASTER_BODY.replace("#{112 if False else 112}", "#112")
    p = run(["gh", "issue", "edit", "112", "--repo", REPO, "--body", body])
    print("master edit", p.returncode, (p.stderr or "")[:200])

    time.sleep(2)
    q = run([
        "gh", "api", "graphql", "-f",
        'query=query { repository(owner:"For-Your-Service", name:"For-Your-Service") { issue(number:112) { trackedIssues(first:20) { nodes { number title } } } } }',
    ])
    print(q.stdout[:1500])

    # Project id + field option ids
    fields = json.loads(run([
        "gh", "project", "field-list", str(PROJECT_NUMBER),
        "--owner", PROJECT_OWNER, "--format", "json",
    ]).stdout)
    field_map = {f["name"]: f for f in fields["fields"]}
    kind = field_map["Kind"]
    priority = field_map["Priority"]
    kind_opts = {o["name"]: o["id"] for o in kind["options"]}
    pri_opts = {o["name"]: o["id"] for o in priority["options"]}

    proj = json.loads(run([
        "gh", "api", "graphql", "-f",
        f'query=query {{ user(login:"{PROJECT_OWNER}") {{ projectV2(number:{PROJECT_NUMBER}) {{ id }} }} }}',
    ]).stdout)
    project_id = proj["data"]["user"]["projectV2"]["id"]

    items = json.loads(run([
        "gh", "project", "item-list", str(PROJECT_NUMBER),
        "--owner", PROJECT_OWNER, "--limit", "100", "--format", "json",
    ]).stdout)["items"]

    def set_select(item_id, field_id, option_id):
        r = run([
            "gh", "project", "item-edit",
            "--project-id", project_id,
            "--id", item_id,
            "--field-id", field_id,
            "--single-select-option-id", option_id,
        ])
        return r.returncode == 0

    print("== Set Kind/Priority on project items ==")
    for it in items:
        content = it.get("content") or {}
        num = content.get("number")
        title = it.get("title") or content.get("title") or ""
        item_id = it["id"]
        if num == 112 or title.startswith("[MASTER]"):
            set_select(item_id, kind["id"], kind_opts["Master"])
            set_select(item_id, priority["id"], pri_opts["P0"])
            print("  Master", num)
        elif title.startswith("[EPIC") or (num in EPIC_PRI):
            set_select(item_id, kind["id"], kind_opts["Epic"])
            pri = EPIC_PRI.get(num, "P1")
            set_select(item_id, priority["id"], pri_opts[pri])
            print("  Epic", num, pri)
        else:
            set_select(item_id, kind["id"], kind_opts["Task"])
        time.sleep(0.15)

    print("Done")


if __name__ == "__main__":
    main()
