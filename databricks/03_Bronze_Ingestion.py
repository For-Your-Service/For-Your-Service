"""
03_Bronze_Ingestion.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# DBTITLE 1,Ingest from GCS using Auto Loader
from pyspark.sql.functions import current_timestamp, input_file_name
from pyspark.sql.types import *

print("="*70)
print("🥉 BRONZE INGESTION - VETERAN PROFILES")
print("="*70)

# GCS paths
gcs_source_path = "gs://fys-veteran-intake-raw/intake/"
checkpoint_path = "/tmp/fys_bronze_checkpoint"

print(f"\n📂 Source: {gcs_source_path}")
print(f"📝 Checkpoint: {checkpoint_path}")

# Note: GCS credentials need to be configured in cluster settings
# For now, this shows the ingestion pattern

print("\n⚠️  Note: GCS access requires service account credentials")
print("Configure in Databricks: Compute -> Advanced Options -> Spark Config")
print("Add: spark.hadoop.google.cloud.auth.service.account.json.keyfile /path/to/keyfile.json")

# Define expected schema (from anonymized profile)
expected_schema = StructType([
    StructField("veteran_id", StringType(), False),
    StructField("intake_id", StringType(), False),
    StructField("timestamp", StringType(), False),

    # Demographics (anonymized)
    StructField("demographics", StructType([
        StructField("birth_year", IntegerType()),
        StructField("age", IntegerType()),
        StructField("location", StructType([
            StructField("city", StringType()),
            StructField("state", StringType()),
            StructField("zip3", StringType()),
            StructField("country", StringType())
        ])),
        StructField("email_hash", StringType())
    ])),

    # Military service (nested struct)
    StructField("military_service", MapType(StringType(), StringType())),

    # Skills, education, certifications (arrays/maps)
    StructField("skills", MapType(StringType(), StringType())),
    StructField("education", ArrayType(MapType(StringType(), StringType()))),
    StructField("certifications", ArrayType(MapType(StringType(), StringType()))),

    # Job preferences
    StructField("job_preferences", MapType(StringType(), StringType())),

    # Transition info
    StructField("transition_info", MapType(StringType(), StringType())),

    # Metadata
    StructField("metadata", MapType(StringType(), StringType())),
    StructField("processing", MapType(StringType(), StringType()))
])

print("\n✅ Schema defined for Bronze ingestion")
print(f"\n🔑 Primary Key: veteran_id")
print(f"📅 Partitioned by: ingestion_date")

# COMMAND ----------

# DBTITLE 1,Create Bronze Delta Table
# For now, create the Bronze table structure
# Once GCS access is configured, uncomment the Auto Loader code below

from pyspark.sql.functions import current_date
from delta.tables import DeltaTable

print("="*70)
print("📍 CREATING BRONZE DELTA TABLE")
print("="*70)

table_name = "main.fys_bronze.veteran_profiles"

print(f"\n📦 Table: {table_name}")

# Check if table exists
try:
    existing_table = spark.table(table_name)
    print(f"\n✅ Table already exists with {existing_table.count()} records")
    display(existing_table.limit(5))
except:
    print(f"\n❗ Table does not exist yet")
    print("\nTo create it, we need either:")
    print("  1. GCS credentials configured to read from gs://fys-veteran-intake-raw/")
    print("  2. Or sample data uploaded for testing")

    # For now, show the Auto Loader pattern that will be used:
    print("\n" + "="*70)
    print("📝 AUTO LOADER PATTERN (When GCS is configured)")
    print("="*70)
    print("""
# Read from GCS using Auto Loader
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", checkpoint_path)
    .option("cloudFiles.inferColumnTypes", "true")
    .load(gcs_source_path)
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file", input_file_name())
    .withColumn("ingestion_date", current_date())
)

# Write to Bronze Delta table
(df.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .option("mergeSchema", "true")
    .partitionBy("ingestion_date")
    .trigger(availableNow=True)
    .table(table_name)
)
    """)

print("\n🚀 Next step: Configure GCS access or create sample data for testing")

# COMMAND ----------

# DBTITLE 1,For Your Service - Bronze Layer Ingestion
# MAGIC %md
# MAGIC # 🥉 For Your Service - Bronze Layer (Raw Ingestion)
# MAGIC
# MAGIC ## Purpose
# MAGIC Ingest anonymized veteran profiles from GCS into Unity Catalog Bronze Delta table.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Data Flow
# MAGIC ```
# MAGIC GCS: gs://fys-veteran-intake-raw/intake/*.json
# MAGIC         ↓
# MAGIC Spark Read JSON (Auto Loader)
# MAGIC         ↓
# MAGIC Bronze Delta Table: main.fys_bronze.veteran_profiles
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Bronze Layer Principles
# MAGIC - **No transformations** - Store raw anonymized JSON as-is
# MAGIC - **Full audit trail** - Capture ingestion metadata
# MAGIC - **Append-only** - Never delete, only add new records
# MAGIC - **Schema evolution** - Handle schema changes gracefully

# COMMAND ----------

# DBTITLE 1,Setup: Create Bronze Schema
# MAGIC %sql
# MAGIC -- Create the FYS Bronze schema in Unity Catalog
# MAGIC CREATE SCHEMA IF NOT EXISTS main.fys_bronze
# MAGIC COMMENT 'For Your Service - Bronze layer (raw anonymized veteran intake data)';
# MAGIC
# MAGIC -- Show schemas
# MAGIC SHOW SCHEMAS IN main LIKE 'fys*';

# COMMAND ----------

