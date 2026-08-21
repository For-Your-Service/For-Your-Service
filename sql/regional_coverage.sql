-- Regional coverage analysis
-- For Your Service - 7 Eagle Group

SELECT
  location.city,
  location.state,
  COUNT(*) as job_count,
  COUNT(DISTINCT source) as source_count,
  COUNT(DISTINCT company) as company_count,
  AVG(salary.min) as avg_min_salary,
  SUM(CASE WHEN salary.is_predicted THEN 0 ELSE 1 END) / COUNT(*) as real_salary_rate
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY location.city, location.state
ORDER BY job_count DESC;
