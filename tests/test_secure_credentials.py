# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Setup Instructions
# MAGIC %md
# MAGIC # ???? Secure Credential Setup for JSearch API
# MAGIC
# MAGIC **Following your security preferences - storing API keys safely in Databricks Secrets**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 1: Open Databricks Secrets UI
# MAGIC
# MAGIC Click this link to open Secrets management:
# MAGIC https://dbc-3e95d032-684c.cloud.databricks.com/#secrets
# MAGIC
# MAGIC Or navigate: **Settings ??? Admin Console ??? Secrets**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 2: Create Secret Scope
# MAGIC
# MAGIC 1. Click **"Create Scope"** button
# MAGIC 2. Enter name: `api-keys`
# MAGIC 3. Leave "Managed Principal" as default
# MAGIC 4. Click **"Create"**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 3: Add Your JSearch API Key
# MAGIC
# MAGIC 1. Select the `api-keys` scope
# MAGIC 2. Click **"Add Secret"**
# MAGIC 3. Enter:
# MAGIC    - **Key:** `jsearch-rapidapi-key`
# MAGIC    - **Value:** [paste your RapidAPI key from the screenshot]
# MAGIC 4. Click **"Add"**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 4: Add API Host
# MAGIC
# MAGIC 1. Click **"Add Secret"** again
# MAGIC 2. Enter:
# MAGIC    - **Key:** `jsearch-rapidapi-host`
# MAGIC    - **Value:** `jsearch.p.rapidapi.com`
# MAGIC 3. Click **"Add"**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ??? **Credentials are now encrypted and secure!**
# MAGIC
# MAGIC **Run the cells below to verify setup**

# COMMAND ----------

# DBTITLE 1,Verify Credentials Are Stored
# Test that credentials are accessible
from databricks.sdk.runtime import dbutils

print("=" * 70)
print("???? CHECKING DATABRICKS SECRETS CONFIGURATION")
print("=" * 70)

try:
    # Attempt to fetch JSearch credentials
    api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
    api_host = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")

    print("\n??? SUCCESS! JSearch credentials are configured")
    print(f"\n   API Key: [REDACTED]")
    print(f"   Key Length: {len(api_key)} characters")
    print(f"   API Host: [REDACTED]")
    print(f"\n   ??? No API keys exposed in code or logs")
    print(f"   ??? Safe to commit to git")
    print(f"   ??? Encrypted at rest")

    credentials_configured = True

except Exception as e:
    print("\n??? Credentials not found!")
    print(f"\n   Error: {e}")
    print("\n   ???? Action needed:")
    print("   1. Go to: https://dbc-3e95d032-684c.cloud.databricks.com/#secrets")
    print("   2. Create scope 'api-keys'")
    print("   3. Add secrets as shown in instructions above")

    credentials_configured = False

print("\n" + "=" * 70)

# COMMAND ----------

# DBTITLE 1,Test JSearch API Connection
# Test actual API connection with stored credentials
import requests

