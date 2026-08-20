# File: terraform/modules/gcp/storage.tf
# Description: GCP Cloud Storage Buckets (Archive & Raw Ingestion) with Lifecycle Rules
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Cloud Storage Archive Bucket
# -----------------------------------------------------------------------------
resource "google_storage_bucket" "archive" {
  name                        = "${var.project_name}-archive-${var.environment}-${random_id.gcp_suffix.hex}"
  location                    = var.region
  force_destroy               = var.environment != "prod"
  uniform_bucket_level_access = true
  storage_class               = "STANDARD"

  versioning {
    enabled = var.environment == "prod"
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  labels = local.common_labels
}

# -----------------------------------------------------------------------------
# 2. Cloud Storage Raw Ingestion Staging Bucket
# -----------------------------------------------------------------------------
resource "google_storage_bucket" "raw_ingestion" {
  name                        = "${var.project_name}-raw-ingest-${var.environment}-${random_id.gcp_suffix.hex}"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 14
    }
    action {
      type = "Delete"
    }
  }

  labels = local.common_labels
}
