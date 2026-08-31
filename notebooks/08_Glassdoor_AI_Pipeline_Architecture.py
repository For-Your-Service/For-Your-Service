"""
08_Glassdoor_AI_Pipeline_Architecture.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# DBTITLE 1,🏗️ For Your Service - Glassdoor AI Assistant Architecture
# MAGIC %md
# MAGIC # 🏗️ For Your Service - Glassdoor AI Assistant Architecture
# MAGIC ## Dual-Cloud (AWS + GCP) + Databricks Vector Search + RAG Pipeline
# MAGIC
# MAGIC **Mission**: Replicate and enhance Glassdoor's AI career assistant specifically for veteran job matching.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Architecture Overview
# MAGIC
# MAGIC ```
# MAGIC ┌─────────────────────────────────────────────────────────────────┐
# MAGIC │                    GCP FREE TIER ($0/month)                      │
# MAGIC │  • Cloud Storage: Archive military career data (5 GB free)       │
# MAGIC │  • BigQuery: Analytics dashboard for 7 Eagle Group (1 TB/month)  │
# MAGIC └────────────────────────┬────────────────────────────────────────┘
# MAGIC                          │ Cross-Cloud Transfer
# MAGIC ┌────────────────────────▼────────────────────────────────────────┐
# MAGIC │                    AWS FREE TIER ($0/month)                      │
# MAGIC │  • S3: Hot staging bucket for daily job scrapes (5 GB free)      │
# MAGIC │  • IAM: Secure Databricks external location access              │
# MAGIC └────────────────────────┬────────────────────────────────────────┘
# MAGIC                          │ Auto Loader
# MAGIC ┌────────────────────────▼────────────────────────────────────────┐
# MAGIC │              DATABRICKS LAKEHOUSE (Unity Catalog)                │
# MAGIC │                                                                  │
# MAGIC │  Bronze → Silver → Gold + Vector Search                          │
# MAGIC │  ├─ MOS Translation Engine (RAG)                                 │
# MAGIC │  ├─ Security Clearance Matching                                  │
# MAGIC │  ├─ Semantic Job Embeddings (384-dim vectors)                    │
# MAGIC │  └─ LLM Orchestration (Glassdoor-style assistant)                │
# MAGIC └──────────────────────────────────────────────────────────────────┘
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Why This Matters for Veterans
# MAGIC
# MAGIC **Glassdoor's Limitation**: Generic skill matching ("Python developer" → "Python jobs")
# MAGIC
# MAGIC **For Your Service Enhancement**:
# MAGIC * **MOS Translation**: "18F Intelligence Sergeant" → DevOps + Python + Security + Leadership
# MAGIC * **Clearance Matching**: Former TS/SCI → jobs requiring Secret/Top Secret
# MAGIC * **Military Context**: Team Sergeant → Senior/Lead roles (not entry-level)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Pipeline Stages
# MAGIC
# MAGIC 1. **Bronze**: Raw job data from Indeed/LinkedIn/Adzuna
# MAGIC 2. **Silver**: MOS-enriched + clearance-tagged jobs
# MAGIC 3. **Gold**: Vector embeddings + semantic search index
# MAGIC 4. **RAG**: Context-aware veteran matching assistant
# MAGIC
# MAGIC **Let's build it step-by-step below.**

# COMMAND ----------

# DBTITLE 1,📦 Part 1: Dual-Cloud Setup (AWS + GCP)
# MAGIC %md
# MAGIC # 📦 Part 1: Dual-Cloud Setup (AWS + GCP)
# MAGIC
# MAGIC ## AWS S3 Configuration (Hot Staging)
# MAGIC
# MAGIC **Purpose**: Daily job scrape ingestion → Databricks Auto Loader
# MAGIC
# MAGIC ### Step 1: Create S3 Bucket
# MAGIC
# MAGIC ```bash
# MAGIC # Run this in AWS CLI or CloudShell
# MAGIC aws s3 mb s3://fys-job-staging-7eagle --region us-east-1
# MAGIC
# MAGIC # Enable versioning for data integrity
# MAGIC aws s3api put-bucket-versioning \
# MAGIC   --bucket fys-job-staging-7eagle \
# MAGIC   --versioning-configuration Status=Enabled
# MAGIC ```
# MAGIC
# MAGIC ### Step 2: IAM Role for Databricks External Location
# MAGIC
# MAGIC ```json
# MAGIC {
# MAGIC   "Version": "2012-10-17",
# MAGIC   "Statement": [
# MAGIC     {
# MAGIC       "Effect": "Allow",
# MAGIC       "Principal": {
# MAGIC         "AWS": "arn:aws:iam::414351767826:role/databricks-unity-catalog-role"
# MAGIC       },
# MAGIC       "Action": "sts:AssumeRole",
# MAGIC       "Condition": {
# MAGIC         "StringEquals": {
# MAGIC           "sts:ExternalId": "YOUR_DATABRICKS_WORKSPACE_ID"
# MAGIC         }
# MAGIC       }
# MAGIC     }
# MAGIC   ]
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC **Policy** (attach to role):
# MAGIC ```json
# MAGIC {
# MAGIC   "Version": "2012-10-17",
# MAGIC   "Statement": [
# MAGIC     {
# MAGIC       "Effect": "Allow",
# MAGIC       "Action": [
# MAGIC         "s3:GetObject",
# MAGIC         "s3:PutObject",
# MAGIC         "s3:DeleteObject",
# MAGIC         "s3:ListBucket"
# MAGIC       ],
# MAGIC       "Resource": [
# MAGIC         "arn:aws:s3:::fys-job-staging-7eagle",
# MAGIC         "arn:aws:s3:::fys-job-staging-7eagle/*"
# MAGIC       ]
# MAGIC     }
# MAGIC   ]
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## GCP Cloud Storage Configuration (Cold Archive)
# MAGIC
# MAGIC **Purpose**: Long-term storage for historical job data + MOS mappings
# MAGIC
# MAGIC ### Step 1: Create GCS Bucket
# MAGIC
# MAGIC ```bash
# MAGIC # Run in GCP Cloud Shell
# MAGIC gsutil mb -c STANDARD -l us-central1 gs://fys-military-data-archive/
# MAGIC
# MAGIC # Set lifecycle policy (auto-archive after 90 days)
# MAGIC echo '{
# MAGIC   "lifecycle": {
# MAGIC     "rule": [
# MAGIC       {
# MAGIC         "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
# MAGIC         "condition": {"age": 90}
# MAGIC       }
# MAGIC     ]
# MAGIC   }
# MAGIC }' > lifecycle.json
# MAGIC
# MAGIC gsutil lifecycle set lifecycle.json gs://fys-military-data-archive/
# MAGIC ```
# MAGIC
# MAGIC ### Step 2: Service Account for BigQuery Analytics
# MAGIC
# MAGIC ```bash
# MAGIC # Create service account for 7 Eagle Group analytics
# MAGIC gcloud iam service-accounts create fys-analytics \
# MAGIC   --display-name="For Your Service Analytics"
# MAGIC
# MAGIC # Grant BigQuery permissions
# MAGIC gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
# MAGIC   --member="serviceAccount:fys-analytics@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
# MAGIC   --role="roles/bigquery.dataViewer"
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Why This Split?
# MAGIC
# MAGIC | Cloud | Purpose | Cost | Databricks Integration |
# MAGIC |-------|---------|------|------------------------|
# MAGIC | **AWS S3** | Hot staging for daily scrapes | $0 (< 5GB) | Native Auto Loader |
# MAGIC | **GCP Storage** | Cold archive for historical data | $0 (< 5GB) | Manual export for analytics |
# MAGIC | **GCP BigQuery** | 7 Eagle Group dashboards | $0 (< 1TB queries/mo) | SQL federation or scheduled export |
# MAGIC
# MAGIC **Next**: Let's configure Databricks Unity Catalog external locations.

# COMMAND ----------

# DBTITLE 1,🔗 Configure Unity Catalog External Locations
# Configure Unity Catalog external locations for AWS S3 and GCP Storage

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import ExternalLocationInfo

print("="*70)
print("🔗 UNITY CATALOG EXTERNAL LOCATION SETUP")
print("="*70)

# NOTE: Run this ONCE to set up external locations
# You need workspace admin privileges

w = WorkspaceClient()

# AWS S3 External Location (Hot Staging)
print("\n📦 Creating AWS S3 External Location...")
try:
    aws_location = w.external_locations.create(
        name="fys_aws_staging",
        url="s3://fys-job-staging-7eagle/",
        credential_name="fys-aws-credential",  # Create this first in Unity Catalog UI
        comment="AWS S3 hot staging for daily job scrapes"
    )
    print(f"✅ AWS location created: {aws_location.name}")
except Exception as e:
    print(f"⚠️ AWS location may already exist: {e}")

# GCP Storage External Location (Cold Archive)
print("\n📦 Creating GCP Storage External Location...")
try:
    gcp_location = w.external_locations.create(
        name="fys_gcp_archive",
        url="gs://fys-military-data-archive/",
        credential_name="fys-gcp-credential",  # Create this first in Unity Catalog UI
        comment="GCP Storage cold archive for historical military data"
    )
    print(f"✅ GCP location created: {gcp_location.name}")
except Exception as e:
    print(f"⚠️ GCP location may already exist: {e}")

print("\n" + "="*70)
print("✅ External locations configured!")
print("="*70)
print("\n📚 Next Steps:")
print("   1. Verify credentials in Unity Catalog UI")
print("   2. Grant read/write permissions to your principal")
print("   3. Test access with: spark.read.json('s3://...')")

# COMMAND ----------

# DBTITLE 1,🧠 Part 2: MOS Translation Engine (Military → Civilian Skills)
# MAGIC %md
# MAGIC # 🧠 Part 2: MOS Translation Engine
# MAGIC ## Military Occupational Specialty → Civilian Skills Mapping
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## The Challenge
# MAGIC
# MAGIC **Military Job Titles Don't Match Civilian Searches**:
# MAGIC
# MAGIC * **18F Intelligence Sergeant** ≠ searches for "Intelligence Sergeant"
# MAGIC * **35T Military Intelligence Systems** ≠ searches for "Military Intelligence"
# MAGIC * **68W Combat Medic** ≠ searches for "Combat Medic"
# MAGIC
# MAGIC **They should match**:
# MAGIC * 18F → DevOps Engineer, Solutions Architect, Security Engineer
# MAGIC * 35T → Network Engineer, Systems Administrator, Cybersecurity Analyst
# MAGIC * 68W → Registered Nurse, Emergency Medical Technician, Healthcare Administrator
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Solution: RAG-Based MOS Translation
# MAGIC
# MAGIC ### Step 1: Build MOS Knowledge Base
# MAGIC
# MAGIC Create a Unity Catalog table with military occupation mappings:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE workspace.fys_gold.mos_translation_index (
# MAGIC   mos_code STRING COMMENT 'Military Occupational Specialty code (e.g., 18F, 35T)',
# MAGIC   branch STRING COMMENT 'Military branch: Army, Navy, Air Force, Marines, Coast Guard',
# MAGIC   title STRING COMMENT 'Official military job title',
# MAGIC   civilian_roles ARRAY<STRING> COMMENT 'Matching civilian job titles',
# MAGIC   core_skills ARRAY<STRING> COMMENT 'Transferable technical skills',
# MAGIC   soft_skills ARRAY<STRING> COMMENT 'Leadership, teamwork, problem-solving',
# MAGIC   clearance_level STRING COMMENT 'Typical clearance: TS/SCI, Secret, Confidential',
# MAGIC   seniority_mapping STRING COMMENT 'E1-E4=Junior, E5-E7=Mid, E8-E9=Senior, O1-O3=Mid, O4+=Senior',
# MAGIC   description STRING COMMENT 'Full operational description for embedding'
# MAGIC )
# MAGIC COMMENT 'Military to civilian skill translation knowledge base';
# MAGIC ```
# MAGIC
# MAGIC ### Step 2: Populate with Military Occupation Data
# MAGIC
# MAGIC **Example for Free Hall's background (18F Intelligence Sergeant)**:
# MAGIC
# MAGIC ```python
# MAGIC mos_data = [
# MAGIC     {
# MAGIC         "mos_code": "18F",
# MAGIC         "branch": "Army",
# MAGIC         "title": "Special Forces Intelligence Sergeant",
# MAGIC         "civilian_roles": [
# MAGIC             "DevOps Engineer",
# MAGIC             "Solutions Architect",
# MAGIC             "Cloud Engineer",
# MAGIC             "Site Reliability Engineer",
# MAGIC             "Security Engineer",
# MAGIC             "Intelligence Analyst"
# MAGIC         ],
# MAGIC         "core_skills": [
# MAGIC             "AWS", "Azure", "Kubernetes", "Docker", "Terraform",
# MAGIC             "Python", "Bash", "Jenkins", "CI/CD", "Linux Administration",
# MAGIC             "Network Security", "Intelligence Analysis", "SIGINT", "HUMINT"
# MAGIC         ],
# MAGIC         "soft_skills": [
# MAGIC             "Leadership", "Team Management", "Critical Thinking",
# MAGIC             "Problem Solving", "Adaptability", "Communication",
# MAGIC             "Cross-functional Collaboration", "Mission Planning"
# MAGIC         ],
# MAGIC         "clearance_level": "TS/SCI",
# MAGIC         "seniority_mapping": "E7-E8 (18 years) = Senior/Lead level",
# MAGIC         "description": """Special Forces Intelligence Sergeant (18F) responsible for
# MAGIC         intelligence collection, analysis, and dissemination in support of special
# MAGIC         operations. Manages tactical and strategic intelligence operations, oversees
# MAGIC         team of intelligence analysts, coordinates with joint/coalition forces,
# MAGIC         maintains TS/SCI clearance. Expert in SIGINT, HUMINT, geospatial intelligence,
# MAGIC         counterintelligence operations. Leads small teams in high-pressure, ambiguous
# MAGIC         environments requiring rapid decision-making and technical innovation."""
# MAGIC     }
# MAGIC ]
# MAGIC
# MAGIC # Insert into table
# MAGIC from pyspark.sql import Row
# MAGIC mos_df = spark.createDataFrame([Row(**x) for x in mos_data])
# MAGIC mos_df.write.mode("append").saveAsTable("workspace.fys_gold.mos_translation_index")
# MAGIC ```
# MAGIC
# MAGIC ### Step 3: Generate Vector Embeddings for MOS Descriptions
# MAGIC
# MAGIC **This enables semantic search**: "Former Special Forces Team Sergeant" → matches 18F embedding
# MAGIC
# MAGIC ```python
# MAGIC from sentence_transformers import SentenceTransformer
# MAGIC import numpy as np
# MAGIC
# MAGIC # Load embedding model
# MAGIC model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim vectors
# MAGIC
# MAGIC # Read MOS data
# MAGIC mos_df = spark.table("workspace.fys_gold.mos_translation_index").toPandas()
# MAGIC
# MAGIC # Generate embeddings from full descriptions
# MAGIC mos_embeddings = model.encode(mos_df['description'].tolist())
# MAGIC
# MAGIC # Add embeddings as new column
# MAGIC mos_df['embedding'] = list(mos_embeddings)
# MAGIC
# MAGIC # Write back to Delta table
# MAGIC spark.createDataFrame(mos_df).write.mode("overwrite").saveAsTable(
# MAGIC     "workspace.fys_gold.mos_embeddings"
# MAGIC )
# MAGIC
# MAGIC print(f"✅ Generated embeddings for {len(mos_df)} MOS codes")
# MAGIC ```
# MAGIC
# MAGIC **Next**: Let's create the RAG retrieval pipeline.

