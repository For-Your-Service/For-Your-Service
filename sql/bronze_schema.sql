-- DEPRECATED: Non-canonical schema reference. See docs/adr/ADR-001-CODE-CANONICAL-CATALOG-SPINE.md

-- DEPRECATED: Non-canonical main.fys_* reference. See docs/adr/ADR-001-CODE-CANONICAL-CATALOG-SPINE.md
-- Bronze Layer: Raw job postings
CREATE TABLE IF NOT EXISTS main.fys_bronze.job_postings (
    job_id STRING NOT NULL,
    source STRING NOT NULL,  -- 'usajobs', 'adzuna', etc.
    raw_json STRING,  -- Full JSON response
    title STRING,
    company STRING,
    description STRING,
    location STRING,
    salary_min DOUBLE,
    salary_max DOUBLE,
    posted_date TIMESTAMP,
    fetched_at TIMESTAMP NOT NULL,
    ingestion_date DATE GENERATED ALWAYS AS (CAST(fetched_at AS DATE))
)
PARTITIONED BY (source, ingestion_date)
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_job_location ON main.fys_bronze.job_postings(location);
CREATE INDEX IF NOT EXISTS idx_posted_date ON main.fys_bronze.job_postings(posted_date);


