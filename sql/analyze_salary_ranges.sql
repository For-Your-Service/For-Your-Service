-- Analyze salary ranges by source and region
-- For Your Service - 7 Eagle Group

SELECT 
  source,
  location.state,
  COUNT(*) as total_jobs,
  PERCENTILE(salary.min, 0.25) as p25_min_salary,
  PERCENTILE(salary.min, 0.50) as median_min_salary,
  PERCENTILE(salary.min, 0.75) as p75_min_salary,
  PERCENTILE(salary.max, 0.25) as p25_max_salary,
  PERCENTILE(salary.max, 0.50) as median_max_salary,
  PERCENTILE(salary.max, 0.75) as p75_max_salary,
  SUM(CASE WHEN salary.is_predicted THEN 1 ELSE 0 END) / COUNT(*) as predicted_rate
FROM workspace.fys_bronze.job_postings
WHERE salary.min IS NOT NULL
AND scrape_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY source, location.state
ORDER BY source, location.state;