# COMMAND ----------

# DBTITLE 1,🔍 Part 3: Vector Search Setup (Databricks)
# Set up Databricks Vector Search for semantic job matching

from databricks.vector_search.client import VectorSearchClient

print("="*70)
print("🔍 DATABRICKS VECTOR SEARCH CONFIGURATION")
print("="*70)

# Initialize Vector Search client
vsc = VectorSearchClient()

print("\n📊 Step 1: Create Vector Search Endpoint...")
try:
    vsc.create_endpoint(
        name="fys_vector_search_endpoint",
        endpoint_type="STANDARD"  # Use SERVERLESS for production
    )
    print("✅ Endpoint created: fys_vector_search_endpoint")
except Exception as e:
    print(f"⚠️ Endpoint may already exist: {e}")

print("\n📊 Step 2: Create Vector Search Index for Jobs...")
try:
    # Index for job embeddings (what Glassdoor searches against)
    vsc.create_delta_sync_index(
        endpoint_name="fys_vector_search_endpoint",
        index_name="workspace.fys_gold.job_embeddings_index",
        source_table_name="workspace.fys_gold.job_embeddings",
        pipeline_type="TRIGGERED",  # Or CONTINUOUS for real-time
        primary_key="job_id",
        embedding_dimension=384,  # all-MiniLM-L6-v2 output dimension
        embedding_vector_column="embedding"
    )
    print("✅ Job embeddings index created")
