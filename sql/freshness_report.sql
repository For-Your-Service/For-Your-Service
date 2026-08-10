-- Job posting freshness report
-- For Your Service - 7 Eagle Group

SELECT 
  CASE 
    WHEN DATEDIFF(CURRENT_DATE, TO_DATE(created_date)) <= 7 THEN '0-7 days'
    WHEN DATEDIFF(CURRENT_DATE, TO_DATE(created_date)) <= 14 THEN '8-14 days'
    WHEN DATEDIFF(CURRENT_DATE, TO_DATE(created_date)) <= 30 THEN '15-30 days'
    ELSE '30+ days'
  END as age_bucket,
  COUNT(*) as job_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM workspace.fys_bronze.job_postings
WHERE scrape_date = CURRENT_DATE
GROUP BY age_bucket
ORDER BY 
  CASE age_bucket
    WHEN '0-7 days' THEN 1
    WHEN '8-14 days' THEN 2
    WHEN '15-30 days' THEN 3
    ELSE 4
  END;
