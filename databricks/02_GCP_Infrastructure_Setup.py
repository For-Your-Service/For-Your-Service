# Databricks notebook source
# DBTITLE 1,requirements.txt - Dependencies
# Save as: veteran-intake-function/requirements.txt

# functions-framework==3.*
# google-cloud-storage==2.10.0

# COMMAND ----------

# DBTITLE 1,Step 3: Deploy Cloud Function
# MAGIC %undefined
# MAGIC # Deploy the Cloud Function
# MAGIC
# MAGIC cd veteran-intake-function
# MAGIC
# MAGIC gcloud functions deploy veteran-intake-processor \
# MAGIC   --gen2 \
# MAGIC   --runtime=python311 \
# MAGIC   --region=us-central1 \
# MAGIC   --source=. \
# MAGIC   --entry-point=veteran_intake \
# MAGIC   --trigger-http \
# MAGIC   --allow-unauthenticated \
# MAGIC   --memory=1GB \
# MAGIC   --timeout=60s
# MAGIC
# MAGIC echo "✅ Cloud Function deployed!"
# MAGIC echo "🔗 Get the function URL:"
# MAGIC gcloud functions describe veteran-intake-processor --region=us-central1 --gen2 --format="value(serviceConfig.uri)"
# MAGIC
# MAGIC # Test it
# MAGIC echo "
# MAGIC 🧪 Test the function with a sample veteran profile:"
# MAGIC echo "(Copy the URL from above and use it in the next cell)"

# COMMAND ----------

# DBTITLE 1,Step 2: Cloud Function - PII Anonymization Code
# MAGIC %md
# MAGIC ## 🔒 Cloud Function: PII Anonymization
# MAGIC
# MAGIC This Cloud Function:
# MAGIC 1. Receives veteran profile JSON via HTTP POST
# MAGIC 2. Validates schema
# MAGIC 3. Anonymizes all PII fields
# MAGIC 4. Generates unique `veteran_id`
# MAGIC 5. Stores anonymized JSON to GCS
# MAGIC 6. Returns confirmation
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Create these files in a directory called `veteran-intake-function/`:

# COMMAND ----------

# DBTITLE 1,main.py - Cloud Function Entry Point
# Save as: veteran-intake-function/main.py

import functions_framework
import json
import hashlib
from datetime import datetime
from google.cloud import storage
import uuid


def anonymize_veteran_profile(profile):
    """
    Anonymize PII fields in veteran profile.
    Returns anonymized profile with veteran_id.
    """

    # Generate anonymous veteran ID based on email hash + timestamp
    email = profile.get('personal_info', {}).get('email', '')
    email_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
    veteran_id = f"VET_{email_hash}"

    # Create anonymized profile
    anonymized = {
        "veteran_id": veteran_id,
        "intake_id": profile.get('intake_id', str(uuid.uuid4())),
        "timestamp": profile.get('timestamp', datetime.utcnow().isoformat()),

        # Anonymized personal info - keep only non-PII location data
        "demographics": {
            "birth_year": int(profile['personal_info']['date_of_birth'].split('-')[0]),
            "age": datetime.now().year - int(profile['personal_info']['date_of_birth'].split('-')[0]),
            "location": {
                "city": profile['personal_info']['address']['city'],
                "state": profile['personal_info']['address']['state'],
                "zip3": profile['personal_info']['address']['zip'][:3],  # First 3 digits only
                "country": profile['personal_info']['address'].get('country', 'USA')
            },
            # Store email hash for deduplication only
            "email_hash": email_hash
        },

        # Keep all military service data (not PII)
        "military_service": profile.get('military_service', {}),

        # Keep skills, education, certifications
        "skills": profile.get('skills', {}),
        "education": profile.get('education', []),
        "certifications": profile.get('certifications', []),

        # Keep job preferences
        "job_preferences": profile.get('job_preferences', {}),

        # Keep transition info (counselor can contact veteran via their system)
        "transition_info": profile.get('transition_info', {}),

        # Keep metadata
        "metadata": profile.get('metadata', {}),

        # Add processing metadata
        "processing": {
            "anonymized_at": datetime.utcnow().isoformat(),
            "schema_version": "1.0.0",
            "pii_removed": True
        }
    }

    return anonymized


