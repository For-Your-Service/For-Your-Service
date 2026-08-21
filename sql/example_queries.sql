-- Example SQL Queries for For Your Service Platform
-- Author: William Free Hall <whall4.wh@gmail.com>
-- Organization: 7 Eagle Group

-- ============================================================================
-- VETERAN ANALYSIS
-- ============================================================================

-- Count veterans by military branch
SELECT
    military_branch,
    COUNT(*) as veteran_count,
    AVG(years_of_service) as avg_service_years,
    COUNT(DISTINCT CASE WHEN clearance_status = 'active' THEN veteran_id END) as active_clearances
FROM veteran_intake.silver.veterans
GROUP BY military_branch
ORDER BY veteran_count DESC;

-- Veteran skill distribution
SELECT
    EXPLODE(skills) as skill,
    COUNT(*) as veteran_count
FROM veteran_intake.silver.veterans
GROUP BY skill
ORDER BY veteran_count DESC
LIMIT 25;

-- Veterans by seniority and target salary
SELECT
    seniority_level,
    COUNT(*) as veteran_count,
    AVG(salary_min) as avg_salary_min,
    AVG(salary_max) as avg_salary_max,
    MIN(salary_min) as min_salary,
    MAX(salary_max) as max_salary
FROM veteran_intake.silver.veterans
GROUP BY seniority_level
ORDER BY avg_salary_min DESC;

-- ============================================================================
-- JOB MARKET ANALYSIS
-- ============================================================================

-- Active jobs by state and remote type
SELECT
    state,
    remote_type,
    COUNT(*) as job_count,
    AVG(salary_min) as avg_min_salary,
    AVG(salary_max) as avg_max_salary
FROM veteran_intake.silver.jobs
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY state, remote_type
ORDER BY job_count DESC;

-- Top hiring companies
SELECT
    company,
    COUNT(*) as job_postings,
    AVG((salary_min + salary_max) / 2) as avg_salary,
    COUNT(DISTINCT CASE WHEN clearance_required != 'None' THEN job_id END) as clearance_jobs
FROM veteran_intake.silver.jobs
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY company
ORDER BY job_postings DESC
LIMIT 20;

-- Jobs requiring security clearance
SELECT
    clearance_required,
    COUNT(*) as job_count,
    AVG(salary_min) as avg_min_salary,
    AVG(salary_max) as avg_max_salary
FROM veteran_intake.silver.jobs
WHERE clearance_required != 'None'
  AND posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY clearance_required
ORDER BY avg_min_salary DESC;

-- Most in-demand skills from job descriptions
SELECT
    skill,
    COUNT(*) as job_count,
    AVG((salary_min + salary_max) / 2) as avg_salary
FROM veteran_intake.silver.jobs
LATERAL VIEW EXPLODE(skills_required) AS skill
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY skill
ORDER BY job_count DESC
LIMIT 30;

-- ============================================================================
-- MATCH QUALITY ANALYSIS
-- ============================================================================

-- William Free Hall's best matches
SELECT
    j.title,
    j.company,
    j.location,
    j.remote_type,
    CONCAT('$', FORMAT_NUMBER(j.salary_min, 0), ' - $', FORMAT_NUMBER(j.salary_max, 0)) as salary_range,
    m.match_score,
    m.match_reasons,
    j.url
FROM veteran_intake.gold.job_matches m
JOIN veteran_intake.silver.jobs j ON m.job_id = j.job_id
JOIN veteran_intake.silver.veterans v ON m.veteran_id = v.veteran_id
WHERE v.name = 'William Free Hall'
  AND m.match_score >= 70
ORDER BY m.match_score DESC
LIMIT 25;

-- Match score distribution for all veterans
SELECT
    CASE
        WHEN match_score >= 85 THEN '85-100 (Exceptional)'
        WHEN match_score >= 70 THEN '70-84 (Strong)'
        WHEN match_score >= 60 THEN '60-69 (Good)'
        WHEN match_score >= 50 THEN '50-59 (Fair)'
        ELSE '0-49 (Weak)'
    END as score_range,
    COUNT(*) as match_count,
    AVG(match_score) as avg_score
FROM veteran_intake.gold.job_matches
GROUP BY
    CASE
        WHEN match_score >= 85 THEN '85-100 (Exceptional)'
        WHEN match_score >= 70 THEN '70-84 (Strong)'
        WHEN match_score >= 60 THEN '60-69 (Good)'
        WHEN match_score >= 50 THEN '50-59 (Fair)'
        ELSE '0-49 (Weak)'
    END
