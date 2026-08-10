# Silver Layer Specification

## Overview

The Silver layer enriches Bronze job postings with:
- O*NET skills taxonomy
- MOS (Military Occupational Specialty) crosswalk
- Standardized job titles
- Industry classifications

## Table Schema

```sql
CREATE TABLE workspace.fys_silver.job_postings_enriched (
  -- From Bronze
  job_id STRING,
  title STRING,
  company STRING,
  
  -- Enrichments
  onet_code STRING,
  onet_title STRING,
  skills ARRAY<STRUCT<skill: STRING, importance: DOUBLE>>,
  mos_matches ARRAY<STRUCT<mos: STRING, similarity: DOUBLE>>,
  standardized_title STRING,
  industry_sector STRING,
  
  -- Metadata
  enriched_date TIMESTAMP,
  enrichment_version STRING
)
PARTITIONED BY (enriched_date);
```

## O*NET Integration

### API Access
- Endpoint: https://services.onetcenter.org/ws/
- Authentication: Free API key required
- Rate Limit: 50 requests/minute

### Skill Extraction Process
1. Parse job description with spaCy NLP
2. Extract technical skills
3. Map to O*NET taxonomy
4. Score skill importance (0-1)

## MOS Crosswalk

Map veteran MOS codes to civilian jobs:
- 18 Series (Special Forces) → Project Manager, Security roles
- 25 Series (Signal) → Network Engineer, IT roles
- 11 Series (Infantry) → Operations, Logistics roles
