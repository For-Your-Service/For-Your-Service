"""
transform_silver.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Import SparkSession to manage the distributed DataFrame runtime environment.
from pyspark.sql import SparkSession

# Import specific built-in transformation and cryptographic functions from pyspark.sql.functions.
from pyspark.sql.functions import col, lit, current_timestamp, regexp_replace, sha2, concat_ws

def run_silver_transformation():
    # Initialize or retrieve the active Spark session for the Silver transformation pipeline.
    spark = SparkSession.builder.appName("ForYourService-SilverTransformation").getOrCreate()

    # Define the source path of the raw Bronze Delta table.
    bronze_table_path = "dbfs:/mnt/lakehouse/bronze/transactions"

    # Load the raw Bronze Delta table into a Spark DataFrame for processing.
    df_bronze = spark.read.format("delta").load(bronze_table_path)

    # Perform cleaning, deduplication, and PII masking transformations on the DataFrame.
    df_silver = df_bronze \
        .dropDuplicates(["record_id"]) \
        .withColumn("cleaned_content", regexp_replace(col("raw_content"), r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]")) \
        .withColumn("secure_hash", sha2(concat_ws("_", col("record_id"), col("source_system")), 256)) \
        .withColumn("processed_timestamp", current_timestamp())

    # Define the target Delta storage path for the Silver layer tables.
    silver_table_path = "dbfs:/mnt/lakehouse/silver/transactions"

    # Write the transformed, scrubbed records into the Silver Delta table using overwrite mode.
    df_silver.write.format("delta").mode("overwrite").save(silver_table_path)

    # Print a confirmation message indicating successful Silver tier processing.
    print(f"Successfully transformed records into Silver Delta table at {silver_table_path}")

if __name__ == "__main__":
    # Execute the silver transformation function when run directly.
    run_silver_transformation()