except Exception as e:
    print(f"⚠️ Index may already exist: {e}")

print("\n📊 Step 3: Create Vector Search Index for MOS Translations...")
try:
    # Index for MOS embeddings (for veteran profile matching)
    vsc.create_delta_sync_index(
        endpoint_name="fys_vector_search_endpoint",
        index_name="workspace.fys_gold.mos_embeddings_index",
        source_table_name="workspace.fys_gold.mos_embeddings",
        pipeline_type="TRIGGERED",
        primary_key="mos_code",
        embedding_dimension=384,
        embedding_vector_column="embedding"
    )
    print("✅ MOS embeddings index created")
except Exception as e:
    print(f"⚠️ Index may already exist: {e}")

print("\n" + "="*70)
print("✅ Vector Search indexes configured!")
print("="*70)
print("\n📚 Index Status:")
print(f"   • Job Embeddings: workspace.fys_gold.job_embeddings_index")
print(f"   • MOS Translations: workspace.fys_gold.mos_embeddings_index")
print("\n🔄 To sync indexes:")
print("   vsc.get_index('workspace.fys_gold.job_embeddings_index').sync()")

# COMMAND ----------

# DBTITLE 1,🤖 Part 4: RAG Pipeline - Veteran Matching Function
# RAG Pipeline: Context-aware veteran job matching (Glassdoor-style)

