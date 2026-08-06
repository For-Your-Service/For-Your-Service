# Architecture Overview

## System Components

### 1. Data Ingestion Layer
* **Orchestrator**: Coordinates API calls
* **Bronze Writer**: Writes raw data to storage
* **Scheduler**: Manages collection frequency

### 2. Feature Engineering Layer
* **MOS Mapper**: Maps military codes to civilian jobs
* **Skill Extractor**: Parses skills from text
* **Embedding Generator**: Creates 384-dim vectors

### 3. Matching Engine
* **Siamese Network**: Computes similarity scores
* **Job Matcher**: Ranks and filters matches

### 4. Data Flow
```
APIs → Orchestrator → Bronze (Raw JSON)
                          ↓
                    Feature Engineering
                          ↓
                    Silver (Normalized)
                          ↓
                    Embedding Generation
                          ↓
                    Gold (384-dim tensors)
                          ↓
                    Siamese Network → Matches
```

## Technology Stack
* **Python 3.11**: Core language
* **Sentence-Transformers**: Embeddings
* **Databricks**: Data platform
* **Unity Catalog**: Data governance
* **Docker**: Containerization
