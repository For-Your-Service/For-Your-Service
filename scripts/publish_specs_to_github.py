#!/usr/bin/env python3
"""Publish docs/epics/specs/*.md as GitHub SPEC issues; link to parent epics."""
from __future__ import annotations

import re
import subprocess
import time
from pathlib import Path

REPO = "For-Your-Service/For-Your-Service"
SPECS = Path("docs/epics/specs")

# filename stem -> parent epic issue number
PARENT = {
    "SPEC-E001-platform-truth": 28,
    "SPEC-E002-bronze-ingestion": 29,
    "SPEC-E003-silver-enrichment": 30,
    "SPEC-E004-gold-embeddings": 31,
    "SPEC-E005-veteran-profile": 32,
    "SPEC-E006-matching-engine": 33,
    "SPEC-E007-serving-api": 34,
    "SPEC-E008-veteran-experience": 35,
    "SPEC-E009-campaign-pathways": 36,
    "SPEC-E010-partner-placement": 37,
    "SPEC-E011-security-privacy": 38,
    "SPEC-E012-quality-observability": 39,
    "SPEC-E013-org-pipelines": 104,
}


def run(args, input_text=None):
    return subprocess.run(
        args, input=input_text, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def main():
    created = []
    for path in sorted(SPECS.glob("SPEC-E*.md")):
        stem = path.stem
        parent = PARENT.get(stem)
        title_human = stem.replace("SPEC-", "").replace("-", " ")
        body = path.read_text(encoding="utf-8")
        header = f"""**Triage:** `ready-for-agent`  
**Parent epic:** #{parent}  
**Master:** #112  
**Seams:** Match serving · Bronze land+DQ · Profile gate  
**Code-canonical:** `workspace.fys_*` from serving  

---

"""
        full = header + body
        # Prefer body-file for size
        tmp = Path("tmp_spec_body.md")
        tmp.write_text(full, encoding="utf-8")
        title = f"[SPEC][ready-for-agent] {title_human}"
        p = run([
            "gh", "issue", "create", "--repo", REPO,
            "--title", title,
            "--body-file", str(tmp),
        ])
        if p.returncode != 0:
            print("FAIL", stem, p.stderr[:300])
            continue
        url = p.stdout.strip()
        num = int(url.rstrip("/").split("/")[-1])
        print("OK", num, stem)
        created.append((stem, num, parent, url))
        # Label attempt (may fail without write)
        run(["gh", "issue", "edit", str(num), "--repo", REPO, "--add-label", "ready-for-agent"])
        # Link on parent epic
        if parent:
            run([
                "gh", "issue", "comment", str(parent), "--repo", REPO,
                "--body", f"### AFK Spec published\n\n- [ ] #{num} — `{stem}` (`ready-for-agent`)\n\nImplement against this spec; code is canonical.",
            ])
        time.sleep(0.45)

    # Update master with SPEC checklist
    spec_lines = "\n".join(f"- [ ] #{n} — {stem}" for stem, n, _, _ in created)
    run([
        "gh", "issue", "comment", "112", "--repo", REPO,
        "--body", f"## SPEC issues (ready-for-agent)\n\n{spec_lines}\n\nIndex: `docs/epics/specs/README.md` (commit when docs land on main).",
    ])

    # Map file
    lines = ["# Published SPEC Issues\n"]
    for stem, num, parent, url in created:
        lines.append(f"- [{stem}]({url}) → parent epic #{parent}")
    Path("docs/epics/specs/GITHUB_SPECS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote docs/epics/specs/GITHUB_SPECS.md")
    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
