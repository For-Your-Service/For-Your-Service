# File: terraform/modules/aws/outputs.tf
# Description: AWS Module Resource Outputs
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

output "s3_data_bucket_id" {
  value       = aws_s3_bucket.data_prod.id
  description = "Primary S3 data lake bucket name"
}

output "s3_data_bucket_arn" {
  value       = aws_s3_bucket.data_prod.arn
  description = "Primary S3 data lake bucket ARN"
}

output "s3_staging_bucket_id" {
  value       = aws_s3_bucket.staging.id
  description = "S3 staging bucket name for Databricks ingestion"
}

output "s3_staging_bucket_arn" {
  value       = aws_s3_bucket.staging.arn
  description = "S3 staging bucket ARN for Databricks ingestion"
}

output "s3_resumes_bucket_id" {
  value       = aws_s3_bucket.resumes.id
  description = "S3 bucket for veteran resumes"
}

output "s3_models_bucket_id" {
  value       = aws_s3_bucket.models.id
  description = "S3 bucket for trained neural network model weights"
}

output "databricks_cross_account_role_arn" {
  value       = aws_iam_role.databricks_s3_role.arn
  description = "IAM Role ARN assumed by Databricks for S3 access"
}

output "app_policy_arn" {
  value       = aws_iam_policy.for_your_service_policy.arn
  description = "Custom ForYourService IAM Policy ARN"
}

output "dynamodb_veterans_table_name" {
  value       = var.enable_dynamodb ? aws_dynamodb_table.veterans[0].name : null
  description = "DynamoDB veterans table name"
}

output "dynamodb_jobs_table_name" {
  value       = var.enable_dynamodb ? aws_dynamodb_table.jobs[0].name : null
  description = "DynamoDB jobs table name"
}

output "lambda_match_api_arn" {
  value       = var.enable_lambda ? aws_lambda_function.match_api[0].arn : null
  description = "Lambda matching API function ARN"
}

output "secrets_manager_secret_arn" {
  value       = aws_secretsmanager_secret.fys_secrets.arn
  description = "AWS Secrets Manager secret ARN for For-Your-Service API keys"
}
