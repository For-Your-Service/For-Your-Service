# Cloud Function: Veteran Intake PII Anonymization
# Receives veteran profile JSON, anonymizes PII, stores to GCS

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
                "zip3": profile['personal_info']['address']['zip'][:3],
                "country": profile['personal_info']['address'].get('country', 'USA')
            },
            "email_hash": email_hash
        },

        "military_service": profile.get('military_service', {}),
        "skills": profile.get('skills', {}),
        "education": profile.get('education', []),
        "certifications": profile.get('certifications', []),
        "job_preferences": profile.get('job_preferences', {}),
        "transition_info": profile.get('transition_info', {}),
        "metadata": profile.get('metadata', {}),

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

    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    try:
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
        bucket_name = 'fys-veteran-intake-raw'
        bucket = storage_client.bucket(bucket_name)

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"intake/{timestamp}_{veteran_id}.json"

        blob = bucket.blob(filename)
        blob.upload_from_string(
            json.dumps(anonymized_profile, indent=2),
            content_type='application/json'
        )

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
