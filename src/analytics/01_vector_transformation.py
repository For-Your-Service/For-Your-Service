# Databricks notebook source
# For Your Service (FYS) - Vector Transformation Engine
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, FloatType

spark = SparkSession.builder.appName("FYS_Vector_Transform").getOrCreate()

def build_candidate_vector(temporal, spatial, clearance, preference, modifier):
    return [
        float(temporal or 0.0),
        float(spatial or 0.0),
        float(clearance or 0.0),
        float(preference or 0.0),
        float(modifier or 0.0)
    ]

vector_udf = udf(build_candidate_vector, ArrayType(FloatType()))

raw_df = spark.read.format("delta").load("gs://fys-landing-dev/sanitized_intake")

vector_df = raw_df.withColumn(
    "candidate_vector",
    vector_udf(
        col("temporal_score"),
        col("spatial_score"),
        col("clearance_score"),
        col("preference_score"),
        col("modifier_score")
    )
)

vector_df.write.format("delta").mode("overwrite").save("gs://fys-landing-dev/vectors")