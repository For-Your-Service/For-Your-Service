# Databricks notebook source
# DBTITLE 1,Job Market Data Ingestion Architecture
# MAGIC %md
# MAGIC # 📊 For Your Service - Job Market Data Sources
# MAGIC
# MAGIC ## Mission
# MAGIC Enrich veteran job matching with **real-time market intelligence**:
# MAGIC * Active job postings by location and role
# MAGIC * Salary ranges and compensation trends
# MAGIC * Skills demand and market saturation
# MAGIC * Company information and culture fit
# MAGIC * Growth trends by occupation and industry
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Data Flow Architecture
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────────────────────────────────────────────────────┐
# MAGIC │  LAYER 1: Job Market APIs (Scheduled Collection)           │
# MAGIC ├─────────────────────────────────────────────────────────────┤
# MAGIC │  • USAJobs API (Government - FREE)                          │
# MAGIC │  • O*NET OnLine (Occupational Data - FREE)                  │
# MAGIC │  • BLS API (Labor Statistics - FREE)                        │
# MAGIC │  • CareerOneStop API (DOL - FREE)                           │
# MAGIC │  • Adzuna API (Job Aggregator - FREE tier: 1K calls/mo)    │
# MAGIC │  • Indeed/LinkedIn (Premium - Future)                       │
# MAGIC └─────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌─────────────────────────────────────────────────────────────┐
# MAGIC │  LAYER 2: Cloud Function Orchestrator (GCP - FREE tier)    │
# MAGIC ├─────────────────────────────────────────────────────────────┤
# MAGIC │  • Scheduled daily/weekly fetches                           │
# MAGIC │  • Rate limit management                                    │
# MAGIC │  • Data normalization and cleaning                          │
# MAGIC │  • Write to GCS: gs://fys-job-market-data/                  │
# MAGIC └─────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌─────────────────────────────────────────────────────────────┐
# MAGIC │  LAYER 3: Databricks Bronze Layer                          │
# MAGIC ├─────────────────────────────────────────────────────────────┤
# MAGIC │  Table: main.fys_bronze.job_postings                        │
# MAGIC │  • Raw job posting JSON                                     │
# MAGIC │  • Metadata: source, fetch_date, location                   │
# MAGIC │  • Partitioned by: state, fetch_date                        │
# MAGIC └─────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌─────────────────────────────────────────────────────────────┐
# MAGIC │  LAYER 4: Silver Layer (Feature Engineering)               │
# MAGIC ├─────────────────────────────────────────────────────────────┤
# MAGIC │  Table: main.fys_silver.job_features                        │
# MAGIC │  • Normalize skills, requirements, locations                │
# MAGIC │  • Extract salary ranges                                    │
# MAGIC │  • MOS code mapping                                         │
# MAGIC │  • Convert to 384-dim feature vectors                       │
# MAGIC └─────────────────────────────────────────────────────────────┘
# MAGIC                            ↓
# MAGIC ┌─────────────────────────────────────────────────────────────┐
# MAGIC │  LAYER 5: Gold Layer (Tensor Ready)                        │
# MAGIC ├─────────────────────────────────────────────────────────────┤
# MAGIC │  Table: main.fys_gold.job_embeddings                        │
# MAGIC │  • 384-dim job feature vectors                              │
# MAGIC │  • Ready for neural network matching                        │
# MAGIC │  • Indexed by: location, industry, salary_range             │
# MAGIC └─────────────────────────────────────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Cost Estimate (FREE Tier)
# MAGIC
# MAGIC | Component | Service | Cost | Limits |
# MAGIC |-----------|---------|------|--------|
# MAGIC | API Calls | USAJobs, O*NET, BLS | **$0** | Unlimited (government) |
# MAGIC | API Calls | Adzuna | **$0** | 1,000 calls/month |
# MAGIC | Storage | GCS | **$0** | 5GB free tier |
# MAGIC | Processing | Cloud Functions | **$0** | 2M invocations/month |
# MAGIC | ETL | Databricks Community | **$0** | 15GB RAM |
# MAGIC | **TOTAL** | | **$0/month** | |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Next Steps
# MAGIC 1. Register for API keys (all FREE)
# MAGIC 2. Build Cloud Function collectors
# MAGIC 3. Set up Bronze ingestion pipeline
# MAGIC 4. Feature engineering (Silver)
# MAGIC 5. Tensor preparation (Gold)

# COMMAND ----------

# DBTITLE 1,1. USAJobs API - Government Jobs (FREE, Unlimited)
print("="*70)
print("🏛️ USAJOBS API - Federal Government Job Postings")
print("="*70)

print("""
✅ PERFECT FOR VETERANS - Many federal jobs have veteran preferences!

📋 What You Get:
  • 20,000+ active federal job postings
  • Veteran preference indicators
  • Security clearance requirements
  • Salary ranges (GS pay scales)
  • Location data (nationwide)
  • Skills and qualifications
  • Military skill translations

💰 Cost: FREE
🔑 Registration: https://developer.usajobs.gov/
📚 Docs: https://developer.usajobs.gov/API-Reference
⚡ Rate Limit: Unlimited (reasonable use)

---

🔧 SETUP INSTRUCTIONS:

1. Go to: https://developer.usajobs.gov/
2. Create account (use whall4.wh@gmail.com)
3. Request API key (instant approval)
4. You'll receive:
   - Authorization Key (your API key)
   - User Agent (your email)

---

📝 SAMPLE REQUEST:
""")

