-- Monitor daily job ingestion metrics
-- For Your Service - 7 Eagle Group

SELECT
  scrape_date,
  source,
  COUNT(*) as job_count,
  AVG(salary.min) as avg_min_salary,
  AVG(salary.max) as avg_max_salary,
  SUM(CASE WHEN salary.is_predicted THEN 0 ELSE 1 END) as real_salary_count,
  COUNT(DISTINCT company) as unique_companies
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY scrape_date, source
ORDER BY scrape_date DESC, source;
