# Databricks notebook source
# For Your Service (FYS) - Tensor Dot Product Matching Engine
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

spark = SparkSession.builder.appName("FYS_Tensor_Match").getOrCreate()

candidates = spark.read.format("delta").load("gs://fys-landing-dev/vectors")
jobs = spark.read.format("delta").load("gs://fys-landing-dev/job_vectors")

matches = candidates.crossJoin(jobs)

matched_df = matches.withColumn(
    "match_score",
    expr("aggregate(zip_with(candidate_vector, job_vector, (x, y) -> x * y), 0.0f, (acc, x) -> acc + x)")
)

matched_df.write.format("delta").mode("overwrite").save("gs://fys-landing-dev/match_results")