sample_code = '''
import requests
import json

# Your credentials from developer.usajobs.gov
API_KEY = "YOUR_API_KEY_HERE"
USER_AGENT = "whall4.wh@gmail.com"

headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": USER_AGENT,
    "Authorization-Key": API_KEY
}

# Search for cybersecurity jobs in California
params = {
    "Keyword": "cybersecurity",
    "LocationName": "California",
    "ResultsPerPage": 100,
    "Page": 1
}

response = requests.get(
    "https://data.usajobs.gov/api/Search",
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    jobs = data["SearchResult"]["SearchResultItems"]
    
    print(f"Found {len(jobs)} jobs")
    
    for job in jobs[:3]:  # Show first 3
        posting = job["MatchedObjectDescriptor"]
        print(f"\\n{'='*60}")
        print(f"Title: {posting['PositionTitle']}")
        print(f"Agency: {posting['OrganizationName']}")
        print(f"Location: {posting['PositionLocationDisplay']}")
        print(f"Salary: {posting['PositionRemuneration'][0]['MinimumRange']} - {posting['PositionRemuneration'][0]['MaximumRange']}")
        print(f"Clearance: {posting.get('SecurityClearance', 'Not specified')}")
        print(f"Veteran Preference: {posting.get('UserArea', {}).get('Details', {}).get('HiringPath', [])}")
else:
    print(f"Error: {response.status_code}")
'''

print(sample_code)

print("\n" + "="*70)
print("💡 KEY FEATURES FOR VETERANS")
print("="*70)
print("""
  ✅ Veteran preference flags (5-point, 10-point)
  ✅ Security clearance levels (Confidential, Secret, Top Secret)
  ✅ Military experience equivalencies
  ✅ GS pay scale data (transparent salary ranges)
  ✅ Federal benefits information
  ✅ Direct hire authorities for veterans
""")

# COMMAND ----------

# DBTITLE 1,2. O*NET OnLine API - Occupational Data (FREE, Unlimited)
print("="*70)
print("📊 O*NET OnLine API - Occupational Skills & Requirements")
print("="*70)

print("""
✅ PERFECT FOR SKILLS MAPPING - Maps military MOS codes to civilian occupations!

📋 What You Get:
  • 1,000+ occupation profiles
  • Skills, abilities, knowledge requirements
  • Work activities and context
  • Education and training requirements
  • Technology skills needed
  • Wage data by occupation
  • Military-to-civilian crosswalks (MOS to O*NET)

💰 Cost: FREE
🔑 Registration: https://services.onetcenter.org/reference/
📚 Docs: https://services.onetcenter.org/ws/online-help/
⚡ Rate Limit: Unlimited (government service)

---

🔧 SETUP INSTRUCTIONS:

1. No API key required!
2. Direct access via web services
3. Username: Use your email (whall4.wh@gmail.com)
4. Password: (leave blank or use any string)

---

📝 SAMPLE REQUEST - Get occupation details:
""")

sample_code = '''
import requests
import json

# No API key needed!
USERNAME = "whall4.wh@gmail.com"

# Example: Get details for "Information Security Analysts" (15-1212.00)
onet_code = "15-1212.00"  # Cybersecurity

response = requests.get(
    f"https://services.onetcenter.org/ws/online/occupations/{onet_code}",
    auth=(USERNAME, "")  # No password required
)

if response.status_code == 200:
    data = response.json()
    print(f"\\nOccupation: {data['title']}")
    print(f"Description: {data['description'][:200]}...")
    
    # Get detailed skills
    skills_response = requests.get(
        f"https://services.onetcenter.org/ws/online/occupations/{onet_code}/skills",
        auth=(USERNAME, "")
    )
    
    if skills_response.status_code == 200:
        skills = skills_response.json()
        print(f"\\n🎯 Top Skills Required:")
        for skill in skills['skill'][:10]:
            print(f"  • {skill['name']} (Level: {skill['level']['value']})") 
else:
    print(f"Error: {response.status_code}")

# MILITARY CROSSWALK - Map MOS to O*NET
print("\\n" + "="*60)
print("🎖️ MILITARY TO CIVILIAN OCCUPATION CROSSWALK")
print("="*60)

# Example: Marines 0621 (Field Radio Operator)
mos_code = "0621"
print(f"\\nMarine MOS {mos_code} (Field Radio Operator) maps to:")
print("  • O*NET 15-1241.00 - Computer Network Support Specialists")
print("  • O*NET 17-2072.00 - Electronics Engineers")
print("  • O*NET 49-2097.00 - Audiovisual Equipment Installers")
print("\\n💡 Use O*NET API to get detailed requirements for each civilian job!")
'''

print(sample_code)

print("\n" + "="*70)
print("💡 KEY FEATURES FOR TENSOR PIPELINE")
print("="*70)
print("""
  ✅ Skills taxonomy (standardized skill names)
  ✅ Ability requirements (cognitive, physical, psychomotor)
  ✅ Knowledge domains (engineering, computers, public safety)
  ✅ Work context (stress tolerance, time pressure)
  ✅ Technology skills (specific software/tools)
  ✅ MOS-to-O*NET crosswalk (veterans.employment.gov/VETS_ONET/)
""")

# COMMAND ----------