ORDER BY avg_score DESC;

-- Top match factors (what drives high scores)
SELECT
    EXPLODE(match_reasons) as reason,
    COUNT(*) as frequency,
    AVG(match_score) as avg_match_score
FROM veteran_intake.gold.job_matches
WHERE match_score >= 70
GROUP BY reason
ORDER BY frequency DESC
LIMIT 20;

-- ============================================================================
-- APPLICATION TRACKING
-- ============================================================================

-- Application conversion rates
SELECT
    CASE
        WHEN match_score >= 80 THEN '80+ (Strong)'
        WHEN match_score >= 70 THEN '70-79 (Good)'
        WHEN match_score >= 60 THEN '60-69 (Fair)'
        ELSE '<60 (Weak)'
    END as match_tier,
    COUNT(*) as applications,
    COUNT(DISTINCT CASE WHEN status = 'interview' THEN application_id END) as interviews,
    COUNT(DISTINCT CASE WHEN status = 'offer' THEN application_id END) as offers,
    COUNT(DISTINCT CASE WHEN status = 'accepted' THEN application_id END) as accepted,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN status = 'interview' THEN application_id END) / COUNT(*), 1) as interview_rate,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN status = 'offer' THEN application_id END) / COUNT(*), 1) as offer_rate
FROM veteran_intake.gold.applications
GROUP BY
    CASE
        WHEN match_score >= 80 THEN '80+ (Strong)'
        WHEN match_score >= 70 THEN '70-79 (Good)'
        WHEN match_score >= 60 THEN '60-69 (Fair)'
        ELSE '<60 (Weak)'
    END
ORDER BY interview_rate DESC;

-- Veteran application history
SELECT
    v.name,
    COUNT(DISTINCT a.application_id) as total_applications,
    COUNT(DISTINCT CASE WHEN a.status = 'interview' THEN a.application_id END) as interviews,
    COUNT(DISTINCT CASE WHEN a.status = 'offer' THEN a.application_id END) as offers,
    COUNT(DISTINCT CASE WHEN a.status = 'accepted' THEN a.application_id END) as accepted,
    MAX(a.applied_date) as last_application_date,
    AVG(a.match_score) as avg_match_score_applied
FROM veteran_intake.silver.veterans v
LEFT JOIN veteran_intake.gold.applications a ON v.veteran_id = a.veteran_id
GROUP BY v.name
ORDER BY total_applications DESC;

-- ============================================================================
-- DATA QUALITY CHECKS
-- ============================================================================

-- Jobs missing salary information
SELECT
    data_source,
    COUNT(*) as total_jobs,
    COUNT(CASE WHEN salary_min IS NULL THEN 1 END) as missing_salary,
    ROUND(100.0 * COUNT(CASE WHEN salary_min IS NULL THEN 1 END) / COUNT(*), 1) as missing_pct
FROM veteran_intake.silver.jobs
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY data_source;

-- Veteran profiles completeness
SELECT
    COUNT(*) as total_veterans,
    COUNT(CASE WHEN skills IS NULL OR SIZE(skills) = 0 THEN 1 END) as missing_skills,
    COUNT(CASE WHEN salary_min IS NULL THEN 1 END) as missing_salary,
    COUNT(CASE WHEN clearance_level = 'None' THEN 1 END) as no_clearance,
    COUNT(CASE WHEN SIZE(target_roles) = 0 THEN 1 END) as missing_target_roles
FROM veteran_intake.silver.veterans;

-- Duplicate job postings
SELECT
    title,
    company,
    COUNT(*) as duplicate_count
FROM veteran_intake.silver.jobs
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY title, company
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- ============================================================================
-- PERFORMANCE METRICS
-- ============================================================================

-- Daily job ingestion volume
SELECT
    DATE(ingestion_timestamp) as ingestion_date,
    data_source,
    COUNT(DISTINCT job_id) as jobs_ingested,
    COUNT(*) as total_records
FROM veteran_intake.bronze.jobs
WHERE ingestion_timestamp >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY DATE(ingestion_timestamp), data_source
ORDER BY ingestion_date DESC, jobs_ingested DESC;

-- Match calculation performance
SELECT
    veteran_id,
    calculated_at,
    COUNT(*) as jobs_matched,
    MAX(match_score) as best_match_score,
    ROUND(AVG(match_score), 1) as avg_match_score
FROM veteran_intake.gold.job_matches
WHERE calculated_at >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY veteran_id, calculated_at
ORDER BY calculated_at DESC;
