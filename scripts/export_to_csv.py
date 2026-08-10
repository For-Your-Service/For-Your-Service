#!/usr/bin/env python3
"""Export Bronze table data to CSV for external analysis"""

def export_bronze_to_csv(spark, output_path, days=7):
    """Export last N days of job data to CSV"""
    
    df = spark.sql(f"""
        SELECT 
          job_id,
          title,
          company,
          source,
          location.city as city,
          location.state as state,
          salary.min as salary_min,
          salary.max as salary_max,
          salary.currency as currency,
          url,
          created_date,
          scrape_date
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date >= CURRENT_DATE - INTERVAL {days} DAYS
        ORDER BY scrape_date DESC, company, title
    """)
    
    # Write to CSV
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)
    
    print(f"✅ Exported {df.count()} records to {output_path}")
    
    return df.count()

if __name__ == "__main__":
    print("CSV Export Utility")
    print("Run: export_bronze_to_csv(spark, '/tmp/jobs_export.csv', days=7)")
