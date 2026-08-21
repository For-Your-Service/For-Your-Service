-- Salary benchmarks by MOS mapping
-- Compare compensation across military specialties

WITH mos_mapping AS (
  SELECT '18Z' as mos, 'Operations Manager' as civilian_title UNION ALL
  SELECT '18E', 'Network Engineer' UNION ALL
  SELECT '18C', 'Infrastructure Engineer' UNION ALL
  SELECT '25B', 'Systems Administrator' UNION ALL
  SELECT '25D', 'Cybersecurity Analyst' UNION ALL
  SELECT '11B', 'Operations Coordinator'
),
job_matches AS (
  SELECT
    m.mos,
    m.civilian_title,
    j.salary,
    j.location
  FROM workspace.fys_bronze.job_postings j
  CROSS JOIN mos_mapping m
  WHERE LOWER(j.title) LIKE CONCAT('%', LOWER(m.civilian_title), '%')
  AND j.scrape_date >= CURRENT_DATE - INTERVAL 30 DAYS
)
SELECT
  mos,
  civilian_title,
  COUNT(*) as matching_jobs,
  PERCENTILE(salary.min, 0.25) as p25_salary,
  PERCENTILE(salary.min, 0.50) as median_salary,
  PERCENTILE(salary.min, 0.75) as p75_salary,
  AVG(salary.min) as avg_min_salary,
  AVG(salary.max) as avg_max_salary
FROM job_matches
GROUP BY mos, civilian_title
ORDER BY median_salary DESC;