# DBTITLE 1,3. BLS API - Labor Statistics (FREE, Unlimited)
print("="*70)
print("📈 BLS API - Bureau of Labor Statistics")
print("="*70)

print("""
✅ PERFECT FOR SALARY & MARKET TRENDS - Official government wage data!

📋 What You Get:
  • Employment statistics by occupation and location
  • Wage data (hourly, annual) by state and metro area
  • Job growth projections
  • Industry employment trends
  • Unemployment rates by region
  • Occupational outlook (10-year forecasts)

💰 Cost: FREE
🔑 Registration: https://data.bls.gov/registrationEngine/
📚 Docs: https://www.bls.gov/developers/
⚡ Rate Limit: 25 requests/day (unregistered), 500/day (registered)

---

🔧 SETUP INSTRUCTIONS:

1. Register at: https://data.bls.gov/registrationEngine/
2. Use email: whall4.wh@gmail.com
3. Receive API key via email (instant)
4. 500 queries per day (more than enough!)

---

📝 SAMPLE REQUEST - Get wage data:
""")

sample_code = '''
import requests
import json
from datetime import datetime

API_KEY = "YOUR_BLS_API_KEY"

# Series IDs for different occupations
# Format: OEUN + State FIPS + Occupation SOC code
series_ids = [
    "OEUN000000015121203",  # Computer Network Architects, US average
    "OEUN000000015121200",  # Information Security Analysts, US average
]

headers = {"Content-type": "application/json"}
payload = json.dumps({
    "seriesid": series_ids,
    "startyear": "2023",
    "endyear": "2024",
    "registrationkey": API_KEY
})

response = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
    data=payload,
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    
    for series in data["Results"]["series"]:
        print(f"\\n{'='*60}")
        print(f"Series ID: {series['seriesID']}")
        
        # Latest data point
        latest = series["data"][0]
        print(f"Period: {latest['year']}-{latest['period']}")
        print(f"Value: {latest['value']}")
        print(f"(Check series catalog for what this value represents)")
else:
    print(f"Error: {response.status_code}")

print("\\n" + "="*60)
print("🗺️ GEOGRAPHIC WAGE DATA")
print("="*60)
print("""
BLS provides wage data by:
  • National average
  • State-level
  • Metropolitan Statistical Area (MSA)
  • Non-metropolitan areas

Example Series IDs:
  • OEUM004074015121203 - Network Architects in San Diego MSA
  • OEUS060000015121203 - Network Architects in California
  • OEUN000000015121203 - Network Architects in US (national)

💡 Build series IDs using:
   OEU + [M=MSA/S=State/N=National] + [FIPS code] + [SOC code]
""")
'''

print(sample_code)

print("\n" + "="*70)
print("💡 KEY FEATURES FOR MATCHING")
print("="*70)
print("""
  ✅ Actual wage data (not estimates)
  ✅ Geographic granularity (match veteran location)
  ✅ Employment projections (show growth opportunities)
  ✅ Historical trends (identify hot markets)
  ✅ Percentile wages (10th, 25th, 50th, 75th, 90th)
""")

# COMMAND ----------

# DBTITLE 1,4. Adzuna API - Job Aggregator (FREE tier: 1K calls/mo)
print("="*70)
print("🔎 Adzuna API - Job Search Aggregator")
print("="*70)

print("""
✅ BEST FOR REAL-TIME JOB LISTINGS - Aggregates from multiple sources!

📋 What You Get:
  • 1M+ active job listings (Indeed, CareerBuilder, company sites)
  • Real-time job postings
  • Salary predictions
  • Company information
  • Location data (lat/long)
  • Category/industry classification
  • Direct application links

💰 Cost: FREE tier (1,000 calls/month)
🔑 Registration: https://developer.adzuna.com/
📚 Docs: https://api.adzuna.com/v1/doc/
⚡ Rate Limit: 1,000 calls/month FREE, then $0.01/call

---

🔧 SETUP INSTRUCTIONS:

1. Register at: https://developer.adzuna.com/signup
2. Use email: whall4.wh@gmail.com
3. Create application
4. Get: Application ID + API Key

---

📝 SAMPLE REQUEST:
""")

sample_code = '''
import requests
import json

APP_ID = "YOUR_APP_ID"
API_KEY = "YOUR_API_KEY"

# Search parameters
params = {
    "app_id": APP_ID,
    "app_key": API_KEY,
    "results_per_page": 50,
    "what": "cybersecurity network",  # Keywords
    "where": "San Diego, CA",  # Location
    "distance": 25,  # Miles radius
    "salary_min": 60000,
    "full_time": 1
}

response = requests.get(
    "https://api.adzuna.com/v1/api/jobs/us/search/1",
    params=params
)

if response.status_code == 200:
    data = response.json()
    print(f"\\nFound {data['count']} jobs")
    print(f"Showing page 1 of {data['count'] // 50 + 1}\\n")
    
    for job in data["results"][:5]:  # Show first 5
        print(f"{'='*60}")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']['display_name']}")
        print(f"Location: {job['location']['display_name']}")
        print(f"Salary: ${job.get('salary_min', 'N/A'):,} - ${job.get('salary_max', 'N/A'):,}")
        print(f"Posted: {job['created'][:10]}")
        print(f"URL: {job['redirect_url']}")
        print(f"Description: {job['description'][:150]}...\\n")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

print("\\n" + "="*60)
print("🎯 ADVANCED SEARCH OPTIONS")
print("="*60)
print("""
Adzuna supports:
  • Category filters (IT, Engineering, Healthcare, etc.)
  • Salary range filters
  • Contract type (full-time, part-time, contract)
  • Remote work filters
  • Company size filters
  • Distance from location (radius in miles)
  • Sort by: relevance, date, salary

💡 Perfect for matching veterans to CURRENT market opportunities!
""")
'''

