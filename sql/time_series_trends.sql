-- Time series analysis of job market trends
-- Track job posting volume over time

SELECT 
  scrape_date,
  source,
  COUNT(*) as daily_jobs,
  AVG(salary.min) as avg_min_salary,
  COUNT(DISTINCT company) as companies_posting,
  -- 7-day moving average
  AVG(COUNT(*)) OVER (
    PARTITION BY source 
    ORDER BY scrape_date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as ma_7day
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY scrape_date, source
ORDER BY scrape_date DESC, source;