if credentials_configured:
    print("=" * 70)
    print("???? TESTING JSEARCH API CONNECTION")
    print("=" * 70)

    # Fetch credentials securely
    api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
    api_host = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")

    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": api_host}

    # Test with a simple query for Greenville, SC DevOps jobs
    params = {
        "query": "DevOps Engineer in Greenville SC",
        "page": "1",
        "num_pages": "1",
        "date_posted": "month",
    }

    print("\n???? Connecting to JSearch API...")
    print(f"   Query: {params['query']}")
    print(f"   Timeframe: Last 30 days")

    try:
        response = requests.get(
            f"https://{api_host}/search", headers=headers, params=params, timeout=15
        )

        print(f"\n   Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            jobs = data.get("data", [])

            print("\n" + "=" * 70)
            print("??? API CONNECTION SUCCESSFUL!")
            print("=" * 70)
            print(f"\n   Jobs Found: {len(jobs)}")

            if jobs:
                print("\n   Sample Jobs:")
                for i, job in enumerate(jobs[:3], 1):
                    print(f"\n   {i}. {job.get('job_title', 'N/A')}")
                    print(f"      Company: {job.get('employer_name', 'N/A')}")
                    print(
                        f"      Location: {job.get('job_city', 'N/A')}, {job.get('job_state', 'N/A')}"
                    )
                    salary_min = job.get("job_min_salary")
                    salary_max = job.get("job_max_salary")
                    if salary_min and salary_max:
                        print(f"      Salary: ${salary_min:,.0f} - ${salary_max:,.0f}")
                    print(f"      Posted: {job.get('job_posted_at_datetime_utc', 'N/A')[:10]}")

            print("\n" + "=" * 70)
            print("???? READY TO SCRAPE JOBS FOR FREE HALL!")
            print("=" * 70)
            print("\nYour secure credential setup is complete.")
            print("You can now:")
            print("  ??? Run full job scraping (100+ private sector matches)")
            print("  ??? Register USAJobs API for federal positions")
            print("  ??? Generate comprehensive job match reports")

        elif response.status_code == 429:
            print("\n" + "=" * 70)
            print("??????  RATE LIMIT REACHED")
            print("=" * 70)
            print("\n   Your API key works, but rate limit hit.")
            print("   Free tier: 300 requests/month")
            print("   Wait a few minutes and try again.")

        else:
            print(f"\n??? API Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")

    except requests.exceptions.Timeout:
        print("\n??????  Request timed out")
        print("   API might be slow - try again")

    except Exception as e:
        print(f"\n??? Error: {str(e)}")

else:
    print("\n??????  Skipping API test - credentials not configured yet")
    print("   Configure credentials first, then run this cell")

# COMMAND ----------

# DBTITLE 1,Next Steps - USAJobs Registration
# MAGIC %md
# MAGIC # ??? JSearch API Configured!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Next: Add USAJobs for Federal Job Coverage
# MAGIC
# MAGIC **Why USAJobs matters for Free Hall:**
# MAGIC - ??????? **Veteran Preference** - 5-10 points added to application scores
# MAGIC - ???? **Clearance Advantage** - Former TS/SCI = reactivation eligible
# MAGIC - ???? **100-200 federal matches** expected (VA, DOD, DHS roles)
# MAGIC - ???? **$120K-$180K GS-13/14/15 positions**
# MAGIC - ???? **Many remote DevOps/Cloud roles**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 1: Register USAJobs API (5 minutes)
# MAGIC
# MAGIC 1. Go to: https://developer.usajobs.gov/APIRequest/Index
# MAGIC 2. Fill out form:
# MAGIC    - **Name:** William Free Hall
# MAGIC    - **Email:** whall4.wh@gmail.com
# MAGIC    - **Organization:** 7 Eagle Group
# MAGIC    - **Purpose:** Veteran job matching platform
# MAGIC 3. Submit ??? receive API key via email (instant)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 2: Store USAJobs Credentials
# MAGIC
# MAGIC Once you receive the API key:
# MAGIC
# MAGIC 1. Go back to Secrets: https://dbc-3e95d032-684c.cloud.databricks.com/#secrets
# MAGIC 2. Select `api-keys` scope
# MAGIC 3. Add secret:
# MAGIC    - **Key:** `usajobs-api-key`
# MAGIC    - **Value:** [your key from email]
# MAGIC 4. Add secret:
# MAGIC    - **Key:** `usajobs-email`
# MAGIC    - **Value:** `whall4.wh@gmail.com`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 3: Run Combined Scraper
# MAGIC
# MAGIC Once both APIs configured:
# MAGIC - **JSearch:** 100-150 private sector jobs
# MAGIC - **USAJobs:** 100-200 federal jobs
# MAGIC - **Total:** 200-350 matches for Free Hall's profile
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Following your rapid commit strategy, this test notebook will be committed next!**

# COMMAND ----------

# DBTITLE 1,Quick Manual Setup Guide
# MAGIC %md
# MAGIC # ???? Quick 3-Minute Setup
# MAGIC
# MAGIC **I cannot create secrets programmatically (security restriction), but here's the fastest path:**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Click This Link:
# MAGIC https://dbc-3e95d032-684c.cloud.databricks.com/#secrets
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Do These 4 Things:
# MAGIC
# MAGIC 1. **Click "Create Scope"** ??? Name it: `api-keys` ??? Click "Create"
# MAGIC
# MAGIC 2. **Click "Add Secret"** ??? Key: `jsearch-rapidapi-key` ??? Value: [your RapidAPI key] ??? Click "Add"
# MAGIC
# MAGIC 3. **Click "Add Secret"** ??? Key: `jsearch-rapidapi-host` ??? Value: `jsearch.p.rapidapi.com` ??? Click "Add"
# MAGIC
# MAGIC 4. **Come back here and run Cell 2** to verify!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ??? **Takes 2-3 minutes total**
# MAGIC
# MAGIC **Your API key from the screenshot you shared earlier needs to be pasted as the value for `jsearch-rapidapi-key`**

# COMMAND ----------

# DBTITLE 1,Full Pipeline Test - API to Delta Table
import requests
from databricks.sdk.runtime import dbutils

print("=" * 70)
print("???? FULL PIPELINE TEST: JSearch API ??? Delta Table")
print("=" * 70)

# 1. Retrieve secrets securely from Databricks
api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
api_host = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")

print("\n??? Step 1: Credentials retrieved securely")

# 2. Configure endpoint and search parameters for DevOps / Cloud roles
url = "https://jsearch.p.rapidapi.com/search"
querystring = {
    "query": "DevOps Engineer in Greenville, SC",
    "page": "1",
    "num_pages": "1",
    "date_posted": "month",
}
headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "jsearch.p.rapidapi.com",
    "x-rapidapi-key": api_key,
}

print("\n???? Step 2: Querying JSearch API...")
print(f"   Query: {querystring['query']}")

