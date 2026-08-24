"""
File: src/spark/pipeline_orchestrator.py
Description: End-to-End Apache Spark Medallion Pipeline Orchestrator for For-Your-Service
Executes: Bronze Feed Ingest -> Silver MOS ETL -> Gold Embeddings -> Batch Matcher & Metrics.
"""

from typing import Optional, Dict, Any
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

from src.spark.bronze_to_silver_etl import BronzeToSilverPipeline
from src.spark.embedding_pipeline import SparkEmbeddingPipeline
from src.spark.batch_matcher import SparkBatchMatcher, VETERAN_INTAKE_SCHEMA


class SparkMedallionOrchestrator:
    """
    Unified coordinator for the Apache Spark / Delta Lake Medallion Pipeline.
    """

    def __init__(self, spark: Optional[SparkSession] = None):
        if spark is None:
            self.spark = (
                SparkSession.builder
                .appName("FYS-Spark-Medallion-Orchestrator")
                .master("local[*]")
                .config("spark.sql.shuffle.partitions", "4")
                .config("spark.driver.memory", "2g")
                .getOrCreate()
            )
        else:
            self.spark = spark

        self.bronze_to_silver = BronzeToSilverPipeline(self.spark)
        self.embedding_pipeline = SparkEmbeddingPipeline(self.spark)
        self.matcher = SparkBatchMatcher(self.spark)

    def run_full_pipeline(
        self,
        bronze_jobs_df: DataFrame,
        veterans_df: DataFrame,
        top_k_per_veteran: int = 5
    ) -> Dict[str, Any]:
        """
        Execute the end-to-end Medallion data flow:
        1. Bronze -> Silver (Cleaning + MOS Crosswalk Tagging)
        2. Silver -> Gold (384-Dim Distributed Neural Embeddings)
        3. Gold + Veterans -> Batch Matches (Distributed Top-K Matrix Similarity)
        4. Metrics Aggregation
        """
        print("\n🚀 [STAGE 1/3] Running Bronze -> Silver ETL (Cleaning & MOS Tagging)...")
        silver_df = self.bronze_to_silver.process(bronze_jobs_df)
        silver_count = silver_df.count()
        print(f"✅ Silver Layer Processed: {silver_count} sanitized job records.")

        print("\n⚡ [STAGE 2/3] Running Silver -> Gold Vector Embedding Generation...")
        gold_df = self.embedding_pipeline.transform(silver_df)
        gold_count = gold_df.count()
        print(f"✅ Gold Layer Processed: {gold_count} vector embedding records.")

        print("\n🎯 [STAGE 3/3] Running Distributed Batch Veteran Matching Engine...")
        matches_df = self.matcher.match_batch(
            veterans_df=veterans_df,
            gold_jobs_df=gold_df,
            top_k=top_k_per_veteran
        )
        matches_count = matches_df.count()
        print(f"✅ Batch Matching Complete: {matches_count} Top-{top_k_per_veteran} job pairings generated.")

        # Aggregate Executive Summary Metrics
        metrics = {
            "total_raw_jobs_ingested": bronze_jobs_df.count(),
            "total_silver_jobs_cleaned": silver_count,
            "total_gold_embedded_jobs": gold_count,
            "total_veterans_processed": veterans_df.count(),
            "total_ranked_matches": matches_count,
            "avg_top_match_score": matches_df.select(F.avg("match_score_pct")).collect()[0][0] or 0.0
        }

        return {
            "silver_df": silver_df,
            "gold_df": gold_df,
            "matches_df": matches_df,
            "metrics": metrics
        }
