"""
normalize_skills.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# MAGIC %md
# MAGIC # Skill Normalization Pipeline
# MAGIC 
# MAGIC Normalize skills from Bronze to Silver

# COMMAND ----------
from src.taxonomy import SkillNormalizer
import pyspark.sql.functions as F

normalizer = SkillNormalizer()

# COMMAND ----------
# Read Bronze resumes
bronze = spark.read.table("main.fys.bronze_resumes")

# COMMAND ----------
# Normalize skills
def normalize_skills_udf(skills):
    return normalizer.normalize_list(skills)

# COMMAND ----------
# Apply normalization
silver = bronze.withColumn("normalized_skills", normalize_skills_udf(F.col("skills")))

# COMMAND ----------
# Write to Silver
silver.write.format("delta").mode("overwrite").saveAsTable("main.fys.silver_resumes")
