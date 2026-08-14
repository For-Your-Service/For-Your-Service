#!/usr/bin/env python3
"""Comment SUPERSEDED on legacy issues we cannot edit/close."""
from __future__ import annotations

import subprocess
import time

REPO = "For-Your-Service/For-Your-Service"
MSGS = {
    1: "SUPERSEDED → MASTER #112 / E002+E013. Code-canonical is `workspace.fys_*` (not GCS landing). **Admin: close.**",
    2: "SUPERSEDED → #112 / FYS-E002. GCP CF demoted; path is Databricks+HF. **Admin: close.**",
    3: "SUPERSEDED → #109 FYS-118 medallion job graph. **Admin: close.**",
    4: "SUPERSEDED → SPEC #114 / Slice 1 E2E. **Admin: close.**",
    5: "Historical DONE — archive under #112. **Admin: close.**",
    6: "Historical DONE — matching continues SPEC #116/#118. **Admin: close.**",
    7: "SUPERSEDED duplicate of GCP CF work → #112 / E002. **Admin: close.**",
    8: "SUPERSEDED → FYS-110 / SPEC #124. **Admin: close.**",
    9: "Historical DONE — archive under #112. **Admin: close.**",
    10: "Historical DONE → SPEC #116/#118. **Admin: close.**",
    11: "Historical DONE → rewrite as FYS-118 #109. **Admin: close.**",
    12: "Historical DONE → E002 under #112. **Admin: close.**",
    13: "SUPERSEDED duplicate GCP CF → FYS-002 / #112. **Admin: close.**",
    14: "SUPERSEDED duplicate E2E → SPEC #114. **Admin: close.**",
    15: "SUPERSEDED duplicate PII → SPEC #123 / FYS-100. **Admin: close.**",
    16: "SUPERSEDED duplicate PII → SPEC #123 / FYS-100. **Admin: close.**",
    21: "SUPERSEDED GCP CF IN PROGRESS → FYS-002 / #112. **Admin: close.**",
    22: "DEFER local Task Scheduler — not Slice 1. Reopen only if needed. **Admin: close or leave.**",
    23: "SUPERSEDED duplicate E2E → SPEC #114. **Admin: close.**",
    24: "SUPERSEDED duplicate PII → SPEC #123. **Admin: close.**",
}


def main():
    for num, msg in MSGS.items():
        p = subprocess.run(
            ["gh", "issue", "comment", str(num), "--repo", REPO, "--body", msg],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        print(("OK" if p.returncode == 0 else "FAIL"), num)
        time.sleep(0.35)
    print("Done")


if __name__ == "__main__":
    main()
