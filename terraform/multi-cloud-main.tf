# File: main.tf
# Description: Multi-Cloud Infrastructure (AWS S3 + GCP Bucket + BigQuery) for For Your Service

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

# ------------------------------------------------------------------------------
# Providers
# ------------------------------------------------------------------------------
provider "aws" {
  region = var.aws_region
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# ------------------------------------------------------------------------------
# Variables
# ------------------------------------------------------------------------------
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS Deployment Region"
}

variable "gcp_project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "gcp_region" {
  type        = string
  default     = "us-central1"
  description = "GCP Free Tier Region"
}

variable "databricks_aws_account_id" {
  type        = string
  default     = "414351767826"
  description = "Databricks Production AWS Account ID"
}

variable "databricks_external_id" {
  type        = string
  default     = "fys-pipeline-external-id"
  description = "Databricks External ID for STS Trust"
}

resource "random_id" "suffix" {
  byte_length = 4
}

# ------------------------------------------------------------------------------
# AWS Resources (S3 Hot Staging & IAM Access)
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "fys_staging" {
  bucket        = "fys-staging-${random_id.suffix.hex}"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "fys_staging_privacy" {
  bucket                  = aws_s3_bucket.fys_staging.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "databricks_s3_role" {
  name = "fys-databricks-s3-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${var.databricks_aws_account_id}:root" }
        Action    = "sts:AssumeRole"
        Condition = {
          StringEquals = { "sts:ExternalId" = var.databricks_external_id }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "s3_access" {
  name = "fys-databricks-s3-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.fys_staging.arn,
          "${aws_s3_bucket.fys_staging.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3" {
  role       = aws_iam_role.databricks_s3_role.name
  policy_arn = aws_iam_policy.s3_access.arn
}

# ------------------------------------------------------------------------------
# GCP Resources (Cloud Storage Archive & BigQuery Analytics)
# ------------------------------------------------------------------------------
resource "google_storage_bucket" "fys_archive" {
  name                        = "fys-archive-${random_id.suffix.hex}"
  location                    = var.gcp_region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "fys_analytics" {
  dataset_id                  = "fys_analytics"
  friendly_name               = "For Your Service Analytics"
  description                 = "Analytics dataset for processed veteran job metrics"
  location                    = var.gcp_region
  default_table_expiration_ms = 3600000000
}

# ------------------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------------------
output "aws_s3_bucket" {
  value = aws_s3_bucket.fys_staging.id
}

output "aws_iam_role_arn" {
  value = aws_iam_role.databricks_s3_role.arn
}

output "gcp_storage_bucket" {
  value = google_storage_bucket.fys_archive.name
}

output "gcp_bigquery_dataset" {
  value = google_bigquery_dataset.fys_analytics.dataset_id
}
