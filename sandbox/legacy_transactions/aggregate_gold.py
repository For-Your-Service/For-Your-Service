# Import SparkSession to initialize the distributed processing context.
from pyspark.sql import SparkSession

# Import aggregation and date functions from pyspark.sql.functions to build metrics.
from pyspark.sql.functions import col, count, max, current_date

def run_gold_aggregations():
    # Initialize or retrieve the active Spark session for the Gold analytical pipeline.
    spark = SparkSession.builder.appName("ForYourService-GoldAggregations").getOrCreate()

    # Define the source path of the trusted Silver Delta table.
    silver_table_path = "dbfs:/mnt/lakehouse/silver/transactions"

    # Load cleaned records from the Silver Delta table into a Spark DataFrame.
    df_silver = spark.read.format("delta").load(silver_table_path)

    # Aggregate records by source system to compute business metrics and reporting summaries.
    df_gold = df_silver \
        .groupBy("source_system") \
        .agg(
            count("record_id").alias("total_transactions"),
            max("processed_timestamp").alias("latest_processed_time")
        ) \
        .withColumn("report_date", current_date())

    # Define the target Delta storage path for the Gold analytical layer.
    gold_table_path = "dbfs:/mnt/lakehouse/gold/transaction_summary"

    # Write the aggregated analytical metrics into the Gold Delta table using overwrite mode.
    df_gold.write.format("delta").mode("overwrite").save(gold_table_path)

    # Print a confirmation message indicating successful Gold tier aggregation.
    print(f"Successfully generated analytical metrics into Gold Delta table at {gold_table_path}")

if __name__ == "__main__":
    # Execute the gold aggregation function when run directly.
    run_gold_aggregations()
