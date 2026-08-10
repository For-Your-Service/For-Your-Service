-- Track job posting lifecycle and fill rates
-- How long jobs stay open (indicator of difficulty filling)

SELECT 
  company,
  COUNT(*) as total_postings,
  AVG(DATEDIFF(CURRENT_DATE, TO_DATE(created_date))) as avg_days_open,
  MIN(DATEDIFF(CURRENT_DATE, TO_DATE(created_date))) as min_days_open,
  MAX(DATEDIFF(CURRENT_DATE, TO_DATE(created_date))) as max_days_open,
  SUM(CASE WHEN DATEDIFF(CURRENT_DATE, TO_DATE(created_date)) > 30 THEN 1 ELSE 0 END) as stale_postings_30d,
  SUM(CASE WHEN DATEDIFF(CURRENT_DATE, TO_DATE(created_date)) > 60 THEN 1 ELSE 0 END) as stale_postings_60d
FROM workspace.fys_bronze.job_postings
WHERE location.city IN ('Greenville', 'Anderson', 'Simpsonville')
AND scrape_date = CURRENT_DATE
GROUP BY company
HAVING COUNT(*) >= 3
ORDER BY avg_days_open DESC;
