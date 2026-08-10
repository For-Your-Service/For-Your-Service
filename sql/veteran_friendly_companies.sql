-- Identify veteran-friendly companies
-- Based on hiring patterns and job descriptions

SELECT 
  company,
  COUNT(*) as total_postings,
  SUM(CASE WHEN LOWER(description) LIKE '%veteran%' THEN 1 ELSE 0 END) as veteran_mentioned,
  SUM(CASE WHEN LOWER(description) LIKE '%clearance%' THEN 1 ELSE 0 END) as clearance_jobs,
  SUM(CASE WHEN LOWER(description) LIKE '%dod%' OR LOWER(description) LIKE '%defense%' THEN 1 ELSE 0 END) as defense_related,
  ROUND(100.0 * SUM(CASE WHEN LOWER(description) LIKE '%veteran%' THEN 1 ELSE 0 END) / COUNT(*), 2) as veteran_mention_rate,
  AVG(salary.min) as avg_min_salary
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY company
HAVING total_postings >= 5
ORDER BY veteran_mention_rate DESC, clearance_jobs DESC
LIMIT 20;
