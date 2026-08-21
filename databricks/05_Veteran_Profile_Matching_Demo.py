# Databricks notebook source
# DBTITLE 1,🎖️ Veteran Profile Matching Demo
# MAGIC %md
# MAGIC # 🎖️ Veteran Profile Matching Demo - Free Hall
# MAGIC
# MAGIC ## Objective
# MAGIC Demonstrate the **end-to-end matching pipeline** using:
# MAGIC * **Real Veteran Data**: Free Hall's resume (Army Green Beret, AWS DevOps, 20+ years experience)
# MAGIC * **Real Job Market Data**: 670 jobs from Adzuna + USAJobs APIs (Bronze table)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Pipeline Flow
# MAGIC
# MAGIC ```
# MAGIC ┌────────────────────────────────────────────────────────────┐
# MAGIC │  STEP 1: Parse Veteran Resume                             │
# MAGIC ├────────────────────────────────────────────────────────────┤
# MAGIC │  • Extract: Skills, Experience, Location, Certifications  │
# MAGIC │  • Normalize: Job titles, technical skills, education      │
# MAGIC │  • MOS Mapping: Green Beret → Civilian occupations        │
# MAGIC └────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌────────────────────────────────────────────────────────────┐
# MAGIC │  STEP 2: Build Veteran Feature Vector                     │
# MAGIC ├────────────────────────────────────────────────────────────┤
# MAGIC │  • Technical Skills: AWS, Kubernetes, Python, etc.         │
# MAGIC │  • Leadership: Team Sergeant, 100+ engineers               │
# MAGIC │  • Clearance: Special Forces (likely TS/SCI)              │
# MAGIC │  • Location: Niceville, FL (preferences: remote/flexible)  │
# MAGIC │  • Salary Target: $120K-$180K (DevOps/Solutions Architect) │
# MAGIC └────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌────────────────────────────────────────────────────────────┐
# MAGIC │  STEP 3: Query Bronze Table (670 Real Jobs)               │
# MAGIC ├────────────────────────────────────────────────────────────┤
# MAGIC │  • 480 from Adzuna                                         │
# MAGIC │  • 190 from USAJobs                                        │
# MAGIC │  • Locations: Virginia Beach VA, San Diego CA, San Antonio │
# MAGIC └────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌────────────────────────────────────────────────────────────┐
# MAGIC │  STEP 4: Calculate Similarity Scores                      │
# MAGIC ├────────────────────────────────────────────────────────────┤
# MAGIC │  • Skills Match: AWS, Kubernetes, DevOps, Python           │
# MAGIC │  • Title Match: Solutions Architect, Cloud Engineer        │
# MAGIC │  • Salary Match: Within $120K-$180K range                  │
# MAGIC │  • Location: Remote-friendly or relocation                 │
# MAGIC └────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌────────────────────────────────────────────────────────────┐
# MAGIC │  STEP 5: Return Top 10 Matches                            │
# MAGIC ├────────────────────────────────────────────────────────────┤
# MAGIC │  • Ranked by similarity score (0-100)                      │
# MAGIC │  • Explanation: Why this job matches                       │
# MAGIC │  • Company, Location, Salary, URL                          │
# MAGIC └────────────────────────────────────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Real Veteran Profile: Free Hall
# MAGIC
# MAGIC **Background:**
# MAGIC * 🎖️ **Army Green Beret Special Forces** (1999-2017) - 18 years
# MAGIC * 🔐 **Likely Clearance**: Top Secret/SCI (Special Forces requirement)
# MAGIC * 📍 **Location**: Niceville, FL (willing to relocate or remote)
# MAGIC * 💼 **Current Role**: AWS DevOps Solution Architect @ ConocoPhillips
# MAGIC * 🎓 **Education**: BS Cybersecurity, AA Computer Programming
# MAGIC * 🏆 **Certifications**: AWS Professional, Azure Professional
# MAGIC
# MAGIC **Top Skills:**
# MAGIC * Cloud: AWS (EKS, VPC, EC2, S3), Azure (Entra ID, DevOps)
# MAGIC * DevOps: Kubernetes, Docker, Terraform, Jenkins, GitHub Enterprise
# MAGIC * Languages: Python, Bash, Java, C, C++, SQL
# MAGIC * Leadership: 100+ engineers trained, Team Sergeant
# MAGIC * Security: GitHub Advanced Security (GHAS), Threat Assessments
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC Let's match Free against the **670 real jobs** in our Bronze table!

