-- Top hiring companies in Greenville MSA
-- For Your Service - 7 Eagle Group

SELECT
  company,
  COUNT(*) as active_postings,
  COUNT(DISTINCT title) as unique_roles,
  AVG(salary.min) as avg_min_salary,
  AVG(salary.max) as avg_max_salary,
  MIN(created_date) as oldest_posting,
  MAX(created_date) as newest_posting
FROM workspace.fys_bronze.job_postings
WHERE location.city IN ('Greenville', 'Anderson', 'Simpsonville', 'Greer')
AND scrape_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY company
HAVING COUNT(*) >= 3
ORDER BY active_postings DESC
LIMIT 20;
