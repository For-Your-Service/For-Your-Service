# Job Matching Test Runs - Comparison

## Overview
This document tracks test runs of the job matching pipeline with different applicant profiles for validation and comparison.

---

## Test Run #1: Free Hall (Developer/Original Test)
**Date:** August 7, 2026  
**Location:** Greenville, SC  
**Experience:** 18 years (Army Green Beret, Team Sergeant)  
**Target Roles:** DevOps Engineer, Solutions Architect, Cloud Engineer  
**Salary Range:** $120,000 - $180,000  
**Top Skills:** AWS, Azure, Kubernetes, Docker, Terraform, Python  

### Results
- **Jobs Scraped:** [See job_matching_results_2026-08-07.md]
- **Resume Quality:** N/A (initial test)
- **Top Match Score:** [TBD]
- **Status:** Initial system validation

---

## Test Run #2: Stephen D. Porterfield
**Date:** August 7, 2026  
**Run ID:** test_20260807_180856  
**Location:** Kingwood, TX  
**Experience:** 4 years (mid-level)  
**Target Roles:** Azure, Cloud Engineer, DevOps, Infrastructure as Code  
**Salary Range:** $90,000 - $140,000  
**Top Skills:** Go, Rust, Azure, Kubernetes, Terraform, GitHub, CI/CD, DevOps  

### Results Summary
- **Jobs Scraped:** 17 (Kingwood, TX area)
- **Resume Quality:** 90/100 ⭐⭐⭐⭐⭐ EXCELLENT
- **Top Match Score:** 73.9/100 (Senior Applications Engineer)
- **Strong Matches (70+):** 4 jobs
- **Good Matches (60-69):** 4 jobs
- **Fair Matches (50-59):** 2 jobs
- **Median Score:** 58.1/100
- **Avg Semantic Similarity:** 0.314

### Top 5 Matches
1. **Senior Applications Engineer** - 73.9/100 (GRAYWOLF INTEGRATED CONSTRUCTION, $129,579)
2. **Director of Quality Modular** - 72.6/100 (GRAYWOLF INTEGRATED CONSTRUCTION, $130,428)
3. **Plant Manager** - 71.1/100 (GRAYWOLF INTEGRATED CONSTRUCTION, $90,704)
4. **Senior Semantic Data Architect** - 70.3/100 (Insperity, $109,681)
5. **Maintenance Tech I** - 68.1/100 (RS Utility Structures Inc, $110,044)

### Resume Analysis
- **Detected Experience:** 4 years
- **Detected Seniority:** Junior (algorithm decision, though profile indicates mid)
- **Location Detected:** Kingwood, TX
- **Skills Found:** 8 technical skills
- **Recommendations:** 1 (use more action verbs)

### Observations
✅ Pipeline successfully processed resume with employment dates  
✅ Auto-detection correctly identified location and years of experience  
✅ Semantic matching found relevant tech roles  
⚠️ Seniority detection marked as "Junior" despite 4 years experience (algorithm threshold)  
⚠️ Some top matches are construction/manufacturing vs. pure tech roles  

### Files
- PDF Report: `results/pdfs/Stephen_D._Porterfield_Job_Match_Report_20260807_181814.pdf`
- Bronze Table: `workspace.fys_bronze.job_postings_test_20260807_180856`

---

## Comparison Insights

### System Performance
1. **Resume Analysis:** Successfully auto-detects experience, location, and skills from text
2. **Job Scraping:** Adapts to different locations (SC vs. TX)
3. **Matching Logic:** Semantic similarity + experience + salary weighting working as designed
4. **PDF Generation:** Clean, professional reports suitable for sharing

### Areas for Improvement
1. **Seniority Algorithm:** Consider lowering "junior → mid" threshold from 5 years to 3 years
2. **Industry Filtering:** May want to filter out non-tech matches for tech roles
3. **Skills Extraction:** Could expand skill detection to catch more technical terms
4. **Match Quality:** Top matches in 70-74 range suggest good fit but room for optimization

### Next Steps
- [ ] Test with more veteran profiles (10+ years experience, executive level)
- [ ] Test with different locations (major metros vs. small cities)
- [ ] Validate salary matching logic across different ranges
- [ ] Compare match quality across different skill sets
- [ ] Gather user feedback on match relevance

---

**Last Updated:** August 7, 2026  
**Maintained by:** 7 Eagle Group Development Team
