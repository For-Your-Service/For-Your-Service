# Databricks notebook source
# MAGIC %md
# MAGIC # Resume Ingestion Pipeline
# MAGIC 
# MAGIC Ingest uploaded resumes into Bronze table

# COMMAND ----------
from src.resume_parsing import ResumeParser
import pyspark.sql.functions as F

parser = ResumeParser()

# COMMAND ----------
# Read uploaded files from volume
files = spark.read.format("binaryFile").load("/Volumes/main/fys/resumes/")

# COMMAND ----------
# Parse each resume
def parse_resume_udf(content):
    try:
        return parser.parse_bytes(content)
    except Exception as e:
        return None

# COMMAND ----------
# Apply parsing
parsed = files.withColumn("parsed", parse_resume_udf(F.col("content")))

# COMMAND ----------
# Write to Bronze
parsed.write.format("delta").mode("append").saveAsTable("main.fys.bronze_resumes")
