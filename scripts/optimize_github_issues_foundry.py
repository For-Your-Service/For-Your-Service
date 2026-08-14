#!/usr/bin/env python3
"""Create Foundry/code-optimized follow-on issues and patch Slice-1 bodies."""
from __future__ import annotations

import json
import subprocess
import time

REPO = "For-Your-Service/For-Your-Service"
MAP = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/FOUNDRY_ONTOLOGY_MAP.md"
SPEC = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/ISSUE_SPECS.md"
RESEARCH = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/RESEARCH_BRIEF.md"


def run(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, input=input_text, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def create(title: str, body: str, labels: list[str]) -> str | None:
    args = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
    for lab in labels:
        args.extend(["--label", lab])
    p = run(args)
    if p.returncode != 0:
        args = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
        p = run(args)
    if p.returncode != 0:
        print("FAIL", title, p.stderr[:300])
        return None
    print("OK", p.stdout.strip())
    time.sleep(0.35)
    return p.stdout.strip()


def edit(number: int, body: str) -> None:
    p = run(["gh", "issue", "edit", str(number), "--repo", REPO, "--body", body])
    print(("OK edit" if p.returncode == 0 else "FAIL edit"), number, (p.stderr or "")[:200])
    time.sleep(0.35)


def comment(number: int, body: str) -> None:
    p = run(["gh", "issue", "comment", str(number), "--repo", REPO, "--body", body])
    print(("OK comment" if p.returncode == 0 else "FAIL comment"), number)
    time.sleep(0.25)


NEW_ISSUES = [
    (
        "[FYS-015] Unify SiameseMatchingModel public API (ImportError)",
        """## Traceability
- **Issue ID:** `FYS-015`
- **Parent epic:** FYS-E006 (#33)
- **Slice:** 1 — plumbing (Foundry Stage 1)
- **Object/Action:** Match object / `RunMatch` function
- **Foundry map:** {map}
- **Research:** {research}

## Problem
`src/matching/matcher.py` imports `SiameseNetwork`, but `siamese_network.py` exports `SiameseMatchingModel`. Package and tests ImportError — neural path is dead.

## Goal
One public matching API that imports cleanly; align names with tests OR fix tests to match reality.

## Code anchors
- `src/matching/matcher.py` (import)
- `src/matching/siamese_network.py` (`SiameseMatchingModel`)
- `src/matching/__init__.py`
- `tests/matching/test_siamese_network.py`
- `tests/unit/test_neural_network.py`

## Foundry gate
A developer can `from src.matching import …` and run a fixture encode/score without ImportError. Deterministic path remains preferred for Slice 1 (`pipeline/job_matcher.py`) until embeddings are real.

## Acceptance criteria
- [ ] Single canonical class/name documented
- [ ] Package imports succeed
- [ ] Tests updated to import real symbols (or deleted if superseded by FYS-016)
- [ ] No silent alias that hides API drift

## Out of scope
Training a production Siamese model; that follows real embeddings (FYS-030).
""".format(map=MAP, research=RESEARCH),
        ["enhancement", "research", "P0", "matching", "tech-debt"],
    ),
    (
        "[FYS-016] Repair or delete lying matching/ingestion tests",
        """## Traceability
- **Issue ID:** `FYS-016`
- **Parent epic:** FYS-E012 (#39)
- **Slice:** 1 — plumbing (Foundry Stage 8 evals)
- **Foundry map:** {map}

## Problem
CI/local tests import symbols that do not exist (`SiameseNetwork`, `fetch_indeed_jobs`, encode helpers). Green test signal is false — Foundry: untested model upgrades / lying checks train teams to ignore failures.

## Goal
Every test in `tests/matching`, `tests/unit/test_neural_network.py`, `tests/unit/test_data_ingestion.py` either passes against real code or is removed with a pointer to the owning issue.

## Code anchors
- `tests/matching/test_siamese_network.py`
- `tests/unit/test_neural_network.py`
- `tests/unit/test_data_ingestion.py`
- Keep: `tests/pipeline/test_job_matcher.py` (working cosine path)

## Foundry gate
`pytest` on those paths either skips with reason tied to an open issue or passes — zero ImportError.

## Acceptance criteria
- [ ] Broken imports fixed or files deleted
- [ ] Document which matcher path is under test (pipeline vs neural)
- [ ] No new tests asserting against placeholder random embeddings as “success”
""".format(map=MAP),
        ["enhancement", "research", "P0", "matching", "tech-debt"],
    ),
    (
        "[FYS-017] Choose single JobMatcher path for Slice 1",
        """## Traceability
- **Issue ID:** `FYS-017`
- **Parent epic:** FYS-E006 (#33)
- **Slice:** 1 — plumbing
- **Object:** Match
- **Foundry map:** {map}

## Problem
Two `JobMatcher` classes: `src/pipeline/job_matcher.py` (cosine, tested, works) vs `src/matching/matcher.py` (neural, broken). Docs claim “neural matching” while HF hardcodes 0.75. Foundry: do not boil the ocean — get plumbing working with the path that already works.

## Goal
ADR: Slice 1 serving path uses **pipeline cosine matcher** (or fail-closed) once real embeddings exist; neural Siamese is Experimental until FYS-015+FYS-030 done. HF `/match` calls the chosen path only.

## Code anchors
- `src/pipeline/job_matcher.py` — KEEP for Slice 1
- `src/matching/matcher.py` — Experimental / fix via FYS-015
- `huggingface/app.py` — wire chosen path (also FYS-054)

## Foundry gate
One sentence in ARCHITECTURE + MATCHING_ALGORITHM: which class serves production `/match`.

## Acceptance criteria
- [ ] ADR committed under docs/
- [ ] HF imports only the chosen matcher
- [ ] Second path labeled Experimental in code comment + docs
""".format(map=MAP),
        ["enhancement", "research", "P0", "matching", "ops"],
    ),
    (
        "[FYS-045] Fix profile package imports (intake/summary missing)",
        """## Traceability
- **Issue ID:** `FYS-045`
- **Parent epic:** FYS-E005 (#32)
- **Object:** Veteran
- **Action:** `CompleteProfile`
- **Foundry map:** {map}

## Problem
`src/profile/models.py` defines solid `VeteranProfile` / self-understanding types, but `__init__.py` imports `.intake` and `.summary` modules that do not exist — package unimportable. Blocks Module 1 / ontology object for Veteran.

## Goal
Make `import src.profile` work: either implement minimal `intake.py` + `summary.py` stubs matching exports, or slim `__init__` to export only existing models until FYS-040/044 land.

## Code anchors
- `src/profile/__init__.py`
- `src/profile/models.py`

## Foundry gate
`from src.profile.models import VeteranProfile` and package import succeed in a one-liner smoke test.

## Acceptance criteria
- [ ] Package imports cleanly
- [ ] `matching_allowed` / readiness helper exported or clearly deferred to FYS-042
- [ ] No fake completeness that sets `ready_for_matching` without schema fields
""".format(map=MAP),
        ["enhancement", "research", "P0", "profile", "tech-debt"],
    ),
    (
        "[FYS-105] Remove hardcoded API credential defaults from config",
        """## Traceability
- **Issue ID:** `FYS-105`
- **Parent epic:** FYS-E011 (#38)
- **Foundry stage:** 3 Connect + markings — secrets at boundary
- **Foundry map:** {map}

## Problem
`src/api/config.py` ships hardcoded credential defaults; orchestrator O*NET init also mismatched. Violates secrets-only-in-scopes and Foundry “mark sensitive at ingest boundary.”

## Goal
Config reads env/Databricks secrets only; empty defaults; fail fast if missing in prod mode.

## Code anchors
- `src/api/config.py`
- `src/ingestion/orchestrator.py` (O*NET ctor)
- Related: FYS-003, FYS-101

## Foundry gate
Grep of `src/api/config.py` shows no live-looking secrets; missing secret → clear error.

## Acceptance criteria
- [ ] Hardcoded defaults removed
- [ ] Sample `.env.example` documents names only
- [ ] Orchestrator O*NET client constructs with documented params
""".format(map=MAP),
        ["enhancement", "research", "P0", "security", "tech-debt"],
    ),
]


# Optimized bodies for Slice-1 issues already filed
SLICE1_EDITS = {
    40: """## Traceability
- **Issue ID:** `FYS-001` · **Epic:** FYS-E001 (#28) · **Slice:** 1
- **Foundry:** Stage 2/8 project truth — one catalog/schema spine
- **Map:** {map}

## Problem
Code uses `workspace.fys_*`; SQL/notebooks use `main.fys_*`; PRODUCTION_STATUS uses `workspace.for_your_service`. Operators cannot trace a number to source (Foundry lineage failure mode: preprocessing / naming off-platform).

## Goal
Canonical schema map: catalog + schema + table for bronze/silver/gold/veteran; ADR picking one naming family.

## Code anchors
- `docs/PRODUCTION_STATUS.md` (`for_your_service`)
- `huggingface/app.py` (`fys_*`)
- `sql/*.sql` (`main.fys_*`)
- `scripts/manual_real_job_uploader.py`

## Foundry gate
Someone other than the author traces a job row from API → UC table name using only the map.

## Acceptance criteria
- [ ] Single table of production names in docs
- [ ] PRODUCTION_STATUS + layer specs + HF SQL agree
- [ ] Explicit deprecate note for non-canonical names
""".format(map=MAP),
    48: """## Traceability
- **Issue ID:** `FYS-014` · **Epic:** FYS-E002 (#29) · **Slice:** 1
- **Object:** JobPosting · **Foundry Stage:** 3 Connect as-is
- **Map:** {map}

## Problem
`BronzeWriter.write_job_postings` logs “would write” and does not persist — ingest is a collector only. No lineage from source sync to table.

## Goal
Write validated batches to canonical bronze table (per FYS-001) with `source`, `ingested_at`, external id for idempotency.

## Code anchors
- `src/ingestion/bronze_writer.py` (stub ~TODO)
- `src/ingestion/orchestrator.py`

## Foundry gate
At least one successful sync with recorded row count into bronze; raw-ish payload preserved (no silent drop of columns).

## Acceptance criteria
- [ ] Real UC/Delta or documented volume write
- [ ] No NotImplemented on primary path
- [ ] Integration/notebook proof with count
""".format(map=MAP),
    54: """## Traceability
- **Issue ID:** `FYS-030` · **Epic:** FYS-E004 (#31) · **Slice:** 1–2
- **Object:** Embedding · **Map:** {map}

## Problem
`EmbeddingGenerator` returns `np.random.rand(384)` — Match scores are noise. Foundry: do not put models in the ontology until they are high-trust; until then fail closed or use deterministic pipeline cosine on real text features only.

## Goal
Load `sentence-transformers/all-MiniLM-L6-v2` (or ADR successor); same text → same vector; store `embedding_model` on output.

## Code anchors
- `src/features/embedding_generator.py` (lines with random)
- [GOLD_LAYER_SPEC.md](../GOLD_LAYER_SPEC.md)

## Foundry gate
Unit test: cosine(self, self) ≈ 1; production path has zero random fallback.

## Acceptance criteria
- [ ] Real model encode
- [ ] Determinism within model
- [ ] No random in prod path
""".format(map=MAP),
    60: """## Traceability
- **Issue ID:** `FYS-042` · **Epic:** FYS-E005 (#32)
- **Object:** Veteran · **Action:** `RunMatch` submission criteria
- **Map:** {map}

## Problem
Matching without completeness gate violates research and Foundry action submission criteria — actions must refuse when rules fail.

## Goal
`ready_for_matching` boolean; Match API returns 4xx + missing fields when false. Depends on FYS-045 package importability.

## Code anchors
- `src/profile/models.py`
- `huggingface/app.py` `/match`

## Foundry gate
Unauthorized/incomplete profile cannot create Match objects.

## Acceptance criteria
- [ ] Gate rules documented
- [ ] API lists missing fields
- [ ] Wired to FYS-061
""".format(map=MAP),
    67: """## Traceability
- **Issue ID:** `FYS-054` · **Epic:** FYS-E006 (#33) · **Slice:** 1
- **Action:** `RunMatch` · **Map:** {map}

## Problem
`huggingface/app.py` hardcodes `match_score=0.75` and canned reasons — unexplainable automation (Foundry Stage 6 anti-pattern).

## Goal
Wire chosen matcher from FYS-017; if embeddings/matcher unavailable, return explicit 503/error — never fake confidence.

## Code anchors
- `huggingface/app.py` (`match_veteran_to_jobs`, ~0.75)
- `src/pipeline/job_matcher.py`

## Foundry gate
Successful match response factors come from code, not string literals; failure mode is visible.

## Acceptance criteria
- [ ] No hardcoded success score on happy path
- [ ] Integration test with fixture embeddings/jobs
""".format(map=MAP),
    70: """## Traceability
- **Issue ID:** `FYS-061` · **Epic:** FYS-E007 (#34) · **Slice:** 1
- **Action:** `RunMatch` · **Surface:** FastAPI (HF)
- **Map:** {map}

## Problem
`/match` must enforce profile gate and return Match objects with factor cards — find → decide path for veteran/counselor.

## Goal
`POST /match` requires `ready_for_matching`; returns jobs + factors + grounded explanation; uses FYS-017 matcher.

## Code anchors
- `huggingface/app.py`
- Depends: FYS-042, FYS-054, FYS-017

## Foundry gate
Primary user path: complete profile → match list with factors without engineer help (API-level).

## Acceptance criteria
- [ ] Gate enforced
- [ ] Factors in response JSON
- [ ] Latency target documented
""".format(map=MAP),
    91: """## Traceability
- **Issue ID:** `FYS-102` · **Epic:** FYS-E011 (#38)
- **Foundry:** Roles / markings at surface
- **Map:** {map}

## Problem
CORS allowlist includes `"*"` with `allow_credentials=True` in `huggingface/app.py` — invalid and unsafe for general use.

## Goal
Explicit origin allowlist for known frontends only.

## Code anchors
- `huggingface/app.py` CORS middleware (~lines 28–38)

## Foundry gate
Browser from unknown origin cannot call credentialed API.

## Acceptance criteria
- [ ] No wildcard in production CORS
- [ ] Documented allowed origins
""".format(map=MAP),
}


EPIC_COMMENT = f"""### Foundry / Ontology optimization (2026-08-14)

Issues under this epic are governed by the Foundry-derived map (object types, actions, Slice 1 plumbing-first):

{MAP}

**Slice 1 (ship first):** profile gate importable → real (or fail-closed) match → bronze write → no fake HF scores.
Campaign/Partner object types stay Later until plumbing works.

Code audit highlights live in `{MAP}` § Code-grounded blockers. New follow-ons: FYS-015, FYS-016, FYS-017, FYS-045, FYS-105.
"""


def main() -> None:
    print("== New issues ==")
    created = []
    for title, body, labels in NEW_ISSUES:
        url = create(title, body, labels)
        if url:
            created.append(url)

    print("== Slice-1 body upgrades ==")
    for num, body in SLICE1_EDITS.items():
        edit(num, body)

    print("== Epic comments ==")
    for num in range(28, 40):
        comment(num, EPIC_COMMENT)

    # Map file
    with open("docs/epics/GITHUB_ISSUE_MAP.md", "w", encoding="utf-8") as f:
        f.write("# GitHub Issue Map — For Your Service\n\n")
        f.write("Filed on `For-Your-Service/For-Your-Service`.\n\n")
        f.write("## Epics\n\n")
        for n, eid in zip(range(28, 40), [f"FYS-E{i:03d}" for i in range(1, 13)]):
            f.write(f"- [{eid}](https://github.com/For-Your-Service/For-Your-Service/issues/{n})\n")
        f.write("\n## Catalog issues\n\n")
        f.write("FYS-001…FYS-114 → GitHub #40–#98 (see `gh issue list`).\n\n")
        f.write("## Foundry / code follow-ons\n\n")
        for u in created:
            f.write(f"- {u}\n")
        f.write(f"\n## Doctrine\n\n- [FOUNDRY_ONTOLOGY_MAP.md](FOUNDRY_ONTOLOGY_MAP.md)\n- [RESEARCH_BRIEF.md](RESEARCH_BRIEF.md)\n")
    print("Wrote docs/epics/GITHUB_ISSUE_MAP.md")
    print("created", created)


if __name__ == "__main__":
    main()