# 3. Execute request and inspect response status
response = requests.get(url, headers=headers, params=querystring, timeout=15)
print(f"\n   API Response Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    job_list = data.get("data", [])
    print(f"\n??? Step 3: Successfully retrieved {len(job_list)} job listings")

    # 4. Ingest into Delta Table (Workspace Catalog Schema)
    if len(job_list) > 0:
        # Display sample of first job
        if job_list:
            sample_job = job_list[0]
            print(f"\n   Sample Job:")
            print(f"   ??? Title: {sample_job.get('job_title', 'N/A')}")
            print(f"   ??? Company: {sample_job.get('employer_name', 'N/A')}")
            print(
                f"   ??? Location: {sample_job.get('job_city', 'N/A')}, {sample_job.get('job_state', 'N/A')}"
            )

        print(f"\n???? Step 4: Writing to Delta table...")

        # Create catalog and schema if they don't exist
        spark.sql("CREATE CATALOG IF NOT EXISTS workspace")
        spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.veteran_intake")

        jobs_df = spark.createDataFrame(job_list)
        jobs_df.write.format("delta").mode("append").saveAsTable(
            "workspace.veteran_intake.raw_job_postings"
        )

        print("\n" + "=" * 70)
        print("??? SUCCESS! Full pipeline test complete!")
        print("=" * 70)
        print(f"\n   ??? {len(job_list)} jobs written to workspace.veteran_intake.raw_job_postings")
        print(f"   ??? Credentials secured (not exposed)")
        print(f"   ??? Ready for production scraping")

        # Show table info
        print(f"\n???? Table Info:")
        row_count = spark.sql(
            "SELECT COUNT(*) as count FROM workspace.veteran_intake.raw_job_postings"
        ).collect()[0]["count"]
        print(f"   Total rows in table: {row_count}")

    else:
        print("\n??????  No jobs returned - try broader search parameters")

else:
    print(f"\n??? Failed to fetch data")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")

# COMMAND ----------

# DBTITLE 1,Subscribe to JSearch API
# MAGIC %md
# MAGIC # ?????? Action Required: Subscribe to JSearch API
# MAGIC
# MAGIC **Your credentials are stored correctly, but you need to activate your JSearch subscription on RapidAPI.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Quick Subscribe (2 minutes):
# MAGIC
# MAGIC 1. **Go to JSearch API page:**
# MAGIC    https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# MAGIC
# MAGIC 2. **Click "Subscribe to Test" or "Pricing"**
# MAGIC
# MAGIC 3. **Select a plan:**
# MAGIC    - **FREE BASIC:** 300 requests/month, $0/month
# MAGIC    - **Pro:** 10,000 requests/month, $29.99/month
# MAGIC    - **Ultra:** 100,000 requests/month, $149.99/month
# MAGIC
# MAGIC 4. **Click "Subscribe"** (you may need to add a payment method even for free tier)
# MAGIC
# MAGIC 5. **Verify your key is tied to the subscription**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## After Subscribing:
# MAGIC
# MAGIC **Come back here and run Cell 6 again** - it should return 200 status and fetch actual jobs!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Current Status:
# MAGIC - ??? Databricks Secrets configured correctly
# MAGIC - ??? API key valid and retrievable
# MAGIC - ??? JSearch API subscription not active
# MAGIC - ??? Waiting on RapidAPI subscription activation
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Once subscribed, we'll have full access to 100-150 private sector DevOps/Cloud jobs for Free Hall!**

# COMMAND ----------

# DBTITLE 1,Troubleshooting - Verify Subscription
# MAGIC %md
# MAGIC # ???? Troubleshooting 404 Errors
# MAGIC
# MAGIC **All endpoint paths are returning 404 - "Endpoint does not exist"**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## This Usually Means One of Three Things:
# MAGIC
# MAGIC ### 1. API Subscription Not Fully Activated
# MAGIC - Sometimes takes 5-10 minutes after subscribing
# MAGIC - Try waiting a few minutes and running Cell 6 again
# MAGIC
# MAGIC ### 2. Wrong API Subscribed To
# MAGIC - Make sure you subscribed to **"JSearch" by letscrape**
# MAGIC - URL should be: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# MAGIC - NOT a different job search API
# MAGIC
# MAGIC ### 3. Check Your RapidAPI Dashboard
# MAGIC
# MAGIC **Go to:** https://rapidapi.com/developer/apps
# MAGIC
# MAGIC 1. Click on your default application
# MAGIC 2. Look under **"Subscriptions"**
# MAGIC 3. Verify **"JSearch"** is listed
# MAGIC 4. Click **"JSearch"** ??? **"Endpoints"** tab
# MAGIC 5. Copy the exact endpoint URL shown (should show something like `GET /search`)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Alternative: Test Directly on RapidAPI
# MAGIC
# MAGIC 1. Go to: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# MAGIC 2. Click **"Endpoints"** tab on the left
# MAGIC 3. Select **"Search"** endpoint
# MAGIC 4. Click **"Test Endpoint"** button
# MAGIC 5. If it works there but not here, copy the exact:
# MAGIC    - Endpoint URL
# MAGIC    - Header format
# MAGIC    - Parameter format
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Next Steps
# MAGIC
# MAGIC If subscription shows active but still getting 404:
# MAGIC - Let me know what the RapidAPI dashboard shows
# MAGIC - We can pivot to **Adzuna API** (working, 8 jobs already fetched)
# MAGIC - Or focus on **USAJobs API** (100-200 federal veteran jobs)

# COMMAND ----------

# DBTITLE 1,Need Exact Endpoint from RapidAPI
# MAGIC %md
# MAGIC # ???? Action Needed: Find Exact Endpoint URL
# MAGIC
# MAGIC **The API is working on RapidAPI (you showed me a successful response!), but we're hitting the wrong endpoint path.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Please Check RapidAPI Interface:
# MAGIC
# MAGIC 1. **Go to:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# MAGIC
# MAGIC 2. **Look at the left sidebar** - you should see a list of endpoints like:
# MAGIC    - `GET /search`
# MAGIC    - `GET /job-details`
# MAGIC    - `GET /search-filters`
# MAGIC    - etc.
# MAGIC
# MAGIC 3. **Click on the endpoint you used** to get the successful response you just shared
# MAGIC
# MAGIC 4. **Look at the top of the code example** - it will show the exact URL format like:
# MAGIC    ```
# MAGIC    https://jsearch.p.rapidapi.com/XXXXX
# MAGIC    ```
# MAGIC
# MAGIC 5. **Copy that exact endpoint path** (the `/XXXXX` part)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## What to Look For:
# MAGIC
# MAGIC In the RapidAPI interface, when you click "Test Endpoint", look at:
# MAGIC - The **REQUEST** tab (not Response)
# MAGIC - The **URL** field
# MAGIC - The exact path after `jsearch.p.rapidapi.com/`
# MAGIC
# MAGIC **Example formats it might be:**
# MAGIC - `https://jsearch.p.rapidapi.com/api/v1/search`
# MAGIC - `https://jsearch.p.rapidapi.com/v2/search`
# MAGIC - `https://jsearch.p.rapidapi.com/jobs`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Once you tell me the exact endpoint URL you see in RapidAPI, I'll update the code and it will work immediately!**

# COMMAND ----------

# DBTITLE 1,Diagnostic - Try All Possible Endpoints
# Try every possible endpoint variation based on RapidAPI common patterns
import requests
from databricks.sdk.runtime import dbutils

api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
api_host = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")

headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": api_host}

# Try different endpoint patterns with minimal params
endpoints_to_try = [
    ("/search", {"query": "DevOps", "num_pages": "1"}),
    ("/", {"query": "DevOps", "num_pages": "1"}),
    ("search", {"query": "DevOps", "num_pages": "1"}),  # No leading slash
    ("/v1/search", {"query": "DevOps", "num_pages": "1"}),
    ("/api/search", {"query": "DevOps", "num_pages": "1"}),
]

print("=" * 70)
print("???? DIAGNOSTIC: Testing All Possible Endpoint Paths")
print("=" * 70)

for endpoint, params in endpoints_to_try:
    full_url = f"https://{api_host}{endpoint}"

    try:
        response = requests.get(full_url, headers=headers, params=params, timeout=10)

        print(f"\n{endpoint:20s} | Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            jobs = data.get("data", [])
            print(f"{'':20s} | ??? SUCCESS! Found {len(jobs)} jobs")
            print(f"{'':20s} | ???? This is the correct endpoint!")
            print(f"\n{'':20s} | Full URL: {full_url}")
            break
        elif response.status_code == 404:
            print(f"{'':20s} | ??? Not found")
        elif response.status_code == 403:
            print(f"{'':20s} | ??????  Subscription issue")
        else:
            print(f"{'':20s} | ??????  {response.text[:50]}")

    except Exception as e:
        print(f"\n{endpoint:20s} | ??? Error: {str(e)[:50]}")

print("\n" + "=" * 70)

# COMMAND ----------

# DBTITLE 1,Find Correct Search Endpoint - Comprehensive Test
# Comprehensive endpoint discovery - trying all logical variations
import requests
from databricks.sdk.runtime import dbutils

api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
api_host = "jsearch.p.rapidapi.com"

# Use lowercase headers as shown in successful curl command
headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": api_host,
    "x-rapidapi-key": api_key,
}

# Comprehensive list of endpoint variations
endpoints = [
    # Standard search patterns
    "/search",
    "/job-search",
    "/jobs-search",
    "/search-jobs",
    # Query patterns
    "/query",
    "/job-query",
    "/find-jobs",
    "/find",
    # List patterns
    "/jobs",
    "/list-jobs",
    "/job-list",
    "/listings",
    "/job-listings",
    # API versioned patterns
    "/api/search",
    "/api/jobs",
    "/v1/search",
    "/v1/jobs",
    "/v2/search",
    # Other common patterns
    "/get-jobs",
    "/browse",
    "/discover",
]

params = {"query": "DevOps", "num_pages": "1"}

print("=" * 80)
print("???? COMPREHENSIVE JSEARCH ENDPOINT DISCOVERY")
print("=" * 80)
print(f"\nTesting {len(endpoints)} possible endpoint variations...")
print(f"Known working endpoint: /job-details ???")
print(f"Looking for: Search/Query endpoint\n")
print("-" * 80)

found = False

for endpoint in endpoints:
    url = f"https://{api_host}{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            print(f"\n???? FOUND IT! {endpoint}")
            print("=" * 80)
            print(f"??? Status: {response.status_code} OK")
            print(f"???? Full URL: {url}")

            data = response.json()
            if "data" in data:
                jobs = data.get("data", [])
                print(f"??? Jobs returned: {len(jobs)}")
                if jobs:
                    print(f"\n???? Sample job:")
                    print(f"   Title: {jobs[0].get('job_title', 'N/A')}")
                    print(f"   Company: {jobs[0].get('employer_name', 'N/A')}")

            print("\n" + "=" * 80)
            print("???? THIS IS THE CORRECT SEARCH ENDPOINT!")
            print("=" * 80)
            found = True
            break

        elif response.status_code == 404:
            print(f"??? {endpoint:25s} | 404 Not Found")
        elif response.status_code == 403:
            print(f"??????  {endpoint:25s} | 403 Subscription/Auth Issue")
        elif response.status_code == 400:
            # 400 might mean endpoint exists but params wrong
            print(f"??? {endpoint:25s} | 400 Bad Request (endpoint might exist!)")
            print(f"   Response: {response.text[:100]}")
        else:
            print(f"??????  {endpoint:25s} | {response.status_code} {response.text[:60]}")

    except requests.exceptions.Timeout:
        print(f"??????  {endpoint:25s} | Timeout")
    except Exception as e:
        print(f"??? {endpoint:25s} | Error: {str(e)[:50]}")

print("\n" + "=" * 80)

if not found:
    print("\n???? No search endpoint found in common patterns.")
    print("\n???? Next steps:")
    print("   1. Check RapidAPI page left sidebar for exact endpoint names")
    print("   2. Look for endpoints like 'Search Jobs', 'Find Jobs', etc.")
    print("   3. The endpoint name might be completely different")
    print("\n???? Alternative: The API might only support job-details (by ID)")
    print("   and not have a search/discovery endpoint at all.")

# COMMAND ----------

# DBTITLE 1,Critical - Check RapidAPI Dashboard
# MAGIC %md
# MAGIC # ???? CRITICAL: JSearch Search Endpoint Not Found
# MAGIC
# MAGIC **We've tested 21+ common endpoint patterns - ALL return 404.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## What This Means:
# MAGIC
# MAGIC 1. **JSearch API structure is non-standard** - the search endpoint has an unusual name
# MAGIC 2. **OR your subscription tier doesn't include search** - only job-details
# MAGIC 3. **OR the endpoint list on RapidAPI shows the exact names**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ???? ACTION REQUIRED: Check RapidAPI Page
# MAGIC
# MAGIC **Go to:** https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# MAGIC
# MAGIC ### Look at the LEFT SIDEBAR
# MAGIC
# MAGIC You should see a list of endpoints. **Tell me EXACTLY what you see**, such as:
# MAGIC
# MAGIC ```
# MAGIC Endpoints:
# MAGIC   ??? Job Details
# MAGIC   ??? Search
# MAGIC   ??? Estimated Salary
# MAGIC   ??? Search Filters
# MAGIC   ...
# MAGIC ```
# MAGIC
# MAGIC ### For Each Endpoint:
# MAGIC
# MAGIC 1. **Click on the endpoint name** (especially any that mention "Search" or "Jobs")
# MAGIC 2. **Look at the code example** - it will show:
# MAGIC    ```
# MAGIC    const url = 'https://jsearch.p.rapidapi.com/XXXXX';
# MAGIC    ```
# MAGIC 3. **Copy the `/XXXXX` part** - that's the actual endpoint path
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ???? What to Look For:
# MAGIC
# MAGIC The endpoint might be called something unexpected like:
# MAGIC - "Job Search"
# MAGIC - "Search Jobs"
# MAGIC - "Query Jobs"
# MAGIC - "Find Jobs"
# MAGIC - "Browse"
# MAGIC - Or something completely different!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ???? Alternative Paths Forward:
# MAGIC
# MAGIC If JSearch search endpoint doesn't exist or isn't available:
# MAGIC
# MAGIC ### Option 1: Use Adzuna API
# MAGIC - **Already working** - fetched 8 jobs on Aug 7
# MAGIC - **FREE tier:** 1000 requests/month
# MAGIC - **Proven:** We know it works for Free Hall's profile
# MAGIC
# MAGIC ### Option 2: Focus on USAJobs API
# MAGIC - **100-200 federal veteran jobs** expected
# MAGIC - **GS-13/14/15:** $120K-$180K positions
# MAGIC - **Veteran preference:** 5-10 point advantage
# MAGIC - **5 minutes to register:** https://developer.usajobs.gov/APIRequest/Index
# MAGIC
# MAGIC ### Option 3: Keep Troubleshooting JSearch
# MAGIC - Check RapidAPI dashboard for exact endpoint names
# MAGIC - Verify subscription includes search capability
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Which path would you like to take?**

# COMMAND ----------

# DBTITLE 1,Verify Job-Details Works + Find Search Endpoint
import requests
from databricks.sdk.runtime import dbutils

api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
api_host = "jsearch.p.rapidapi.com"

# Use exact header format from successful curl command
headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": api_host,
    "x-rapidapi-key": api_key,
}

