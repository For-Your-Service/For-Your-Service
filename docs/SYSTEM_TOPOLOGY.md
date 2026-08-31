# For Your Service — Military Skills Tensor Translation Engine

*Automated Architecture Sync: 2026-08-31 13:01:39 UTC*

## Live System Topology

```mermaid
flowchart TD
    subgraph Live_Sources [Real-World Ingestion Feeds]
        A[USAJOBS Live API] --> D[(Raw Staging Layer)]
        B[O*NET SOC Taxonomy] --> D
        C[DoD MOS Manuals] --> D
    end

    subgraph Core_Engine [PySpark & Tensor Matching]
        D --> E[PySpark Vector Pipeline]
        E --> F[Cosine Similarity / Tensor Matrix]
        F --> G[(DuckDB / Delta Lake)]
    end

    subgraph Presentation [Operational Surface]
        G --> H[Streamlit UI :8501]
        H --> I[Civilian Career Roadmaps]
    end
```

## Repository Health & Verification
- **Data Integrity:** 100% Live Public Feeds (No Synthetic Rows)
- **Local Engine:** Omarchy Native / Background systemd & FastAPI services
- **Continuous Remediation:** Enabled via Gemini agent hooks & Autonomous Flywheel