from databricks.vector_search.client import VectorSearchClient
from sentence_transformers import SentenceTransformer
import pandas as pd

print("="*70)
print("🤖 RAG PIPELINE: VETERAN JOB MATCHING ASSISTANT")
print("="*70)

# Initialize components
vsc = VectorSearchClient()
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_veteran_to_jobs(veteran_profile: dict, top_k: int = 10) -> pd.DataFrame:
    """
    Glassdoor-style AI assistant for veteran job matching.

    Args:
        veteran_profile: Dict with keys:
            - name: str
            - mos_code: str (e.g., '18F')
            - years_experience: int
            - clearance_level: str (e.g., 'TS/SCI', 'Secret')
            - target_city: str
            - target_state: str
            - salary_min: int
            - salary_max: int
        top_k: Number of top matches to return

    Returns:
        DataFrame with ranked job matches and explanations
    """

    print(f"\n👤 Matching veteran: {veteran_profile['name']}")
    print(f"   📍 Location: {veteran_profile['target_city']}, {veteran_profile['target_state']}")
    print(f"   🎖️ MOS: {veteran_profile['mos_code']}")
    print(f"   🔐 Clearance: {veteran_profile['clearance_level']}")

    # Step 1: Look up MOS translation
    print("\n🔍 Step 1: Translating military experience to civilian skills...")

    mos_query = f"""{veteran_profile['mos_code']} {veteran_profile.get('military_branch', '')}
    {veteran_profile['years_experience']} years experience {veteran_profile['clearance_level']}"""

    mos_embedding = model.encode([mos_query])[0]

    # Search MOS translation index
    mos_results = vsc.get_index("workspace.fys_gold.mos_embeddings_index").similarity_search(
        query_vector=mos_embedding.tolist(),
        columns=["mos_code", "title", "civilian_roles", "core_skills", "clearance_level"],
        num_results=3
    )

    if mos_results and 'result' in mos_results and 'data_array' in mos_results['result']:
        top_mos = mos_results['result']['data_array'][0]
        civilian_roles = top_mos[2]  # civilian_roles column
        core_skills = top_mos[3]     # core_skills column
        print(f"✅ Matched MOS: {top_mos[1]}")
        print(f"   → Civilian roles: {', '.join(civilian_roles[:3])}")
    else:
        print("⚠️ No MOS match found, using generic profile")
        civilian_roles = ["Software Engineer", "DevOps Engineer"]
        core_skills = ["Python", "AWS", "Linux"]

    # Step 2: Build enriched veteran profile for embedding
    print("\n🧠 Step 2: Generating veteran profile embedding...")

    veteran_text = f"""
    Veteran Profile:
    - Name: {veteran_profile['name']}
    - Military Role: {top_mos[1] if mos_results else 'Unknown'}
    - Experience: {veteran_profile['years_experience']} years
    - Clearance: {veteran_profile['clearance_level']}
    - Skills: {', '.join(core_skills)}
    - Target Roles: {', '.join(civilian_roles)}
    - Location: {veteran_profile['target_city']}, {veteran_profile['target_state']}
    - Salary Range: ${veteran_profile['salary_min']:,} - ${veteran_profile['salary_max']:,}
    """

    veteran_embedding = model.encode([veteran_text])[0]

    # Step 3: Search job embeddings index
    print("\n🔍 Step 3: Searching {top_k} best matching jobs...")

    job_results = vsc.get_index("workspace.fys_gold.job_embeddings_index").similarity_search(
        query_vector=veteran_embedding.tolist(),
        columns=["job_id", "title", "company", "location", "salary_min", "salary_max",
                 "clearance_required", "description"],
        num_results=top_k * 3,  # Get extra for filtering
        filters={
            "location": f"{veteran_profile['target_city']}, {veteran_profile['target_state']}"
        }
    )

    # Step 4: Post-filter and rank
    print("\n🎯 Step 4: Applying clearance and salary filters...")

    if not job_results or 'result' not in job_results:
        print("❌ No jobs found matching criteria")
        return pd.DataFrame()

    jobs_df = pd.DataFrame(
        job_results['result']['data_array'],
        columns=["job_id", "title", "company", "location", "salary_min",
                 "salary_max", "clearance_required", "description", "similarity_score"]
    )

    # Filter by clearance (match or lower)
    clearance_hierarchy = {"None": 0, "Confidential": 1, "Secret": 2, "TS": 3, "TS/SCI": 4}
    veteran_clearance_level = clearance_hierarchy.get(veteran_profile['clearance_level'], 0)

    jobs_df['clearance_level'] = jobs_df['clearance_required'].map(
        lambda x: clearance_hierarchy.get(x, 0)
    )
    jobs_df = jobs_df[jobs_df['clearance_level'] <= veteran_clearance_level]

    # Filter by salary
    jobs_df = jobs_df[
        (jobs_df['salary_min'] >= veteran_profile['salary_min'] * 0.8) &  # Allow 20% below
        (jobs_df['salary_max'] <= veteran_profile['salary_max'] * 1.2)    # Allow 20% above
    ]

    # Take top K after filtering
    jobs_df = jobs_df.head(top_k)

    print(f"✅ Found {len(jobs_df)} matching jobs")

    # Step 5: Generate explanations (Glassdoor-style)
    print("\n📝 Step 5: Generating match explanations...")

    def generate_explanation(row):
        reasons = []
        if row['similarity_score'] > 0.85:
            reasons.append("🎯 Excellent semantic match to your military background")
        if row['clearance_required'] != "None":
            reasons.append(f"🔐 Utilizes your {veteran_profile['clearance_level']} clearance")
        if any(skill.lower() in row['description'].lower() for skill in core_skills[:5]):
            reasons.append("💡 Matches your core technical skills")
        if row['salary_min'] >= veteran_profile['salary_min']:
            reasons.append(f"💰 Meets salary target (${row['salary_min']:,} - ${row['salary_max']:,})")
        return " | ".join(reasons)

    jobs_df['match_explanation'] = jobs_df.apply(generate_explanation, axis=1)

    return jobs_df[['title', 'company', 'location', 'salary_min', 'salary_max',
                    'clearance_required', 'similarity_score', 'match_explanation']]

