-- Analyze skill demand relevant to veterans
-- Tracks which skills are most requested in job postings

SELECT 
  skill,
  COUNT(DISTINCT job_id) as job_count,
  ROUND(100.0 * COUNT(DISTINCT job_id) / (SELECT COUNT(*) FROM workspace.fys_bronze.job_postings), 2) as market_penetration_pct,
  AVG(salary.min) as avg_min_salary,
  AVG(salary.max) as avg_max_salary,
  COUNT(DISTINCT company) as companies_hiring
FROM (
  -- Extract skills from job descriptions
  SELECT 
    job_id,
    company,
    salary,
    CASE 
      WHEN LOWER(description) LIKE '%aws%' THEN 'AWS'
      WHEN LOWER(description) LIKE '%azure%' THEN 'Azure'
      WHEN LOWER(description) LIKE '%kubernetes%' THEN 'Kubernetes'
      WHEN LOWER(description) LIKE '%docker%' THEN 'Docker'
      WHEN LOWER(description) LIKE '%terraform%' THEN 'Terraform'
      WHEN LOWER(description) LIKE '%python%' THEN 'Python'
      WHEN LOWER(description) LIKE '%java%' THEN 'Java'
      WHEN LOWER(description) LIKE '%jenkins%' THEN 'Jenkins'
      WHEN LOWER(description) LIKE '%git%' THEN 'Git'
      WHEN LOWER(description) LIKE '%ci/cd%' THEN 'CI/CD'
    END as skill
  FROM workspace.fys_bronze.job_postings
  WHERE scrape_date >= CURRENT_DATE - INTERVAL 30 DAYS
) skills_extract
WHERE skill IS NOT NULL
GROUP BY skill
ORDER BY job_count DESC;
