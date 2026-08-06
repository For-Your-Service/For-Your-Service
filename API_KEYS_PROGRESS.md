# API Keys Progress Tracker

**Updated:** 2026-08-06 13:22  
**Project:** For Your Service - Job Market Data Pipeline  

---

## 🎯 Status Overview

| API | Status | Priority | Use Case |
|-----|--------|----------|----------|
| **Adzuna** | ✅ ACTIVE | HIGH | Real-time job listings |
| **USAJobs** | 🔄 IN PROGRESS | HIGH | Federal jobs with veteran preferences |
| **BLS** | ⏸️ PENDING | MEDIUM | Wage data by location |
| **O*NET** | ✅ NO KEY NEEDED | MEDIUM | Skills mapping, MOS crosswalk |
| **CareerOneStop** | ⏸️ PENDING | LOW | Veteran-friendly employers |

---

## ✅ Completed: Adzuna

**Registered:** 2026-08-06  
**Status:** Working and tested  
**Test Results:**
- 240 jobs collected in first run
- 99% salary data completeness
- 135 unique companies
- 3 locations covered

**API Limits:**
- Free tier: 1,000 calls/month
- Current usage: 30 calls (3%)

---

## 🔄 In Progress: USAJobs

**Registration Started:** 2026-08-06 13:22  
**URL:** https://developer.usajobs.gov/  
**Expected Completion:** 2 minutes  

**What We'll Get:**
- Authorization Key (instant on screen)
- User-Agent: whall4.wh@gmail.com
- Access to 20,000+ federal jobs
- Unlimited API calls

**Why This Matters:**
Federal jobs are CRITICAL for veterans because:
1. Veteran preference points (5-point, 10-point)
2. Security clearances transfer
3. Military experience counts
4. Transparent GS pay scales

---

## ⏸️ Remaining APIs

### BLS (Bureau of Labor Statistics)
**Priority:** Medium  
**Time to Register:** 3 minutes  
**URL:** https://data.bls.gov/registrationEngine/  
**Use Case:** Official wage data by location  
**Limit:** 500 calls/day (free)

### CareerOneStop
**Priority:** Low (nice-to-have)  
**Time to Register:** 3 minutes  
**URL:** https://www.careeronestop.org/Developers/WebAPI/registration.aspx  
**Use Case:** Veteran-friendly employers, training programs  
**Limit:** Unlimited

---

## 📊 Pipeline Readiness

### Current State
```
[Scraper] ✅ Built and tested
    ↓
[Adzuna] ✅ Collecting real data
    ↓
[USAJobs] 🔄 Adding now (2 min ETA)
    ↓
[BLS] ⏸️ Optional wage enhancement
    ↓
[Bronze Layer] ⏸️ Ready to build (next step)
```

### Next Steps After USAJobs
1. ✅ Test USAJobs integration (run scraper)
2. ✅ Collect combined Adzuna + USAJobs data
3. ✅ Commit working multi-source scraper
4. 🎯 Build Bronze layer ingestion
5. 🎯 Decide if BLS is needed for MVP

---

## 💰 Cost Tracking

| API | Monthly Limit | Current Usage | Cost |
|-----|---------------|---------------|------|
| Adzuna | 1,000 calls | 30 (3%) | $0 |
| USAJobs | Unlimited | 0 | $0 |
| BLS | 500/day | 0 | $0 |
| O*NET | Unlimited | 0 | $0 |
| CareerOneStop | Unlimited | 0 | $0 |
| **TOTAL** | | | **$0/month** |

---

## 🎯 Success Criteria

✅ **Phase 1:** Primary data sources (Adzuna + USAJobs)  
⏸️ **Phase 2:** Enhanced data (BLS wages)  
⏸️ **Phase 3:** Veteran-specific (CareerOneStop)  

**Current Progress:** Phase 1 - 50% complete (Adzuna done, USAJobs in progress)