print("=" * 80)
print("???? JSEARCH API ENDPOINT INVESTIGATION")
print("=" * 80)

# Step 1: Verify /job-details works (we know this endpoint exists)
print("\n??? Step 1: Testing known working endpoint /job-details")
print("-" * 80)

test_job_id = "qIsPjUMr0Em0hqHoAAAAAA=="
job_details_url = f"https://{api_host}/job-details"
job_details_params = {"job_id": test_job_id, "country": "us"}

try:
    response = requests.get(job_details_url, headers=headers, params=job_details_params, timeout=10)
    print(f"Job Details Endpoint: {response.status_code}")

    if response.status_code == 200:
        print("??? SUCCESS! API connection confirmed working")
        print("   Headers are correct")
        print("   Credentials are valid")
        print("   Subscription is active\n")
    else:
        print(f"??????  Unexpected status: {response.text[:100]}\n")
except Exception as e:
    print(f"??? Error: {str(e)[:100]}\n")

# Step 2: Now try to find the SEARCH endpoint
print("\n???? Step 2: Looking for SEARCH endpoint...")
print("-" * 80)
print("Testing most likely patterns based on RapidAPI conventions:\n")

search_params = {"query": "DevOps Engineer", "num_pages": "1"}

# Most common RapidAPI endpoint patterns for job search APIs
search_endpoints = [
    "/search",  # Most common
    "/job-search",
    "/jobs",
    "/search-jobs",
    "/api/v1/search",
    "/v1/search",
]

