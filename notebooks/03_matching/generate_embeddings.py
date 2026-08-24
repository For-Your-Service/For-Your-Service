# Databricks notebook source
# MAGIC %md
# MAGIC # Generate Resume Embeddings
# MAGIC 
# MAGIC Create vector embeddings for fast matching

# COMMAND ----------
from src.matching.two_stage import BiEncoder
import numpy as np

encoder = BiEncoder()

# COMMAND ----------
# Read Silver resumes
resumes = spark.read.table("main.fys.silver_resumes")

# COMMAND ----------
# Generate embeddings
def embed_resume_udf(text):
    return encoder.encode_candidate(text).tolist()

# COMMAND ----------
# Apply embedding
embeddings = resumes.withColumn("embedding", embed_resume_udf(F.col("resume_text")))

# COMMAND ----------
# Write to Gold
embeddings.write.format("delta").mode("overwrite").saveAsTable("main.fys.gold_resume_embeddings")
