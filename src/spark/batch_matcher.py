"""
File: src/spark/batch_matcher.py
Description: Distributed Batch Veteran Matching Engine using Apache Spark & Matrix Similarity
Scores batches of transitioning service members against all defense & civilian job embeddings in parallel.
"""

from typing import Optional, List, Dict
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession, DataFrame, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, BooleanType, 
    ArrayType, FloatType, IntegerType
)
from src.spark.embedding_pipeline import _generate_vector, EMBEDDING_DIM


# Schema for Veteran Intake Batch
VETERAN_INTAKE_SCHEMA = StructType([
    StructField("veteran_id", StringType(), False),
    StructField("full_name", StringType(), True),
    StructField("branch", StringType(), True),
    StructField("rank", StringType(), True),
    StructField("mos_code", StringType(), True),
    StructField("mos_title", StringType(), True),
    StructField("skills", ArrayType(StringType()), True),
    StructField("clearance_level", StringType(), True),
    StructField("target_city", StringType(), True),
    StructField("target_state", StringType(), True),
    StructField("remote_ok", BooleanType(), True)
])


class SparkBatchMatcher:
    """
    Spark-native distributed batch matching engine for military-to-civilian job placement.
    """

    def __init__(self, spark: Optional[SparkSession] = None):
        if spark is None:
            self.spark = (
                SparkSession.builder
                .appName("FYS-Batch-Matching-Engine")
                .master("local[*]")
                .config("spark.sql.shuffle.partitions", "4")
                .getOrCreate()
            )
        else:
            self.spark = spark

    @staticmethod
    def _cosine_similarity_udf(vec1: List[float], vec2: List[float]) -> float:
        """Calculate dot product / cosine similarity between two normalized vectors."""
        if not vec1 or not vec2:
            return 0.0
        v1 = np.asarray(vec1, dtype=np.float32)
        v2 = np.asarray(vec2, dtype=np.float32)
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        if n1 == 0 or n2 == 0:
            return 0.0
        dot = float(np.dot(v1, v2) / (n1 * n2))
        return max(0.0, min(1.0, dot))

    def match_batch(
        self, 
        veterans_df: DataFrame, 
        gold_jobs_df: DataFrame, 
        top_k: int = 5
    ) -> DataFrame:
        """
        Execute distributed matrix matching between all veterans and all Gold job postings.
        Returns Top-K scored matches per veteran with detailed scoring breakdown.
        """
        spark = self.spark

        # 1. Prepare Veteran Embedding representation
        vector_gen_udf = F.udf(_generate_vector, ArrayType(FloatType()))
        
        vets = (
            veterans_df
            .withColumn("skills_str", F.concat_ws(", ", F.coalesce(F.col("skills"), F.array())))
            .withColumn(
                "profile_text",
                F.concat_ws(
                    " | ",
                    F.col("branch"),
                    F.col("rank"),
                    F.col("mos_code"),
                    F.col("mos_title"),
                    F.col("skills_str"),
                    F.col("clearance_level")
                )
            )
            .withColumn("veteran_vector", vector_gen_udf(F.col("profile_text")))
        )

        # 2. Rename columns to avoid collisions during cross-join
        vets_sub = vets.select(
            F.col("veteran_id"),
            F.col("full_name"),
            F.col("branch"),
            F.col("mos_code"),
            F.col("clearance_level").alias("vet_clearance"),
            F.col("target_city").alias("vet_city"),
            F.col("target_state").alias("vet_state"),
            F.col("remote_ok").alias("vet_remote_ok"),
            F.col("veteran_vector")
        )

        jobs_sub = gold_jobs_df.select(
            F.col("job_id"),
            F.col("title").alias("job_title"),
            F.col("company"),
            F.col("city").alias("job_city"),
            F.col("state").alias("job_state"),
            F.col("remote_allowed"),
            F.col("required_clearance"),
            F.col("matched_mos_codes"),
            F.col("military_career_category"),
            F.col("salary_avg"),
            F.col("url"),
            F.col("embedding").alias("job_vector")
        )

        # 3. Distributed Cross Join & Neural Similarity Computation
        cos_sim_udf = F.udf(self._cosine_similarity_udf, DoubleType())

        # Join and compute base vector similarity
        paired = vets_sub.crossJoin(jobs_sub)
        paired = paired.withColumn(
            "neural_similarity",
            cos_sim_udf(F.col("veteran_vector"), F.col("job_vector"))
        )

        # 4. Multi-Factor Business Logic Scoring

        # A) Clearance Matching Boost
        clearance_boost = (
            F.when(
                (F.col("required_clearance") == "Top Secret / SCI") & 
                (F.col("vet_clearance").like("%Top Secret%")), 
                F.lit(1.15)
            )
            .when(
                (F.col("required_clearance") == "Secret") & 
                (F.col("vet_clearance").like("%Secret%")), 
                F.lit(1.10)
            )
            .when(F.col("required_clearance") == "None", F.lit(1.0))
            .otherwise(F.lit(0.85))  # Penalty if clearance requirement not met
        )

        # B) Geographic / Remote Match Boost
        location_boost = (
            F.when(
                (F.lower(F.col("vet_city")) == F.lower(F.col("job_city"))) & 
                (F.upper(F.col("vet_state")) == F.upper(F.col("job_state"))), 
                F.lit(1.15)
            )
            .when(
                (F.upper(F.col("vet_state")) == F.upper(F.col("job_state"))), 
                F.lit(1.08)
            )
            .when(
                (F.col("vet_remote_ok") == True) & (F.col("remote_allowed") == True), 
                F.lit(1.10)
            )
            .otherwise(F.lit(0.95))
        )

        # C) MOS Crosswalk Direct Alignment Boost
        mos_boost = (
            F.when(
                F.array_contains(F.col("matched_mos_codes"), F.col("mos_code")),
                F.lit(1.15)
            ).otherwise(F.lit(1.0))
        )

        # Combine into Composite Match Score
        scored = (
            paired
            .withColumn("clearance_multiplier", clearance_boost)
            .withColumn("location_multiplier", location_boost)
            .withColumn("mos_multiplier", mos_boost)
            .withColumn(
                "raw_score",
                F.col("neural_similarity") * 
                F.col("clearance_multiplier") * 
                F.col("location_multiplier") * 
                F.col("mos_multiplier")
            )
            .withColumn(
                "match_score_pct",
                F.round(F.least(F.lit(100.0), F.col("raw_score") * 100.0), 1)
            )
        )

        # 5. Generate Human-Readable Recommendation Summary
        summary_expr = F.concat_ws(
            " | ",
            F.concat(F.col("match_score_pct"), F.lit("% Match")),
            F.concat(F.lit("Category: "), F.col("military_career_category")),
            F.when(F.col("mos_multiplier") > 1.0, F.concat(F.lit("Direct MOS "), F.col("mos_code"), F.lit(" Alignment"))).otherwise(F.lit("Transferable Skill Match")),
            F.when(F.col("clearance_multiplier") > 1.0, F.lit("Security Clearance Verified")).otherwise(F.lit("Standard Clearance"))
        )
        scored = scored.withColumn("match_explanation", summary_expr)

        # 6. Rank Top-K Matches per Veteran
        window_spec = Window.partitionBy("veteran_id").orderBy(F.col("match_score_pct").desc())
        ranked = (
            scored
            .withColumn("rank", F.row_number().over(window_spec))
            .filter(F.col("rank") <= top_k)
            .select(
                "veteran_id",
                "full_name",
                "branch",
                "mos_code",
                "rank",
                "job_id",
                "job_title",
                "company",
                "job_city",
                "job_state",
                "remote_allowed",
                "required_clearance",
                "salary_avg",
                "match_score_pct",
                "match_explanation",
                "url"
            )
        )

        return ranked
