# Live Veteran Job Matching Test

Run end-to-end job matching with **REAL data from USAJobs API** and your actual resume.

## Quick Start

1. **Upload your resume** (PDF or DOCX) to the `data/resumes/` directory

2. **Run the live test:**
```bash
python scripts/live_test.py data/resumes/your_resume.pdf
```

3. **View results** in the console and saved JSON file

## What It Does

The live test performs:

1. ✅ **Fetches 50 real federal jobs** from USAJobs API
   - Filters for veteran-friendly positions
   - Targets Greenville, SC area
   - Keywords: DevOps, Cloud Engineer, Solutions Architect, SRE, Platform Engineer

2. ✅ **Parses your resume**
   - Extracts skills, experience, education
   - Enriches with military-to-civilian skill mappings
   - Normalizes skills to canonical forms

3. ✅ **Runs gap analysis** for each job
   - Identifies matching skills (your strengths)
   - Finds missing skills (gaps to fill)
   - Calculates match scores (0-100%)

4. ✅ **Generates recommendations**
   - Resume improvement suggestions
   - Job search strategy tips
   - Skill development plan with timelines
   - Networking advice for veterans

5. ✅ **Saves results** to JSON
   - Complete match data
   - Top 5 recommended jobs
   - Full candidate profile
   - Timestamped for tracking

## Example Output

```
================================================================================
FOR YOUR SERVICE - LIVE VETERAN JOB MATCHING
7 Eagle Group
================================================================================

📄 Resume: data/resumes/free_hall_resume.pdf

🔧 Initializing live matcher...
✓ Matcher ready

🔍 Search Parameters:
   Location: Greenville, SC
   Keywords: DevOps, Cloud Engineer, Solutions Architect, Site Reliability, Platform Engineer
   Job Limit: 50
   Min Salary: $120,000

⏳ Fetching live jobs from USAJobs API...
   (This may take 10-30 seconds)

✓ Fetched 43 veteran-friendly jobs

================================================================================
✅ MATCHING COMPLETE - RESULTS BELOW
================================================================================

📋 CANDIDATE PROFILE
--------------------------------------------------------------------------------
Name: Free Hall
Email: whall4.wh@gmail.com
Location: Greenville, SC
Experience: 18 years
Skills (15): AWS, Azure, Kubernetes, Docker, Terraform, Python, Bash, Jenkins...

🎖️  Military Background:
   Branch: Army
   MOS: 18Z
   Clearance: TS/SCI (expired)

📊 MATCH SUMMARY
--------------------------------------------------------------------------------
Jobs Analyzed: 43
Best Match Score: 87.5%
Average Match Score: 64.2%

🎯 TOP 5 JOB MATCHES
--------------------------------------------------------------------------------

1. Cloud Infrastructure Engineer
   Job ID: 12345678
   Match Score: 87.5%
   Readiness: Ready to apply immediately
   ✓ Matching Skills: AWS, Kubernetes, Terraform, Docker, Python
   ⚠ Missing Skills: Azure, Monitoring

2. DevOps Platform Engineer
   Job ID: 87654321
   Match Score: 82.3%
   Readiness: Ready to apply immediately
   ✓ Matching Skills: AWS, Docker, Jenkins, Kubernetes, CI/CD
   ⚠ Missing Skills: GitLab

...

💡 PERSONALIZED RECOMMENDATIONS
--------------------------------------------------------------------------------

📝 Resume Improvements:
   • Summary: Add professional summary highlighting 18 years experience...
   • Experience: Translate '18Z' to 'Special Forces Team Sergeant'...
   • Skills: Quantify achievements: team sizes, infrastructure scale...

🎯 Job Search Tips:
   • Strong match! Apply immediately and emphasize matching skills
   • Highlight security clearance prominently if active/recent
   • Target defense contractors and government contractors first

📚 Skill Development Plan:
   1. Azure - 4-6 weeks
   2. Monitoring (Prometheus/Grafana) - 2-4 weeks
   3. GitLab CI/CD - 2-3 weeks

💾 Results saved to: results/match_results_free_hall_resume_20260811_163045.json
```

## Data Sources

- **USAJobs API** (free tier)
  - Federal government positions
  - Veteran hiring preference filter
  - No API key required (uses email only)
  - Live data, updated daily

## Customization

Edit `scripts/live_test.py` to change:

```python
# Search location
location = "Greenville, SC"  # Change to your target location

# Job keywords
keywords = ["DevOps", "Cloud Engineer", "Solutions Architect"]

# Minimum salary
salary_min = 120000  # Change to your requirement

# Number of jobs to fetch
job_limit = 50  # Increase for more results
```

## Requirements

All dependencies are already installed:
- PyPDF2 (resume parsing)
- python-docx (resume parsing)
- requests (API calls)
- numpy (matching calculations)

## Troubleshooting

**No jobs found:**
- Try broader keywords
- Expand location radius
- Lower salary_min requirement

**Resume parsing error:**
- Ensure resume is PDF or DOCX format
- Check file is not corrupted
- Try re-saving from Word/PDF editor

**API timeout:**
- USAJobs API can be slow
- Script auto-retries failed requests
- Reduce job_limit if persistent issues

## Next Steps

After your live test:

1. **Review top matches** - Apply to jobs with 75%+ match scores
2. **Follow recommendations** - Update resume per suggestions
3. **Build missing skills** - Follow the skill development plan
4. **Network** - Join 7 Eagle Group veteran events
5. **Re-run test** - After upskilling to see improved matches

## Author

**Free Hall** <whall4.wh@gmail.com>  
7 Eagle Group  
Army Green Beret (18Z), 1999-2017
