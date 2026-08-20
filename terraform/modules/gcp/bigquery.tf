# File: terraform/modules/gcp/bigquery.tf
# Description: GCP BigQuery Datasets & Tables for Analytics & Reporting
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. BigQuery Analytics Dataset
# -----------------------------------------------------------------------------
resource "google_bigquery_dataset" "fys_analytics" {
  count                       = var.enable_bigquery ? 1 : 0
  dataset_id                  = "fys_analytics_${replace(var.environment, "-", "_")}"
  friendly_name               = "For Your Service Analytics (${var.environment})"
  description                 = "Analytics dataset for processed veteran job metrics, skills crosswalk, and match history"
  location                    = var.region
  default_table_expiration_ms = var.environment == "prod" ? null : 7776000000 # 90 days for non-prod

  labels = local.common_labels
}

# -----------------------------------------------------------------------------
# 2. BigQuery Ingested Jobs Table (Partitioned by ingestion date)
# -----------------------------------------------------------------------------
resource "google_bigquery_table" "ingested_jobs" {
  count               = var.enable_bigquery ? 1 : 0
  dataset_id          = google_bigquery_dataset.fys_analytics[0].dataset_id
  table_id            = "ingested_job_postings"
  deletion_protection = var.environment == "prod"

  time_partitioning {
    type  = "DAY"
    field = "ingestion_timestamp"
  }

  schema = jsonencode([
    {
      name = "job_id",
      type = "STRING",
      mode = "REQUIRED",
      description = "Unique Job ID from source"
    },
    {
      name = "title",
      type = "STRING",
      mode = "REQUIRED",
      description = "Job Title"
    },
    {
      name = "company",
      type = "STRING",
      mode = "NULLABLE",
      description = "Company Name"
    },
    {
      name = "source",
      type = "STRING",
      mode = "REQUIRED",
      description = "Source platform (USAJOBS, JSearch, Adzuna)"
    },
    {
      name = "location",
      type = "STRING",
      mode = "NULLABLE",
      description = "Job Location"
    },
    {
      name = "career_track",
      type = "STRING",
      mode = "NULLABLE",
      description = "Inferred Career Track"
    },
    {
      name = "ingestion_timestamp",
      type = "TIMESTAMP",
      mode = "REQUIRED",
      description = "Timestamp when job was ingested"
    }
  ])

  labels = local.common_labels
}
