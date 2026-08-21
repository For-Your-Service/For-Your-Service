-- Job Title Standardization
-- Maps variations to canonical titles

CREATE OR REPLACE VIEW workspace.fys_silver.standardized_titles AS
SELECT
  job_id,
  title as original_title,
  CASE
    -- DevOps variations
    WHEN LOWER(title) LIKE '%devops%engineer%' THEN 'DevOps Engineer'
    WHEN LOWER(title) LIKE '%dev%ops%' THEN 'DevOps Engineer'
    WHEN LOWER(title) LIKE '%platform%engineer%' THEN 'Platform Engineer'
    WHEN LOWER(title) LIKE '%site%reliability%' THEN 'Site Reliability Engineer'
    WHEN LOWER(title) LIKE '%sre%' THEN 'Site Reliability Engineer'

    -- Cloud variations
    WHEN LOWER(title) LIKE '%cloud%architect%' THEN 'Cloud Architect'
    WHEN LOWER(title) LIKE '%solutions%architect%' THEN 'Solutions Architect'
    WHEN LOWER(title) LIKE '%aws%engineer%' THEN 'Cloud Engineer - AWS'
    WHEN LOWER(title) LIKE '%azure%engineer%' THEN 'Cloud Engineer - Azure'

    -- Software Engineer variations
    WHEN LOWER(title) LIKE '%software%engineer%' THEN 'Software Engineer'
    WHEN LOWER(title) LIKE '%full%stack%' THEN 'Full Stack Engineer'
    WHEN LOWER(title) LIKE '%backend%' THEN 'Backend Engineer'
    WHEN LOWER(title) LIKE '%frontend%' THEN 'Frontend Engineer'

    -- Data roles
    WHEN LOWER(title) LIKE '%data%engineer%' THEN 'Data Engineer'
    WHEN LOWER(title) LIKE '%data%scientist%' THEN 'Data Scientist'
    WHEN LOWER(title) LIKE '%machine%learning%' THEN 'Machine Learning Engineer'

    -- Security roles
    WHEN LOWER(title) LIKE '%security%engineer%' THEN 'Security Engineer'
    WHEN LOWER(title) LIKE '%infosec%' THEN 'Information Security Specialist'
    WHEN LOWER(title) LIKE '%cyber%' THEN 'Cybersecurity Analyst'

    -- Management roles
    WHEN LOWER(title) LIKE '%engineering%manager%' THEN 'Engineering Manager'
    WHEN LOWER(title) LIKE '%tech%lead%' THEN 'Technical Lead'
    WHEN LOWER(title) LIKE '%staff%engineer%' THEN 'Staff Engineer'

    ELSE title  -- Keep original if no match
  END as standardized_title,

  -- Extract seniority level
  CASE
    WHEN LOWER(title) LIKE '%senior%' OR LOWER(title) LIKE '%sr.%' THEN 'Senior'
    WHEN LOWER(title) LIKE '%staff%' OR LOWER(title) LIKE '%principal%' THEN 'Staff'
    WHEN LOWER(title) LIKE '%junior%' OR LOWER(title) LIKE '%jr.%' THEN 'Junior'
    WHEN LOWER(title) LIKE '%lead%' OR LOWER(title) LIKE '%manager%' THEN 'Lead'
    ELSE 'Mid-Level'
  END as seniority_level

FROM workspace.fys_bronze.job_postings;
