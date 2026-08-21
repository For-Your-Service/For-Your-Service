#!/usr/bin/env python3
"""Generate comprehensive data quality report"""

from datetime import datetime


def generate_report(spark):
    """Generate data quality metrics"""

    report = {"report_date": datetime.now().isoformat(), "period": "Last 7 days", "metrics": {}}

    # Total records
    total_df = spark.sql("""
        SELECT COUNT(*) as total
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
    """)
    report["metrics"]["total_records"] = total_df.collect()[0]["total"]

    # Completeness checks
    completeness_df = spark.sql("""
        SELECT
          ROUND(100.0 * SUM(CASE WHEN title IS NOT NULL AND title != '' THEN 1 ELSE 0 END) / COUNT(*), 2) as title_completeness,
          ROUND(100.0 * SUM(CASE WHEN company IS NOT NULL AND company != '' THEN 1 ELSE 0 END) / COUNT(*), 2) as company_completeness,
          ROUND(100.0 * SUM(CASE WHEN salary.min IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as salary_completeness,
          ROUND(100.0 * SUM(CASE WHEN description IS NOT NULL AND description != '' THEN 1 ELSE 0 END) / COUNT(*), 2) as description_completeness
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
    """)

    completeness = completeness_df.collect()[0].asDict()
    report["metrics"]["completeness"] = completeness

    # Duplicate check
    duplicate_df = spark.sql("""
        SELECT COUNT(*) - COUNT(DISTINCT job_id) as duplicates
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
    """)
    report["metrics"]["duplicates"] = duplicate_df.collect()[0]["duplicates"]

    # Source breakdown
    source_df = spark.sql("""
        SELECT source, COUNT(*) as count
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
        GROUP BY source
    """)
    report["metrics"]["by_source"] = {row["source"]: row["count"] for row in source_df.collect()}

    # Overall quality score
    avg_completeness = sum(completeness.values()) / len(completeness)
    duplicate_rate = report["metrics"]["duplicates"] / report["metrics"]["total_records"] * 100
    quality_score = avg_completeness * (1 - duplicate_rate / 100)

    report["quality_score"] = round(quality_score, 2)
    report["status"] = "PASS" if quality_score >= 75 else "FAIL"

    return report


if __name__ == "__main__":
    print("Data Quality Report Generator")
    print("Run this in Databricks with Spark context")
