# ⚡ Apache Spark & Delta Lake Medallion Architecture
## Distributed Veteran-Job Matching Engine | For-Your-Service

---

## 🏛️ System Overview

The **For-Your-Service Spark Medallion Engine** transforms multi-source defense and civilian job feeds into high-throughput semantic embeddings and runs distributed batch matrix matching against cohorts of transitioning veterans.

```mermaid
flowchart LR
    subgraph Bronze["🥉 Bronze Layer (Raw Feeds)"]
        B1["USAJOBS API"]
        B2["Adzuna API"]
        B3["JSearch RapidAPI"]
        B4["BLS Wage Feeds"]
    end

    subgraph Silver["🥈 Silver Layer (Cleaned & MOS Enriched)"]
        S1["HTML Strip & Regex Sanitization"]
        S2["Deduplication Engine"]
        S3["MOS/AFSC/Rating Universal Crosswalk"]
        S4["Clearance Level Detection"]
    end

    subgraph Gold["🥇 Gold Layer (Distributed Embeddings)"]
        G1["Vectorized Pandas Iterator UDF"]
        G2["384-Dim Normalized Tensors"]
        G3["Delta Lake Partitioned Storage"]
    end

    subgraph Matching["🎯 Distributed Batch Matching Engine"]
        M1["Broadcast Veteran Profiles"]
        M2["Distributed Cosine Similarity Matrix"]
        M3["Multi-Factor Scoring (MOS + Clearance + Location)"]
        M4["Top-K Ranked Recommendations"]
    end

    Bronze --> Silver --> Gold --> Matching
```

---

## 📦 Component Specification

### 1. Bronze-to-Silver ETL (`src.spark.bronze_to_silver_etl`)
* **Sanitization:** Distributed regex-based HTML tag removal, whitespace normalizer, and salary range aggregation.
* **Security Clearance Extraction:** Automatically flags `Top Secret / SCI`, `Secret`, or `Public Trust` requirements.
* **MOS Crosswalk:** Cross-references `app.mos_data.MOS_DATABASE` across all 6 service branches to tag jobs with matching military specialties.

### 2. Distributed Embedding Pipeline (`src.spark.embedding_pipeline`)
* **Throughput:** Utilizes PySpark `@pandas_udf(ArrayType(FloatType()))` with iterator batching to eliminate Python worker serialization overhead.
* **Dimensionality:** 384-dimensional unit-length L2 normalized semantic vectors (`sentence-transformers/all-MiniLM-L6-v2` architecture).

### 3. Batch Veteran Matcher (`src.spark.batch_matcher`)
* **Matrix Computation:** Distributed cross-product cosine dot products computed in parallel across Spark cluster nodes.
* **Composite Weighting:**
  $$\text{Composite Score} = \text{Cosine Sim} \times \text{Clearance Multiplier} \times \text{Location Multiplier} \times \text{MOS Multiplier}$$
* **Top-K Windowing:** Uses `row_number().over(Window.partitionBy("veteran_id"))` to extract top candidates.

---

## 🚀 Execution Guide

```python
from pyspark.sql import SparkSession
from src.spark import SparkMedallionOrchestrator

spark = SparkSession.builder.appName("FYS-Lakehouse").getOrCreate()
orchestrator = SparkMedallionOrchestrator(spark)

# Run full medallion pipeline
result = orchestrator.run_full_pipeline(bronze_jobs_df, veterans_df, top_k_per_veteran=5)

# Access artifacts
silver_df = result["silver_df"]
gold_df = result["gold_df"]
matches_df = result["matches_df"]
metrics = result["metrics"]
```
