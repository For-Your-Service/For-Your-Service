import json
import os
from google.cloud import storage
from anonymizer import sanitize_payload
from validator import validate_intake_schema

BUCKET_NAME = os.environ.get("GCP_LANDING_BUCKET", "fys-landing-dev")


def ingest_candidate_intake(request):
    """GCP Cloud Function HTTP entry point for candidate intake payloads."""
    request_json = request.get_json(silent=True)

    if not request_json:
        return json.dumps({"error": "Invalid or missing JSON payload"}), 400

    # 1. Validate Schema
    is_valid, err_msg = validate_intake_schema(request_json)
    if not is_valid:
        return json.dumps({"status": "rejected", "reason": err_msg}), 422

    # 2. Anonymize PII
    sanitized_data, candidate_uuid = sanitize_payload(request_json)

    # 3. Write Sanitized Vector Data to GCP Landing Storage
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"sanitized_intake/{candidate_uuid}.json")
    blob.upload_from_string(json.dumps(sanitized_data), content_type="application/json")

    return (
        json.dumps(
            {
                "status": "success",
                "candidate_uuid": candidate_uuid,
                "destination": f"gs://{BUCKET_NAME}/sanitized_intake/{candidate_uuid}.json",
            }
        ),
        200,
    )