print("\n" + "="*70)
print("✅ RAG pipeline function ready!")
print("="*70)
print("\n📚 Usage:")
print("   results = match_veteran_to_jobs(veteran_profile, top_k=10)")
print("   display(results)")

# COMMAND ----------

# DBTITLE 1,🎯 Test RAG Pipeline with Free Hall Profile
# Test the RAG pipeline with Free Hall's veteran profile

print("="*70)
print("🎯 TESTING RAG PIPELINE - FREE HALL PROFILE")
print("="*70)

# Free Hall's veteran profile
free_hall_profile = {
    "name": "William Free Hall",
    "mos_code": "18F",
    "military_branch": "Army",
    "years_experience": 28,  # 18 military + 10 technical
    "clearance_level": "TS/SCI",
    "target_city": "Greenville",
    "target_state": "SC",
    "salary_min": 120000,
    "salary_max": 180000
}

print("\n👤 Veteran Profile:")
for key, value in free_hall_profile.items():
    print(f"   {key}: {value}")

print("\n" + "="*70)
print("🚀 Running RAG pipeline...")
print("="*70)

# Run the matching function
try:
    matches = match_veteran_to_jobs(free_hall_profile, top_k=10)

    if len(matches) > 0:
        print("\n" + "="*70)
        print("🏆 TOP 10 VETERAN JOB MATCHES")
        print("="*70)

        for idx, row in matches.iterrows():
            print(f"\n{idx + 1}. {row['title']} @ {row['company']}")
            print(f"   📍 {row['location']}")
            print(f"   💰 ${row['salary_min']:,} - ${row['salary_max']:,}")
            print(f"   🔐 Clearance: {row['clearance_required']}")
            print(f"   📊 Similarity: {row['similarity_score']:.2%}")
            print(f"   {row['match_explanation']}")
    else:
        print("\n⚠️ No matches found. Possible reasons:")
        print("   1. Vector search indexes need to be synced")
        print("   2. No jobs in target location (Greenville, SC)")
        print("   3. Job embeddings table is empty")
        print("\n💡 Run the Silver → Gold pipeline first to populate embeddings.")

