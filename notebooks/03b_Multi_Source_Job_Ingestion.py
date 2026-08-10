# Databricks notebook source
# DBTITLE 1,Multi-Source Job Ingestion Pipeline
# MAGIC %md
# MAGIC # 🌐 For Your Service - Multi-Source Job Ingestion Pipeline
# MAGIC
# MAGIC ## 📊 Data Sources
# MAGIC
# MAGIC ### 1. **USAJOBS API** (Federal/Contractor Roles)
# MAGIC - **Authentication:** API Key + User-Agent header
# MAGIC - **Target:** Federal government and contractor positions
# MAGIC - **Clearance Availability:** High (many TS/SCI roles)
# MAGIC
# MAGIC ### 2. **JSearch API** (RapidAPI - Multi-Board Aggregation)
# MAGIC - **Authentication:** RapidAPI gateway key
# MAGIC - **Coverage:** Indeed, LinkedIn, Glassdoor, ZipRecruiter
# MAGIC - **Target:** Private sector, broad coverage
# MAGIC
# MAGIC ### 3. **Adzuna API** (Salary Benchmarking & Volume)
# MAGIC - **Authentication:** App ID + App Key
# MAGIC - **Strength:** Real salary data, regional volume metrics
# MAGIC - **Target:** Market intelligence and compensation data
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Regional Focus
# MAGIC - **Primary MSA:** Greenville-Anderson, SC (Metropolitan Statistical Area)
# MAGIC - **Target Radius:** 50-mile radius from Greenville, SC
# MAGIC - **Coordinates:** 34.8526° N, 82.3940° W
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔄 Normalization Schema
# MAGIC All sources normalized to:
# MAGIC ```python
# MAGIC {
# MAGIC   "job_id": "<source>_<native_id_hash>",
# MAGIC   "title": "DevOps Engineer",
# MAGIC   "company": "7 Eagle Group",
# MAGIC   "location_msa": "Greenville-Anderson, SC",
# MAGIC   "compensation_min": 120000.0,
# MAGIC   "compensation_max": 180000.0,
# MAGIC   "source_board": "usajobs|jsearch|adzuna",
# MAGIC   "timestamp_ingested": "2026-08-10T12:00:00Z"
# MAGIC }
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Configuration & API Keys (Databricks Secrets)
# API Configuration using Databricks Secrets
# Following 7 Eagle Group security best practices

import os
import requests
import json
from datetime import datetime
from pyspark.sql import functions as F
from pyspark.sql.types import *
import hashlib

print("="*70)
print("🔐 MULTI-SOURCE JOB INGESTION - API CONFIGURATION")
print("="*70)

# Databricks Secrets scope (create with: databricks secrets create-scope --scope fys-apis)
# Store keys with: databricks secrets put --scope fys-apis --key <key_name>

# For testing, use environment variables or Databricks Secrets
try:
    # USAJOBS API
    USAJOBS_API_KEY = dbutils.secrets.get(scope="fys-apis", key="usajobs-api-key")
    USAJOBS_USER_AGENT = dbutils.secrets.get(scope="fys-apis", key="usajobs-user-agent")
    print("✅ USAJOBS credentials loaded")
except:
    USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "")
    USAJOBS_USER_AGENT = os.getenv("USAJOBS_USER_AGENT", "whall4.wh@gmail.com")
    print("⚠️  USAJOBS: Using environment variables (fallback)")

try:
    # JSearch API (RapidAPI)
    JSEARCH_API_KEY = dbutils.secrets.get(scope="fys-apis", key="jsearch-rapidapi-key")
    print("✅ JSearch credentials loaded")
except:
    JSEARCH_API_KEY = os.getenv("JSEARCH_RAPIDAPI_KEY", "")
    print("⚠️  JSearch: Using environment variables (fallback)")

try:
    # Adzuna API
    ADZUNA_APP_ID = dbutils.secrets.get(scope="fys-apis", key="adzuna-app-id")
    ADZUNA_APP_KEY = dbutils.secrets.get(scope="fys-apis", key="adzuna-app-key")
    print("✅ Adzuna credentials loaded")
except:
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
    print("⚠️  Adzuna: Using environment variables (fallback)")

print("\n📍 Target Location: Greenville, SC (MSA)")
print("🎯 Radius: 50 miles")
print("\n" + "="*70)

