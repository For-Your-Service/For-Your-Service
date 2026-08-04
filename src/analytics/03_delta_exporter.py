# Databricks notebook source
# For Your Service (FYS) - Delta Lake Exporter
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number

spark = SparkSession.builder.appName("FYS_Delta_Exporter").getOrCreate()

results = spark.read.format("delta").load("gs://fys-landing-dev/match_results")

window_spec = Window.partitionBy("candidate_uuid").orderBy(col("match_score").desc())

top_matches = results.withColumn("rank", row_number().over(window_spec)).filter(col("rank") <= 5)

top_matches.write.format("delta").mode("overwrite").saveAsTable("fys_catalog.analytics.top_candidate_matches")