except Exception as e:
    print(f"\n❌ Error running RAG pipeline: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("   1. Ensure vector search endpoint is RUNNING")
    print("   2. Check if indexes exist and are synced")
    print("   3. Verify source tables have data")
    print("   4. Run: vsc.list_indexes()")

# COMMAND ----------

# DBTITLE 1,🚀 Part 5: Production Deployment Checklist
# MAGIC %md
# MAGIC # 🚀 Part 5: Production Deployment Checklist
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Infrastructure Deployment Order
# MAGIC
# MAGIC ### Phase 1: Cloud Foundation (Week 1)
# MAGIC
# MAGIC - [ ] **AWS S3 Setup**
# MAGIC   - Create `fys-job-staging-7eagle` bucket
# MAGIC   - Configure IAM role for Databricks
# MAGIC   - Create Unity Catalog external location
# MAGIC   - Test write access from Databricks
# MAGIC
# MAGIC - [ ] **GCP Storage Setup**
# MAGIC   - Create `fys-military-data-archive` bucket
# MAGIC   - Set up lifecycle policy (90-day archive)
# MAGIC   - Create service account for BigQuery
# MAGIC   - Test cross-cloud transfer
# MAGIC
# MAGIC - [ ] **Unity Catalog Schema**
# MAGIC   ```sql
# MAGIC   CREATE SCHEMA IF NOT EXISTS workspace.fys_bronze COMMENT 'Raw job data ingestion';
# MAGIC   CREATE SCHEMA IF NOT EXISTS workspace.fys_silver COMMENT 'Cleaned and enriched jobs';
# MAGIC   CREATE SCHEMA IF NOT EXISTS workspace.fys_gold COMMENT 'Vector embeddings and indexes';
# MAGIC   ```
# MAGIC
# MAGIC ### Phase 2: Data Pipeline (Week 2)
# MAGIC
# MAGIC - [ ] **Bronze Layer**
# MAGIC   - Auto Loader from AWS S3 → `workspace.fys_bronze.job_postings`
# MAGIC   - Daily Indeed/LinkedIn/Adzuna scrapes
# MAGIC   - Schema enforcement and validation
# MAGIC
# MAGIC - [ ] **Silver Layer**
# MAGIC   - MOS translation table: `workspace.fys_gold.mos_translation_index`
# MAGIC   - Job enrichment pipeline (clearance tagging, seniority detection)
# MAGIC   - Deduplication and data quality checks
# MAGIC
# MAGIC - [ ] **Gold Layer**
# MAGIC   - Generate job embeddings: `workspace.fys_gold.job_embeddings`
# MAGIC   - Generate MOS embeddings: `workspace.fys_gold.mos_embeddings`
# MAGIC   - Create vector search indexes
# MAGIC
# MAGIC ### Phase 3: Vector Search & RAG (Week 3)
# MAGIC
# MAGIC - [ ] **Databricks Vector Search**
# MAGIC   - Create endpoint: `fys_vector_search_endpoint`
# MAGIC   - Sync job embeddings index
# MAGIC   - Sync MOS embeddings index
# MAGIC   - Performance testing (< 100ms query latency)
# MAGIC
# MAGIC - [ ] **RAG Pipeline**
# MAGIC   - Deploy `match_veteran_to_jobs()` function
# MAGIC   - Test with Free Hall profile
# MAGIC   - Test with 5 additional veteran profiles
# MAGIC   - Validate match quality (precision/recall)
# MAGIC
# MAGIC ### Phase 4: API & Frontend (Week 4)
# MAGIC
# MAGIC - [ ] **Databricks SQL Endpoint**
# MAGIC   - Create serverless SQL warehouse
# MAGIC   - Grant 7 Eagle Group access
# MAGIC   - Set up query federation (if using BigQuery dashboards)
# MAGIC
# MAGIC - [ ] **API Layer** (Optional - for web UI)
# MAGIC   - Databricks REST API or Flask wrapper
# MAGIC   - Authentication (OAuth2 or API keys)
# MAGIC   - Rate limiting
# MAGIC
# MAGIC - [ ] **Hugging Face Spaces Deployment** (FREE tier)
# MAGIC   - Gradio UI for veteran job search
# MAGIC   - Connect to Databricks SQL endpoint
# MAGIC   - Deploy at: https://huggingface.co/spaces/7-eagle-group/for-your-service
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Cost Monitoring
# MAGIC
# MAGIC | Component | Monthly Cost | Notes |
# MAGIC |-----------|--------------|-------|
# MAGIC | **AWS S3** | $0 | < 5 GB free tier |
# MAGIC | **GCP Storage** | $0 | < 5 GB free tier |
# MAGIC | **GCP BigQuery** | $0 | < 1 TB queries/month |
# MAGIC | **Databricks Compute** | $0 - $50 | Use serverless SQL (pay-per-query) |
# MAGIC | **Databricks Vector Search** | $0 - $100 | STANDARD endpoint (vs $600/mo for SERVERLESS) |
# MAGIC | **Hugging Face Spaces** | $0 | FREE tier (persistent) |
# MAGIC | **TOTAL** | **$0 - $150/month** | Target: < $100/month |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Success Metrics
# MAGIC
# MAGIC **Technical KPIs**:
# MAGIC * Vector search latency: < 100ms
# MAGIC * Job match relevance: > 80% precision @ top 10
# MAGIC * MOS translation accuracy: > 90% (validated by 7 Eagle Group)
# MAGIC * Pipeline uptime: > 99%
# MAGIC
# MAGIC **Business KPIs** (7 Eagle Group):
# MAGIC * Veteran placements: Track via dashboard
# MAGIC * Time-to-match: Reduce from weeks → hours
# MAGIC * Veteran satisfaction: Survey after placement
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Next Steps
# MAGIC
# MAGIC 1. **Run this notebook** to set up the RAG pipeline
# MAGIC 2. **Scrape Greenville, SC jobs** (replace Houston test data)
# MAGIC 3. **Populate MOS translation table** with 50+ military occupations
# MAGIC 4. **Test with 10 veteran profiles** (not just Free Hall)
# MAGIC 5. **Deploy to Hugging Face Spaces** for 7 Eagle Group demo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **🎖️ For Your Service - Powered by Databricks + AWS + GCP**

# COMMAND ----------