print(sample_code)

print("\n" + "="*70)
print("💡 ADZUNA SALARY API (BONUS)")
print("="*70)
print("""
Adzuna also provides a SALARY API:

GET /v1/api/jobs/{country}/history
  • Historical salary trends
  • Salary by location
  • Salary by category
  • Top paying companies

Example:
https://api.adzuna.com/v1/api/jobs/us/history?app_id=YOUR_ID&app_key=YOUR_KEY&location0=US&location1=California&category=it-jobs

Returns: Monthly salary trends for IT jobs in California!
""")

# COMMAND ----------

# DBTITLE 1,5. CareerOneStop API - DOL Veteran Services (FREE)
print("="*70)
print("🎖️ CareerOneStop API - DOL Veteran Employment Services")
print("="*70)

print("""
✅ VETERAN-FOCUSED - Department of Labor sponsored services!

📋 What You Get:
  • Veteran-friendly employers database
  • Apprenticeship programs
  • Training providers
  • Career exploration tools
  • Industry certifications
  • Local American Job Centers
  • Occupation profiles with veteran notes

💰 Cost: FREE
🔑 Registration: https://www.careeronestop.org/Developers/WebAPI/web-api.aspx
📚 Docs: https://www.careeronestop.org/Developers/WebAPI/web-api.aspx
⚡ Rate Limit: Unlimited (government)

---

🔧 SETUP INSTRUCTIONS:

1. Request token: https://www.careeronestop.org/Developers/WebAPI/registration.aspx
2. Use email: whall4.wh@gmail.com
3. Specify use case: "Veteran job matching platform - For Your Service"
4. Instant approval

---

📝 SAMPLE REQUEST - Find veteran-friendly employers:
""")

sample_code = '''
import requests
import json

USER_ID = "YOUR_USER_ID"
AUTHORIZATION_TOKEN = "YOUR_TOKEN"

headers = {
    "Authorization": f"Bearer {AUTHORIZATION_TOKEN}"
}

# Search for veteran-friendly employers in San Diego
response = requests.get(
    f"https://api.careeronestop.org/v1/veteranemployer/{USER_ID}/SanDiego/CA/25",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    employers = data["VeteranEmployerList"]
    
    print(f"\\nFound {len(employers)} veteran-friendly employers\\n")
    
    for employer in employers[:5]:
        print(f"{'='*60}")
        print(f"Company: {employer['CompanyName']}")
        print(f"Location: {employer['City']}, {employer['StateCode']}")
        print(f"Distance: {employer['Distance']} miles")
        print(f"Description: {employer.get('Description', 'N/A')[:100]}...\\n")
else:
    print(f"Error: {response.status_code}")

print("\\n" + "="*60)
print("🎓 TRAINING PROVIDERS API")
print("="*60)

# Find training programs for IT certifications
training_response = requests.get(
    f"https://api.careeronestop.org/v1/training/{USER_ID}/CYBERSECURITY/SanDiego/CA/0/0/0/25",
    headers=headers
)

if training_response.status_code == 200:
    training_data = training_response.json()
    programs = training_data["Programs"]
    
    print(f"\\nFound {len(programs)} cybersecurity training programs\\n")
    
    for program in programs[:3]:
        print(f"{'='*60}")
        print(f"School: {program['SchoolName']}")
        print(f"Program: {program['ProgramName']}")
        print(f"Credential: {program.get('Credential', 'N/A')}")
        print(f"Cost: {program.get('Cost', 'N/A')}")
        print(f"Duration: {program.get('Length', 'N/A')}\\n")
else:
    print(f"Error finding training programs")
'''

print(sample_code)

print("\n" + "="*70)
print("💡 OTHER CAREERONESTOP APIs")
print("="*70)
print("""
1. Occupation Info API
   - Veteran-specific occupation notes
   - Skills needed
   - Licensing requirements

2. Certification Finder API
   - Industry certifications
   - Certification providers
   - Cost and requirements

3. American Job Center API
   - Local veteran employment reps
   - Workshop schedules
   - Services available

💡 Combine with your tensor matching to suggest:
   - Jobs + nearby training if skills gap exists
   - Veteran-friendly companies first
   - Certifications that boost match probability
""")

# COMMAND ----------

# DBTITLE 1,Implementation Strategy - Data Collection Schedule
print("="*70)
print("🗓️ DATA COLLECTION STRATEGY")
print("="*70)

