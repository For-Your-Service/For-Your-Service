"""
03_delta_exporter.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # 3. Counselor Delta Exporter
# MAGIC Extracts top 5 job matches per candidate and stores in Delta Gold Layer.

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number

spark = SparkSession.builder.appName("FYS_Delta_Exporter").getOrCreate()

results = spark.read.format("delta").load("gs://fys-landing-dev/match_results")

# Partition by candidate to rank top 5 matching roles
window_spec = Window.partitionBy("candidate_uuid").orderBy(col("match_score").desc())

top_matches = results.withColumn("rank", row_number().over(window_spec)).filter(col("rank") <= 5)

# Save into Gold Delta Table for direct Counselor Dashboard querying
top_matches.write.format("delta").mode("overwrite").saveAsTable(
    "fys_catalog.analytics.top_candidate_matches"
)
print("Top candidate matches exported to fys_catalog.analytics.top_candidate_matches.")
