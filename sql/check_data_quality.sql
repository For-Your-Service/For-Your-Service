-- Data quality checks for Bronze table
-- For Your Service - 7 Eagle Group

-- Check for duplicate job_ids
SELECT 
  'Duplicate job_ids' as check_name,
  COUNT(*) - COUNT(DISTINCT job_id) as issue_count
FROM workspace.fys_bronze.job_postings
WHERE scrape_date >= CURRENT_DATE - INTERVAL 1 DAYS

UNION ALL

-- Check for missing required fields
SELECT 
  'Missing titles' as check_name,
  COUNT(*) as issue_count
FROM workspace.fys_bronze.job_postings
WHERE title IS NULL OR title = ''
AND scrape_date >= CURRENT_DATE - INTERVAL 1 DAYS

UNION ALL

-- Check for missing companies
SELECT 
  'Missing companies' as check_name,
  COUNT(*) as issue_count
FROM workspace.fys_bronze.job_postings
WHERE company IS NULL OR company = ''
AND scrape_date >= CURRENT_DATE - INTERVAL 1 DAYS;
