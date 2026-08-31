"""
01_vector_transformation.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # 1. Candidate Vector Transformation Engine
# MAGIC Transforms raw intake records into normalized 5D candidate feature vectors.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, FloatType

spark = SparkSession.builder.appName("FYS_Vector_Transform").getOrCreate()


def build_5d_vector(temporal, spatial, clearance, preference, modifier):
    return [
        float(temporal or 0.0),
        float(spatial or 0.0),
        float(clearance or 0.0),
        float(preference or 0.0),
        float(modifier or 0.0),
    ]


vector_udf = udf(build_5d_vector, ArrayType(FloatType()))

# Read raw landing payload
raw_df = spark.read.format("delta").load("gs://fys-landing-dev/sanitized_intake")

# Transform into normalized candidate feature vectors
vector_df = raw_df.withColumn(
    "candidate_vector",
    vector_udf(
        col("temporal_score"),
        col("spatial_score"),
        col("clearance_score"),
        col("preference_score"),
        col("modifier_score"),
    ),
)

# Write transformed vectors out to Delta stage
vector_df.write.format("delta").mode("overwrite").save("gs://fys-landing-dev/vectors")
print("Vector transformation pipeline executed successfully.")
