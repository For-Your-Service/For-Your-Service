# File: terraform/environments/dev/outputs.tf
# Description: Development Environment Outputs
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

output "aws_s3_data_bucket" {
  value = var.enable_aws ? module.aws[0].s3_data_bucket_id : null
}

output "aws_s3_staging_bucket" {
  value = var.enable_aws ? module.aws[0].s3_staging_bucket_id : null
}

output "gcp_storage_archive_bucket" {
  value = var.enable_gcp ? module.gcp[0].archive_bucket_name : null
}

output "databricks_bronze_schema" {
  value = var.enable_databricks ? module.databricks[0].bronze_schema_name : null
}

output "huggingface_space_url" {
  value = var.enable_huggingface ? module.huggingface[0].space_url : null
}