# COMMAND ----------

# DBTITLE 1,Define Veteran Profile - William Free Hall (Enhanced)
# Parse Free Hall's resume into structured veteran profile

print("="*70)
print("🎖️ VETERAN PROFILE - Free Hall")
print("="*70)

veteran_profile = {
    "name": "William Free Hall",
    "location": {
        "current_city": "Niceville",
        "current_state": "FL",
        "target_city": "Greenville",
        "target_state": "SC",
        "willing_to_relocate": True,
        "remote_preference": True
    },

    "military": {
        "branch": "Army",
        "mos": "18 Series (Special Forces - Green Beret)",
        "rank": "Team Sergeant",
        "years_served": 18,
        "service_dates": "1999-2017",
        "clearance": "Former TS/SCI (1999-2017, expired - no longer active)",
        "clearance_notes": "18 years handling classified material, security-first mindset remains"
    },

    "target_roles": [
        "DevOps Engineer",
        "Solutions Architect",
        "Cloud Engineer",
        "Site Reliability Engineer",
        "Platform Engineer",
        "Technical Sales Engineer"
    ],

    "skills": {
        "cloud_platforms": ["AWS", "Azure", "EKS", "EC2", "S3", "VPC", "Fargate"],
        "devops_tools": ["Kubernetes", "Docker", "Terraform", "Jenkins", "Ansible", "GitHub"],
        "languages": ["Python", "Bash", "Java", "C", "C++", "SQL"],
        "operating_systems": ["Linux", "RHEL", "Ubuntu", "Amazon Linux", "Windows"],
        "security": ["GitHub Advanced Security", "GHAS", "Threat Assessment", "Security Clearance"],
        "leadership": ["Team Leadership", "Technical Training", "Stakeholder Management"]
    },

    "certifications": [
        "AWS Professional",
        "Azure Professional",
        "Cybersecurity Training (Syracuse O2O)"
    ],

    "education": [
        "BS Cybersecurity (2020-2022)",
        "AA Computer Programming (2018-2020)"
    ],

    "experience": [
        {
            "company": "ConocoPhillips",
            "title": "AWS DevOps Solution Architect / Azure Cloud Engineer",
            "years": "2023-2025",
            "key_achievements": [
                "Built automated CI/CD pipelines with GitHub Enterprise",
                "Designed scalable AWS EKS (Kubernetes) environments",
                "Led Azure DevOps to GitHub Enterprise migration (100+ engineers)"
            ]
        },
        {
            "company": "US Army Special Forces",
            "title": "Team Sergeant / Senior Program Manager",
            "years": "1999-2017",
            "key_achievements": [
                "Technical advisor to senior commanders",
                "Secured $1M-$2.5M budgets for tactical systems",
                "Led high-stakes technical intelligence briefings"
            ]
        }
    ],

    "salary_target": {
        "min": 120000,
        "max": 180000,
        "currency": "USD"
    }
}

print("\n📄 Profile Summary:")
print(f"   Name: {veteran_profile['name']}")
print(f"   Location: {veteran_profile['location']['city']}, {veteran_profile['location']['state']}")
print(f"   Military: {veteran_profile['military']['branch']} ({veteran_profile['military']['mos']})")
print(f"   Years Served: {veteran_profile['military']['years_served']}")
print(f"   Clearance: {veteran_profile['military']['clearance']}")
print(f"   Salary Target: ${veteran_profile['salary_target']['min']:,} - ${veteran_profile['salary_target']['max']:,}")

print(f"\n🎯 Target Roles:")
for role in veteran_profile['target_roles']:
    print(f"   • {role}")

print(f"\n🛠️ Top Skills:")
for category, skills in veteran_profile['skills'].items():
    print(f"   {category.replace('_', ' ').title()}: {', '.join(skills[:5])}")

print("\n" + "="*70)
print("✅ Veteran profile structured and ready for matching")
print("="*70)

# COMMAND ----------

# DBTITLE 1,Query Bronze Table & Calculate Match Scores
# Query Bronze table and calculate similarity scores

from pyspark.sql.functions import col, lower, concat_ws

print("="*70)
print("🔍 Querying Bronze Table for Job Matches")
print("="*70)

# Load all jobs from Bronze table
table_name = "workspace.fys_bronze.job_postings"
jobs_df = spark.sql(f"""
    SELECT
        job_id,
        title,
        company,
        source,
        location.city as city,
        location.state as state,
        location.display as location_display,
        salary.min as salary_min,
        salary.max as salary_max,
        description,
        requirements,
        url
    FROM {table_name}
    WHERE salary.max IS NOT NULL  -- Only jobs with salary data
""")

