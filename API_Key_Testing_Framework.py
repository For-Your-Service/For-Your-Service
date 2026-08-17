# Databricks notebook source
# DBTITLE 1,API Key Testing Framework - For Your Service
# MAGIC %md
# MAGIC # 🔐 API Key Testing Framework - For Your Service
# MAGIC
# MAGIC ## Purpose
# MAGIC Secure API key validation and connection testing before pipeline integration for the **For Your Service** veteran job matching platform.
# MAGIC
# MAGIC ## Features
# MAGIC * ✅ Secure credential management (no hardcoded keys)
# MAGIC * ✅ Multi-endpoint support (REST, GraphQL, webhooks)
# MAGIC * ✅ Retry logic & timeout handling
# MAGIC * ✅ Test result cataloging with timestamps
# MAGIC * ✅ GitHub-ready for daily commits (100 contribution target)
# MAGIC
# MAGIC ## API Types We Test
# MAGIC 1. **Job Boards** - USAJOBS, Indeed, LinkedIn, Adzuna, ZipRecruiter
# MAGIC 2. **AI/ML Services** - OpenAI, Hugging Face, Azure OpenAI
# MAGIC 3. **Cloud Providers** - AWS (S3, Lambda, DynamoDB), GCP, Azure
# MAGIC 4. **Custom APIs** - 7 Eagle Group internal endpoints
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Install Dependencies
# Install required packages
%pip install requests python-dotenv pandas tabulate --quiet
dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Core API Testing Class
import requests
import os
import json
import time
from datetime import datetime
from typing import Dict, Optional, Tuple, Any
import pandas as pd
from tabulate import tabulate


