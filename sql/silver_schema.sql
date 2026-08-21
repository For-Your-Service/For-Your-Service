-- Silver Layer: Normalized and enriched job data
CREATE TABLE IF NOT EXISTS main.fys_silver.job_features (
    job_id STRING NOT NULL PRIMARY KEY,
    source STRING NOT NULL,
    title STRING,
    company STRING,
    description_clean STRING,

    -- Normalized fields
    location_city STRING,
    location_state STRING,
    location_lat DOUBLE,
    location_lng DOUBLE,

    -- Salary
    salary_min DOUBLE,
    salary_max DOUBLE,
    salary_avg DOUBLE GENERATED ALWAYS AS ((salary_min + salary_max) / 2),

    -- Skills
    technical_skills ARRAY<STRING>,
    soft_skills ARRAY<STRING>,
    certifications ARRAY<STRING>,

    -- MOS mapping
    relevant_mos_codes ARRAY<STRING>,
    onet_codes ARRAY<STRING>,

    -- Metadata
    posted_date TIMESTAMP,
    expires_date TIMESTAMP,
    is_remote BOOLEAN,
    veteran_preference BOOLEAN,
    clearance_required STRING,

    -- Timestamps
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
)
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true'
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_state ON main.fys_silver.job_features(location_state);
CREATE INDEX IF NOT EXISTS idx_remote ON main.fys_silver.job_features(is_remote);