# Greenville, SC coordinates for geo-filtering
GREENVILLE_LAT = 34.8526
GREENVILLE_LON = -82.3940
SEARCH_RADIUS_MILES = 50

# COMMAND ----------

# DBTITLE 1,1️⃣ USAJOBS API - Federal & Contractor Roles
def fetch_usajobs_data(keywords, location="Greenville, SC", max_results=100):
    """
    Fetch jobs from USAJOBS API (Federal/Contractor roles)
    
    Authentication: API Key + User-Agent header
    Target: Federal positions, high clearance availability
    """
    print("\n" + "="*70)
    print("🏛️  FETCHING FROM USAJOBS API")
    print("="*70)
    
    if not USAJOBS_API_KEY:
        print("❌ USAJOBS API key not configured")
        return []
    
    url = "https://data.usajobs.gov/api/search"
    
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_USER_AGENT,
        "Authorization-Key": USAJOBS_API_KEY
    }
    
    params = {
        "Keyword": keywords,
        "LocationName": location,
        "ResultsPerPage": min(max_results, 500),  # API max is 500
        "Fields": "min"  # Minimal fields for efficiency
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        jobs = data.get("SearchResult", {}).get("SearchResultItems", [])
        print(f"✅ Retrieved {len(jobs)} jobs from USAJOBS")
        
        # Normalize to common schema
        normalized_jobs = []
        for item in jobs:
            job = item.get("MatchedObjectDescriptor", {})
            
            # Generate unique job_id hash
            native_id = job.get("PositionID", "")
            job_id = f"usajobs_{hashlib.md5(native_id.encode()).hexdigest()[:16]}"
            
            # Extract salary range
            salary_min = job.get("PositionRemuneration", [{}])[0].get("MinimumRange", None)
            salary_max = job.get("PositionRemuneration", [{}])[0].get("MaximumRange", None)
            
            normalized_jobs.append({
                "job_id": job_id,
                "title": job.get("PositionTitle", ""),
                "company": job.get("OrganizationName", "US Government"),
                "source": "usajobs",
                "location": {
                    "city": job.get("PositionLocationDisplay", "").split(",")[0] if "," in job.get("PositionLocationDisplay", "") else "",
                    "state": "SC",  # Filtered by search
                    "display": job.get("PositionLocationDisplay", ""),
                    "latitude": None,
                    "longitude": None
                },
                "salary": {
                    "min": float(salary_min) if salary_min else None,
                    "max": float(salary_max) if salary_max else None,
                    "is_predicted": False
                },
                "description": job.get("UserArea", {}).get("Details", {}).get("JobSummary", ""),
                "requirements": job.get("QualificationSummary", ""),
                "url": job.get("PositionURI", ""),
                "category": job.get("JobCategory", [{}])[0].get("Name", "") if job.get("JobCategory") else "",
                "contract_type": job.get("PositionSchedule", [{}])[0].get("Name", "") if job.get("PositionSchedule") else "",
                "created_date": job.get("PublicationStartDate", ""),
                "scraped_at": datetime.now().isoformat(),
                "source_board": "usajobs"
            })
        
        return normalized_jobs
        
    except requests.exceptions.RequestException as e:
        print(f"❌ USAJOBS API Error: {e}")
        return []

# Test USAJOBS connector
usajobs_data = fetch_usajobs_data(
    keywords="DevOps OR Cloud OR Kubernetes OR AWS",
    location="Greenville, SC",
    max_results=100
)

print(f"\n📊 USAJOBS Results: {len(usajobs_data)} jobs")

# COMMAND ----------

# DBTITLE 1,2️⃣ JSearch API - Multi-Board Aggregation (RapidAPI)
def fetch_jsearch_data(query, location="Greenville, SC", max_results=100):
    """
    Fetch jobs from JSearch API via RapidAPI
    
    Coverage: Indeed, LinkedIn, Glassdoor, ZipRecruiter
    Authentication: RapidAPI gateway key
    """
    print("\n" + "="*70)
    print("🔍 FETCHING FROM JSEARCH API (RapidAPI)")
    print("="*70)
    
    if not JSEARCH_API_KEY:
        print("❌ JSearch API key not configured")
        return []
    
    url = "https://jsearch.p.rapidapi.com/search"
    
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    params = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "date_posted": "month",  # Last 30 days
        "employment_types": "FULLTIME,CONTRACTOR",
        "radius": "50",  # 50 miles
        "location": location
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        jobs = data.get("data", [])
        print(f"✅ Retrieved {len(jobs)} jobs from JSearch")
        
        # Normalize to common schema
        normalized_jobs = []
        for job in jobs:
            # Generate unique job_id hash
            native_id = job.get("job_id", "")
            job_id = f"jsearch_{hashlib.md5(native_id.encode()).hexdigest()[:16]}"
            
            normalized_jobs.append({
                "job_id": job_id,
                "title": job.get("job_title", ""),
                "company": job.get("employer_name", ""),
                "source": "jsearch",
                "location": {
                    "city": job.get("job_city", ""),
                    "state": job.get("job_state", ""),
                    "display": job.get("job_location", ""),
                    "latitude": job.get("job_latitude", None),
                    "longitude": job.get("job_longitude", None)
                },
                "salary": {
                    "min": float(job.get("job_min_salary", 0)) if job.get("job_min_salary") else None,
                    "max": float(job.get("job_max_salary", 0)) if job.get("job_max_salary") else None,
                    "is_predicted": job.get("job_salary_currency") != "USD"  # Flag non-USD as predicted
                },
                "description": job.get("job_description", ""),
                "requirements": job.get("job_highlights", {}).get("Qualifications", []),
                "url": job.get("job_apply_link", ""),
                "category": job.get("job_employment_type", ""),
                "contract_type": job.get("job_employment_type", ""),
                "created_date": job.get("job_posted_at_datetime_utc", ""),
                "scraped_at": datetime.now().isoformat(),
                "source_board": job.get("job_publisher", "jsearch")
            })
        
        return normalized_jobs
        
    except requests.exceptions.RequestException as e:
        print(f"❌ JSearch API Error: {e}")
        return []

# Test JSearch connector
jsearch_data = fetch_jsearch_data(
    query="DevOps Engineer in Greenville, SC",
    location="Greenville, SC",
    max_results=100
)

print(f"\n📊 JSearch Results: {len(jsearch_data)} jobs")

# COMMAND ----------

# DBTITLE 1,3️⃣ Adzuna API - Salary Data & Market Intelligence
def fetch_adzuna_data(keywords, location="Greenville, SC", max_results=100):
    """
    Fetch jobs from Adzuna API
    
    Strength: Real salary data, market intelligence
    Authentication: App ID + App Key
    """
    print("\n" + "="*70)
    print("💰 FETCHING FROM ADZUNA API")
    print("="*70)
    
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        print("❌ Adzuna API credentials not configured")
        return []
    
    # Adzuna US endpoint
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
    
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": keywords,
        "where": location,
        "results_per_page": min(max_results, 50),  # API max is 50 per page
        "distance": 50,  # 50 miles
        "max_days_old": 30,  # Last 30 days
        "sort_by": "relevance"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        jobs = data.get("results", [])
        print(f"✅ Retrieved {len(jobs)} jobs from Adzuna")
        print(f"📊 Mean Salary: ${data.get('mean', 0):,.0f}" if data.get('mean') else "")
        
        # Normalize to common schema
        normalized_jobs = []
        for job in jobs:
            # Generate unique job_id hash
            native_id = job.get("id", "")
            job_id = f"adzuna_{hashlib.md5(str(native_id).encode()).hexdigest()[:16]}"
            
            normalized_jobs.append({
                "job_id": job_id,
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", ""),
                "source": "adzuna",
                "location": {
                    "city": job.get("location", {}).get("display_name", "").split(",")[0] if job.get("location") else "",
                    "state": "SC",
                    "display": job.get("location", {}).get("display_name", ""),
                    "latitude": job.get("latitude", None),
                    "longitude": job.get("longitude", None)
                },
                "salary": {
                    "min": float(job.get("salary_min", 0)) if job.get("salary_min") else None,
                    "max": float(job.get("salary_max", 0)) if job.get("salary_max") else None,
                    "is_predicted": job.get("salary_is_predicted", False)
                },
                "description": job.get("description", ""),
                "requirements": "",  # Adzuna doesn't separate requirements
                "url": job.get("redirect_url", ""),
                "category": job.get("category", {}).get("label", ""),
                "contract_type": job.get("contract_type", ""),
                "created_date": job.get("created", ""),
                "scraped_at": datetime.now().isoformat(),
                "source_board": "adzuna"
            })
        
        return normalized_jobs
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Adzuna API Error: {e}")
        return []

# Test Adzuna connector
adzuna_data = fetch_adzuna_data(
    keywords="DevOps Cloud AWS Kubernetes",
    location="Greenville, SC",
    max_results=100
)

print(f"\n📊 Adzuna Results: {len(adzuna_data)} jobs")

# COMMAND ----------

# DBTITLE 1,🔄 Combine & Deduplicate Multi-Source Data
print("\n" + "="*70)
print("🔄 COMBINING MULTI-SOURCE JOB DATA")
print("="*70)

# Combine all sources
all_jobs = usajobs_data + jsearch_data + adzuna_data

print(f"\n📊 Total Jobs Retrieved:")
print(f"   🏛️  USAJOBS: {len(usajobs_data)}")
print(f"   🔍 JSearch: {len(jsearch_data)}")
print(f"   💰 Adzuna: {len(adzuna_data)}")
print(f"   " + "-"*50)
print(f"   📦 Total: {len(all_jobs)} jobs")

# Deduplicate by job_id (already unique per source, but check for cross-source dupes)
unique_jobs = {}
for job in all_jobs:
    job_id = job["job_id"]
    if job_id not in unique_jobs:
        unique_jobs[job_id] = job
    else:
        # Keep the one with more complete data (e.g., has salary)
        if job["salary"]["min"] and not unique_jobs[job_id]["salary"]["min"]:
            unique_jobs[job_id] = job

deduped_jobs = list(unique_jobs.values())

print(f"\n✅ After Deduplication: {len(deduped_jobs)} unique jobs")
print(f"🗑️  Removed {len(all_jobs) - len(deduped_jobs)} duplicates")

# Regional filtering: Keep only jobs within Greenville MSA
print("\n" + "="*70)
print("📍 REGIONAL FILTERING - GREENVILLE MSA")
print("="*70)

filtered_jobs = []
for job in deduped_jobs:
    # Check if location matches Greenville area
    location_display = job["location"]["display"].lower()
    city = job["location"]["city"].lower()
    
    # Accept if:
    # 1. City is Greenville or nearby (Anderson, Simpsonville, Mauldin, etc.)
    # 2. State is SC and no conflicting city
    # 3. Has lat/lon within radius (TODO: implement haversine distance)
    
    greenville_keywords = [
        "greenville", "anderson", "simpsonville", "mauldin", 
        "greer", "easley", "spartanburg", "clemson"
    ]
    
    if any(keyword in location_display or keyword in city for keyword in greenville_keywords):
        filtered_jobs.append(job)
    elif job["location"]["state"] == "SC" and not any(x in location_display for x in ["charleston", "columbia", "myrtle beach"]):
        filtered_jobs.append(job)

print(f"✅ Greenville MSA Jobs: {len(filtered_jobs)}")
print(f"🗑️  Filtered Out: {len(deduped_jobs) - len(filtered_jobs)} jobs (outside target region)")

if not filtered_jobs:
    print("\n⚠️  No jobs found in Greenville MSA from any source")
    print("   This may indicate:")
    print("   1. API credentials not configured")
    print("   2. No jobs posted in target region recently")
    print("   3. Search query too restrictive")

# COMMAND ----------

# DBTITLE 1,💾 Write to Bronze Delta Table
if filtered_jobs:
    print("\n" + "="*70)
    print("💾 WRITING TO BRONZE DELTA TABLE")
    print("="*70)
    
    # Convert to Spark DataFrame
    from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
    
    # Define schema matching Bronze table
    location_schema = StructType([
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("display", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True)
    ])
    
    salary_schema = StructType([
        StructField("min", DoubleType(), True),
        StructField("max", DoubleType(), True),
        StructField("is_predicted", BooleanType(), True)
    ])
    
    schema = StructType([
        StructField("job_id", StringType(), False),
        StructField("title", StringType(), True),
        StructField("company", StringType(), True),
        StructField("source", StringType(), True),
        StructField("location", location_schema, True),
        StructField("salary", salary_schema, True),
        StructField("description", StringType(), True),
        StructField("requirements", StringType(), True),
        StructField("url", StringType(), True),
        StructField("category", StringType(), True),
        StructField("contract_type", StringType(), True),
        StructField("created_date", StringType(), True),
        StructField("scraped_at", StringType(), True),
        StructField("source_board", StringType(), True)
    ])
    
    # Create DataFrame
    df = spark.createDataFrame(filtered_jobs, schema=schema)
    
    # Add ingestion metadata
    df = df.withColumn("scrape_date", F.current_date().cast("string")) \
           .withColumn("ingestion_timestamp", F.current_timestamp())
    
    # Write to Bronze table (append mode with merge on job_id to avoid duplicates)
    table_name = "workspace.fys_bronze.job_postings"
    
    print(f"\n📦 Target Table: {table_name}")
    print(f"📊 Records to Insert: {df.count()}")
    
    try:
        # Use merge to upsert based on job_id
        from delta.tables import DeltaTable
        
        if spark.catalog.tableExists(table_name):
            delta_table = DeltaTable.forName(spark, table_name)
            
            # Merge: Update if exists, Insert if new
            delta_table.alias("target").merge(
                df.alias("source"),
                "target.job_id = source.job_id"
            ).whenMatchedUpdateAll() \
             .whenNotMatchedInsertAll() \
             .execute()
            
            print("✅ Data merged into Bronze table (upsert completed)")
        else:
            # Table doesn't exist, create it
            df.write.format("delta") \
              .mode("append") \
              .partitionBy("scrape_date") \
              .option("mergeSchema", "true") \
              .saveAsTable(table_name)
            
            print("✅ Bronze table created and data written")
        
        # Verify
        result_count = spark.table(table_name).count()
        print(f"\n📊 Bronze Table Total Records: {result_count}")
        
    except Exception as e:
        print(f"❌ Error writing to Bronze table: {e}")
        print("\n📝 DataFrame Preview:")
        df.show(5, truncate=False)
else:
    print("\n⚠️  No jobs to write (filtered_jobs is empty)")

# COMMAND ----------

# DBTITLE 1,📊 Ingestion Summary & Telemetry
print("\n" + "="*70)
print("📊 INGESTION SUMMARY - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("="*70)

print(f"\n🌐 Sources Queried:")
print(f"   🏛️  USAJOBS API: {'✅ Connected' if USAJOBS_API_KEY else '❌ Not Configured'}")
print(f"   🔍 JSearch API: {'✅ Connected' if JSEARCH_API_KEY else '❌ Not Configured'}")
print(f"   💰 Adzuna API: {'✅ Connected' if ADZUNA_APP_ID else '❌ Not Configured'}")

print(f"\n📈 Results:")
print(f"   Raw Jobs Retrieved: {len(all_jobs)}")
print(f"   After Deduplication: {len(deduped_jobs)}")
print(f"   Greenville MSA Filtered: {len(filtered_jobs)}")
print(f"   Written to Bronze: {len(filtered_jobs) if filtered_jobs else 0}")

if filtered_jobs:
    print(f"\n💰 Salary Statistics (Greenville MSA):")
    salaries = [j["salary"]["min"] for j in filtered_jobs if j["salary"]["min"]]
    if salaries:
        print(f"   Min: ${min(salaries):,.0f}")
        print(f"   Max: ${max(salaries):,.0f}")
        print(f"   Avg: ${sum(salaries)/len(salaries):,.0f}")
    else:
        print("   No salary data available")
    
    print(f"\n🏢 Top Companies:")
    companies = {}
    for job in filtered_jobs:
        company = job["company"]
        companies[company] = companies.get(company, 0) + 1
    
    for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {company}: {count} jobs")

print("\n" + "="*70)
print("✅ MULTI-SOURCE INGESTION COMPLETE")
print("="*70)

print("\n🎯 Next Steps:")
print("1. Schedule this notebook to run daily (Databricks Jobs)")
print("2. Set up Databricks Secrets for API keys")
print("3. Monitor Bronze table growth: SELECT COUNT(*) FROM workspace.fys_bronze.job_postings")
print("4. Build Silver layer for O*NET skill crosswalk matching")
print("5. Feed normalized tensors into neural matching engine")

# COMMAND ----------

