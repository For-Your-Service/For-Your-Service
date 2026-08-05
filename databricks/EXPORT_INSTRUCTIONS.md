# Databricks Notebooks Export Instructions

## Notebooks to Export

The following notebooks need to be manually exported from Databricks and added to the `/databricks/` directory:

### 1. 01_intake_schema_definition.py
**Source:** `/Users/whall4.wh@gmail.com/For-Your-Service/01_Intake_Schema_Definition`
**Contains:**
- Complete veteran profile JSON schema (15 sections)
- PII identification and anonymization strategy
- Example veteran profile with realistic data
- Field mappings and validation rules

### 2. 03_bronze_ingestion.py
**Source:** `/Users/whall4.wh@gmail.com/For-Your-Service/03_Bronze_Ingestion`
**Contains:**
- GCS Auto Loader configuration
- Unity Catalog schema creation
- Bronze Delta table ingestion
- Audit trail metadata capture

### 3. 04_silver_feature_engineering.py (Placeholder)
**Status:** To be implemented
**Will contain:**
- MOS code → civilian skill mapping
- Certification standardization
- Feature vector creation
- Location normalization

### 4. 05_gold_tensor_engine.py (Placeholder)
**Status:** To be implemented
**Will contain:**
- PySpark MLlib vector operations
- Multi-dimensional vector dot products
- Placement probability matrix generation

---

## How to Export Notebooks

### Method 1: Export Individual Notebooks
1. Open each notebook in Databricks
2. Click File → Export → Source File (.py)
3. Save to the `databricks/` directory in this export
4. Rename to match the names above

### Method 2: Export as DBC Archive
1. Right-click the `/For-Your-Service/` folder in workspace
2. Select Export → DBC Archive
3. Extract the DBC archive
4. Copy the .py files to `databricks/` directory

### Method 3: Use Databricks CLI
```bash
# Install Databricks CLI
pip install databricks-cli

# Configure authentication
databricks configure --token

# Export notebooks
databricks workspace export /Users/whall4.wh@gmail.com/For-Your-Service/01_Intake_Schema_Definition databricks/01_intake_schema_definition.py
databricks workspace export /Users/whall4.wh@gmail.com/For-Your-Service/03_Bronze_Ingestion databricks/03_bronze_ingestion.py
```

---

## Alternative: Keep Notebooks in Databricks Only

For now, you can:
1. Push the current repo structure (without notebook files)
2. Team members import notebooks directly from Databricks workspace
3. Keep the canonical notebook source in Databricks
4. Export to GitHub only when ready for version control

---

## Recommended Workflow

**Option A - Databricks-first:**
- Keep notebooks in Databricks workspace
- Use Databricks Repos for Git integration
- Link workspace folder to GitHub repo

**Option B - GitHub-first:**
- Export notebooks as .py files to GitHub
- Import from GitHub when working in Databricks
- Commit changes back to GitHub

Choose based on your team's preference!
