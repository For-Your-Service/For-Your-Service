#!/usr/bin/env python3
"""Create FYS architecture epics + issues on GitHub via gh CLI."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any

REPO = "For-Your-Service/For-Your-Service"
SPEC = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/ISSUE_SPECS.md"
PROGRAM = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/PROGRAM.md"
RESEARCH = "https://github.com/For-Your-Service/For-Your-Service/blob/main/docs/epics/RESEARCH_BRIEF.md"


def run(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def gh_api(method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, str]:
    args = ["gh", "api", "-X", method, path]
    if body is not None:
        args.extend(["--input", "-"])
        p = run(args, json.dumps(body))
    else:
        p = run(args)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def ensure_label(name: str, color: str, description: str) -> None:
    code, out = gh_api(
        "POST",
        f"repos/{REPO}/labels",
        {"name": name, "color": color, "description": description},
    )
    if code == 0:
        print(f"  label + {name}")
        return
    code2, out2 = gh_api(
        "PATCH",
        f"repos/{REPO}/labels/{name}",
        {"name": name, "color": color, "description": description},
    )
    if code2 == 0:
        print(f"  label ~ {name}")
    else:
        print(f"  label ! {name}: {out.strip()[:200]} | {out2.strip()[:200]}")


def ensure_milestone(title: str) -> int | None:
    code, out = gh_api(
        "POST",
        f"repos/{REPO}/milestones",
        {"title": title, "state": "open"},
    )
    if code == 0:
        num = json.loads(out.split("\n")[0] if out.strip().startswith("{") else out).get("number")
        # gh api may return raw JSON
        try:
            data = json.loads(out)
            num = data["number"]
        except Exception:
            p = run(["gh", "api", f"repos/{REPO}/milestones", "--jq", f'.[] | select(.title=="{title}") | .number'])
            num = int(p.stdout.strip()) if p.stdout.strip().isdigit() else None
        print(f"  milestone + {title} -> {num}")
        return num
    # fetch existing
    p = run(["gh", "api", f"repos/{REPO}/milestones", "--jq", f'.[] | select(.title=="{title}") | .number'])
    if p.stdout.strip().isdigit():
        num = int(p.stdout.strip())
        print(f"  milestone = {title} -> {num}")
        return num
    print(f"  milestone ! {title}: {out.strip()[:300]}")
    return None


def create_issue(title: str, body: str, labels: list[str], milestone: int | None) -> str | None:
    args = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
    for lab in labels:
        args.extend(["--label", lab])
    if milestone is not None:
        args.extend(["--milestone", str(milestone)])
    p = run(args)
    if p.returncode != 0:
        # retry without labels/milestone if label permission flaky
        print(f"  WARN first try failed: {p.stderr.strip()[:200]}")
        args = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
        p = run(args)
    if p.returncode != 0:
        print(f"  FAIL {title}: {p.stderr.strip()[:300]}")
        return None
    url = p.stdout.strip()
    print(f"  OK {url}")
    time.sleep(0.4)
    return url


LABELS = [
    ("epic", "B392F0", "Capability epic (parent)"),
    ("research", "0E8A16", "Derived from architecture research"),
    ("P0", "D93F0B", "Required for trustworthy matching"),
    ("P1", "FBCA04", "Campaign / UX / partner differentiation"),
    ("P2", "C5DEF5", "Scale and intelligence later"),
    ("bronze", "CD7F32", "Bronze / ingestion"),
    ("silver", "C0C0C0", "Silver / enrichment"),
    ("gold", "FFD700", "Gold / embeddings"),
    ("profile", "1D76DB", "Veteran profile system"),
    ("matching", "5319E7", "Matching engine"),
    ("ingestion", "BFDADC", "Job ingestion"),
    ("api", "006B75", "Serving API"),
    ("ux", "E99695", "Veteran experience UI"),
    ("campaign", "F9D0C4", "Campaign and pathways"),
    ("partner", "D4C5F9", "Partner / 7 Eagle placement"),
    ("security", "B60205", "Security and privacy"),
    ("ops", "FEF2C0", "Platform truth / ops"),
    ("tech-debt", "EEEEEE", "Stubs, drift, placeholders"),
    ("enhancement", "a2eeef", "New feature or request"),
]

MILESTONES = [
    "M0 Truth and Safety",
    "M1 Know Yourself",
    "M2 Real Match Substrate",
    "M3 Serve and UX",
    "M4 Campaign Differentiator",
    "M5 Partner Scale",
]

EPICS = [
    ("FYS-E001", "Platform Truth", "M0", "P0", "ops", "One production path; schema + credential docs match runtime."),
    ("FYS-E002", "Bronze Ingestion", "M2", "P0", "ingestion,bronze", "Reliable multi-source job landings, validated, scheduled."),
    ("FYS-E003", "Silver Enrichment", "M2", "P0", "silver", "O*NET skills + MOS soft prior + titles/industry."),
    ("FYS-E004", "Gold Embeddings", "M2", "P0", "gold", "Real 384-dim vectors for jobs + veterans."),
    ("FYS-E005", "Veteran Profile System", "M1", "P0", "profile", "Self-understanding + profile gate + context loader."),
    ("FYS-E006", "Matching Engine", "M2", "P0", "matching", "Hard filters → hybrid → white-box → grounded explain."),
    ("FYS-E007", "Serving API", "M3", "P0", "api", "FastAPI contracts for profile, match, jobs, health."),
    ("FYS-E008", "Veteran Experience", "M3", "P1", "ux", "Wizard + match dashboard for general veteran UX."),
    ("FYS-E009", "Campaign and Pathways", "M4", "P1", "campaign", "Bidirectional fit, Side Door, SkillBridge/federal tags."),
    ("FYS-E010", "Partner Placement", "M5", "P1", "partner", "7 Eagle batch + SITREP + conversion metrics."),
    ("FYS-E011", "Security and Privacy", "M0", "P0", "security", "Secrets, CORS, PII split ops vs analytics."),
    ("FYS-E012", "Quality and Observability", "M5", "P1", "ops", "Tests, Precision@k, monitoring, runbooks."),
]

# id, title, epic, milestone key, priority, labels, problem, goal, acceptance bullets
ISSUES: list[tuple] = [
    ("FYS-001", "Canonical Unity Catalog schema map", "FYS-E001", "M0", "P0", "ops,tech-debt",
     "Docs and code disagree on table names (fys_* vs for_your_service).",
     "Single schema map of bronze/silver/gold/profile tables.",
     ["One doc table lists every production table name", "PRODUCTION_STATUS and layer specs use same names"]),
    ("FYS-002", "Single production serving path", "FYS-E001", "M0", "P0", "ops",
     "AWS/GCP/HF/Databricks surfaces compete for the production path.",
     "Document and enforce Databricks lakehouse + HF FastAPI as production.",
     ["README + DEPLOYMENT_STRATEGY state one primary path", "Deploy checklist matches that path only"]),
    ("FYS-003", "API credential status truth", "FYS-E001", "M0", "P0", "ops,tech-debt",
     "Credential docs conflict (working vs 401).",
     "Living status matrix per provider (USAJOBS, JSearch, Adzuna, O*NET).",
     ["Matrix: provider → secret → last verified → status"]),
    ("FYS-004", "Nested/duplicate tree cleanup plan", "FYS-E001", "M0", "P0", "ops,tech-debt",
     "Nested For-Your-Service/ confuses contributors.",
     "Document canonical root; remove or deprecate duplicate tree.",
     ["ROOT_DIRECTORY_GUIDE states canonical paths", "Duplicate marked DEPRECATED or removed"]),
    ("FYS-010", "Harden multi-source orchestrator", "FYS-E002", "M2", "P0", "ingestion,bronze",
     "Partial failures undermine general job supply.",
     "USAJOBS + JSearch + Adzuna with per-source success/fail.",
     ["One source failure does not abort others", "Bronze rows carry source, ingested_at, provenance"]),
    ("FYS-011", "Bronze schema and validation", "FYS-E002", "M2", "P0", "ingestion,bronze",
     "Incomplete jobs can land in bronze.",
     "Validator rejects incomplete jobs; quarantine invalids.",
     ["Required title, company/agency, location/remote, source id", "Invalid rows quarantined with reason"]),
    ("FYS-012", "Regional config MSA packs", "FYS-E002", "M2", "P1", "ingestion",
     "Region logic is hard-coded / Greenville-only.",
     "Config-driven region packs (Greenville first).",
     ["Region pack config documented", "Default region in README"]),
    ("FYS-013", "Ingestion schedule and idempotency", "FYS-E002", "M2", "P1", "ingestion",
     "Re-runs can duplicate postings.",
     "Daily schedule with idempotent source+external id keys.",
     ["Same-day re-run does not duplicate active postings"]),
    ("FYS-014", "Fix BronzeWriter stub path", "FYS-E002", "M2", "P0", "ingestion,bronze,tech-debt",
     "Stub writer blocks production landings.",
     "Working write path to Unity Catalog bronze.",
     ["Integration/notebook writes a batch", "No NotImplemented on primary path"]),
    ("FYS-020", "O*NET client production path", "FYS-E003", "M2", "P0", "silver",
     "O*NET not reliably wired for enrichment.",
     "Live O*NET client with secrets + rate limit + cache.",
     ["Occupations + skills fetch for sample codes", "Cache avoids API hammering"]),
    ("FYS-021", "MOS to O*NET soft prior", "FYS-E003", "M2", "P0", "silver,matching",
     "Static MOS tables insufficient; MOS must be soft prior not sole ranker.",
     "Map MOS/AFSC/rating → SOC/O*NET set with provenance.",
     ["Ranked SOC candidates for common MOS", "Empty crosswalk does not mean empty match results"]),
    ("FYS-022", "Skill extraction to O*NET taxonomy", "FYS-E003", "M2", "P0", "silver",
     "Jobs lack structured skills for matching.",
     "Job description → skills array with importance + enrichment_version.",
     ["Silver rows include skills struct array", "enrichment_version set"]),
    ("FYS-023", "Standardized titles and industry", "FYS-E003", "M2", "P1", "silver",
     "Titles/industry inconsistent across sources.",
     "Populate standardized_title and industry_sector on silver.",
     ["Mapping rules documented", "High fill rate on fixture corpus"]),
    ("FYS-024", "Silver transform job", "FYS-E003", "M2", "P0", "silver",
     "Bronze→Silver not aligned to SILVER_LAYER_SPEC.",
     "Idempotent enrich job with enriched_date partition.",
     ["Idempotent enrich", "Matches SILVER_LAYER_SPEC"]),
    ("FYS-030", "Replace placeholder embeddings", "FYS-E004", "M2", "P0", "gold,tech-debt",
     "np.random.rand embeddings invalidate all match claims.",
     "Load sentence-transformers MiniLM; encode real text.",
     ["Same text → same vector", "No random fallback in production", "Unit test cosine(self,self)≈1"]),
    ("FYS-031", "Job embedding pipeline", "FYS-E004", "M2", "P0", "gold",
     "Gold job vectors missing or fake.",
     "Title+description+skills → 384-dim gold with embedding_model.",
     ["Gold schema matches GOLD_LAYER_SPEC", "Model name stored per row"]),
    ("FYS-032", "Veteran embedding from civilianized text", "FYS-E004", "M2", "P0", "gold,profile",
     "Raw MOS jargon embeddings mismatch employers.",
     "Embed civilianized_summary + skills (depends on FYS-043).",
     ["Uses civilianized text", "Documented in MATCHING_ALGORITHM"]),
    ("FYS-033", "Embedding versioning and rebuild", "FYS-E004", "M2", "P1", "gold",
     "Model bumps leave stale vectors.",
     "Rebuild runbook; filter match queries by embedding_model.",
     ["Rebuild runbook exists", "embedding_model filter on match"]),
    ("FYS-040", "Self-understanding intake schema", "FYS-E005", "M1", "P0", "profile",
     "Matching without self-understanding produces wrong-channel noise.",
     "Exactly 3 Five Elements, Operator Compass, archetype, prefer/avoid, WHY.",
     ["Schema in VETERAN_PROFILE_SCHEMA", "ready_for_matching requires this block"]),
    ("FYS-041", "Core veteran profile", "FYS-E005", "M1", "P0", "profile",
     "Incomplete military/constraint data for general users.",
     "Identity + MOS + clearance + geo/remote + salary + ETS + targets.",
     ["Completeness checker lists missing fields", "Generic fixture + demo fixture"]),
    ("FYS-042", "Profile completeness gate", "FYS-E005", "M1", "P0", "profile,api",
     "Match can run on incomplete profiles.",
     "ready_for_matching boolean; match API rejects false.",
     ["Gate rules documented", "API returns missing-field list"]),
    ("FYS-043", "Military to civilian translation fields", "FYS-E005", "M1", "P0", "profile",
     "Employers do not understand MOS jargon.",
     "civilianized_summary + skill vocabulary + quantified bullets.",
     ["Translator stores fields on profile", "Used by embeddings and explanations"]),
    ("FYS-044", "Profile context loader hot summary", "FYS-E005", "M1", "P0", "profile",
     "Full profiles are too heavy for API/agents.",
     "Token-efficient hot summary; deep slices on demand.",
     ["Default = summary only", "Expand flags for deep sections"]),
    ("FYS-050", "Hard filters before rank", "FYS-E006", "M2", "P0", "matching",
     "Location/clearance treated as soft noise; research says hard gates.",
     "Pre-filter geo/remote/radius, clearance, salary, work auth.",
     ["Clearance-required jobs excluded when lacking clearance", "Soft-fail message when empty"]),
    ("FYS-051", "Hybrid retrieval BM25 plus dense", "FYS-E006", "M2", "P0", "matching",
     "Dense-only retrieval misses keyword/MOS tokens.",
     "Candidate set from lexical + vector before scoring.",
     ["Configurable k per channel", "Dedupe by job_id"]),
    ("FYS-052", "Multi-factor white-box score", "FYS-E006", "M2", "P0", "matching",
     "Black-box cosine cannot be trusted or explained.",
     "Weighted skills + MOS prior + values + clearance + salary; factor JSON.",
     ["Weights documented", "No hardcoded constant score on primary path"]),
    ("FYS-053", "Grounded match explanations", "FYS-E006", "M2", "P0", "matching",
     "LLM narratives invent skills employers never asked for.",
     "Narrative from factor card only.",
     ["Explanation cites only present factors"]),
    ("FYS-054", "Remove stub match scores in HF paths", "FYS-E006", "M2", "P0", "matching,api,tech-debt",
     "HF/app hardcodes confidence (e.g. 0.75).",
     "Real matcher or explicit unavailable error.",
     ["No hardcoded confidence on success path"]),
    ("FYS-055", "MOS prior integration in ranker", "FYS-E006", "M2", "P0", "matching,silver",
     "MOS prior not wired into scoring.",
     "Silver mos_matches boosts; does not sole-rank.",
     ["Non-prior jobs can still surface"]),
    ("FYS-060", "Veteran profile API", "FYS-E007", "M3", "P0", "api,profile",
     "No stable CRUD for general veteran profiles.",
     "Upsert/get summary on FastAPI with OpenAPI schema.",
     ["OpenAPI documents schema", "PII only on authenticated ops paths"]),
    ("FYS-061", "Match API with profile gate", "FYS-E007", "M3", "P0", "api,matching",
     "/match must not run without ready_for_matching.",
     "POST /match returns jobs + factors + explanation.",
     ["Gate enforced", "Latency target documented"]),
    ("FYS-062", "Jobs query API", "FYS-E007", "M3", "P1", "api",
     "UI/debug lack filtered job list.",
     "Filtered job list from silver/gold.",
     ["Basic filters work"]),
    ("FYS-063", "Health and readiness endpoints", "FYS-E007", "M3", "P0", "api",
     "Cannot tell process up vs Databricks/model ready.",
     "/health + /ready (Databricks + model flag).",
     ["Both endpoints documented and tested"]),
    ("FYS-064", "Rate limiting and caching", "FYS-E007", "M3", "P1", "api",
     "Public API can be abused / repeat-expensive.",
     "Rate limits + cache per RATE_LIMITING.md.",
     ["Limits documented and enforced"]),
    ("FYS-070", "Profile creation wizard", "FYS-E008", "M3", "P1", "ux,profile",
     "Veterans need guided intake, not raw JSON.",
     "Multi-step: self-understanding → military → preferences → gate.",
     ["Cannot finish without gate fields", "Mobile-responsive basics"]),
    ("FYS-071", "Recommendation dashboard", "FYS-E008", "M3", "P1", "ux,matching",
     "No veteran-facing match UI.",
     "Cards with score, factors, pathway badges, CTAs.",
     ["Factor visibility on each card"]),
    ("FYS-072", "Match explanation UI", "FYS-E008", "M3", "P1", "ux,matching",
     "Black-box scores erode trust.",
     "Factor breakdown visible in UI.",
     ["No score-only view as sole UX"]),
    ("FYS-073", "Email notifications", "FYS-E008", "M5", "P2", "ux",
     "Veterans miss new high-fit roles.",
     "Optional email on new matches / campaign updates.",
     ["Opt-in only"]),
    ("FYS-074", "Accessibility pass", "FYS-E008", "M3", "P1", "ux",
     "Must meet basic a11y for general use.",
     "Pass checklist in ACCESSIBILITY.md.",
     ["Keyboard + contrast basics"]),
    ("FYS-080", "Bidirectional employer Go/No-Go", "FYS-E009", "M4", "P1", "campaign,matching",
     "One-way job scores ignore company↔candidate fit weights from research.",
     "Weighted fit + tiers Apply Now / Prepare / Monitor / Bypass.",
     ["Location can hard-fail", "Tier stored on package"]),
    ("FYS-081", "Campaign entity and funnel", "FYS-E009", "M4", "P1", "campaign",
     "No first-class apply+outreach object.",
     "company + role + application + outreach + funnel stages.",
     ["Stages Target→Offer (or equivalent)", "Health color on stalled stages"]),
    ("FYS-082", "Side Door warm outreach hooks", "FYS-E009", "M4", "P1", "campaign",
     "Cold ATS alone fails; research needs warm path.",
     "Same-day ATS apply + warm-path task list (CRM-lite).",
     ["Outreach tasks linked to campaign", "Response tracking field"]),
    ("FYS-083", "SkillBridge CSP pathway tags", "FYS-E009", "M4", "P1", "campaign",
     "Pathway windows missed vs ETS.",
     "Tag jobs/employers; ETS eligibility warnings.",
     ["Badges on matches", "Timeline warnings"]),
    ("FYS-084", "Federal USAJOBS preference path", "FYS-E009", "M4", "P1", "campaign",
     "Federal preference path under-surfaced.",
     "Badge + guidance for preference-eligible USAJOBS roles.",
     ["Badge on eligible silver/gold rows"]),
    ("FYS-085", "HoH fellowship channel tags", "FYS-E009", "M4", "P2", "campaign",
     "Fellowship/HoH channels not tagged.",
     "Optional pathway tags for HoH/fellowships.",
     ["Tags appear when source supports them"]),
    ("FYS-090", "Partner organization object", "FYS-E010", "M5", "P1", "partner",
     "No partner tenancy for 7 Eagle cohorts.",
     "Partner id, users, cohort permissions.",
     ["Partner record creatable"]),
    ("FYS-091", "Cohort batch veteran ingest", "FYS-E010", "M5", "P1", "partner",
     "Partners cannot onboard cohorts at once.",
     "CSV/API batch create under partner.",
     ["Batch creates profiles under partner"]),
    ("FYS-092", "Funnel SITREP dashboard", "FYS-E010", "M5", "P1", "partner",
     "Partners lack placement funnel visibility.",
     "Aggregates + drill-down; weekly export; PII-minimized.",
     ["Aggregates without excess PII", "SITREP export"]),
    ("FYS-093", "Placement outcome metrics", "FYS-E010", "M5", "P1", "partner",
     "No offer-before-ETS / time-to-interview metrics.",
     "Align METRICS.md with partner outcomes.",
     ["Offer-before-ETS tracked", "Time-to-first-interview tracked"]),
    ("FYS-100", "Ops vs analytics PII split", "FYS-E011", "M0", "P0", "security",
     "PII in APIs vs anonymizer docs inconsistent.",
     "Ops may hold contact; analytics/match use anonymized projection.",
     ["Anonymizer on analytics path", "Docs match code"]),
    ("FYS-101", "Secrets only in scopes", "FYS-E011", "M0", "P0", "security",
     "Secret leakage risk in config samples.",
     "No secrets in git; Databricks + HF secret names documented.",
     ["No secrets in tracked samples", "Secret names documented"]),
    ("FYS-102", "CORS lockdown", "FYS-E011", "M0", "P0", "security,api",
     "CORS * is unsafe for general use.",
     "Allowlist known frontends.",
     ["No wildcard CORS in production config"]),
    ("FYS-103", "AuthN for write APIs", "FYS-E011", "M3", "P1", "security,api",
     "Write APIs open or underspecified.",
     "Token/API key for profile write + partner routes.",
     ["Unauthenticated writes rejected"]),
    ("FYS-104", "Retention alignment", "FYS-E011", "M5", "P1", "security",
     "Retention policy may not match pipeline reality.",
     "Align DATA_RETENTION_POLICY with tables.",
     ["Policy cites actual tables"]),
    ("FYS-110", "Match path unit and integration tests", "FYS-E012", "M2", "P1", "matching",
     "Match path under-tested.",
     "Tests for filters, scoring, gate, no-random-embeddings.",
     ["CI-covered tests for match path"]),
    ("FYS-111", "Precision at k and NDCG harness", "FYS-E012", "M5", "P1", "matching",
     "No offline ranking quality measure.",
     "Labeled pairs + offline eval job.",
     ["Harness runs on fixture labels"]),
    ("FYS-112", "Monitoring hooks", "FYS-E012", "M3", "P1", "ops",
     "Production blind spots.",
     "Hooks per MONITORING.md for API + ingest.",
     ["Health metrics documented"]),
    ("FYS-113", "Daily operations runbook update", "FYS-E012", "M2", "P1", "ops",
     "Ops runbook stale vs new architecture.",
     "Update DAILY_OPERATIONS for ingest + match + gate.",
     ["Runbook lists daily checks"]),
    ("FYS-114", "Placement success instrumentation", "FYS-E012", "M5", "P1", "partner,campaign",
     "Cannot measure funnel conversion.",
     "Events: profile_complete, match_view, apply, outreach, interview, offer.",
     ["Events defined and emit points documented"]),
]


def epic_body(eid: str, name: str, outcome: str, children: list[str]) -> str:
    checklist = "\n".join(f"- [ ] {c}" for c in children)
    return f"""## Epic {eid}: {name}

