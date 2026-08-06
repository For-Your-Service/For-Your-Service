-- Gold Layer: Neural network-ready embeddings
CREATE TABLE IF NOT EXISTS main.fys_gold.job_embeddings (
    job_id STRING NOT NULL PRIMARY KEY,
    embedding ARRAY<DOUBLE>,  -- 384-dimensional vector
    
    -- Metadata for filtering
    location_state STRING,
    salary_range STRING,  -- 'low', 'medium', 'high'
    industry STRING,
    is_remote BOOLEAN,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL,
    embedding_version STRING  -- Track model version
)
TBLPROPERTIES (
    'delta.feature.domainMetadata' = 'supported'
);

-- Add constraints
ALTER TABLE main.fys_gold.job_embeddings 
ADD CONSTRAINT embedding_length_check 
CHECK (size(embedding) = 384);

-- Create veteran embeddings table
CREATE TABLE IF NOT EXISTS main.fys_gold.veteran_embeddings (
    veteran_id STRING NOT NULL PRIMARY KEY,
    embedding ARRAY<DOUBLE>,  -- 384-dimensional vector
    
    -- Metadata
    mos_code STRING,
    location_state STRING,
    years_of_service INT,
    clearance_level STRING,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    embedding_version STRING
)
TBLPROPERTIES (
    'delta.feature.domainMetadata' = 'supported'
);