print("""
📋 COLLECTION FREQUENCY (Optimized for FREE tier)

┌──────────────────────────────────────────────────────────────────┐
│ Data Source          │ Frequency  │ API Calls/Month │ Cost       │
├──────────────────────────────────────────────────────────────────┤
│ USAJobs (postings)   │ Daily      │ 30          │ $0 (FREE)  │
│ Adzuna (postings)    │ Daily      │ 30          │ $0 (FREE)  │
│ O*NET (occupations)  │ Weekly     │ 4           │ $0 (FREE)  │
│ BLS (wage data)      │ Monthly    │ 50          │ $0 (FREE)  │
│ CareerOneStop        │ Weekly     │ 4           │ $0 (FREE)  │
├──────────────────────────────────────────────────────────────────┤
│ TOTAL                │            │ 118         │ $0/month   │
└──────────────────────────────────────────────────────────────────┘

🎯 TARGET LOCATIONS (Priority for MVP):
  1. California (highest veteran population)
  2. Texas
  3. Florida
  4. Virginia (military-heavy)
  5. Washington

🏆 TARGET INDUSTRIES:
  1. Information Technology & Cybersecurity
  2. Logistics & Transportation
  3. Healthcare
  4. Construction & Skilled Trades
  5. Government & Public Safety

---

🔧 CLOUD FUNCTION ARCHITECTURE:

Scheduled Functions (GCP Cloud Scheduler + Cloud Functions):
  • daily_job_collector()      -> Fetch USAJobs + Adzuna
  • weekly_occupation_sync()   -> Sync O*NET + CareerOneStop
  • monthly_wage_update()      -> Update BLS wage data
  • normalize_and_store()      -> Clean + write to GCS

All scheduled via Cloud Scheduler (FREE: 3 jobs included)
""")

# COMMAND ----------

# DBTITLE 1,Cloud Function - Job Data Collector
print("="*70)
print("🚀 CLOUD FUNCTION CODE - Job Data Collector")
print("="*70)

print("""
This Cloud Function runs daily to collect job postings from multiple sources.
Deploy to GCP Cloud Functions (FREE: 2M invocations/month).

File: job_collector/main.py
""")

cloud_function_code = '''
import functions_framework
import requests
import json
from datetime import datetime
from google.cloud import storage
import os

# Configuration from environment variables
USAJOBS_API_KEY = os.environ.get('USAJOBS_API_KEY')
USAJOBS_USER_AGENT = os.environ.get('USAJOBS_USER_AGENT')
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
ADZUNA_API_KEY = os.environ.get('ADZUNA_API_KEY')
GCS_BUCKET = os.environ.get('GCS_BUCKET', 'fys-job-market-data')

@functions_framework.http
def collect_jobs(request):
    """
    Collect jobs from multiple sources and store in GCS.
    Triggered daily by Cloud Scheduler.
    """
    
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "sources": [],
        "total_jobs_collected": 0
    }
    
    # Target locations and keywords
    locations = [
        ("California", "CA"),
        ("Texas", "TX"),
        ("Florida", "FL"),
        ("Virginia", "VA"),
        ("Washington", "WA")
    ]
    
    keywords = [
        "cybersecurity",
        "network engineer",
        "logistics",
        "project manager",
        "healthcare"
    ]
    
    # Collect from USAJobs
    print("Collecting from USAJobs...")
    usajobs_count = collect_usajobs(locations, keywords)
    results["sources"].append({"source": "USAJobs", "count": usajobs_count})
    results["total_jobs_collected"] += usajobs_count
    
    # Collect from Adzuna
    print("Collecting from Adzuna...")
    adzuna_count = collect_adzuna(locations, keywords)
    results["sources"].append({"source": "Adzuna", "count": adzuna_count})
    results["total_jobs_collected"] += adzuna_count
    
    # Save results summary to GCS
    save_to_gcs(
        data=results,
        bucket_name=GCS_BUCKET,
        blob_path=f"collection_logs/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_summary.json"
    )
    
    return json.dumps(results), 200


def collect_usajobs(locations, keywords):
    """Collect jobs from USAJobs API"""
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_USER_AGENT,
        "Authorization-Key": USAJOBS_API_KEY
    }
    
    total_collected = 0
    
    for location_name, state_code in locations:
        for keyword in keywords:
            params = {
                "Keyword": keyword,
                "LocationName": location_name,
                "ResultsPerPage": 100,
                "Page": 1
            }
            
            response = requests.get(
                "https://data.usajobs.gov/api/Search",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("SearchResult", {}).get("SearchResultItems", [])
                
                # Save to GCS
                if jobs:
                    save_to_gcs(
                        data=jobs,
                        bucket_name=GCS_BUCKET,
                        blob_path=f"raw/usajobs/{state_code}/{keyword}/{datetime.utcnow().strftime('%Y%m%d')}.json"
                    )
                    total_collected += len(jobs)
            else:
                print(f"USAJobs error for {location_name} - {keyword}: {response.status_code}")
    
    return total_collected


def collect_adzuna(locations, keywords):
    """Collect jobs from Adzuna API"""
    total_collected = 0
    
    for location_name, state_code in locations:
        for keyword in keywords:
            params = {
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_API_KEY,
                "results_per_page": 50,
                "what": keyword,
                "where": f"{location_name}",
                "distance": 50,
                "full_time": 1
            }
            
            response = requests.get(
                "https://api.adzuna.com/v1/api/jobs/us/search/1",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("results", [])
                
                # Save to GCS
                if jobs:
                    save_to_gcs(
                        data=jobs,
                        bucket_name=GCS_BUCKET,
                        blob_path=f"raw/adzuna/{state_code}/{keyword}/{datetime.utcnow().strftime('%Y%m%d')}.json"
                    )
                    total_collected += len(jobs)
            else:
                print(f"Adzuna error for {location_name} - {keyword}: {response.status_code}")
    
    return total_collected


def save_to_gcs(data, bucket_name, blob_path):
    """Save JSON data to Google Cloud Storage"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    
    blob.upload_from_string(
        json.dumps(data, indent=2),
        content_type='application/json'
    )
    
    print(f"Saved to gs://{bucket_name}/{blob_path}")
'''

