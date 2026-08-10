-- Remote vs On-Site job availability
-- Important for veteran location flexibility

SELECT 
  CASE 
    WHEN LOWER(title) LIKE '%remote%' OR LOWER(description) LIKE '%fully remote%' THEN 'Fully Remote'
    WHEN LOWER(description) LIKE '%hybrid%' THEN 'Hybrid'
    WHEN LOWER(description) LIKE '%onsite%' OR LOWER(description) LIKE '%on-site%' THEN 'On-Site'
    ELSE 'Unspecified'
  END as work_arrangement,
  COUNT(*) as job_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage,
  AVG(salary.min) as avg_min_salary,
  AVG(salary.max) as avg_max_salary
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY work_arrangement
ORDER BY job_count DESC;