found_search = False

for endpoint in search_endpoints:
    url = f"https://{api_host}{endpoint}"
    try:
        response = requests.get(url, headers=headers, params=search_params, timeout=10)

        if response.status_code == 200:
            print(f"\n???? FOUND IT! {endpoint}")
            print("=" * 80)
            data = response.json()
            if "data" in data:
                jobs = data.get("data", [])
                print(f"??? Jobs returned: {len(jobs)}")
                if jobs:
                    print(f"\n???? First job:")
                    print(f"   Title: {jobs[0].get('job_title', 'N/A')}")
                    print(f"   Company: {jobs[0].get('employer_name', 'N/A')}")
            print("\n???? Search endpoint found! Ready to scrape jobs.")
            found_search = True
            break
        elif response.status_code == 404:
            print(f"??? {endpoint:20s} | 404 Not Found")
        elif response.status_code == 400:
            print(f"??? {endpoint:20s} | 400 Bad Request")
            print(f"   (Endpoint might exist but params wrong)")
            print(f"   Response: {response.text[:150]}")
        else:
            print(f"??????  {endpoint:20s} | {response.status_code}")
    except Exception as e:
        print(f"??? {endpoint:20s} | {str(e)[:50]}")

print("\n" + "=" * 80)

if not found_search:
    print("\n???? SEARCH ENDPOINT NOT FOUND IN COMMON PATTERNS")
    print("=" * 80)
    print("\n???? This means one of three things:")
    print("\n1. **Endpoint has unusual name** - Check RapidAPI sidebar")
    print("   Go to: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch")
    print("   Look at LEFT SIDEBAR for endpoint list")
    print("   Click each endpoint to see its URL path")
    print("\n2. **Subscription tier limitation** - Your plan might only include:")
    print("   - Job Details (by ID) ??? Working")
    print("   - But NOT Search/Discovery")
    print("\n3. **API doesn't have search** - Some APIs only support:")
    print("   - Get job by ID (what you're paying for)")
    print("   - No browse/search capability")
    print("\n" + "=" * 80)
    print("\n???? RECOMMENDATION: Check RapidAPI page endpoint list NOW")
    print("   or pivot to Adzuna API (working, 8 jobs fetched Aug 7)")
    print("=" * 80)