print(f"\n✅ Loaded {jobs_df.count()} jobs from Bronze table")

# Convert to pandas for easier text processing
import pandas as pd
jobs_pdf = jobs_df.toPandas()

print(f"\n📊 Jobs by Location:")
print(jobs_pdf.groupby('state')['job_id'].count().to_dict())

print(f"\n💰 Salary Range: ${jobs_pdf['salary_min'].min():,.0f} - ${jobs_pdf['salary_max'].max():,.0f}")

print("\n" + "="*70)
print("✅ Ready to calculate match scores")
print("="*70)

# COMMAND ----------

# DBTITLE 1,Calculate Similarity Scores - Keyword Matching Algorithm
# Simple keyword-based matching algorithm (MVP version)
# Production would use 384-dim embeddings + neural network

import re

print("="*70)
print("🧮 Calculating Match Scores")
print("="*70)

# Extract all veteran skills as keywords (flattened)
veteran_keywords = []
for skill_category in veteran_profile['skills'].values():
    veteran_keywords.extend([s.lower() for s in skill_category])

# Add target role keywords
veteran_keywords.extend([role.lower() for role in veteran_profile['target_roles']])

print(f"\n🎯 Veteran Keywords ({len(set(veteran_keywords))} unique): ")
print(f"   {', '.join(list(set(veteran_keywords))[:15])}...")

def calculate_match_score(job_row):
    """
    Calculate similarity score (0-100) between veteran profile and job posting.

    Scoring factors:
    1. Skills Match (40 points): Keyword overlap in title + description + requirements
    2. Salary Match (30 points): Overlap with veteran's target salary range
    3. Title Match (20 points): Target role keywords in job title
    4. Company/Industry (10 points): Bonus for tech companies, government, defense
    """
    score = 0
    match_reasons = []

    # Combine all job text for keyword matching
    job_text = ' '.join([
        str(job_row['title']),
        str(job_row['description']) if pd.notna(job_row['description']) else '',
        str(job_row['requirements']) if pd.notna(job_row['requirements']) else ''
    ]).lower()

    # 1. Skills Match (40 points)
    skills_matched = [kw for kw in veteran_keywords if kw in job_text]
    skills_score = min(40, len(skills_matched) * 2)  # 2 points per matched skill, max 40
    score += skills_score

    if skills_score > 20:
        match_reasons.append(f"{len(skills_matched)} skills matched ({', '.join(skills_matched[:5])})")

    # 2. Salary Match (30 points)
    vet_min = veteran_profile['salary_target']['min']
    vet_max = veteran_profile['salary_target']['max']
    job_min = job_row['salary_min'] if pd.notna(job_row['salary_min']) else 0
    job_max = job_row['salary_max'] if pd.notna(job_row['salary_max']) else 0

    if job_max >= vet_min and job_min <= vet_max:
        # Salary ranges overlap
        overlap_amount = min(job_max, vet_max) - max(job_min, vet_min)
        overlap_pct = overlap_amount / (vet_max - vet_min)
        salary_score = min(30, overlap_pct * 30)
        score += salary_score

        if salary_score > 15:
            match_reasons.append(f"Salary ${job_min:,.0f}-${job_max:,.0f} in target range")

    # 3. Title Match (20 points)
    job_title = str(job_row['title']).lower()
    title_keywords_matched = [role for role in veteran_profile['target_roles']
                               if any(word in job_title for word in role.lower().split())]

    title_score = min(20, len(title_keywords_matched) * 10)  # 10 points per matched target role
    score += title_score

    if title_score > 0:
        match_reasons.append(f"Title matches: {', '.join(title_keywords_matched)}")

    # 4. Company/Industry Bonus (10 points)
    company_name = str(job_row['company']).lower() if pd.notna(job_row['company']) else ''
    source = str(job_row['source']).lower()

    # Bonus for government jobs (veteran preference)
    if source == 'usajobs' or 'government' in job_text:
        score += 5
        match_reasons.append("Government job (veteran preference)")

    # Bonus for tech/defense companies
    if any(tech in company_name for tech in ['northrop', 'lockheed', 'raytheon', 'amazon', 'microsoft', 'google']):
        score += 5
        match_reasons.append("Major tech/defense company")

    return {
        'score': round(score, 1),
        'match_reasons': match_reasons,
        'skills_matched': len(skills_matched)
    }