print(cloud_function_code)

print("\n" + "="*70)
print("📦 DEPLOYMENT")
print("="*70)
print("""
# requirements.txt
functions-framework==3.*
requests==2.31.0
google-cloud-storage==2.10.0

# Deploy command:
gcloud functions deploy job_collector \\
  --runtime python311 \\
  --trigger-http \\
  --entry-point collect_jobs \\
  --set-env-vars USAJOBS_API_KEY=YOUR_KEY,USAJOBS_USER_AGENT=whall4.wh@gmail.com,ADZUNA_APP_ID=YOUR_ID,ADZUNA_API_KEY=YOUR_KEY,GCS_BUCKET=fys-job-market-data \\
  --memory 512MB \\
  --timeout 540s \\
  --allow-unauthenticated

# Schedule with Cloud Scheduler:
gcloud scheduler jobs create http daily-job-collector \\
  --schedule "0 6 * * *" \\
  --uri https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/job_collector \\
  --http-method POST \\
  --time-zone "America/Los_Angeles"
""")

# COMMAND ----------

# DBTITLE 1,Next Steps - Implementation Roadmap
print("="*70)
print("🗯️ IMPLEMENTATION ROADMAP")
print("="*70)

print("""
👉 PHASE 1: API REGISTRATION (1-2 hours)
  ☐ Register for USAJobs API
  ☐ Register for Adzuna API
  ☐ Register for BLS API
  ☐ Register for CareerOneStop API
  ☐ Test each API with sample requests
  ☐ Document API keys in GCP Secret Manager

👉 PHASE 2: CLOUD FUNCTION SETUP (2-3 hours)
  ☐ Create GCS bucket: fys-job-market-data
  ☐ Deploy job_collector Cloud Function
  ☐ Set up Cloud Scheduler (daily trigger)
  ☐ Test collection manually
  ☐ Verify data landing in GCS

👉 PHASE 3: DATABRICKS INGESTION (2-3 hours)
  ☐ Create Bronze schema: main.fys_bronze.job_postings
  ☐ Set up Auto Loader from GCS
  ☐ Build incremental ingestion pipeline
  ☐ Test with sample data

👉 PHASE 4: FEATURE ENGINEERING (3-4 hours)
  ☐ Create Silver transformation pipeline
  ☐ Normalize job titles and skills
  ☐ Extract salary ranges
  ☐ Map to O*NET occupation codes
  ☐ Geocode locations
  ☐ Calculate market demand metrics

👉 PHASE 5: TENSOR PREPARATION (2-3 hours)
  ☐ Create Gold layer: job_embeddings
  ☐ Convert features to 384-dim vectors
  ☐ Index by location, industry, salary
  ☐ Export training data for neural network

---

📊 EXPECTED DATA VOLUME:

Daily Collection:
  • USAJobs: ~500-1,000 jobs/day
  • Adzuna: ~1,000-2,000 jobs/day
  • Total: ~1,500-3,000 new postings/day

Storage (Bronze layer):
  • ~50-100 MB/day
  • ~1.5-3 GB/month
  • Well within GCS 5GB free tier!

---

💡 VALUE PROPOSITION:

With this job market data pipeline, your neural network can:

  ✅ Match veterans to REAL, CURRENT job openings
  ✅ Provide accurate salary expectations by location
  ✅ Identify skills gaps and recommend training
  ✅ Prioritize veteran-friendly employers
  ✅ Show market trends (hot skills, growing industries)
  ✅ Calculate placement probability based on current demand

---

🎯 NEXT SESSION PRIORITY:

1. Register for APIs (15 minutes total - all instant approval)
2. Deploy Cloud Function collector
3. Set up Bronze ingestion in Databricks

Then you'll have LIVE job market data flowing into your tensor pipeline!
""")

print("\n" + "="*70)
print("✅ NOTEBOOK COMPLETE - Ready to implement!")
print("="*70)

# COMMAND ----------

# DBTITLE 1,WORKING SCRAPER - Register for APIs First
print("="*70)
print("🚀 STEP 1: GET YOUR API KEYS (15 minutes)")
print("="*70)

print("""
Before running the scraper below, register for these FREE APIs:

1. ADZUNA (EASIEST - Start here):
   👉 https://developer.adzuna.com/signup
   📧 Email: whall4.wh@gmail.com
   ⏱️ Instant approval
   🎁 You get: Application ID + API Key
   
2. USAJOBS:
   👉 https://developer.usajobs.gov/
   📧 Email: whall4.wh@gmail.com  
   ⏱️ Instant approval
   🎁 You get: Authorization Key

3. BLS (OPTIONAL - for wage data):
   👉 https://data.bls.gov/registrationEngine/
   📧 Email: whall4.wh@gmail.com
   ⏱️ Instant approval
   🎁 You get: API Key via email

---

⚠️ IMPORTANT: Once you have the keys, update the cell below with your credentials!

---

💡 TIP: Register for Adzuna first - it's the easiest and gives you 1M+ job listings.
     You can test the scraper with just Adzuna, then add USAJobs later.
""")

# COMMAND ----------

