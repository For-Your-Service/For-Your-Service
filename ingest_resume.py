from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
import json

# Initialize Spark Session with Delta Lake extensions and packages
spark = SparkSession.builder \
    .appName("FYS-Resume-Ingestion") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Load Pipeline Configuration
with open("pipeline_config.json", "r") as f:
    config = json.load(f)

resume_path = config["ResumeManifest"]
target_sector = config["TargetSector"]

# Read Resume Manifest into Spark DataFrame
resume_df = spark.read.text(resume_path) \
    .withColumn("SourceFile", lit(resume_path)) \
    .withColumn("TargetSector", lit(target_sector)) \
    .withColumn("IngestedAt", current_timestamp())

# Write to Bronze Tier Delta Table
resume_df.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable("fys_bronze.resume_ingestion_queue")

print(f"Successfully ingested {resume_path} into the Bronze layer for {target_sector}.")