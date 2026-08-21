-- For Your Service Database Schema
-- Unity Catalog: veteran_intake
-- Author: William Free Hall <whall4.wh@gmail.com>
-- Organization: 7 Eagle Group
-- Created: August 10, 2026

-- ============================================================================
-- CATALOG AND SCHEMAS
-- ============================================================================

CREATE CATALOG IF NOT EXISTS veteran_intake
COMMENT 'For Your Service - Veteran job matching platform data';

CREATE SCHEMA IF NOT EXISTS veteran_intake.bronze
COMMENT 'Raw data ingestion layer';

CREATE SCHEMA IF NOT EXISTS veteran_intake.silver
COMMENT 'Cleaned and normalized data';

CREATE SCHEMA IF NOT EXISTS veteran_intake.gold
COMMENT 'Business-ready aggregations and match scores';

-- ============================================================================
-- BRONZE LAYER: Raw Ingestion
-- ============================================================================

-- Job postings from external APIs
CREATE TABLE IF NOT EXISTS veteran_intake.bronze.jobs (
    job_id STRING NOT NULL,
    title STRING,
    company STRING,
    location STRING,
    description STRING,
    requirements STRING,
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    remote STRING,
    clearance_required STRING,
    posted_date DATE,
    data_source STRING COMMENT 'USAJobs, Adzuna, Indeed, LinkedIn',
    ingestion_timestamp TIMESTAMP,
    url STRING,
    raw_json STRING COMMENT 'Original API response'
)
USING DELTA
COMMENT 'Raw job postings from external APIs'
PARTITIONED BY (data_source, DATE(ingestion_timestamp));

-- Veteran profiles
CREATE TABLE IF NOT EXISTS veteran_intake.bronze.veterans (
    veteran_id STRING NOT NULL,
    profile_data STRING COMMENT 'JSON blob of veteran profile',
    ingestion_timestamp TIMESTAMP,
    source STRING COMMENT 'manual_entry, resume_parse, api_import'
)
USING DELTA
COMMENT 'Raw veteran profiles';

-- ============================================================================
-- SILVER LAYER: Cleaned Data
-- ============================================================================

-- Cleaned job postings
CREATE TABLE IF NOT EXISTS veteran_intake.silver.jobs (
    job_id STRING NOT NULL PRIMARY KEY,
    title STRING NOT NULL,
    company STRING NOT NULL,
    location STRING,
    city STRING,
    state STRING,
    remote_type STRING COMMENT 'remote, hybrid, onsite',
    description STRING,
    requirements ARRAY<STRING>,
    skills_required ARRAY<STRING>,
    salary_min DECIMAL(10,2),
    salary_max DECIMAL(10,2),
    salary_currency STRING DEFAULT 'USD',
    clearance_required STRING,
    seniority_level STRING,
    posted_date DATE,
    expires_date DATE,
    data_source STRING,
    url STRING,
    embedding ARRAY<DOUBLE> COMMENT '384-dim vector embedding',
    embedding_model STRING DEFAULT 'all-MiniLM-L6-v2',
    updated_at TIMESTAMP
)
USING DELTA
COMMENT 'Cleaned and normalized job postings with embeddings'
PARTITIONED BY (state, DATE(posted_date));

