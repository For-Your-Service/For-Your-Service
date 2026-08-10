-- Geographic heatmap of job opportunities
-- Visualize job density across regions

SELECT 
  location.city,
  location.state,
  location.latitude,
  location.longitude,
  COUNT(*) as job_count,
  AVG(salary.min) as avg_salary,
  COUNT(DISTINCT company) as unique_companies,
  -- Categorical bucket for heatmap
  CASE 
    WHEN COUNT(*) >= 100 THEN 'Very High'
    WHEN COUNT(*) >= 50 THEN 'High'
    WHEN COUNT(*) >= 20 THEN 'Medium'
    WHEN COUNT(*) >= 5 THEN 'Low'
    ELSE 'Very Low'
  END as density_category
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
AND location.latitude IS NOT NULL
AND location.longitude IS NOT NULL
GROUP BY 
  location.city, 
  location.state, 
  location.latitude, 
  location.longitude
ORDER BY job_count DESC;