# Calculate scores for all jobs
print(f"\n🔄 Scoring {len(jobs_pdf)} jobs...")

jobs_pdf['match_data'] = jobs_pdf.apply(calculate_match_score, axis=1)
jobs_pdf['match_score'] = jobs_pdf['match_data'].apply(lambda x: x['score'])
jobs_pdf['match_reasons'] = jobs_pdf['match_data'].apply(lambda x: ', '.join(x['match_reasons']))
jobs_pdf['skills_matched'] = jobs_pdf['match_data'].apply(lambda x: x['skills_matched'])

# Sort by score
jobs_pdf_sorted = jobs_pdf.sort_values('match_score', ascending=False)

print(f"\n✅ Scored all jobs!")
print(f"\n📈 Score Distribution:")
print(f"   Top Score: {jobs_pdf_sorted['match_score'].max():.1f}")
print(f"   Median Score: {jobs_pdf_sorted['match_score'].median():.1f}")
print(f"   Jobs scoring >50: {len(jobs_pdf_sorted[jobs_pdf_sorted['match_score'] > 50])}")
print(f"   Jobs scoring >70: {len(jobs_pdf_sorted[jobs_pdf_sorted['match_score'] > 70])}")

print("\n" + "="*70)
print("✅ Match scoring complete - ready to show top matches")
print("="*70)

# COMMAND ----------

# DBTITLE 1,🏆 Top 10 Job Matches for Free Hall
# Display top 10 matches with full details

print("="*70)
print("🏆 TOP 10 JOB MATCHES FOR FREE HALL")
print("="*70)

top_10 = jobs_pdf_sorted.head(10)

for idx, (i, job) in enumerate(top_10.iterrows(), 1):
    print(f"\n\n{'#'*70}")
    print(f"MATCH #{idx} - Score: {job['match_score']:.1f}/100")
    print(f"{'#'*70}")

    print(f"\n💼 JOB TITLE: {job['title']}")
    print(f"🏢 COMPANY: {job['company']}")
    print(f"📍 LOCATION: {job['city']}, {job['state']}")
    print(f"💰 SALARY: ${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}")
    print(f"📊 SOURCE: {job['source']}")

    print(f"\n🎯 WHY THIS MATCHES:")
    if job['match_reasons']:
        for reason in job['match_reasons'].split(', '):
            print(f"   ✅ {reason}")
    else:
        print(f"   • {job['skills_matched']} skills matched")

    print(f"\n🔗 APPLICATION URL:")
    print(f"   {job['url']}")

    # Show snippet of job description
    if pd.notna(job['description']):
        desc_snippet = job['description'][:300].replace('\n', ' ')
        print(f"\n📝 DESCRIPTION SNIPPET:")
        print(f"   {desc_snippet}...")

print("\n\n" + "="*70)
print("✅ MATCHING COMPLETE")
print("="*70)

print(f"\n📊 SUMMARY:")
print(f"   Total Jobs Evaluated: {len(jobs_pdf)}")
print(f"   Top Match Score: {top_10.iloc[0]['match_score']:.1f}/100")
print(f"   Average Top-10 Score: {top_10['match_score'].mean():.1f}/100")
print(f"   Jobs scoring >60: {len(jobs_pdf_sorted[jobs_pdf_sorted['match_score'] > 60])}")

print(f"\n🎖️ VETERAN: Free Hall")
print(f"   Location: {veteran_profile['location']['city']}, {veteran_profile['location']['state']}")
print(f"   Target Salary: ${veteran_profile['salary_target']['min']:,} - ${veteran_profile['salary_target']['max']:,}")
print(f"   Clearance: {veteran_profile['military']['clearance']}")
print(f"   Years Military: {veteran_profile['military']['years_served']}")

print("\n" + "="*70)
print("🚀 NEXT STEPS: Build Silver Layer (Feature Engineering)")
print("="*70)
print("""
This MVP demonstrates keyword-based matching.

Production pipeline will use:
  1. Silver Layer: NLP feature extraction, skill normalization
  2. Gold Layer: 384-dim embeddings (sentence-transformers)
  3. Neural Network: Siamese twin tower architecture
  4. Training: Contrastive loss on veteran-job pairs
  5. Inference: Fast similarity search with FAISS/Annoy

Expected improvement: 60-80% match accuracy (vs 40-50% keyword-based)
""")

# COMMAND ----------