-- Veteran profiles (normalized)
CREATE TABLE IF NOT EXISTS veteran_intake.silver.veterans (
    veteran_id STRING NOT NULL PRIMARY KEY,
    name STRING NOT NULL,
    email STRING NOT NULL UNIQUE,
    phone STRING,

    -- Location
    city STRING,
    state STRING,
    zip STRING,
    willing_to_relocate BOOLEAN DEFAULT FALSE,
    remote_preference STRING,

    -- Military
    military_branch STRING,
    mos_afsc STRING,
    rank STRING,
    service_start DATE,
    service_end DATE,
    years_of_service INTEGER,
    clearance_level STRING,
    clearance_status STRING COMMENT 'active, expired, inactive',
    deployments INTEGER,

    -- Professional
    total_civilian_years INTEGER,
    current_title STRING,
    current_company STRING,
    seniority_level STRING,

    -- Skills
    skills ARRAY<STRING>,
    certifications ARRAY<STRUCT<name:STRING, issuer:STRING, date_obtained:DATE>>,

    -- Preferences
    target_roles ARRAY<STRING>,
    salary_min INTEGER,
    salary_max INTEGER,
    employment_types ARRAY<STRING>,

    -- Embedding
    embedding ARRAY<DOUBLE> COMMENT '384-dim vector embedding',
    embedding_model STRING DEFAULT 'all-MiniLM-L6-v2',

    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
COMMENT 'Normalized veteran profiles with embeddings';

-- Job embeddings (separate for efficient vector search)
CREATE TABLE IF NOT EXISTS veteran_intake.silver.job_embeddings (
    job_id STRING NOT NULL PRIMARY KEY,
    embedding ARRAY<DOUBLE> NOT NULL COMMENT '384-dim vector',
    embedding_model STRING DEFAULT 'all-MiniLM-L6-v2',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
USING DELTA
COMMENT 'Pre-computed job embeddings for fast similarity search';

-- ============================================================================
-- GOLD LAYER: Business Aggregations
-- ============================================================================

-- Job matches per veteran
CREATE TABLE IF NOT EXISTS veteran_intake.gold.job_matches (
    match_id STRING NOT NULL PRIMARY KEY,
    veteran_id STRING NOT NULL,
    job_id STRING NOT NULL,

    -- Match scores
    semantic_similarity DOUBLE COMMENT 'Cosine similarity 0-1',
    match_score INTEGER COMMENT 'Final score 0-100',

    -- Score components
    base_score DOUBLE,
    location_adjustment DOUBLE,
    salary_adjustment DOUBLE,
    clearance_adjustment DOUBLE,
    seniority_adjustment DOUBLE,

    -- Match reasons
    match_reasons ARRAY<STRING>,
    match_concerns ARRAY<STRING>,

    -- Metadata
    calculated_at TIMESTAMP,
    model_version STRING
)
USING DELTA
COMMENT 'Job match scores for each veteran'
PARTITIONED BY (veteran_id);

-- Aggregated match statistics
CREATE TABLE IF NOT EXISTS veteran_intake.gold.veteran_match_summary (
    veteran_id STRING NOT NULL PRIMARY KEY,
    veteran_name STRING,

    -- Match statistics
    total_jobs_analyzed INTEGER,
    top_match_score INTEGER,
    median_match_score INTEGER,
    strong_matches_70_plus INTEGER,
    good_matches_60_69 INTEGER,
    fair_matches_50_59 INTEGER,
    weak_matches_below_50 INTEGER,

    -- Top job match
    top_job_id STRING,
    top_job_title STRING,
    top_job_company STRING,

    -- Last run
    last_run_timestamp TIMESTAMP,
    jobs_scraped_count INTEGER
)
USING DELTA
COMMENT 'Summary statistics per veteran';

-- Application tracking
CREATE TABLE IF NOT EXISTS veteran_intake.gold.applications (
    application_id STRING NOT NULL PRIMARY KEY,
    veteran_id STRING NOT NULL,
    job_id STRING NOT NULL,
    match_score INTEGER,

    -- Application status
    status STRING COMMENT 'applied, interview, offer, rejected, accepted',
    applied_date DATE,
    status_updated_at TIMESTAMP,

    -- Outcome
    outcome STRING,
    feedback STRING,

    created_at TIMESTAMP
)
USING DELTA
COMMENT 'Track veteran job applications and outcomes'
PARTITIONED BY (veteran_id, DATE(applied_date));

-- ============================================================================
-- VIEWS
-- ============================================================================

-- Active jobs (posted in last 30 days)
CREATE OR REPLACE VIEW veteran_intake.gold.active_jobs AS
SELECT
    job_id,
    title,
    company,
    location,
    salary_min,
    salary_max,
    remote_type,
    clearance_required,
    posted_date,
    url
FROM veteran_intake.silver.jobs
WHERE posted_date >= CURRENT_DATE - INTERVAL 30 DAYS
  AND (expires_date IS NULL OR expires_date >= CURRENT_DATE);

-- Best matches (score >= 70) for all veterans
CREATE OR REPLACE VIEW veteran_intake.gold.best_matches AS
SELECT
    v.name AS veteran_name,
    v.veteran_id,
    j.title AS job_title,
    j.company,
    j.location,
    j.salary_min,
    j.salary_max,
    m.match_score,
    m.match_reasons,
    j.url
FROM veteran_intake.gold.job_matches m
JOIN veteran_intake.silver.veterans v ON m.veteran_id = v.veteran_id
JOIN veteran_intake.silver.jobs j ON m.job_id = j.job_id
WHERE m.match_score >= 70
ORDER BY m.match_score DESC;

-- ============================================================================
-- INDEXES (for performance)
-- ============================================================================

-- Optimize tables for common queries
OPTIMIZE veteran_intake.silver.jobs ZORDER BY (state, posted_date);
OPTIMIZE veteran_intake.silver.veterans ZORDER BY (state, seniority_level);
OPTIMIZE veteran_intake.gold.job_matches ZORDER BY (veteran_id, match_score);

-- ============================================================================
-- GRANTS (Unity Catalog permissions)
-- ============================================================================

-- Grant read access to analysts
GRANT SELECT ON SCHEMA veteran_intake.gold TO `analysts`;

-- Grant write access to data engineers
GRANT ALL PRIVILEGES ON SCHEMA veteran_intake.bronze TO `data_engineers`;
GRANT ALL PRIVILEGES ON SCHEMA veteran_intake.silver TO `data_engineers`;
GRANT ALL PRIVILEGES ON SCHEMA veteran_intake.gold TO `data_engineers`;
