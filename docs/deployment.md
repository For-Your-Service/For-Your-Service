# Deployment Guide

## Prerequisites

1. **GCP Project**
   - Project ID: `uap-scraper-lab-2026` (or create new)
   - IAM Role: Editor or Owner
   - APIs enabled: Cloud Functions, Cloud Storage

2. **Databricks Workspace**
   - Unity Catalog enabled
   - Serverless compute available
   - GCS access configured

3. **Tools**
   - gcloud CLI installed and configured
   - git installed

---

## Step 1: Clone Repository

```bash
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service
```

---

## Step 2: Deploy GCP Infrastructure

### Create GCS Bucket

```bash
BUCKET_NAME="fys-veteran-intake-raw"
PROJECT_ID="uap-scraper-lab-2026"
REGION="us-central1"

# Create bucket
gsutil mb -p ${PROJECT_ID} -c STANDARD -l ${REGION} gs://${BUCKET_NAME}

# Set lifecycle (30-day retention)
cat > lifecycle.json <<EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 30}
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://${BUCKET_NAME}
```

### Deploy Cloud Function

```bash
cd cloud-functions/veteran-intake

gcloud functions deploy veteran-intake-processor \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=veteran_intake \
  --trigger-http \
  --allow-unauthenticated \
  --memory=1GB \
  --timeout=60s

# Get function URL
gcloud functions describe veteran-intake-processor \
  --region=us-central1 \
  --gen2 \
  --format="value(serviceConfig.uri)"
```

---

## Step 3: Configure Databricks

### Import Notebooks

1. Go to Databricks workspace
2. Navigate to `/Workspace/Users/<your-email>/`
3. Import notebooks from `/databricks/` directory

### Configure GCS Access

1. Create GCP service account:
   ```bash
   gcloud iam service-accounts create fys-databricks-sa \
     --display-name="FYS Databricks Service Account"
   
   # Grant Storage Object Viewer role
   gcloud projects add-iam-policy-binding ${PROJECT_ID} \
     --member="serviceAccount:fys-databricks-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
     --role="roles/storage.objectViewer"
   
   # Create key
   gcloud iam service-accounts keys create fys-sa-key.json \
     --iam-account=fys-databricks-sa@${PROJECT_ID}.iam.gserviceaccount.com
   ```

2. Upload key to Databricks Secrets or configure in notebook

3. Configure in notebooks:
   ```python
   spark.conf.set(
       "spark.hadoop.google.cloud.auth.service.account.json.keyfile",
       "/path/to/fys-sa-key.json"
   )
   ```

### Create Unity Catalog Schemas

```sql
CREATE SCHEMA IF NOT EXISTS main.fys_bronze
  COMMENT 'Bronze layer - raw anonymized veteran intake';

CREATE SCHEMA IF NOT EXISTS main.fys_silver
  COMMENT 'Silver layer - feature engineering and transformations';

CREATE SCHEMA IF NOT EXISTS main.fys_gold
  COMMENT 'Gold layer - job matching tensor engine';
```

---

## Step 4: Test Pipeline

### Test Cloud Function

```bash
# Get function URL
FUNCTION_URL=$(gcloud functions describe veteran-intake-processor \
  --region=us-central1 --gen2 --format="value(serviceConfig.uri)")

# Send test veteran profile (create test_veteran_profile.json first)
curl -X POST ${FUNCTION_URL} \
  -H "Content-Type: application/json" \
  -d @test_veteran_profile.json
```

### Run Bronze Ingestion

1. Open `03_bronze_ingestion.py` in Databricks
2. Run all cells
3. Verify data in `main.fys_bronze.veteran_profiles`

---

## Step 5: Monitoring

### Cloud Function Logs

```bash
gcloud functions logs read veteran-intake-processor \
  --region=us-central1 \
  --gen2 \
  --limit=50
```

### GCS Bucket Contents

```bash
gsutil ls -r gs://fys-veteran-intake-raw/intake/
```

### Databricks Tables

```sql
-- Check Bronze table
SELECT COUNT(*) FROM main.fys_bronze.veteran_profiles;

-- View recent intakes
SELECT veteran_id, timestamp, military_service.branch
FROM main.fys_bronze.veteran_profiles
ORDER BY timestamp DESC
LIMIT 10;
```

---

## Troubleshooting

### Cloud Function Errors

```bash
# View recent errors
gcloud functions logs read veteran-intake-processor \
  --region=us-central1 \
  --gen2 \
  --filter="severity=ERROR" \
  --limit=20
```

### GCS Access Issues

- Verify service account has `roles/storage.objectViewer`
- Check key file path in Databricks config
- Test access: `gsutil ls gs://fys-veteran-intake-raw/`

### Schema Validation Failures

- Check Cloud Function logs for specific field errors
- Verify intake JSON matches schema in `01_intake_schema_definition.py`

---

## Production Checklist

- [ ] GCS bucket created with lifecycle policy
- [ ] Cloud Function deployed and tested
- [ ] Databricks GCS access configured
- [ ] Unity Catalog schemas created
- [ ] Bronze ingestion tested
- [ ] Monitoring/alerting configured
- [ ] Team members have appropriate IAM roles
- [ ] Documentation reviewed
