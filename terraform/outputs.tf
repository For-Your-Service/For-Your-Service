# File: terraform/outputs.tf
# Description: Multi-Cloud Aggregated Architecture Outputs
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# AWS Outputs
# -----------------------------------------------------------------------------
output "aws_s3_data_bucket" {
  value       = var.enable_aws ? module.aws[0].s3_data_bucket_id : null
  description = "AWS S3 Data Lake & Resume Bucket Name"
}

output "aws_s3_staging_bucket" {
  value       = var.enable_aws ? module.aws[0].s3_staging_bucket_id : null
  description = "AWS S3 Staging Bucket for Databricks Pipeline"
}

output "aws_dynamodb_veterans_table" {
  value       = var.enable_aws ? module.aws[0].dynamodb_veterans_table_name : null
  description = "AWS DynamoDB Veterans Profiles Table Name"
}

output "aws_dynamodb_jobs_table" {
  value       = var.enable_aws ? module.aws[0].dynamodb_jobs_table_name : null
  description = "AWS DynamoDB Job Postings Table Name"
}

output "aws_databricks_role_arn" {
  value       = var.enable_aws ? module.aws[0].databricks_cross_account_role_arn : null
  description = "AWS IAM Role ARN for Databricks Unity Catalog External Location"
}

# -----------------------------------------------------------------------------
# GCP Outputs
# -----------------------------------------------------------------------------
output "gcp_storage_archive_bucket" {
  value       = var.enable_gcp ? module.gcp[0].archive_bucket_name : null
  description = "GCP Cloud Storage Archive Bucket Name"
}

output "gcp_bigquery_analytics_dataset" {
  value       = var.enable_gcp ? module.gcp[0].bigquery_dataset_id : null
  description = "GCP BigQuery Analytics Dataset ID"
}

output "gcp_pipeline_operator_role" {
  value       = var.enable_gcp ? module.gcp[0].custom_role_id : null
  description = "GCP IAM Custom Pipeline Operator Role ID"
}

# -----------------------------------------------------------------------------
# Databricks Outputs
# -----------------------------------------------------------------------------
output "databricks_bronze_schema" {
  value       = var.enable_databricks ? module.databricks[0].bronze_schema_name : null
  description = "Databricks Unity Catalog Bronze Schema"
}

output "databricks_silver_schema" {
  value       = var.enable_databricks ? module.databricks[0].silver_schema_name : null
  description = "Databricks Unity Catalog Silver Schema"
}

output "databricks_gold_schema" {
  value       = var.enable_databricks ? module.databricks[0].gold_schema_name : null
  description = "Databricks Unity Catalog Gold Schema"
}

output "databricks_sql_warehouse_id" {
  value       = var.enable_databricks ? module.databricks[0].sql_warehouse_id : null
  description = "Databricks Serverless SQL Warehouse ID"
}

# -----------------------------------------------------------------------------
# Hugging Face Outputs
# -----------------------------------------------------------------------------
output "huggingface_space_url" {
  value       = var.enable_huggingface ? module.huggingface[0].space_url : null
  description = "Hugging Face Spaces Public URL for FastAPI Matching API"
}
