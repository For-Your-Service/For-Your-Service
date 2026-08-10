-- Create Bronze Layer Tables
-- Raw data ingestion tables

USE CATALOG veteran_intake;
USE SCHEMA bronze;

-- Bronze jobs table
CREATE TABLE IF NOT EXISTS bronze_jobs (
    job_id STRING NOT NULL,
    title STRING,
    company STRING,
    location STRING,
    description STRING,
    required_skills ARRAY<STRING>,
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    remote STRING,
    clearance_required STRING,
    veteran_friendly BOOLEAN,
    posted_date DATE,
    data_source STRING NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL,
    raw_json STRING
)
USING DELTA
PARTITIONED BY (DATE(ingestion_timestamp))
COMMENT 'Raw job postings from all data sources';

-- Bronze veteran profiles
CREATE TABLE IF NOT EXISTS bronze_veteran_profiles (
    veteran_id STRING NOT NULL,
    name STRING NOT NULL,
    military_branch STRING,
    rank STRING,
    mos STRING,
    specialty STRING,
    years_service INT,
    clearance_level STRING,
    clearance_status STRING,
    target_location STRING,
    target_radius_miles INT,
    desired_roles ARRAY<STRING>,
    technical_skills ARRAY<STRING>,
    certifications ARRAY<STRING>,
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    remote_acceptable BOOLEAN,
    ingestion_timestamp TIMESTAMP NOT NULL
)
USING DELTA
COMMENT 'Raw veteran profiles from intake forms';

-- Show created tables
SHOW TABLES;