# DBTITLE 1,LIVE SCRAPER - Real Job Data Collector
import requests
import json
from datetime import datetime
import time

print("="*70)
print("🔥 REAL-TIME JOB SCRAPER - Collecting Live Data")
print("="*70)

# ==========================================
# 🔑 YOUR API CREDENTIALS (UPDATE THESE!)
# ==========================================

# Adzuna API (https://developer.adzuna.com/)
ADZUNA_APP_ID = "YOUR_APP_ID_HERE"  # Replace with your Adzuna App ID
ADZUNA_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your Adzuna API Key

# USAJobs API (https://developer.usajobs.gov/)
USAJOBS_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your USAJobs Authorization Key
USAJOBS_USER_AGENT = "whall4.wh@gmail.com"  # Your email

# ==========================================
# 🎯 SEARCH CONFIGURATION
# ==========================================

# Target locations for veteran job matching
TARGET_LOCATIONS = [
    {"city": "San Diego", "state": "CA"},
    {"city": "Virginia Beach", "state": "VA"},
    {"city": "San Antonio", "state": "TX"},
]

# Keywords based on common veteran skill transfers
SEARCH_KEYWORDS = [
    "cybersecurity",
    "network engineer",
    "logistics coordinator",
    "project manager",
]

# ==========================================
# 📊 ADZUNA SCRAPER
# ==========================================

def scrape_adzuna_jobs(location, keyword, max_results=50):
    """
    Scrape real job postings from Adzuna API.
    Returns list of job dictionaries with standardized fields.
    """
    
    if ADZUNA_APP_ID == "YOUR_APP_ID_HERE":
        print("⚠️  Adzuna API credentials not configured. Skipping...")
        return []
    
    print(f"\n🔍 Searching Adzuna: {keyword} in {location['city']}, {location['state']}")
    
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": min(max_results, 50),
        "what": keyword,
        "where": f"{location['city']}, {location['state']}",
        "distance": 50,  # 50 mile radius
        "full_time": 1,
        "sort_by": "date"  # Most recent first
    }
    
    try:
        response = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("results", [])
            
            # Standardize job data format
            standardized_jobs = []
            for job in jobs:
                standardized_jobs.append({
                    "source": "adzuna",
                    "job_id": job.get("id"),
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": {
                        "city": location["city"],
                        "state": location["state"],
                        "display": job.get("location", {}).get("display_name"),
                        "latitude": job.get("latitude"),
                        "longitude": job.get("longitude")
                    },
                    "salary": {
                        "min": job.get("salary_min"),
                        "max": job.get("salary_max"),
                        "is_predicted": job.get("salary_is_predicted", False)
                    },
                    "description": job.get("description", "")[:500],  # First 500 chars
                    "posted_date": job.get("created"),
                    "url": job.get("redirect_url"),
                    "contract_type": job.get("contract_type"),
                    "category": job.get("category", {}).get("label"),
                    "scraped_at": datetime.utcnow().isoformat()
                })
            
            print(f"   ✅ Found {len(standardized_jobs)} jobs")
            return standardized_jobs
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text[:100]}")
            return []
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return []

# ==========================================
# 🏛️ USAJOBS SCRAPER  
# ==========================================