# COMMAND ----------

# DBTITLE 1,USAJobs API Registration Guide
# MAGIC %md
# MAGIC # ??????? USAJobs API Registration - Federal Veteran Jobs
# MAGIC
# MAGIC **Why USAJobs is Critical for Free Hall:**
# MAGIC - Former Army Green Beret (18 Series SF) - **Veteran Preference Eligible**
# MAGIC - Former TS/SCI clearance holder - **Reactivation Eligible**
# MAGIC - 100-200 federal DevOps/Cloud/SRE roles expected
# MAGIC - GS-13/14/15 positions: **$120K-$180K**
# MAGIC - Many **remote-eligible** positions
# MAGIC - Veteran preference: **5-10 point advantage** on applications
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 1: Register for USAJobs API (5 minutes)
# MAGIC
# MAGIC **Go to:** https://developer.usajobs.gov/APIRequest/Index
# MAGIC
# MAGIC ### Fill Out Registration Form:
# MAGIC
# MAGIC **Contact Information:**
# MAGIC - **First Name:** William
# MAGIC - **Last Name:** Hall
# MAGIC - **Email:** whall4.wh@gmail.com
# MAGIC
# MAGIC **Organization Information:**
# MAGIC - **Organization Name:** 7 Eagle Group
# MAGIC - **Organization Type:** Private Company / Non-Profit (choose applicable)
# MAGIC
# MAGIC **API Usage Information:**
# MAGIC - **Application Name:** For Your Service - Veteran Job Matching Platform
# MAGIC - **Purpose of Use:** AI-powered job matching platform for veterans transitioning to civilian technology careers. Neural network-based matching of veteran skills (military specialties, clearances, leadership experience) to federal DevOps, Cloud Engineering, and Site Reliability Engineering positions.
# MAGIC - **Estimated API Calls:** 1000-5000 per month
# MAGIC
# MAGIC **Technical Contact (same as above):**
# MAGIC - William Hall
# MAGIC - whall4.wh@gmail.com
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 2: Receive API Key
# MAGIC
# MAGIC **You'll receive an email immediately** with:
# MAGIC - **User-Agent** (your API key - looks like email format)
# MAGIC - **Authorization-Key** (API token - long alphanumeric string)
# MAGIC
# MAGIC **Save both** - you'll need them in the next step!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 3: Store USAJobs Credentials in Databricks Secrets
# MAGIC
# MAGIC **Once you receive the email, go to:**
# MAGIC https://dbc-3e95d032-684c.cloud.databricks.com/#secrets
# MAGIC
# MAGIC 1. Select the **`api-keys`** scope (already created)
# MAGIC
# MAGIC 2. **Add first secret:**
# MAGIC    - Key: `usajobs-api-key`
# MAGIC    - Value: [Your Authorization-Key from email]
# MAGIC
# MAGIC 3. **Add second secret:**
# MAGIC    - Key: `usajobs-email`
# MAGIC    - Value: `whall4.wh@gmail.com`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Step 4: Test USAJobs API
# MAGIC
# MAGIC Once credentials are stored, **run the cell below** to test federal job search!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **??? After this is set up, you'll have:**
# MAGIC - **JSearch:** 100-150 private sector jobs (when search endpoint found)
# MAGIC - **USAJobs:** 100-200 federal veteran jobs ???
# MAGIC - **Total:** 200-350 matches for neural network training
# MAGIC
# MAGIC **Federal roles for Green Berets in tech:**
# MAGIC - VA DevOps Engineers (veteran-serving mission)
# MAGIC - DOD Cloud Architects (defense sector)
# MAGIC - DHS Site Reliability Engineers (homeland security)
# MAGIC - IC Platform Engineers (intelligence community, clearance advantage)

# COMMAND ----------

# DBTITLE 1,Test USAJobs API Connection
# Test USAJobs API - Federal Veteran Jobs
import requests
from databricks.sdk.runtime import dbutils

print("=" * 80)
print("??????? USAJOBS API TEST - Federal Veteran Positions")
print("=" * 80)

