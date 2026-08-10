-- System Health Monitoring
-- Quick health check queries

-- Pipeline freshness check
SELECT 
    'bronze_jobs' as table_name,
    MAX(ingestion_timestamp) as latest_record,
    TIMESTAMPDIFF(MINUTE, MAX(ingestion_timestamp), CURRENT_TIMESTAMP) as minutes_since_last_update,
    CASE 
        WHEN TIMESTAMPDIFF(MINUTE, MAX(ingestion_timestamp), CURRENT_TIMESTAMP) > 60 THEN 'STALE'
        ELSE 'FRESH'
    END as status
FROM veteran_intake.bronze_jobs

UNION ALL

SELECT 
    'gold_matches' as table_name,
    MAX(match_date) as latest_record,
    DATEDIFF(CURRENT_DATE, MAX(match_date)) as days_since_last_update,
    CASE 
        WHEN DATEDIFF(CURRENT_DATE, MAX(match_date)) > 1 THEN 'STALE'
        ELSE 'FRESH'
    END as status
FROM veteran_intake.gold_matches;

-- Error rate check
SELECT 
    DATE(timestamp) as error_date,
    error_type,
    COUNT(*) as error_count
FROM veteran_intake.error_log
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
GROUP BY error_date, error_type
ORDER BY error_count DESC;

-- Data quality summary
SELECT 
    'Bronze Jobs' as layer,
    COUNT(*) as total_records,
    SUM(CASE WHEN title IS NULL OR company IS NULL THEN 1 ELSE 0 END) as quality_issues,
    ROUND(100.0 * SUM(CASE WHEN title IS NOT NULL AND company IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as quality_pct
FROM veteran_intake.bronze_jobs
WHERE DATE(ingestion_timestamp) = CURRENT_DATE;
