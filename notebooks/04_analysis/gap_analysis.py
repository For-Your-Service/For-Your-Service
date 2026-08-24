# Databricks notebook source
# MAGIC %md
# MAGIC # Gap Analysis Dashboard
# MAGIC 
# MAGIC Analyze skill gaps across veteran population

# COMMAND ----------
from src.advice import GapAnalyzer

# COMMAND ----------
# Read resumes and jobs
resumes = spark.read.table("main.fys.silver_resumes")
jobs = spark.read.table("main.fys.silver_jobs")

# COMMAND ----------
# Compute gaps
analyzer = GapAnalyzer()

# Most common missing skills
display(
    spark.sql("""
        SELECT skill_name, COUNT(*) as candidates_missing
        FROM main.fys.skill_gaps
        WHERE required_by_job = true
        GROUP BY skill_name
        ORDER BY candidates_missing DESC
        LIMIT 20
    """)
)
