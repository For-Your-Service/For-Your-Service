# File: terraform/modules/gcp/outputs.tf
# Description: GCP Module Resource Outputs
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

output "archive_bucket_name" {
  value       = google_storage_bucket.archive.name
  description = "GCP Cloud Storage archive bucket name"
}

output "archive_bucket_url" {
  value       = google_storage_bucket.archive.url
  description = "GCP Cloud Storage archive bucket URL"
}

output "raw_ingestion_bucket_name" {
  value       = google_storage_bucket.raw_ingestion.name
  description = "GCP Cloud Storage raw ingestion bucket name"
}

output "bigquery_dataset_id" {
  value       = var.enable_bigquery ? google_bigquery_dataset.fys_analytics[0].dataset_id : null
  description = "GCP BigQuery analytics dataset ID"
}

output "custom_role_id" {
  value       = google_project_iam_custom_role.fys_pipeline_operator.role_id
  description = "GCP IAM Custom Pipeline Operator Role ID"
}

output "pipeline_service_account_email" {
  value       = google_service_account.pipeline_sa.email
  description = "GCP IAM Service Account email for data pipeline connectors"
}

output "cloud_function_url" {
  value       = var.enable_cloud_functions ? (length(google_cloudfunctions_function.veteran_intake) > 0 ? google_cloudfunctions_function.veteran_intake[0].https_trigger_url : null) : null
  description = "GCP Cloud Function HTTPS trigger URL for veteran intake"
}
