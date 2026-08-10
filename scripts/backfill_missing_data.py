#!/usr/bin/env python3
"""Backfill missing job data from specific dates"""
from datetime import datetime, timedelta

def backfill_dates(spark, start_date, end_date):
    """Re-run ingestion for missing date range"""
    
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    backfilled = []
    
    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Check if data exists
        check_df = spark.sql(f"""
            SELECT COUNT(*) as count
            FROM workspace.fys_bronze.job_postings
            WHERE scrape_date = '{date_str}'
        """)
        
        count = check_df.collect()[0]["count"]
        
        if count == 0:
            print(f"🔄 Backfilling {date_str}...")
            # Trigger ingestion notebook here
            # dbutils.notebook.run("/path/to/ingestion", 1800, {"target_date": date_str})
            backfilled.append(date_str)
        else:
            print(f"✅ {date_str} already has {count} records")
        
        current_date += timedelta(days=1)
    
    return backfilled

if __name__ == "__main__":
    print("Backfill Utility")
    print("Run: backfill_dates(spark, '2026-08-01', '2026-08-10')")
