# File: main.tf
# Description: AWS S3 & IAM Infrastructure for Databricks Cross-Account Integration
# Organization: 7 Eagle Group
# Project: For Your Service

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ------------------------------------------------------------------------------
# Variables
# ------------------------------------------------------------------------------
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for deployment"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment stage"
}

variable "databricks_aws_account_id" {
  type        = string
  default     = "414351767826" # Standard Databricks production AWS account ID
  description = "Databricks account ID for cross-account trust"
}

variable "databricks_external_id" {
  type        = string
  default     = "fys-pipeline-test-id"
  description = "Unique External ID provided by your Databricks storage credential configuration"
}

# ------------------------------------------------------------------------------
# Random suffix for unique bucket names
# ------------------------------------------------------------------------------
resource "random_id" "suffix" {
  byte_length = 4
}

# ------------------------------------------------------------------------------
# Amazon S3 Staging Bucket (Free Tier Compliant: < 5 GB)
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "fys_databricks_staging" {
  bucket        = "fys-pipeline-staging-${var.environment}-${random_id.suffix.hex}"
  force_destroy = true

  tags = {
    Project      = "ForYourService"
    Environment  = var.environment
    ManagedBy    = "Terraform"
    Owner        = "Free Hall"
    Organization = "7 Eagle Group"
  }
}

# Block all public access by default
resource "aws_s3_bucket_public_access_block" "fys_staging_privacy" {
  bucket                  = aws_s3_bucket.fys_databricks_staging.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning for data protection
resource "aws_s3_bucket_versioning" "fys_staging_versioning" {
  bucket = aws_s3_bucket.fys_databricks_staging.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "fys_staging_encryption" {
  bucket = aws_s3_bucket.fys_databricks_staging.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ------------------------------------------------------------------------------
# IAM Policy for Databricks S3 Access
# ------------------------------------------------------------------------------
resource "aws_iam_policy" "databricks_s3_access_policy" {
  name        = "fys-databricks-s3-access-policy"
  description = "Allows Databricks clusters to access S3 staging data for For Your Service"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          aws_s3_bucket.fys_databricks_staging.arn,
          "${aws_s3_bucket.fys_databricks_staging.arn}/*"
        ]
      }
    ]
  })

  tags = {
    Project      = "ForYourService"
    Environment  = var.environment
    ManagedBy    = "Terraform"
    Owner        = "Free Hall"
    Organization = "7 Eagle Group"
  }
}

# ------------------------------------------------------------------------------
# IAM Cross-Account Role for Databricks
# ------------------------------------------------------------------------------
resource "aws_iam_role" "databricks_cross_account_role" {
  name        = "fys-databricks-cross-account-role"
  description = "Role assumed by Databricks to access S3 resources"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.databricks_aws_account_id}:root"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.databricks_external_id
          }
        }
      }
    ]
  })

  tags = {
    Project      = "ForYourService"
    Environment  = var.environment
    ManagedBy    = "Terraform"
    Owner        = "Free Hall"
    Organization = "7 Eagle Group"
  }
}

resource "aws_iam_role_policy_attachment" "databricks_s3_attach" {
  role       = aws_iam_role.databricks_cross_account_role.name
  policy_arn = aws_iam_policy.databricks_s3_access_policy.arn
}

# ------------------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------------------
output "s3_bucket_name" {
  value       = aws_s3_bucket.fys_databricks_staging.id
  description = "S3 bucket name to use as Databricks External Location"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.fys_databricks_staging.arn
  description = "S3 bucket ARN"
}

output "databricks_role_arn" {
  value       = aws_iam_role.databricks_cross_account_role.arn
  description = "IAM Role ARN to enter in Databricks Storage Credential"
}

output "databricks_role_name" {
  value       = aws_iam_role.databricks_cross_account_role.name
  description = "IAM Role name for reference"
}

output "databricks_external_id" {
  value       = var.databricks_external_id
  description = "External ID used for cross-account access"
  sensitive   = true
}
