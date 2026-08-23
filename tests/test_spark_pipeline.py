"""
File: tests/test_spark_pipeline.py
Description: Unit and integration tests for the Apache Spark Medallion Matching Pipeline.
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, BooleanType, ArrayType
)

from src.spark.bronze_to_silver_etl import BronzeToSilverPipeline
from src.spark.embedding_pipeline import SparkEmbeddingPipeline, EMBEDDING_DIM
from src.spark.batch_matcher import SparkBatchMatcher, VETERAN_INTAKE_SCHEMA
from src.spark.pipeline_orchestrator import SparkMedallionOrchestrator


@pytest.fixture(scope="session")
def spark_session():
    """Create a lightweight local SparkSession for testing."""
    spark = (
        SparkSession.builder
        .appName("FYS-Spark-Testing")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()


@pytest.fixture
def sample_bronze_jobs(spark_session):
    """Sample Bronze raw job postings representing different industries and defense requirements."""
    schema = StructType([
        StructField("job_id", StringType(), False),
        StructField("title", StringType(), False),
        StructField("company", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("description", StringType(), True),
        StructField("salary_min", DoubleType(), True),
        StructField("salary_max", DoubleType(), True),
        StructField("remote_allowed", BooleanType(), True)
    ])

    data = [
        (
            "job_01",
            "Senior Cloud Solutions Architect",
            "Lockheed Martin",
            "Greenville",
            "SC",
            "<p>Looking for an experienced Cloud Architect to manage AWS and Databricks. Top Secret clearance required. Operations leadership experience preferred.</p>",
            140000.0,
            185000.0,
            False
        ),
        (
            "job_02",
            "Cybersecurity SOC Analyst",
            "Raytheon Technologies",
            "Huntsville",
            "AL",
            "<div>Monitor SIEM alerts, incident response, network threat analysis. Secret clearance required. CompTIA Security+ or CISSP.</div>",
            90000.0,
            120000.0,
            True
        ),
        (
            "job_03",
            "Fleet Logistics & Warehouse Supervisor",
            "Boeing",
            "Charleston",
            "SC",
            "Oversee warehouse supply chain, inventory management, logistics distribution, DOT compliance.",
            75000.0,
            95000.0,
            False
        ),
        (
            "job_04",
            "Senior Cloud Solutions Architect",  # Duplicate to test deduplication
            "Lockheed Martin",
            "Greenville",
            "SC",
            "Duplicate posting",
            140000.0,
            185000.0,
            False
        )
    ]

    return spark_session.createDataFrame(data, schema)


@pytest.fixture
def sample_veterans(spark_session):
    """Sample transitioning veteran profiles."""
    data = [
        (
            "VET_001",
            "Free Hall",
            "Army",
            "E-8 | Master Sergeant",
            "18Z",
            "Special Forces Senior Sergeant",
            ["cloud architecture", "leadership", "operations research", "python", "databricks"],
            "Top Secret / SCI",
            "Greenville",
            "SC",
            True
        ),
        (
            "VET_002",
            "Marcus Vance",
            "Army",
            "E-6 | Staff Sergeant",
            "25D",
            "Cyber Network Defender",
            ["siem", "splunk", "wireshark", "incident response", "security+"],
            "Secret",
            "Huntsville",
            "AL",
            True
        ),
        (
            "VET_003",
            "Sarah Jenkins",
            "Army",
            "E-5 | Sergeant",
            "88M",
            "Motor Transport Operator",
            ["fleet management", "logistics", "route planning", "cargo safety"],
            "Secret",
            "Charleston",
            "SC",
            False
        )
    ]

    return spark_session.createDataFrame(data, VETERAN_INTAKE_SCHEMA)


def test_bronze_to_silver_pipeline(spark_session, sample_bronze_jobs):
    """Test data cleaning, HTML stripping, salary calculation, and MOS tagging."""
    pipeline = BronzeToSilverPipeline(spark_session)
    silver_df = pipeline.process(sample_bronze_jobs)

    # 1. Deduplication Check (4 rows down to 3)
    assert silver_df.count() == 3

    # 2. HTML Tag Stripping Check
    first_row = silver_df.filter(silver_df.job_id == "job_01").collect()[0]
    assert "<p>" not in first_row.description
    assert "</p>" not in first_row.description

    # 3. Clearance Detection Check
    assert first_row.required_clearance == "Top Secret / SCI"

    # 4. Salary Average Check
    assert first_row.salary_avg == 162500.0

    # 5. MOS Tagging Check
    assert len(first_row.matched_mos_codes) > 0


def test_embedding_pipeline(spark_session, sample_bronze_jobs):
    """Test distributed 384-dimensional vector embedding transformation."""
    etl = BronzeToSilverPipeline(spark_session)
    silver_df = etl.process(sample_bronze_jobs)

    embedding_pipeline = SparkEmbeddingPipeline(spark_session)
    gold_df = embedding_pipeline.transform(silver_df)

    rows = gold_df.collect()
    assert len(rows) == 3
    for r in rows:
        assert len(r.embedding) == EMBEDDING_DIM
        assert r.embedding_dim == EMBEDDING_DIM


def test_batch_matcher(spark_session, sample_bronze_jobs, sample_veterans):
    """Test distributed matrix matching, business rule weighting, and Top-K ranking."""
    etl = BronzeToSilverPipeline(spark_session)
    silver_df = etl.process(sample_bronze_jobs)

    embedding_pipeline = SparkEmbeddingPipeline(spark_session)
    gold_df = embedding_pipeline.transform(silver_df)

    matcher = SparkBatchMatcher(spark_session)
    matches_df = matcher.match_batch(sample_veterans, gold_df, top_k=2)

    # Each of 3 veterans should receive up to 2 matches (Total 6 rows)
    assert matches_df.count() == 6

    # Verify Veteran 1 (Free Hall, 18Z, TS/SCI, Greenville) matches with Lockheed Martin job in Greenville
    vet1_matches = matches_df.filter(matches_df.veteran_id == "VET_001").collect()
    assert len(vet1_matches) == 2
    assert vet1_matches[0].match_score_pct > 0.0
    assert "job_title" in matches_df.columns
    assert "match_explanation" in matches_df.columns


def test_end_to_end_orchestrator(spark_session, sample_bronze_jobs, sample_veterans):
    """Test full Medallion pipeline execution."""
    orchestrator = SparkMedallionOrchestrator(spark_session)
    result = orchestrator.run_full_pipeline(sample_bronze_jobs, sample_veterans, top_k_per_veteran=3)

    assert "silver_df" in result
    assert "gold_df" in result
    assert "matches_df" in result
    assert "metrics" in result
    assert result["metrics"]["total_raw_jobs_ingested"] == 4
    assert result["metrics"]["total_silver_jobs_cleaned"] == 3
    assert result["metrics"]["total_veterans_processed"] == 3
