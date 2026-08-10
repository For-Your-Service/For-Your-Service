-- Security Clearance Analytics
-- Analyze clearance requirements and veteran clearance levels

-- Job postings by clearance requirement
SELECT 
    clearance_required,
    COUNT(*) as job_count,
    AVG(salary_min) as avg_salary_min,
    AVG(salary_max) as avg_salary_max
FROM veteran_intake.silver_jobs
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY clearance_required
ORDER BY job_count DESC;

-- Veterans by clearance level
SELECT 
    clearance_level,
    clearance_status,
    COUNT(*) as veteran_count,
    AVG(years_service) as avg_years_service
FROM veteran_intake.veteran_profiles
GROUP BY clearance_level, clearance_status
ORDER BY clearance_level, clearance_status;

-- Match success by clearance alignment
SELECT 
    v.clearance_level as veteran_clearance,
    j.clearance_required as job_requirement,
    COUNT(*) as matches,
    AVG(m.match_score) as avg_match_score
FROM veteran_intake.gold_matches m
JOIN veteran_intake.veteran_profiles v ON m.veteran_id = v.veteran_id
JOIN veteran_intake.silver_jobs j ON m.job_id = j.job_id
WHERE m.match_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY v.clearance_level, j.clearance_required
ORDER BY matches DESC;
