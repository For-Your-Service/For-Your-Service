# Research Brief — For Your Service Architecture

**Organization:** 7 Eagle Group  
**Product:** For Your Service (general-use veteran → civilian placement)  
**Last Updated:** 2026-08-14  
**Status:** Planning input for [PROGRAM.md](PROGRAM.md) and [../ROADMAP.md](../ROADMAP.md)

---

## BLUF

Do **not** build another national job board. Build a **profile-gated, explainable matching + placement campaign OS** on the existing medallion stack (Bronze → Silver → Gold → Match → FastAPI), optimized for veterans and for partners like **7 Eagle Group**.

---

## Problem (from domain research)

Veterans fail placement less from lack of competence than from:

1. **Miscommunication** — MOS / jargon not translated into civilian language employers understand  
2. **Wrong channel** — cold ATS when warm paths, SkillBridge, or federal preference would win  
3. **Poor fit** — location, WLB, mission, clearance, and salary treated as soft ranking noise  

Self-understanding + a complete profile must **gate** matching.

---

## Competitive Landscape (what exists)

| Player | What they own | Gap for FYS |
|--------|---------------|-------------|
| RecruitMilitary / Hire Heroes / HOH | Events, coaching, employer access | Not a living match + campaign OS on owned data |
| ClearanceJobs | Cleared talent marketplace | Clearance-centric; not full transition campaign |
| USAJOBS + preference | Federal pipeline | Federal-only; weak civilian semantic match |
| My Next Move / O*NET / CareerOneStop | MOS → occupation crosswalk | Strong substrate; weak live multi-source jobs + campaign |
| LinkedIn | Graph + jobs | Generic; weak MOS/clearance/SkillBridge semantics |
| SkillBridge directories | Internship pathways | Listing, not person↔job fit + funnel |
| Orion / niche boards | Segmented talent | Not partner placement SITREP + Side Door |

**Seekers are free; money sits with employers and placement partners.** FYS should serve veterans first and **instrument outcomes for 7 Eagle**.

---

## White Space (what FYS should own)

| Capability | Why |
|------------|-----|
| **O*NET MOS crosswalk as soft prior** | Proven public substrate; boost retrieval, don’t sole-rank |
| **Semantic person ↔ job match** | After civilian translation of military experience |
| **Hard filters before cosine** | Geo, clearance, salary, remote as gates |
| **White-box factor scores + grounded explain** | Trust; LLM narrates factors only |
| **Multi-source + regional live jobs** | USAJOBS / JSearch / Adzuna (+ later sources) on Databricks medallion |
| **SkillBridge / federal / HoH pathway tags** | Right channel, ETS clocks |
| **Campaign OS (apply + Side Door)** | Funnel Target → Offer; warm outreach same day as ATS |
| **Partner SITREP** | Batch veterans, conversion metrics, PII-minimized |

---

## Product Blueprint (skill chains to productize)

Mandatory skill chains to **productize** (not re-invent as ad-hoc chat):

| Intent | Chain |
|--------|-------|
| Apply | Company Research → JOI → Resume → Hook |
| Find roles | Concierge → Research → JOI |
| Interview | Person Research → SAR-6 |
| Outreach | Network Intelligence → Outreach Pipeline |

**Company Research fit weights (steal for FYS-E006 / FYS-E009):**

| Factor | Weight | Notes |
|--------|--------|-------|
| Location | 25% | Often hard Go/No-Go |
| Work-life balance | 20% | |
| Mission alignment | 20% | |
| Compensation | 15% | |
| Culture | 15% | |
| Clearance | 5% | Hard gate when role requires it |

Recommendation tiers: **Apply Now / Prepare / Monitor / Bypass**.

---

## Architecture Reality Check (repo today)

| Claimed | Reality risk | Roadmap response |
|---------|--------------|------------------|
| Semantic embeddings | Placeholder `np.random.rand` in embedding path | FYS-E004 / FYS-040 |
| Match scores | Hardcoded confidence in some HF paths | FYS-E006 |
| Bronze writer | Stub / incomplete paths | FYS-E002 |
| MOS mapper | Thin vs [MOS_CROSSWALK.md](../MOS_CROSSWALK.md) / O*NET docs | FYS-E003 |
| Schema names | `fys_*` vs `for_your_service` drift | FYS-E001 |
| Security | CORS `*`, PII in APIs vs anonymizer docs | FYS-E011 |
| Nested tree | Duplicate `For-Your-Service/` | FYS-E001 |

**Rule:** One documented production path (Databricks lakehouse + HF FastAPI) before expanding AWS/GCP surfaces.

---

## Non-Goals

- Competing with LinkedIn as a general social network  
- Credential mills / paid “guaranteed placement” theater  
- Matching without a profile + self-understanding gate  
- Multi-cloud sprawl before one path works end-to-end  
- Black-box scores with no factor card  

---

## Success Metrics

| Metric | Layer |
|--------|-------|
| Profile completion / `ready_for_matching` rate | Profile |
| % matches with factor explanations | Matching |
| Apply conversion | Campaign |
| Warm-path response rate (≥10% target) | Side Door |
| Offers before ETS | Partner SITREP |
| Median match latency &lt; 2s | Serving |
| Precision@k / NDCG on labeled pairs | ML quality |

---

## Sources

- Competitive scan (placement boards, federal, O*NET, SkillBridge, clearance)  
- Technical matching pattern: hard filter → hybrid retrieve → white-box score → grounded explain  
- Domain requirements: MOS crosswalk, demilitarized profile, bidirectional Go/No-Go, funnel, clearance, pathways  
- Existing FYS docs: [ARCHITECTURE.md](../ARCHITECTURE.md), [DEPLOYMENT_STRATEGY.md](../DEPLOYMENT_STRATEGY.md), [MATCHING_ALGORITHM.md](../MATCHING_ALGORITHM.md), [VETERAN_PROFILE_SCHEMA.md](../VETERAN_PROFILE_SCHEMA.md)

---

Built with ❤️ for those who served. 🇺🇸
