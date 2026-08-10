# Gold Layer Specification

## Overview

The Gold layer contains neural embeddings for semantic matching.

## Table Schema

```sql
CREATE TABLE workspace.fys_gold.job_embeddings (
  job_id STRING PRIMARY KEY,
  embedding ARRAY<FLOAT>,  -- 384 dimensions
  embedding_model STRING,  -- 'all-MiniLM-L6-v2'
  embedding_date TIMESTAMP
)
PARTITIONED BY (embedding_date);
```

## Embedding Model

**Model:** sentence-transformers/all-MiniLM-L6-v2
- **Dimensions:** 384
- **Max sequence:** 256 tokens
- **Performance:** ~14k sentences/sec on CPU

## Embedding Process

1. Concat title + description + skills
2. Truncate to 256 tokens
3. Generate embedding via model
4. Normalize to unit vector
5. Store in Gold table

## Similarity Calculation

```python
cosine_similarity = np.dot(veteran_emb, job_emb) / (
    np.linalg.norm(veteran_emb) * np.linalg.norm(job_emb)
)
```

Threshold: 0.7 for high match