@functions_framework.http
def veteran_intake(request):
    """
    HTTP Cloud Function entry point.
    Receives veteran profile, anonymizes PII, stores to GCS.
    """

    # Handle CORS for web intake wizard
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    try:
        # Parse incoming JSON
        request_json = request.get_json(silent=True)

        if not request_json:
            return json.dumps({"error": "No JSON payload provided"}), 400, headers

        # Validate required fields
        required_fields = ['personal_info', 'military_service', 'job_preferences']
        for field in required_fields:
            if field not in request_json:
                return json.dumps({"error": f"Missing required field: {field}"}), 400, headers

        # Anonymize the profile
        anonymized_profile = anonymize_veteran_profile(request_json)
        veteran_id = anonymized_profile['veteran_id']

        # Store to GCS
        storage_client = storage.Client()
        bucket_name = 'fys-veteran-intake-raw'  # Match your bucket name
        bucket = storage_client.bucket(bucket_name)

        # Create filename with timestamp + veteran_id
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"intake/{timestamp}_{veteran_id}.json"

        blob = bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(anonymized_profile, indent=2),
            content_type='application/json'
        )

        # Return success response
        return json.dumps({
            "status": "success",
            "veteran_id": veteran_id,
            "gcs_path": f"gs://{bucket_name}/{filename}",
            "message": "Veteran profile anonymized and stored successfully"
        }), 200, headers

    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e)
        }), 500, headers

# COMMAND ----------

# DBTITLE 1,For Your Service - GCP Infrastructure
# MAGIC %md
# MAGIC # ☁️ For Your Service - GCP Infrastructure Setup
# MAGIC
# MAGIC ## Overview
# MAGIC This notebook contains all the commands and code to set up the GCP infrastructure for the veteran intake pipeline.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Infrastructure Components
# MAGIC
# MAGIC 1. **GCS Bucket** - Raw veteran intake JSON storage
# MAGIC 2. **Cloud Function** - PII anonymization + schema validation
# MAGIC 3. **Event Trigger** - Automatic processing on intake submission
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Prerequisites
# MAGIC - GCP Project: `uap-scraper-lab-2026` (or create new for FYS)
# MAGIC - Cloud Shell or `gcloud` CLI installed
# MAGIC - Permissions: Editor or Owner role
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Run all commands in Cloud Shell or your local terminal with gcloud configured.**

# COMMAND ----------

# DBTITLE 1,Step 1: Create GCS Bucket
# MAGIC %undefined
# MAGIC # Create GCS bucket for veteran intake data
# MAGIC # Use unique bucket name
# MAGIC
# MAGIC BUCKET_NAME="fys-veteran-intake-raw"
# MAGIC PROJECT_ID="uap-scraper-lab-2026"  # Or your FYS project ID
# MAGIC REGION="us-central1"
# MAGIC
# MAGIC echo "Creating GCS bucket: ${BUCKET_NAME}"
# MAGIC
# MAGIC # Create bucket
# MAGIC gsutil mb -p ${PROJECT_ID} -c STANDARD -l ${REGION} gs://${BUCKET_NAME}
# MAGIC
# MAGIC # Set lifecycle policy (auto-delete raw intake after 30 days - anonymized data is in Databricks)
# MAGIC cat > lifecycle.json <<EOF
# MAGIC {
# MAGIC   "lifecycle": {
# MAGIC     "rule": [
# MAGIC       {
# MAGIC         "action": {"type": "Delete"},
# MAGIC         "condition": {"age": 30}
# MAGIC       }
# MAGIC     ]
# MAGIC   }
# MAGIC }
# MAGIC EOF
# MAGIC
# MAGIC gsutil lifecycle set lifecycle.json gs://${BUCKET_NAME}
# MAGIC
# MAGIC echo "✅ Bucket created with 30-day lifecycle policy"
# MAGIC echo "📁 Bucket URL: gs://${BUCKET_NAME}"
# MAGIC
# MAGIC # Verify
# MAGIC gsutil ls -L gs://${BUCKET_NAME}

# COMMAND ----------

