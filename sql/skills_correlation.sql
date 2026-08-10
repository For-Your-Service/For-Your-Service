-- Skill correlation analysis
-- Which skills commonly appear together

WITH skill_matrix AS (
  SELECT 
    job_id,
    CASE WHEN LOWER(description) LIKE '%aws%' THEN 1 ELSE 0 END as has_aws,
    CASE WHEN LOWER(description) LIKE '%azure%' THEN 1 ELSE 0 END as has_azure,
    CASE WHEN LOWER(description) LIKE '%kubernetes%' THEN 1 ELSE 0 END as has_k8s,
    CASE WHEN LOWER(description) LIKE '%docker%' THEN 1 ELSE 0 END as has_docker,
    CASE WHEN LOWER(description) LIKE '%terraform%' THEN 1 ELSE 0 END as has_terraform,
    CASE WHEN LOWER(description) LIKE '%python%' THEN 1 ELSE 0 END as has_python,
    CASE WHEN LOWER(description) LIKE '%jenkins%' THEN 1 ELSE 0 END as has_jenkins
  FROM workspace.fys_bronze.job_postings
  WHERE scrape_date >= CURRENT_DATE - INTERVAL 7 DAYS
)
SELECT 
  'AWS + Kubernetes' as skill_pair,
  SUM(has_aws * has_k8s) as co_occurrence,
  ROUND(100.0 * SUM(has_aws * has_k8s) / SUM(has_aws), 2) as pct_of_aws_jobs
FROM skill_matrix
UNION ALL
SELECT 
  'AWS + Terraform',
  SUM(has_aws * has_terraform),
  ROUND(100.0 * SUM(has_aws * has_terraform) / SUM(has_aws), 2)
FROM skill_matrix
UNION ALL
SELECT 
  'Docker + Kubernetes',
  SUM(has_docker * has_k8s),
  ROUND(100.0 * SUM(has_docker * has_k8s) / SUM(has_docker), 2)
FROM skill_matrix
ORDER BY co_occurrence DESC;
