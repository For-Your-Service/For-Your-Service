#!/usr/bin/env python3
"""Alert system for data anomalies"""

def check_anomalies(spark):
    """Check for data quality anomalies"""
    
    alerts = []
    
    # Check 1: Zero ingestion
    zero_df = spark.sql("""
        SELECT source, COUNT(*) as count
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS
        GROUP BY source
    """)
    
    for row in zero_df.collect():
        if row['count'] == 0:
            alerts.append({
                "severity": "CRITICAL",
                "message": f"Zero jobs ingested from {row['source']}"
            })
    
    # Check 2: Low ingestion (< 20 jobs)
    for row in zero_df.collect():
        if 0 < row['count'] < 20:
            alerts.append({
                "severity": "WARNING",
                "message": f"Low ingestion from {row['source']}: {row['count']} jobs"
            })
    
    # Check 3: High null rate
    null_df = spark.sql("""
        SELECT 
          ROUND(100.0 * SUM(CASE WHEN salary.min IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as null_pct
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS
    """)
    
    null_pct = null_df.collect()[0]['null_pct']
    if null_pct > 50:
        alerts.append({
            "severity": "WARNING",
            "message": f"High salary null rate: {null_pct}%"
        })
    
    # Check 4: Duplicate rate
    dup_df = spark.sql("""
        SELECT 
          COUNT(*) as total,
          COUNT(DISTINCT job_id) as unique_ids,
          COUNT(*) - COUNT(DISTINCT job_id) as duplicates
        FROM workspace.fys_bronze.job_postings
        WHERE scrape_date = CURRENT_DATE - INTERVAL 1 DAYS
    """)
    
    dup_row = dup_df.collect()[0]
    dup_rate = 100.0 * dup_row['duplicates'] / dup_row['total']
    if dup_rate > 10:
        alerts.append({
            "severity": "WARNING",
            "message": f"High duplicate rate: {dup_rate:.2f}%"
        })
    
    return alerts

if __name__ == "__main__":
    print("Anomaly Detection")
    print("Run: check_anomalies(spark)")
