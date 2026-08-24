"""
File: src/spark/bronze_to_silver_etl.py
Description: Apache Spark Bronze-to-Silver ETL Pipeline for For-Your-Service
Cleans raw job feeds (USAJOBS, JSearch, Adzuna) and enriches with Military MOS/AFSC/Rating taxonomy.
"""

from typing import Optional, List, Dict
import re
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, BooleanType,
    ArrayType, TimestampType, IntegerType
)

try:
    from app.mos_data import MOS_DATABASE
except ImportError:
    MOS_DATABASE = {}


# Define Silver Standard Schema
SILVER_JOB_SCHEMA = StructType([
    StructField("job_id", StringType(), False),
    StructField("source", StringType(), True),
    StructField("title", StringType(), False),
    StructField("company", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("location", StringType(), True),
    StructField("remote_allowed", BooleanType(), True),
    StructField("description", StringType(), True),
    StructField("cleaned_text", StringType(), True),
    StructField("salary_min", DoubleType(), True),
    StructField("salary_max", DoubleType(), True),
    StructField("salary_avg", DoubleType(), True),
    StructField("url", StringType(), True),
    StructField("required_clearance", StringType(), True),
    StructField("matched_mos_codes", ArrayType(StringType()), True),
    StructField("military_career_category", StringType(), True),
    StructField("ingest_timestamp", TimestampType(), True)
])


class BronzeToSilverPipeline:
    """
    Spark-native distributed data cleaning & MOS enrichment pipeline.
    """

    def __init__(self, spark: Optional[SparkSession] = None):
        if spark is None:
            self.spark = (
                SparkSession.builder
                .appName("FYS-BronzeToSilver-ETL")
                .master("local[*]")
                .config("spark.sql.shuffle.partitions", "4")
                .config("spark.driver.memory", "2g")
                .getOrCreate()
            )
        else:
            self.spark = spark

    @staticmethod
    def _clean_html_text(text: Optional[str]) -> str:
        """Strip HTML tags, formatting artifacts, and extra whitespace."""
        if not text:
            return ""
        # Remove HTML tags
        clean = re.sub(r"<[^>]+>", " ", str(text))
        # Remove excessive whitespace & special chars
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean

    @staticmethod
    def _extract_mos_matches(title: str, description: str) -> Dict[str, any]:
        """
        Scan job text against the military MOS crosswalk database.
        Returns matched MOS codes and primary career category.
        """
        combined = f"{title or ''} {description or ''}".lower()
        matched_codes = []
        categories = []

        for code, data in MOS_DATABASE.items():
            # Check for direct MOS code mention or civilian title match
            code_lower = code.lower()
            if f"mos {code_lower}" in combined or f" {code_lower} " in combined:
                matched_codes.append(code)
                categories.append(data.get("category", "General Defense"))
                continue

            for civ_title in data.get("civilian_titles", []):
                if civ_title.lower() in combined:
                    matched_codes.append(code)
                    categories.append(data.get("category", "General Defense"))
                    break

        # Fallback keyword categorization if no explicit MOS matched
        primary_category = categories[0] if categories else "General Technical & Operations"
        if not matched_codes:
            if any(k in combined for k in ["cyber", "security", "soc", "siem", "firewall"]):
                matched_codes = ["25D", "17C", "CTN", "0689"]
                primary_category = "Cybersecurity"
            elif any(k in combined for k in ["cloud", "devops", "aws", "azure", "kubernetes", "systems admin"]):
                matched_codes = ["25B", "IT", "1D7X1", "0671"]
                primary_category = "Information Technology & Cloud"
            elif any(k in combined for k in ["logistics", "supply", "warehouse", "freight", "transport"]):
                matched_codes = ["88M", "92A", "92Y", "LS", "0431"]
                primary_category = "Logistics & Supply Chain"
            elif any(k in combined for k in ["mechanic", "technician", "diesel", "aviation", "electrical"]):
                matched_codes = ["91B", "15T", "ET", "MM", "MK"]
                primary_category = "Maintenance & Mechanics"

        return {
            "matched_codes": list(set(matched_codes))[:5],
            "category": primary_category
        }

    def process(self, bronze_df: DataFrame) -> DataFrame:
        """
        Execute distributed data cleansing, schema standardization, deduplication, and MOS tagging.
        """
        spark = self.spark

        # Register UDFs
        clean_html_udf = F.udf(self._clean_html_text, StringType())

        mos_schema = StructType([
            StructField("matched_codes", ArrayType(StringType())),
            StructField("category", StringType())
        ])
        enrich_mos_udf = F.udf(self._extract_mos_matches, mos_schema)

        # Standardize field presence
        df = bronze_df
        cols = [c.lower() for c in df.columns]

        if "job_id" not in cols:
            df = df.withColumn("job_id", F.concat_ws("_", F.lit("job"), F.monotonically_increasing_id()))
        if "source" not in cols:
            df = df.withColumn("source", F.lit("multi_source_feed"))
        if "remote_allowed" not in cols:
            if "remote_option" in cols:
                df = df.withColumn("remote_allowed", F.col("remote_option").cast(BooleanType()))
            else:
                df = df.withColumn("remote_allowed", F.lit(False))
        if "salary_min" not in cols:
            df = df.withColumn("salary_min", F.lit(None).cast(DoubleType()))
        if "salary_max" not in cols:
            df = df.withColumn("salary_max", F.lit(None).cast(DoubleType()))
        if "required_clearance" not in cols:
            df = df.withColumn("required_clearance", F.lit("None"))

        # Clean strings and HTML
        df = (
            df.withColumn("title", F.trim(F.col("title")))
            .withColumn("company", F.trim(F.coalesce(F.col("company"), F.lit("Confidential"))))
            .withColumn("city", F.trim(F.coalesce(F.col("city"), F.lit("Greenville"))))
            .withColumn("state", F.upper(F.trim(F.coalesce(F.col("state"), F.lit("SC")))))
            .withColumn("description", clean_html_udf(F.coalesce(F.col("description"), F.lit(""))))
            .withColumn("location", F.concat_ws(", ", F.col("city"), F.col("state")))
        )

        # Calculate average salary
        df = df.withColumn(
            "salary_avg",
            F.when(
                (F.col("salary_min").isNotNull()) & (F.col("salary_max").isNotNull()),
                (F.col("salary_min") + F.col("salary_max")) / 2.0
            ).otherwise(F.coalesce(F.col("salary_min"), F.col("salary_max")))
        )

        # Create rich concatenated representation for downstream embeddings
        df = df.withColumn(
            "cleaned_text",
            F.concat_ws(
                " | ",
                F.col("title"),
                F.col("company"),
                F.col("location"),
                F.col("description")
            )
        )

        # Detect Security Clearance Requirements
        df = df.withColumn(
            "required_clearance",
            F.when(F.lower(F.col("cleaned_text")).like("%top secret%") | F.lower(F.col("cleaned_text")).like("%ts/sci%"), F.lit("Top Secret / SCI"))
            .when(F.lower(F.col("cleaned_text")).like("%secret%"), F.lit("Secret"))
            .otherwise(F.lit("None"))
        )

        # Apply MOS crosswalk enrichment
        df = df.withColumn("mos_meta", enrich_mos_udf(F.col("title"), F.col("description")))
        df = (
            df.withColumn("matched_mos_codes", F.col("mos_meta.matched_codes"))
            .withColumn("military_career_category", F.col("mos_meta.category"))
            .drop("mos_meta")
        )

        # Ingest timestamp
        df = df.withColumn("ingest_timestamp", F.current_timestamp())

        # Deduplicate on (title, company, city, state)
        df_deduped = df.dropDuplicates(["title", "company", "city", "state"])

        return df_deduped
