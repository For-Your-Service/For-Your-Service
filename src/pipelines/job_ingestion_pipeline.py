"""
Job Data Ingestion Pipeline

Fetches jobs from APIs → UC Volume → Spark DataFrame → Delta Lake
Medallion Architecture: Bronze (raw) → Silver (cleaned) → Gold (matched)

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import requests
import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, current_timestamp, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import logging


logger = logging.getLogger(__name__)


class JobDataIngestionPipeline:
    """
    End-to-end job data pipeline
    
    Flow:
    1. Fetch from Adzuna/LinkedIn/Indeed APIs
    2. Stage raw JSON in UC Volume (/Volumes/main/default/job_data/raw)
    3. Load into Spark DataFrame
    4. Write to Bronze Delta table (raw)
    5. Transform to Silver (normalized)
    6. Match to Gold (veteran-specific matched jobs)
    """
    
    def __init__(
        self,
        volume_path: str = "/Volumes/main/default/job_data",
        catalog: str = "main",
        schema: str = "default"
    ):
        """
        Initialize pipeline
        
        Args:
            volume_path: UC Volume base path
            catalog: Unity Catalog name
            schema: Schema name
        """
        self.volume_path = volume_path
        self.raw_path = f"{volume_path}/raw"
        self.catalog = catalog
        self.schema = schema
        
        try:
            self.spark = SparkSession.builder.getOrCreate()
            self.spark.sql(f"USE CATALOG {catalog}")
            self.spark.sql(f"USE SCHEMA {schema}")
        except Exception as e:
            logger.warning(f"Spark session warning: {e}")
            self.spark = None
    
    def fetch_adzuna_jobs(
        self,
        app_id: str,
        app_key: str,
        keywords: str = "DevOps Engineer",
        location: str = "Greenville, SC",
        max_results: int = 50
    ) -> dict:
        """
        Fetch jobs from Adzuna API
        
        Args:
            app_id: Adzuna application ID
            app_key: Adzuna application key
            keywords: Job search terms
            location: Target location
            max_results: Max jobs to fetch
            
        Returns:
            API response with job results
        """
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": keywords,
            "where": location,
            "results_per_page": min(max_results, 50),
            "content-type": "application/json",
            "sort_by": "date",
            "max_days_old": 30
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            logger.info(f"Fetched {len(results)} jobs from Adzuna")
            
            return {
                "fetched_at": datetime.now().isoformat(),
                "source": "adzuna",
                "keywords": keywords,
                "location": location,
                "count": len(results),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Adzuna API error: {e}")
            return {
                "error": str(e),
                "results": [],
                "fetched_at": datetime.now().isoformat()
            }
    
    def save_to_volume(self, data: dict, filename: str = None) -> str:
        """
        Save raw JSON to UC Volume
        
        Args:
            data: Job data dictionary
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            source = data.get('source', 'unknown')
            location = data.get('location', '').replace(',', '').replace(' ', '_')
            filename = f"jobs_{source}_{location}_{timestamp}.json"
        
        # Ensure raw directory exists
        import os
        os.makedirs(self.raw_path, exist_ok=True)
        
        filepath = f"{self.raw_path}/{filename}"
        
        # Write JSON to UC Volume
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved to UC Volume: {filepath}")
        
        return filepath
    
    def load_from_volume_to_spark(self, pattern: str = "*.json"):
        """
        Load JSON files from UC Volume into Spark DataFrame
        
        Args:
            pattern: File pattern to match
            
        Returns:
            Spark DataFrame with job data
        """
        if not self.spark:
            raise RuntimeError("Spark session not available")
        
        path = f"{self.raw_path}/{pattern}"
        
        logger.info(f"Reading from UC Volume: {path}")
        
        # Read JSON files into Spark
        df = self.spark.read.json(path)
        
        count = df.count()
        logger.info(f"Loaded {count} records into Spark DataFrame")
        
        return df
    
    def write_bronze_table(
        self,
        df,
        table_name: str = "job_matching_bronze"
    ):
        """
        Write raw data to Bronze Delta table
        
        Args:
            df: Spark DataFrame
            table_name: Target table name
        """
        if not self.spark:
            raise RuntimeError("Spark session not available")
        
        try:
            # Add ingestion metadata
            df_with_meta = df.withColumn("ingested_at", current_timestamp())
            
            # Write to Delta Lake (append mode)
            full_table = f"{self.catalog}.{self.schema}.{table_name}"
            df_with_meta.write.mode("append").saveAsTable(full_table)
            
            logger.info(f"Written to Bronze table: {full_table}")
            
        except Exception as e:
            logger.error(f"Bronze write failed: {e}")
            raise
    
    def normalize_to_silver(
        self,
        bronze_table: str = "job_matching_bronze",
        silver_table: str = "job_matching_silver"
    ):
        """
        Transform Bronze → Silver (cleaned, normalized)
        
        Args:
            bronze_table: Source table
            silver_table: Target table
        """
        if not self.spark:
            raise RuntimeError("Spark session not available")
        
        try:
            full_bronze = f"{self.catalog}.{self.schema}.{bronze_table}"
            full_silver = f"{self.catalog}.{self.schema}.{silver_table}"
            
            # Read Bronze
            bronze_df = self.spark.table(full_bronze)
            
            # Explode results array
            if "results" in bronze_df.columns:
                jobs_df = bronze_df.select(
                    "fetched_at",
                    "source",
                    "keywords",
                    "location",
                    explode(col("results")).alias("job")
                )
                
                # Extract job fields
                silver_df = jobs_df.select(
                    col("fetched_at"),
                    col("source"),
                    col("keywords"),
                    col("location").alias("search_location"),
                    col("job.id").alias("job_id"),
                    col("job.title").alias("title"),
                    col("job.company.display_name").alias("company"),
                    col("job.location.display_name").alias("job_location"),
                    col("job.description").alias("description"),
                    col("job.salary_min").cast("int").alias("salary_min"),
                    col("job.salary_max").cast("int").alias("salary_max"),
                    col("job.redirect_url").alias("url"),
                    col("job.created").alias("posted_date"),
                    current_timestamp().alias("processed_at")
                )
                
                # Write to Silver
                silver_df.write.mode("append").saveAsTable(full_silver)
                
                logger.info(f"Normalized to Silver: {full_silver}")
                
        except Exception as e:
            logger.error(f"Silver transformation failed: {e}")
            raise
    
    def run_full_pipeline(
        self,
        adzuna_app_id: str,
        adzuna_app_key: str,
        keywords_list: list = None,
        locations: list = None
    ) -> dict:
        """
        Execute full ingestion pipeline
        
        Args:
            adzuna_app_id: Adzuna API ID
            adzuna_app_key: Adzuna API key
            keywords_list: List of job keywords
            locations: List of target locations
            
        Returns:
            Pipeline execution summary
        """
        if keywords_list is None:
            keywords_list = ["DevOps Engineer", "Cloud Engineer"]
        
        if locations is None:
            locations = ["Greenville, SC", "Remote"]
        
        summary = {
            "start_time": datetime.now().isoformat(),
            "jobs_fetched": 0,
            "files_saved": [],
            "errors": []
        }
        
        # Fetch from all combinations
        for keywords in keywords_list:
            for location in locations:
                try:
                    # Fetch from API
                    data = self.fetch_adzuna_jobs(
                        app_id=adzuna_app_id,
                        app_key=adzuna_app_key,
                        keywords=keywords,
                        location=location
                    )
                    
                    if data.get("results"):
                        # Save to UC Volume
                        filepath = self.save_to_volume(data)
                        summary["files_saved"].append(filepath)
                        summary["jobs_fetched"] += len(data["results"])
                    
                except Exception as e:
                    summary["errors"].append({
                        "keywords": keywords,
                        "location": location,
                        "error": str(e)
                    })
        
        # Load into Spark (if available)
        if self.spark and summary["jobs_fetched"] > 0:
            try:
                df = self.load_from_volume_to_spark()
                
                # Write to Bronze
                self.write_bronze_table(df)
                
                # Transform to Silver
                self.normalize_to_silver()
                
                summary["pipeline_status"] = "SUCCESS"
                
            except Exception as e:
                summary["pipeline_status"] = "FAILED"
                summary["errors"].append({
                    "stage": "spark_processing",
                    "error": str(e)
                })
        elif not self.spark:
            summary["pipeline_status"] = "PARTIAL_SUCCESS"
            summary["note"] = "Data saved to UC Volume, Spark processing skipped"
        
        summary["end_time"] = datetime.now().isoformat()
        
        return summary


def run_ingestion_demo():
    """Quick demo of pipeline"""
    pipeline = JobDataIngestionPipeline()
    
    # Demo with test credentials
    summary = pipeline.run_full_pipeline(
        adzuna_app_id="test",
        adzuna_app_key="test",
        keywords_list=["DevOps Engineer"],
        locations=["Greenville, SC"]
    )
    
    print("=" * 80)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 80)
    print(json.dumps(summary, indent=2))
    
    return pipeline


if __name__ == "__main__":
    run_ingestion_demo()
