-- Job Ingestion Metrics
-- Monitor data pipeline health

-- Jobs ingested by source (last 7 days)
SELECT 
    data_source,
    COUNT(*) as jobs_ingested,
    COUNT(DISTINCT DATE(ingestion_timestamp)) as active_days,
    MIN(ingestion_timestamp) as first_ingestion,
    MAX(ingestion_timestamp) as latest_ingestion
FROM veteran_intake.bronze_jobs
WHERE ingestion_timestamp >= CURRENT_TIMESTAMP - INTERVAL 7 DAYS
GROUP BY data_source
ORDER BY jobs_ingested DESC;

-- Ingestion rate by hour
SELECT 
    DATE_TRUNC('hour', ingestion_timestamp) as hour,
    data_source,
    COUNT(*) as jobs_count
FROM veteran_intake.bronze_jobs
WHERE ingestion_timestamp >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
GROUP BY hour, data_source
ORDER BY hour DESC, jobs_count DESC;

-- Data quality metrics
SELECT 
    data_source,
    COUNT(*) as total_records,
    SUM(CASE WHEN title IS NULL THEN 1 ELSE 0 END) as missing_title,
    SUM(CASE WHEN company IS NULL THEN 1 ELSE 0 END) as missing_company,
    SUM(CASE WHEN location IS NULL THEN 1 ELSE 0 END) as missing_location,
    SUM(CASE WHEN salary_min IS NULL THEN 1 ELSE 0 END) as missing_salary
FROM veteran_intake.bronze_jobs
WHERE DATE(ingestion_timestamp) = CURRENT_DATE
GROUP BY data_source;
