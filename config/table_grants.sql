-- Unity Catalog Permissions for For Your Service
-- Organization: 7 Eagle Group

-- Grant READ on Bronze table
GRANT SELECT ON TABLE workspace.fys_bronze.job_postings
TO `fys-analysts`;

-- Grant WRITE on Silver table
GRANT SELECT, INSERT, UPDATE ON TABLE workspace.fys_silver.job_postings_enriched
TO `fys-data-engineers`;

-- Grant READ on Gold table
GRANT SELECT ON TABLE workspace.fys_gold.job_embeddings
TO `fys-ml-engineers`;

-- Grant MODIFY on all tables to admin group
GRANT ALL PRIVILEGES ON SCHEMA workspace.fys_bronze TO `fys-admins`;
GRANT ALL PRIVILEGES ON SCHEMA workspace.fys_silver TO `fys-admins`;
GRANT ALL PRIVILEGES ON SCHEMA workspace.fys_gold TO `fys-admins`;

-- Create service principal for automated jobs
CREATE SERVICE PRINCIPAL IF NOT EXISTS 'fys-job-runner';

GRANT SELECT, INSERT ON TABLE workspace.fys_bronze.job_postings
TO SERVICE PRINCIPAL 'fys-job-runner';
