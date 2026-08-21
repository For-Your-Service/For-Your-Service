-- Analyze jobs requiring security clearance
-- Veterans with clearance have competitive advantage

SELECT
  CASE
    WHEN LOWER(description) LIKE '%top secret%' OR LOWER(description) LIKE '%ts/sci%' THEN 'TS/SCI'
    WHEN LOWER(description) LIKE '%secret%clearance%' THEN 'Secret'
    WHEN LOWER(description) LIKE '%clearance%eligible%' THEN 'Clearance Eligible'
    ELSE 'No Clearance Required'
  END as clearance_level,
  COUNT(*) as job_count,
  AVG(salary.min) as avg_min_salary,
  AVG(salary.max) as avg_max_salary,
  COUNT(DISTINCT company) as companies
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY clearance_level
ORDER BY
  CASE clearance_level
    WHEN 'TS/SCI' THEN 1
    WHEN 'Secret' THEN 2
    WHEN 'Clearance Eligible' THEN 3
    ELSE 4
  END;