**Outcome:** {outcome}

**Program:** {PROGRAM}  
**Research:** {RESEARCH}  
**Issue specs:** {SPEC}

### Child issues
{checklist}

### Definition of done
- [ ] All child issues closed or explicitly deferred
- [ ] Related architecture docs updated
- [ ] No new placeholder embeddings / hardcoded match scores introduced
"""


def issue_body(iid: str, epic: str, epic_url: str | None, problem: str, goal: str, acceptance: list[str]) -> str:
    ac = "\n".join(f"- [ ] {a}" for a in acceptance)
    parent = epic_url or epic
    return f"""## Traceability
- **Issue ID:** `{iid}`
- **Parent epic:** {parent}
- **Spec:** {SPEC} (search `{iid}`)
- **Program:** {PROGRAM}
- **Research:** {RESEARCH}

## Problem
{problem}

## Goal
{goal}

## Acceptance criteria
{ac}

## Test plan
- [ ] Unit and/or integration coverage for touched path
- [ ] Docs updated when schema/API changes
"""


def main() -> int:
    print("== Labels ==")
    for name, color, desc in LABELS:
        ensure_label(name, color, desc)

    print("== Milestones ==")
    ms_map: dict[str, int | None] = {}
    keys = ["M0", "M1", "M2", "M3", "M4", "M5"]
    for key, title in zip(keys, MILESTONES):
        ms_map[key] = ensure_milestone(title)

    # map short M0 -> number for issues
    children_by_epic: dict[str, list[str]] = {e[0]: [] for e in EPICS}
    for row in ISSUES:
        children_by_epic[row[2]].append(f"{row[0]} — {row[1]}")

    print("== Epics ==")
    epic_urls: dict[str, str] = {}
    epic_numbers: dict[str, str] = {}
    for eid, name, mkey, pri, labs, outcome in EPICS:
        labels = ["epic", "research", "enhancement", pri] + labs.split(",")
        url = create_issue(
            f"[EPIC {eid}] {name}",
            epic_body(eid, name, outcome, children_by_epic[eid]),
            labels,
            ms_map.get(mkey),
        )
        if url:
            epic_urls[eid] = url
            epic_numbers[eid] = url.rstrip("/").split("/")[-1]

    print("== Issues ==")
    created = 0
    failed = 0
    for row in ISSUES:
        iid, title, epic, mkey, pri, labs, problem, goal, acceptance = row
        labels = ["research", "enhancement", pri] + [x.strip() for x in labs.split(",") if x.strip()]
        parent_ref = epic_urls.get(epic)
        if parent_ref:
            parent_ref = f"{epic} (#{epic_numbers[epic]})"
        url = create_issue(
            f"[{iid}] {title}",
            issue_body(iid, epic, parent_ref, problem, goal, acceptance),
            labels,
            ms_map.get(mkey),
        )
        if url:
            created += 1
        else:
            failed += 1

    print(f"\nDone. issues_ok={created} issues_fail={failed} epics={len(epic_urls)}")
    # write mapping for user
    with open("docs/epics/GITHUB_ISSUE_MAP.md", "w", encoding="utf-8") as f:
        f.write("# GitHub Issue Map — For Your Service\n\n")
        f.write(f"Generated after filing research architecture issues.\n\n")
        f.write("## Epics\n\n")
        for eid, url in epic_urls.items():
            f.write(f"- [{eid}]({url})\n")
        f.write("\nSee also: [ISSUE_SPECS.md](ISSUE_SPECS.md) · [PROGRAM.md](PROGRAM.md)\n")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