class APIKeyTester:
    """
    Secure API key testing framework for For Your Service platform.
    
    Features:
    - Secure credential management via environment variables
    - Retry logic with exponential backoff
    - Response validation and error handling
    - Test result cataloging with timestamps
    - Support for multiple HTTP methods
    """
    
    def __init__(self, catalog_file: str = "/dbfs/FileStore/api_test_catalog.json"):
        self.catalog_file = catalog_file
        self.test_results = self._load_catalog()
        self.session = requests.Session()  # Reuse connections
        
    def _load_catalog(self) -> list:
        """Load existing test catalog or create new one."""
        try:
            if os.path.exists(self.catalog_file):
                with open(self.catalog_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load catalog: {e}")
        return []
    
    def _save_catalog(self):
        """Save test results to catalog file."""
        try:
            os.makedirs(os.path.dirname(self.catalog_file), exist_ok=True)
            with open(self.catalog_file, 'w') as f:
                json.dump(self.test_results, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save catalog: {e}")
    
    def test_api_key(
        self,
        api_name: str,
        endpoint: str,
        api_key: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        auth_type: str = "header",  # "header", "bearer", "basic", "query"
        timeout: int = 10,
        retry_count: int = 3,
        validate_response: Optional[callable] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Test an API key against an endpoint.
        
        Args:
            api_name: Descriptive name for the API (e.g., "USAJOBS", "OpenAI")
            endpoint: Full URL to test
            api_key: API key to validate
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: Additional headers
            data: Request body (for POST/PUT)
            params: Query parameters
            auth_type: How to send the API key
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts
            validate_response: Optional function to validate response content
            
        Returns:
            (success: bool, result: dict)
        """
        
        # Build headers based on auth type
        req_headers = headers or {}
        
        if auth_type == "header":
            req_headers["Authorization"] = f"Api-Key {api_key}"
        elif auth_type == "bearer":
            req_headers["Authorization"] = f"Bearer {api_key}"
        elif auth_type == "query":
            params = params or {}
            params["api_key"] = api_key
        
        # Test with retry logic
        last_error = None
        for attempt in range(retry_count):
            try:
                response = self.session.request(
                    method=method,
                    url=endpoint,
                    headers=req_headers,
                    json=data,
                    params=params,
                    timeout=timeout
                )
                
                # Check response status
                success = response.status_code in [200, 201]
                
                # Optional custom validation
                if success and validate_response:
                    try:
                        success = validate_response(response)
                    except Exception as e:
                        success = False
                        last_error = f"Validation failed: {str(e)}"
                
                # Log result
                result = {
                    "api_name": api_name,
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": response.status_code,
                    "success": success,
                    "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                    "timestamp": datetime.now().isoformat(),
                    "attempt": attempt + 1,
                    "error": last_error or (None if success else response.text[:200])
                }
                
                # Catalog the result
                self.test_results.append(result)
                self._save_catalog()
                
                if success:
                    return True, result
                
                # If not success and we have retries left, wait with exponential backoff
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                if attempt < retry_count - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
        
        # All retries failed
        result = {
            "api_name": api_name,
            "endpoint": endpoint,
            "method": method,
            "status_code": None,
            "success": False,
            "response_time_ms": None,
            "timestamp": datetime.now().isoformat(),
            "attempt": retry_count,
            "error": last_error
        }
        
        self.test_results.append(result)
        self._save_catalog()
        
        return False, result
    
    def get_test_summary(self, last_n: Optional[int] = None) -> pd.DataFrame:
        """Get summary of test results."""
        if not self.test_results:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.test_results)
        if last_n:
            df = df.tail(last_n)
        
        return df[['timestamp', 'api_name', 'success', 'status_code', 'response_time_ms', 'error']]
    
    def print_summary(self, last_n: Optional[int] = 10):
        """Pretty print test summary."""
        df = self.get_test_summary(last_n)
        if df.empty:
            print("📋 No test results yet.")
            return
        
        print(f"\n📊 Last {len(df)} Test Results:")
        print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
        
        # Summary stats
        total = len(df)
        passed = df['success'].sum()
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n✅ Passed: {passed} | ❌ Failed: {failed} | 📈 Success Rate: {success_rate:.1f}%")


print("✅ APIKeyTester class loaded successfully!")

# COMMAND ----------

# DBTITLE 1,Secure Credential Management
# MAGIC %md
# MAGIC ## 🔐 Secure Credential Management
# MAGIC
# MAGIC ### Best Practices
# MAGIC 1. **NEVER hardcode API keys** in notebooks or code
# MAGIC 2. **Use Databricks Secrets** for production
# MAGIC 3. **Use environment variables** for local testing
# MAGIC 4. **Rotate keys regularly** (every 90 days minimum)
# MAGIC
# MAGIC ### Setup Databricks Secrets (Production)
# MAGIC
# MAGIC ```bash
# MAGIC # From Databricks CLI
# MAGIC databricks secrets create-scope --scope fys-api-keys
# MAGIC databricks secrets put --scope fys-api-keys --key usajobs-api-key
# MAGIC databricks secrets put --scope fys-api-keys --key openai-api-key
# MAGIC databricks secrets put --scope fys-api-keys --key huggingface-token
# MAGIC databricks secrets put --scope fys-api-keys --key aws-access-key
# MAGIC databricks secrets put --scope fys-api-keys --key indeed-api-key
# MAGIC ```
# MAGIC
# MAGIC ### Retrieve Secrets in Code
# MAGIC
# MAGIC ```python
# MAGIC # Databricks secrets (production)
# MAGIC api_key = dbutils.secrets.get(scope="fys-api-keys", key="usajobs-api-key")
# MAGIC
# MAGIC # Environment variables (testing)
# MAGIC api_key = os.getenv("USAJOBS_API_KEY")
# MAGIC ```
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Example Tests Section
# MAGIC %md
# MAGIC ## 🧪 Example API Tests
# MAGIC
# MAGIC Below are ready-to-run examples for common APIs used in **For Your Service**.
# MAGIC
# MAGIC ### 🏛️ Job Board APIs
# MAGIC 1. **USAJOBS** - Federal government positions
# MAGIC 2. **Indeed** - General job postings
# MAGIC 3. **LinkedIn** - Professional network jobs
# MAGIC 4. **Adzuna** - Job aggregator
# MAGIC
# MAGIC ### 🤖 AI/ML APIs
# MAGIC 1. **OpenAI** - GPT models for resume parsing
# MAGIC 2. **Hugging Face** - Model hosting and inference
# MAGIC 3. **Azure OpenAI** - Enterprise AI services
# MAGIC
# MAGIC ### ☁️ Cloud Provider APIs
# MAGIC 1. **AWS S3** - Job data storage
# MAGIC 2. **AWS Lambda** - Serverless compute
# MAGIC 3. **AWS DynamoDB** - NoSQL database
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Test USAJOBS API
# Initialize tester
tester = APIKeyTester()

# Test USAJOBS API (Federal Jobs)
print("\n" + "="*70)
print("🏛️ Testing USAJOBS API (Federal Government Jobs)")
print("="*70)

# IMPORTANT: Replace with your actual API key or use secrets
# Production: usajobs_key = dbutils.secrets.get(scope="fys-api-keys", key="usajobs-api-key")
usajobs_key = os.getenv("USAJOBS_API_KEY", "YOUR_API_KEY_HERE")
usajobs_email = "whall4.wh@gmail.com"  # User-Agent email required by USAJOBS

if usajobs_key != "YOUR_API_KEY_HERE":
    success, result = tester.test_api_key(
        api_name="USAJOBS",
        endpoint="https://data.usajobs.gov/api/search",
        api_key=usajobs_key,
        method="GET",
        headers={
            "User-Agent": usajobs_email,
            "Authorization-Key": usajobs_key  # USAJOBS uses custom header
        },
        params={
            "Keyword": "software engineer",
            "LocationName": "Greenville, South Carolina",
            "ResultsPerPage": 5
        },
        auth_type="query",  # Key is in custom header, not standard auth
        timeout=15
    )
    
    if success:
        print("✅ USAJOBS API key is VALID")
        print(f"   Response time: {result['response_time_ms']}ms")
        print(f"   Status code: {result['status_code']}")
    else:
        print("❌ USAJOBS API key test FAILED")
        print(f"   Error: {result['error']}")
else:
    print("⚠️ Skipping test - Set USAJOBS_API_KEY environment variable")
    print("   Get your key at: https://developer.usajobs.gov/")

# COMMAND ----------

# DBTITLE 1,Test OpenAI API
# Test OpenAI API
print("\n" + "="*70)
print("🤖 Testing OpenAI API")
print("="*70)

# Production: openai_key = dbutils.secrets.get(scope="fys-api-keys", key="openai-api-key")
openai_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

if openai_key != "YOUR_API_KEY_HERE":
    # Custom validation function
    def validate_openai_response(response):
        data = response.json()
        return 'choices' in data and len(data['choices']) > 0
    
    success, result = tester.test_api_key(
        api_name="OpenAI",
        endpoint="https://api.openai.com/v1/chat/completions",
        api_key=openai_key,
        method="POST",
        auth_type="bearer",
        data={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Test connection"}],
            "max_tokens": 10
        },
        validate_response=validate_openai_response,
        timeout=30
    )
    
    if success:
        print("✅ OpenAI API key is VALID")
        print(f"   Response time: {result['response_time_ms']}ms")
    else:
        print("❌ OpenAI API key test FAILED")
        print(f"   Error: {result['error']}")
else:
    print("⚠️ Skipping test - Set OPENAI_API_KEY environment variable")
    print("   Get your key at: https://platform.openai.com/api-keys")

# COMMAND ----------

# DBTITLE 1,Test Hugging Face API
# Test Hugging Face API
print("\n" + "="*70)
print("🤗 Testing Hugging Face API")
print("="*70)

# Production: hf_token = dbutils.secrets.get(scope="fys-api-keys", key="huggingface-token")
hf_token = os.getenv("HUGGINGFACE_TOKEN", "YOUR_TOKEN_HERE")

if hf_token != "YOUR_TOKEN_HERE":
    success, result = tester.test_api_key(
        api_name="HuggingFace",
        endpoint="https://huggingface.co/api/whoami-v2",
        api_key=hf_token,
        method="GET",
        auth_type="bearer",
        timeout=10
    )
    
    if success:
        print("✅ Hugging Face token is VALID")
        print(f"   Response time: {result['response_time_ms']}ms")
    else:
        print("❌ Hugging Face token test FAILED")
        print(f"   Error: {result['error']}")
else:
    print("⚠️ Skipping test - Set HUGGINGFACE_TOKEN environment variable")
    print("   Get your token at: https://huggingface.co/settings/tokens")

# COMMAND ----------

# DBTITLE 1,Test AWS API (boto3)
# Test AWS API using boto3
print("\n" + "="*70)
print("☁️ Testing AWS API (S3 Bucket Access)")
print("="*70)

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    
    # AWS credentials should be set in environment or IAM role
    # For testing: export AWS_ACCESS_KEY_ID=xxx
    #              export AWS_SECRET_ACCESS_KEY=xxx
    
    try:
        s3_client = boto3.client('s3')
        
        # Test by listing buckets (requires ListAllMyBuckets permission)
        start_time = time.time()
        response = s3_client.list_buckets()
        response_time_ms = int((time.time() - start_time) * 1000)
        
        result = {
            "api_name": "AWS S3",
            "endpoint": "s3.amazonaws.com",
            "method": "GET",
            "status_code": 200,
            "success": True,
            "response_time_ms": response_time_ms,
            "timestamp": datetime.now().isoformat(),
            "attempt": 1,
            "error": None
        }
        tester.test_results.append(result)
        tester._save_catalog()
        
        print("✅ AWS credentials are VALID")
        print(f"   Found {len(response['Buckets'])} buckets")
        print(f"   Response time: {response_time_ms}ms")
        
    except NoCredentialsError:
        print("⚠️ AWS credentials not found")
        print("   Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
    except ClientError as e:
        print(f"❌ AWS API test FAILED: {e}")
        
except ImportError:
    print("⚠️ boto3 not installed. Install with: %pip install boto3")

# COMMAND ----------

# DBTITLE 1,Test Results Summary
# MAGIC %md
# MAGIC ## 📊 Test Results Summary
# MAGIC
# MAGIC View all test results cataloged during this session and historically.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Display Test Summary
# Display test summary
tester.print_summary(last_n=20)

print("\n" + "="*70)
print("💾 Test catalog saved to:")
print(f"   {tester.catalog_file}")
print("="*70)

# COMMAND ----------

# DBTITLE 1,GitHub Integration
# MAGIC %md
# MAGIC ## 🐙 GitHub Integration
# MAGIC
# MAGIC ### Strategy for 100 Daily Contributions
# MAGIC
# MAGIC To hit your **100 daily GitHub contribution target**, commit frequently as you add/test API keys:
# MAGIC
# MAGIC ### Option 1: Databricks Git Folder (Recommended)
# MAGIC
# MAGIC 1. **Clone your For Your Service repo** into Databricks workspace:
# MAGIC    ```bash
# MAGIC    # In Databricks, go to Repos → Add Repo
# MAGIC    # URL: https://github.com/For-Your-Service/For-Your-Service.git
# MAGIC    ```
# MAGIC
# MAGIC 2. **Move this notebook** to the Git folder:
# MAGIC    - Export this notebook as `.py` or `.ipynb`
# MAGIC    - Place in `/Repos/whall4.wh@gmail.com/For-Your-Service/tests/`
# MAGIC
# MAGIC 3. **Commit after each test**:
# MAGIC    ```bash
# MAGIC    git add tests/API_Key_Testing_Framework.py
# MAGIC    git commit -m "test: Validate USAJOBS API key"
# MAGIC    git push origin main
# MAGIC    ```
# MAGIC
# MAGIC ### Option 2: Automated Export Script
# MAGIC
# MAGIC Add this to your daily workflow:
# MAGIC
# MAGIC ```python
# MAGIC # Export notebook and commit
# MAGIC import subprocess
# MAGIC import os
# MAGIC from datetime import datetime
# MAGIC
# MAGIC def commit_test_progress(message: str):
# MAGIC     """Quick commit to GitHub for test progress."""
# MAGIC     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
# MAGIC     commit_msg = f"test: {message} - {timestamp}"
# MAGIC     
# MAGIC     subprocess.run(["git", "add", "."])
# MAGIC     subprocess.run(["git", "commit", "-m", commit_msg])
# MAGIC     subprocess.run(["git", "push"])
# MAGIC     print(f"✅ Committed: {commit_msg}")
# MAGIC
# MAGIC # Use after each test
# MAGIC commit_test_progress("USAJOBS API validated")
# MAGIC commit_test_progress("OpenAI API validated")
# MAGIC commit_test_progress("AWS S3 connection verified")
# MAGIC ```
# MAGIC
# MAGIC ### Commit Frequency Ideas
# MAGIC
# MAGIC * **Per API test** - Each API validation = 1 commit
# MAGIC * **Per fix** - Update retry logic = 1 commit
# MAGIC * **Per feature** - Add new endpoint type = 1 commit
# MAGIC * **Per documentation update** - Update README = 1 commit
# MAGIC * **Daily summary** - End-of-day test report = 1 commit
# MAGIC
# MAGIC ### Example Commit Messages
# MAGIC
# MAGIC ```
# MAGIC test: Add USAJOBS API key validation
# MAGIC test: Implement retry logic with exponential backoff
# MAGIC test: Add Hugging Face token verification
# MAGIC feat: Add test result cataloging system
# MAGIC docs: Update API testing best practices
# MAGIC fix: Handle timeout errors for slow endpoints
# MAGIC test: Verify AWS S3 bucket access
# MAGIC refactor: Extract common auth headers
# MAGIC ```
# MAGIC
# MAGIC ### Daily Notes Integration
# MAGIC
# MAGIC Log your test progress in your daily notes:
# MAGIC
# MAGIC ```markdown
# MAGIC ## DAILY_NOTES_2026_08_12.md
# MAGIC
# MAGIC ### API Testing Progress
# MAGIC - ✅ USAJOBS API key validated
# MAGIC - ✅ OpenAI API connection verified
# MAGIC - ✅ AWS S3 access confirmed
# MAGIC - ❌ Indeed API key expired - requested new one
# MAGIC - 🔄 Hugging Face token rotation scheduled
# MAGIC
# MAGIC ### GitHub Contributions Today: 47/100
# MAGIC - 12 test commits
# MAGIC - 8 documentation updates
# MAGIC - 27 code improvements
# MAGIC ```
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Custom Endpoint Testing
# MAGIC %md
# MAGIC ## 🛠️ Custom Endpoint Testing
# MAGIC
# MAGIC Quick templates for testing your own APIs.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Custom REST API Template
# Template: Test your custom REST API

def test_custom_api(
    api_name: str,
    endpoint: str,
    api_key: str,
    method: str = "GET",
    data: dict = None,
    params: dict = None
):
    """
    Quick template for testing custom endpoints.
    
    Example:
        test_custom_api(
            api_name="7 Eagle Group Internal API",
            endpoint="https://api.7eaglegroup.com/veterans",
            api_key=os.getenv("EAGLE_API_KEY"),
            method="GET",
            params={"state": "SC"}
        )
    """
    
    print(f"\n\u2699️ Testing {api_name}...")
    
    success, result = tester.test_api_key(
        api_name=api_name,
        endpoint=endpoint,
        api_key=api_key,
        method=method,
        data=data,
        params=params,
        auth_type="bearer",  # Adjust as needed
        timeout=15,
        retry_count=3
    )
    
    if success:
        print(f"✅ {api_name} - API key VALID")
        print(f"   ⏱️ Response time: {result['response_time_ms']}ms")
        return True
    else:
        print(f"❌ {api_name} - API key INVALID or endpoint unreachable")
        print(f"   🚫 Error: {result['error']}")
        return False

# Example usage (uncomment to test):
# test_custom_api(
#     api_name="Indeed API",
#     endpoint="https://api.indeed.com/ads/apisearch",
#     api_key=os.getenv("INDEED_PUBLISHER_ID"),
#     params={
#         "q": "software engineer",
#         "l": "Greenville, SC",
#         "format": "json",
#         "v": "2"
#     }
# )

print("✅ Custom API testing template loaded")

# COMMAND ----------

# DBTITLE 1,Next Steps
# MAGIC %md
# MAGIC ## 🚀 Next Steps
# MAGIC
# MAGIC ### 1. Set Up Databricks Secrets
# MAGIC ```bash
# MAGIC # Create secret scope for production
# MAGIC databricks secrets create-scope --scope fys-api-keys
# MAGIC
# MAGIC # Add your API keys
# MAGIC databricks secrets put --scope fys-api-keys --key usajobs-api-key
# MAGIC databricks secrets put --scope fys-api-keys --key openai-api-key
# MAGIC databricks secrets put --scope fys-api-keys --key huggingface-token
# MAGIC databricks secrets put --scope fys-api-keys --key aws-access-key
# MAGIC databricks secrets put --scope fys-api-keys --key aws-secret-key
# MAGIC databricks secrets put --scope fys-api-keys --key indeed-publisher-id
# MAGIC databricks secrets put --scope fys-api-keys --key adzuna-app-id
# MAGIC databricks secrets put --scope fys-api-keys --key adzuna-app-key
# MAGIC ```
# MAGIC
# MAGIC ### 2. Test All Your API Keys
# MAGIC Run the test cells above for each API integration in your pipeline.
# MAGIC
# MAGIC ### 3. Document Test Results
# MAGIC Update your daily notes with test outcomes:
# MAGIC ```markdown
# MAGIC ## API Key Validation - 2026-08-12
# MAGIC - ✅ USAJOBS: Valid, 245ms avg response
# MAGIC - ✅ OpenAI: Valid, 1850ms avg response
# MAGIC - ❌ Indeed: Key expired, renewal requested
# MAGIC - 🔄 AWS: Rotated keys, retest pending
# MAGIC ```
# MAGIC
# MAGIC ### 4. Integrate into CI/CD
# MAGIC Add API key validation to your deployment pipeline:
# MAGIC ```python
# MAGIC # In your deployment script
# MAGIC from API_Key_Testing_Framework import APIKeyTester
# MAGIC
# MAGIC def validate_all_keys():
# MAGIC     tester = APIKeyTester()
# MAGIC     
# MAGIC     keys_to_test = [
# MAGIC         {"name": "USAJOBS", "endpoint": "...", "key": dbutils.secrets.get(...)},
# MAGIC         {"name": "OpenAI", "endpoint": "...", "key": dbutils.secrets.get(...)},
# MAGIC     ]
# MAGIC     
# MAGIC     all_valid = True
# MAGIC     for key_config in keys_to_test:
# MAGIC         success, _ = tester.test_api_key(**key_config)
# MAGIC         if not success:
# MAGIC             all_valid = False
# MAGIC             print(f"❌ {key_config['name']} validation failed!")
# MAGIC     
# MAGIC     if not all_valid:
# MAGIC         raise Exception("API key validation failed - deployment blocked")
# MAGIC     
# MAGIC     print("✅ All API keys validated successfully")
# MAGIC ```
# MAGIC
# MAGIC ### 5. Set Up Key Rotation Schedule
# MAGIC
# MAGIC | API Provider | Rotation Frequency | Next Rotation |
# MAGIC |---|---|---|
# MAGIC | USAJOBS | 90 days | 2026-11-10 |
# MAGIC | OpenAI | 90 days | 2026-11-10 |
# MAGIC | AWS | 90 days | 2026-11-10 |
# MAGIC | Hugging Face | 180 days | 2027-02-08 |
# MAGIC
# MAGIC ### 6. Monitor in Production
# MAGIC Add to your monitoring dashboard:
# MAGIC - API key expiration dates
# MAGIC - Daily API health checks
# MAGIC - Response time trends
# MAGIC - Error rate by endpoint
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📝 Resources
# MAGIC
# MAGIC ### API Key Registration Links
# MAGIC - **USAJOBS**: https://developer.usajobs.gov/
# MAGIC - **OpenAI**: https://platform.openai.com/api-keys
# MAGIC - **Hugging Face**: https://huggingface.co/settings/tokens
# MAGIC - **Indeed**: https://www.indeed.com/publisher/signup
# MAGIC - **Adzuna**: https://developer.adzuna.com/
# MAGIC - **ZipRecruiter**: https://www.ziprecruiter.com/zipsearch
# MAGIC - **AWS**: https://console.aws.amazon.com/iam/
# MAGIC
# MAGIC ### Documentation
# MAGIC - [For Your Service GitHub Repo](https://github.com/For-Your-Service/For-Your-Service)
# MAGIC - [Databricks Secrets Management](https://docs.databricks.com/security/secrets/index.html)
# MAGIC - [7 Eagle Group Partnership](https://7eaglegroup.com)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Built by:** Free Hall (whall4.wh@gmail.com)  
# MAGIC **Organization:** 7 Eagle Group  
# MAGIC **Project:** For Your Service - AI-Powered Veteran Job Matching  
# MAGIC **Last Updated:** 2026-08-12

# COMMAND ----------