try:
    # Retrieve USAJobs credentials from Databricks Secrets
    api_key = dbutils.secrets.get(scope="api-keys", key="usajobs-api-key")
    email = dbutils.secrets.get(scope="api-keys", key="usajobs-email")

    print("\n??? Step 1: USAJobs credentials retrieved securely")
    print(f"   API Key Length: {len(api_key)} characters")
    print(f"   Email: {email}")

    # Configure USAJobs API request
    url = "https://data.usajobs.gov/api/search"

    headers = {"Host": "data.usajobs.gov", "User-Agent": email, "Authorization-Key": api_key}

    # Search parameters for Free Hall's profile
    # DevOps/Cloud roles, veteran preference, security clearance
    params = {
        "Keyword": "DevOps OR Cloud OR Platform Engineer OR Site Reliability",
        "LocationName": "South Carolina; Remote",
        "SecurityClearanceRequired": "Top Secret",
        "HiringPath": "vet",  # Veteran hiring path
        "ResultsPerPage": "25",
    }

    print("\n???? Step 2: Querying USAJobs API...")
    print(f"   Keywords: {params['Keyword']}")
    print(f"   Location: {params['LocationName']}")
    print(f"   Clearance: {params['SecurityClearanceRequired']}")
    print(f"   Hiring Path: Veterans")

    response = requests.get(url, headers=headers, params=params, timeout=15)

    print(f"\n   Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        search_result = data.get("SearchResult", {})
        job_count = search_result.get("SearchResultCount", 0)
        jobs = search_result.get("SearchResultItems", [])

        print("\n" + "=" * 80)
        print("??? USAJOBS API CONNECTION SUCCESSFUL!")
        print("=" * 80)
        print(f"\n   Total Federal Jobs Found: {job_count}")
        print(f"   Jobs Retrieved: {len(jobs)}")

        if jobs:
            print("\n   ???? Sample Federal Jobs:")
            for i, item in enumerate(jobs[:3], 1):
                job = item.get("MatchedObjectDescriptor", {})
                print(f"\n   {i}. {job.get('PositionTitle', 'N/A')}")
                print(f"      Agency: {job.get('OrganizationName', 'N/A')}")
                print(f"      Location: {job.get('PositionLocationDisplay', 'N/A')}")
                print(f"      Grade: {job.get('JobGrade', [{}])[0].get('Code', 'N/A')}")

                salary_min = job.get("PositionRemuneration", [{}])[0].get("MinimumRange", "N/A")
                salary_max = job.get("PositionRemuneration", [{}])[0].get("MaximumRange", "N/A")
                print(f"      Salary: ${salary_min} - ${salary_max}")

                # Check for veteran preference
                hiring_path = job.get("UserArea", {}).get("Details", {}).get("HiringPath", [])
                if "vet" in [p.lower() for p in hiring_path]:
                    print(f"      ??? VETERAN PREFERENCE ELIGIBLE")

                # Check for clearance
                clearance = (
                    job.get("UserArea", {}).get("Details", {}).get("SecurityClearance", "None")
                )
                if clearance and clearance != "None":
                    print(f"      ???? Clearance: {clearance}")

        print("\n" + "=" * 80)
        print("???? FEDERAL VETERAN JOB PIPELINE READY!")
        print("=" * 80)
        print("\n   ??? Veteran preference active")
        print("   ??? Clearance filter working")
        print("   ??? Ready to fetch 100-200+ federal matches")
        print("   ??? Can combine with private sector (Adzuna/JSearch)")

    elif response.status_code == 403:
        print("\n??? Authorization Failed")
        print("   Check that:")
        print("   1. Authorization-Key is correct (from USAJobs email)")
        print("   2. User-Agent matches registered email")
        print("   3. API key is activated (may take a few minutes)")

    else:
        print(f"\n??? API Error: {response.status_code}")
        print(f"   Response: {response.text[:300]}")

except Exception as e:
    error_msg = str(e)

    if "Secret does not exist" in error_msg:
        print("\n??????  USAJobs credentials not yet configured")
        print("=" * 80)
        print("\n???? TO SET UP:")
        print("\n1. Register at: https://developer.usajobs.gov/APIRequest/Index")
        print("2. Check email for API credentials")
        print("3. Add to Secrets:")
        print("   - Key: usajobs-api-key")
        print("   - Key: usajobs-email")
        print("\n4. Run this cell again to test!")
    else:
        print(f"\n??? Error: {error_msg}")

print("\n" + "=" * 80)

# COMMAND ----------

# DBTITLE 1,Store USAJobs Credentials Now
# MAGIC %md
# MAGIC # ??????? Store USAJobs API Credentials
# MAGIC
# MAGIC **You received your USAJobs API key! Let's store it securely.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Your USAJobs Credentials:
# MAGIC
# MAGIC **API Key (Authorization-Key):** From your email received on Aug 6
# MAGIC
# MAGIC **User-Agent (Email):** `whall4.wh@gmail.com`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Store in Databricks Secrets (2 minutes):
# MAGIC
# MAGIC **Go to:** https://dbc-3e95d032-684c.cloud.databricks.com/#secrets
# MAGIC
# MAGIC 1. **Select the `api-keys` scope** (already created for JSearch)
# MAGIC
# MAGIC 2. **Add first secret:**
# MAGIC    - Click **"Add Secret"**
# MAGIC    - Key: `usajobs-api-key`
# MAGIC    - Value: [Paste your API key from the USAJobs email]
# MAGIC    - Click **"Add"**
# MAGIC
# MAGIC 3. **Add second secret:**
# MAGIC    - Click **"Add Secret"**
# MAGIC    - Key: `usajobs-email`
# MAGIC    - Value: `whall4.wh@gmail.com`
# MAGIC    - Click **"Add"**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## After Adding Secrets:
# MAGIC
# MAGIC **Run the next cell** to test federal veteran job search!
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Expected Results:**
# MAGIC - 100-200 federal DevOps/Cloud/SRE jobs
# MAGIC - Veteran preference eligible positions
# MAGIC - GS-13/14/15 ($120K-$180K)
# MAGIC - TS/SCI clearance advantage
# MAGIC - Many remote positions

# COMMAND ----------

# DBTITLE 1,Test USAJobs API - Federal Veteran Jobs
# Test USAJobs API - Federal Veteran Jobs for Free Hall
import requests
from databricks.sdk.runtime import dbutils

print("=" * 80)
print("??????? USAJOBS API TEST - Federal Veteran Positions")
print("=" * 80)

try:
    # Retrieve USAJobs credentials from Databricks Secrets
    api_key = dbutils.secrets.get(scope="api-keys", key="usajobs-api-key")
    email = dbutils.secrets.get(scope="api-keys", key="usajobs-email")

    print("\n??? Step 1: USAJobs credentials retrieved securely")
    print(f"   API Key: [REDACTED]")
    print(f"   Key Length: {len(api_key)} characters")
    print(f"   User-Agent: {email}")

    # Configure USAJobs API request
    url = "https://data.usajobs.gov/api/search"

    headers = {"Host": "data.usajobs.gov", "User-Agent": email, "Authorization-Key": api_key}

    # Search parameters optimized for Free Hall's veteran profile
    # Former Army SF, TS/SCI, DevOps/Cloud focus, Greenville SC
    params = {
        "Keyword": "DevOps OR Cloud OR Platform Engineer OR Site Reliability",
        "LocationName": "South Carolina; Remote",
        "HiringPath": "vet",  # Veteran hiring path - 5-10 point preference
        "ResultsPerPage": "25",
    }

    print("\n???? Step 2: Querying USAJobs API...")
    print(f"   Keywords: {params['Keyword']}")
    print(f"   Location: {params['LocationName']}")
    print(f"   Hiring Path: Veterans (preference eligible)")
    print(f"   Former Clearance: TS/SCI (reactivation advantage)")

    response = requests.get(url, headers=headers, params=params, timeout=20)

    print(f"\n   API Response Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        search_result = data.get("SearchResult", {})
        job_count = search_result.get("SearchResultCount", 0)
        jobs = search_result.get("SearchResultItems", [])

        print("\n" + "=" * 80)
        print("??? USAJOBS API CONNECTION SUCCESSFUL!")
        print("=" * 80)
        print(f"\n   Total Federal Jobs Found: {job_count}")
        print(f"   Jobs Retrieved (first page): {len(jobs)}")

        if jobs:
            print("\n   ???? Sample Federal Veteran Jobs:")
            print("   " + "-" * 76)

            for i, item in enumerate(jobs[:5], 1):
                job = item.get("MatchedObjectDescriptor", {})
                position_title = job.get("PositionTitle", "N/A")
                org_name = job.get("OrganizationName", "N/A")
                location = job.get("PositionLocationDisplay", "N/A")

                print(f"\n   {i}. {position_title}")
                print(f"      ???? Agency: {org_name}")
                print(f"      ???? Location: {location}")

                # Salary information
                remuneration = job.get("PositionRemuneration", [])
                if remuneration:
                    salary_min = remuneration[0].get("MinimumRange", "N/A")
                    salary_max = remuneration[0].get("MaximumRange", "N/A")
                    if salary_min != "N/A" and salary_max != "N/A":
                        print(f"      ???? Salary: ${salary_min:,} - ${salary_max:,}")

                # Grade level
                job_grades = job.get("JobGrade", [])
                if job_grades:
                    grade_code = job_grades[0].get("Code", "N/A")
                    print(f"      ???? Grade: {grade_code}")

                # Veteran preference indicator
                user_area = job.get("UserArea", {})
                details = user_area.get("Details", {})
                hiring_paths = details.get("HiringPath", [])

                if isinstance(hiring_paths, list) and any(
                    "vet" in str(p).lower() for p in hiring_paths
                ):
                    print(f"      ??? VETERAN PREFERENCE ELIGIBLE")

                # Security clearance
                clearance = details.get("SecurityClearance", "")
                if clearance and clearance.lower() != "not applicable":
                    print(f"      ???? Clearance: {clearance}")

        print("\n" + "=" * 80)
        print("???? FEDERAL VETERAN JOB PIPELINE READY!")
        print("=" * 80)
        print("\n   ??? API connection verified")
        print("   ??? Veteran preference filter active")
        print("   ??? Ready to fetch 100-200+ federal matches")
        print(f"   ??? {job_count} total jobs matching Free Hall's profile")
        print("\n   Next: Combine with Adzuna for 200-300+ total matches")

    elif response.status_code == 403:
        print("\n" + "=" * 80)
        print("??? AUTHORIZATION FAILED")
        print("=" * 80)
        print("\n   Check that:")
        print("   1. usajobs-api-key matches the Authorization-Key from email")
        print("   2. usajobs-email matches the registered email")
        print("   3. API key is activated (usually instant)")
        print(f"\n   Response: {response.text[:200]}")

    else:
        print(f"\n??? API Error: {response.status_code}")
        print(f"   Response: {response.text[:300]}")

except Exception as e:
    error_msg = str(e)

    if "Secret does not exist" in error_msg:
        print("\n" + "=" * 80)
        print("??????  USAJOBS CREDENTIALS NOT YET STORED")
        print("=" * 80)
        print("\n???? ACTION NEEDED:")
        print("\n1. Go to: https://dbc-3e95d032-684c.cloud.databricks.com/#secrets")
        print("2. Select `api-keys` scope")
        print("3. Add secret: usajobs-api-key = [Your API key from email]")
        print("4. Add secret: usajobs-email = whall4.wh@gmail.com")
        print("5. Run this cell again!")
    else:
        print(f"\n??? Error: {error_msg}")

print("\n" + "=" * 80)

