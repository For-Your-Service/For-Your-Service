# 🏗️ For Your Service - System Architecture

## High-Level Overview

```
┌─────────────────┐
│   Job APIs      │
│ (3 sources)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Bronze Layer    │
│ (Raw Ingestion) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Silver Layer    │
│ (O*NET Skills)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gold Layer     │
│ (Embeddings)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Neural Network  │
│ (Matching)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │
│  (REST API)     │
└─────────────────┘
```

## Components

### Data Ingestion (Bronze)
- **Purpose:** Raw job data from APIs
- **Frequency:** Daily at 6 AM
- **Table:** workspace.fys_bronze.job_postings
- **Partitioning:** By scrape_date

### Data Enrichment (Silver)
- **Purpose:** O*NET skill crosswalk
- **Process:** NLP + skill extraction
- **Table:** workspace.fys_silver.job_postings_enriched

### Embeddings (Gold)
- **Purpose:** 384-dim semantic vectors
- **Model:** sentence-transformers/all-MiniLM-L6-v2
- **Table:** workspace.fys_gold.job_embeddings

### Matching Engine
- **Architecture:** Siamese Twin Tower
- **Input:** Veteran profile + Job embeddings
- **Output:** Similarity score (0-1)

### API Backend
- **Framework:** FastAPI
- **Deployment:** Hugging Face Spaces (FREE)
- **Endpoints:** /match, /jobs, /veteran
