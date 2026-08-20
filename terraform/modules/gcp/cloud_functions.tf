# File: terraform/modules/gcp/cloud_functions.tf
# Description: GCP Cloud Function for Veteran Intake Webhook & Processing
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Cloud Storage Bucket for Function Source Code
# -----------------------------------------------------------------------------
resource "google_storage_bucket" "function_source" {
  count                       = var.enable_cloud_functions ? 1 : 0
  name                        = "${var.project_name}-cf-source-${var.environment}-${random_id.gcp_suffix.hex}"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }

  labels = local.common_labels
}

# -----------------------------------------------------------------------------
# 2. Package Cloud Function Source Code
# -----------------------------------------------------------------------------
data "archive_file" "veteran_intake_archive" {
  count       = var.enable_cloud_functions ? 1 : 0
  type        = "zip"
  output_path = "${path.module}/veteran_intake.zip"

  source {
    content  = <<-EOT
      import functions_framework
      import json

      @functions_framework.http
      def veteran_intake_http(request):
          request_json = request.get_json(silent=True)
          return (json.dumps({"status": "received", "message": "Veteran intake processed successfully"}), 200, {"Content-Type": "application/json"})
    EOT
    filename = "main.py"
  }

  source {
    content  = <<-EOT
      functions-framework==3.*
      google-cloud-storage>=2.0.0
      google-cloud-bigquery>=3.0.0
    EOT
    filename = "requirements.txt"
  }
}

resource "google_storage_bucket_object" "veteran_intake_zip" {
  count  = var.enable_cloud_functions ? 1 : 0
  name   = "veteran_intake_${data.archive_file.veteran_intake_archive[0].output_md5}.zip"
  bucket = google_storage_bucket.function_source[0].name
  source = data.archive_file.veteran_intake_archive[0].output_path
}

# -----------------------------------------------------------------------------
# 3. Cloud Function (Gen 1 / Gen 2 compatible)
# -----------------------------------------------------------------------------
resource "google_cloudfunctions_function" "veteran_intake" {
  count                 = var.enable_cloud_functions ? 1 : 0
  name                  = "${var.project_name}-veteran-intake-${var.environment}"
  description           = "Serverless webhook for veteran intake processing"
  runtime               = "python311"
  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_source[0].name
  source_archive_object = google_storage_bucket_object.veteran_intake_zip[0].name
  trigger_http          = true
  entry_point           = "veteran_intake_http"
  timeout               = 60
  service_account_email = google_service_account.pipeline_sa.email

  environment_variables = {
    ENVIRONMENT     = var.environment
    PROJECT_ID      = var.project_id
    ARCHIVE_BUCKET  = google_storage_bucket.archive.name
    BIGQUERY_DATASET = var.enable_bigquery ? google_bigquery_dataset.fys_analytics[0].dataset_id : ""
  }

  labels = local.common_labels
}