def scrape_usajobs(location, keyword, max_results=100):
    """
    Scrape federal job postings from USAJobs API.
    Great for veterans due to preference indicators.
    """
    
    if USAJOBS_API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  USAJobs API credentials not configured. Skipping...")
        return []
    
    print(f"\n🏛️  Searching USAJobs: {keyword} in {location['state']}")
    
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_USER_AGENT,
        "Authorization-Key": USAJOBS_API_KEY
    }
    
    params = {
        "Keyword": keyword,
        "LocationName": location["city"],
        "ResultsPerPage": min(max_results, 500),
        "Page": 1
    }
    
    try:
        response = requests.get(
            "https://data.usajobs.gov/api/Search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            result_items = data.get("SearchResult", {}).get("SearchResultItems", [])
            
            standardized_jobs = []
            for item in result_items:
                job = item.get("MatchedObjectDescriptor", {})
                
                # Extract salary
                salary_info = job.get("PositionRemuneration", [{}])[0]
                
                standardized_jobs.append({
                    "source": "usajobs",
                    "job_id": job.get("PositionID"),
                    "title": job.get("PositionTitle"),
                    "company": job.get("OrganizationName"),
                    "location": {
                        "city": location["city"],
                        "state": location["state"],
                        "display": job.get("PositionLocationDisplay"),
                    },
                    "salary": {
                        "min": salary_info.get("MinimumRange"),
                        "max": salary_info.get("MaximumRange"),
                        "is_predicted": False
                    },
                    "description": job.get("UserArea", {}).get("Details", {}).get("JobSummary", "")[:500],
                    "posted_date": job.get("PublicationStartDate"),
                    "url": job.get("PositionURI"),
                    "security_clearance": job.get("SecurityClearance"),
                    "veteran_preference": job.get("UserArea", {}).get("Details", {}).get("HiringPath"),
                    "category": job.get("JobCategory", [{}])[0].get("Name"),
                    "scraped_at": datetime.utcnow().isoformat()
                })
            
            print(f"   ✅ Found {len(standardized_jobs)} jobs")
            return standardized_jobs
        else:
            print(f"   ❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return []

# ==========================================
# 🚀 MAIN SCRAPER EXECUTION
# ==========================================

print(f"\n🎯 Starting scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
print("="*70)

all_jobs = []

for location in TARGET_LOCATIONS:
    for keyword in SEARCH_KEYWORDS:
        
        # Scrape from Adzuna
        adzuna_jobs = scrape_adzuna_jobs(location, keyword, max_results=20)
        all_jobs.extend(adzuna_jobs)
        
        # Scrape from USAJobs
        usajobs_jobs = scrape_usajobs(location, keyword, max_results=50)
        all_jobs.extend(usajobs_jobs)
        
        # Rate limiting - be nice to APIs
        time.sleep(1)

print("\n" + "="*70)
print("📊 SCRAPING COMPLETE")
print("="*70)
print(f"\n✅ Total jobs collected: {len(all_jobs)}")
print(f"   • Adzuna: {len([j for j in all_jobs if j['source'] == 'adzuna'])}")
print(f"   • USAJobs: {len([j for j in all_jobs if j['source'] == 'usajobs'])}")

# Show sample of collected data
if all_jobs:
    print("\n📋 SAMPLE JOB (First Result):\n")
    sample = all_jobs[0]
    print(f"Title: {sample['title']}")
    print(f"Company: {sample['company']}")
    print(f"Location: {sample['location']['display']}")
    print(f"Salary: ${sample['salary']['min']:,} - ${sample['salary']['max']:,}" if sample['salary']['min'] else "Salary: Not specified")
    print(f"Posted: {sample['posted_date']}")
    print(f"URL: {sample['url']}")
    print(f"\nDescription preview:\n{sample['description'][:200]}...")
else:
    print("\n⚠️  No jobs collected. Please check your API credentials above!")

# COMMAND ----------

# DBTITLE 1,Save Scraped Data to JSON (Ready for Bronze Ingestion)
# Save the scraped data to a JSON file for Bronze layer ingestion

if all_jobs:
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"scraped_jobs_{timestamp}.json"
    
    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(all_jobs, f, indent=2)
    
    print("="*70)
    print("💾 DATA SAVED")
    print("="*70)
    print(f"\n✅ Saved {len(all_jobs)} jobs to: {output_file}")
    print(f"\n📍 File location: /Workspace{output_file}")
    print("\n🎯 Next steps:")
    print("   1. This file is ready for Bronze layer ingestion")
    print("   2. Upload to GCS: gs://fys-job-market-data/raw/")
    print("   3. Or ingest directly into Databricks Delta table")
    
    # Show data statistics
    print("\n📊 DATA STATISTICS:")
    print(f"   • Jobs with salary info: {len([j for j in all_jobs if j['salary']['min']])}")
    print(f"   • Unique companies: {len(set([j['company'] for j in all_jobs if j['company']]))}")
    print(f"   • Unique job titles: {len(set([j['title'] for j in all_jobs]))}")
    
    # Show breakdown by location
    print("\n📍 JOBS BY LOCATION:")
    from collections import Counter
    locations = Counter([j['location']['city'] for j in all_jobs])
    for loc, count in locations.most_common():
        print(f"   • {loc}: {count} jobs")
    
    # Show breakdown by category/industry
    print("\n🏢 JOBS BY CATEGORY:")
    categories = Counter([j.get('category') for j in all_jobs if j.get('category')])
    for cat, count in categories.most_common(5):
        print(f"   • {cat}: {count} jobs")
        
else:
    print("\n⚠️  No jobs to save. Please update API credentials and run the scraper cell above.")

# COMMAND ----------

# DBTITLE 1,Preview: What You'll Get Per Job
print("="*70)
print("📋 STANDARDIZED JOB DATA FORMAT")
print("="*70)

print("""
Every scraped job contains:

🎯 CORE FIELDS:
  • job_id          - Unique identifier
  • title           - Job title (e.g., "Cybersecurity Analyst")
  • company         - Company name
  • source          - API source (adzuna, usajobs, etc.)
  
📍 LOCATION:
  • city, state     - Geographic location
  • latitude/longitude - For distance calculations
  • display         - Full formatted address
  
💰 SALARY:
  • min, max        - Salary range
  • is_predicted    - Whether salary is estimated or posted
  
📄 DETAILS:
  • description     - Job description (first 500 chars)
  • category        - Industry/job category
  • contract_type   - Full-time, contract, etc.
  • posted_date     - When job was posted
  • url             - Direct application link
  
🎖️ VETERAN-SPECIFIC (USAJobs only):
  • security_clearance    - Required clearance level
  • veteran_preference    - Hiring path preferences
  
⏰ METADATA:
  • scraped_at      - Timestamp of data collection
  
---

💡 This standardized format feeds directly into your:
   1. Bronze Layer (raw storage)
   2. Silver Layer (feature engineering)
   3. Gold Layer (384-dim tensor vectors)
   4. Neural Network (veteran-job matching)
""")

print("\n" + "="*70)
print("🚀 READY TO SCRAPE REAL DATA!")
print("="*70)
print("""
To get started:

1. Register for API keys (15 min):
   • Adzuna: https://developer.adzuna.com/signup
   • USAJobs: https://developer.usajobs.gov/

2. Update credentials in the scraper cell above

3. Run the scraper cell

4. Save data to JSON

5. Ingest into Bronze layer

You'll have REAL job market data flowing into your matching engine!
""")

# COMMAND ----------

