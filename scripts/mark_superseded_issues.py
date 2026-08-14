#!/usr/bin/env python3
"""Mark obsolete issues SUPERSEDED (edit-only; close requires admin)."""
from __future__ import annotations

import json
import subprocess
import time

REPO = "For-Your-Service/For-Your-Service"

SUPERSEDED = {
    1: ("#112 / FYS-E002+E013", "GCP landing bucket — production spine is workspace.fys_* via Databricks+HF"),
    2: ("#112 / FYS-E002", "GCP Cloud Function ingest — demoted; see FYS-002 single path"),
    3: ("#112 / FYS-118", "Delta ingest config — continues as medallion job graph"),
    4: ("#112 / SPEC #114", "E2E CF→GCS→DBX — Slice 1 E2E replaces this"),
    5: ("#112", "Historical DONE — archive under new program"),
    6: ("#112 / E004+E006", "Historical DONE analytics — matching continues under SPECs"),
    7: ("#112 / E002", "Duplicate GCP CF IN PROGRESS"),
    8: ("#112 / FYS-110", "E2E TODO — covered by quality + bronze specs"),
    9: ("#112", "Historical DONE foundation"),
    10: ("#112 / E004+E006", "Historical DONE vector pipeline"),
    11: ("#109 FYS-118", "Historical DONE job JSON — rewrite without /Users paths"),
    12: ("#112 / E002", "Historical DONE GCP microservices"),
    13: ("#112 / FYS-002", "Duplicate GCP CF IN PROGRESS"),
    14: ("#112 / SPEC #114", "Duplicate E2E backlog"),
    15: ("#123 SPEC-E011 / FYS-100", "Duplicate PII backlog"),
    16: ("#123 SPEC-E011 / FYS-100", "Duplicate PII backlog"),
    21: ("#112 / FYS-002", "GCP CF — not on code-canonical serving path"),
    22: ("#112", "Local Task Scheduler — defer; not Slice 1"),
    23: ("#112 / SPEC #114", "Duplicate E2E backlog"),
    24: ("#123 SPEC-E011 / FYS-100", "Duplicate PII backlog"),
}


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    for num, (replaces, why) in SUPERSEDED.items():
        view = run(["gh", "issue", "view", str(num), "--repo", REPO, "--json", "title,body,state"])
        if view.returncode != 0:
            print("skip", num)
            continue
        data = json.loads(view.stdout)
        if data["state"] != "OPEN":
            print("already closed", num)
            continue
        title = data["title"]
        if not title.startswith("[SUPERSEDED]"):
            new_title = f"[SUPERSEDED] {title}"[:256]
            p = run(["gh", "issue", "edit", str(num), "--repo", REPO, "--title", new_title])
            print(("OK title" if p.returncode == 0 else "FAIL title"), num, (p.stderr or "")[:100])
            time.sleep(0.3)
        body = data.get("body") or ""
        banner = (
            f"> **SUPERSEDED — do not implement.** Replaced by {replaces}. "
            f"{why} **Org admin: please close this issue.**\n\n"
        )
        if "SUPERSEDED — do not implement" not in body:
            p = run(["gh", "issue", "edit", str(num), "--repo", REPO, "--body", banner + body])
            print(("OK body" if p.returncode == 0 else "FAIL body"), num, (p.stderr or "")[:100])
            time.sleep(0.3)
        run([
            "gh", "issue", "comment", str(num), "--repo", REPO,
            "--body",
            f"Marked superseded. Track work on MASTER #112. Replacement: {replaces}. **Org admin please close.**",
        ])
        time.sleep(0.35)

    nums = ", ".join(f"#{n}" for n in sorted(SUPERSEDED))
    run([
        "gh", "issue", "comment", "112", "--repo", REPO,
        "--body",
        "## Admin close list (filer lacks CloseIssue permission)\n\n"
        f"Please **close** these superseded/historical issues: {nums}\n\n"
        "They are titled `[SUPERSEDED]` and point at this program / SPECs.\n"
        "Also run `scripts/github_admin_setup.ps1` for `ready-for-agent` labels.",
    ])
    print("Done")


if __name__ == "__main__":
    main()
