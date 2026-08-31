"""
02_tensor_dot_product.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # 2. Tensor Dot Product Matching Engine
# MAGIC Calculates placement probability score between Candidate Feature Vectors and Job Requirement Vectors.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder.appName("FYS_Tensor_Match").getOrCreate()

candidates = spark.read.format("delta").load("gs://fys-landing-dev/vectors")
jobs = spark.read.format("delta").load("gs://fys-landing-dev/job_vectors")

# Cross-join candidate vectors with open job vectors
matches = candidates.crossJoin(jobs)

# Compute dot product sum across all 5 dimensions
matched_df = matches.withColumn(
    "match_score",
    expr(
        "aggregate(zip_with(candidate_vector, job_vector, (x, y) -> x * y), 0.0f, (acc, x) -> acc + x)"
    ),
)

matched_df.write.format("delta").mode("overwrite").save("gs://fys-landing-dev/match_results")
print("Tensor matching matrix computed successfully.")
