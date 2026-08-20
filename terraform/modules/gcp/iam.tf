# File: terraform/modules/gcp/iam.tf
# Description: GCP IAM Custom Roles, Service Accounts, and Least-Privilege Policies
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Custom IAM Role: fysPipelineOperator
# -----------------------------------------------------------------------------
resource "google_project_iam_custom_role" "fys_pipeline_operator" {
  role_id     = "fysPipelineOperator_${replace(var.environment, "-", "_")}"
  title       = "For-Your-Service Pipeline Operator (${var.environment})"
  description = "Custom role with specific permissions for managing data ingestion, GCS buckets, and Databricks pipeline connectors."
  stage       = "GA"

  permissions = [
    "storage.buckets.get",
    "storage.buckets.list",
    "storage.objects.create",
    "storage.objects.delete",
    "storage.objects.get",
    "storage.objects.list",
    "bigquery.datasets.get",
    "bigquery.tables.get",
    "bigquery.tables.list",
    "bigquery.tables.getData",
    "bigquery.tables.updateData",
    "resourcemanager.projects.get"
  ]
}

# -----------------------------------------------------------------------------
# 2. Pipeline Ingestion Service Account
# -----------------------------------------------------------------------------
resource "google_service_account" "pipeline_sa" {
  account_id   = "${var.project_name}-sa-${var.environment}"
  display_name = "For Your Service Pipeline Service Account (${var.environment})"
  description  = "Service account used by ingestion jobs, Cloud Functions, and Databricks external connectors"
}

# -----------------------------------------------------------------------------
# 3. Bind Custom Role to Service Account
# -----------------------------------------------------------------------------
resource "google_project_iam_member" "pipeline_sa_custom_role" {
  project = var.project_id
  role    = google_project_iam_custom_role.fys_pipeline_operator.id
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# -----------------------------------------------------------------------------
# 4. BigQuery Data Editor for Pipeline SA
# -----------------------------------------------------------------------------
resource "google_project_iam_member" "pipeline_sa_bigquery_editor" {
  count   = var.enable_bigquery ? 1 : 0
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}
