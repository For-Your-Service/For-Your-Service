# File: outputs.tf
# Description: Output values from For Your Service AWS infrastructure
# Organization: 7 Eagle Group

output "s3_bucket_name" {
  value       = aws_s3_bucket.fys_databricks_staging.id
  description = "S3 bucket name - Use this as Databricks External Location"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.fys_databricks_staging.arn
  description = "S3 bucket ARN for reference"
}

output "s3_bucket_region" {
  value       = aws_s3_bucket.fys_databricks_staging.region
  description = "S3 bucket region"
}

output "databricks_role_arn" {
  value       = aws_iam_role.databricks_cross_account_role.arn
  description = "IAM Role ARN - Enter this in Databricks Storage Credential"
}

output "databricks_role_name" {
  value       = aws_iam_role.databricks_cross_account_role.name
  description = "IAM Role name for reference"
}

output "databricks_policy_arn" {
  value       = aws_iam_policy.databricks_s3_access_policy.arn
  description = "IAM Policy ARN for S3 access"
}

output "databricks_external_id" {
  value       = var.databricks_external_id
  description = "External ID used for cross-account access"
  sensitive   = true
}

output "setup_complete" {
  value       = <<-EOT
    ✅ AWS Infrastructure Deployed Successfully!
    
    Next Steps for Databricks Integration:
    
    1. Create Storage Credential in Databricks:
       - Go to: Catalog → Storage Credentials → Create
       - Name: fys-aws-storage-credential
       - IAM Role ARN: ${aws_iam_role.databricks_cross_account_role.arn}
       - External ID: ${var.databricks_external_id}
    
    2. Create External Location:
       - Go to: Catalog → External Locations → Create
       - Name: fys-s3-staging
       - Storage Credential: fys-aws-storage-credential
       - URL: s3://${aws_s3_bucket.fys_databricks_staging.id}/
    
    3. Test Access:
       - Use Databricks SQL or notebook to read/write to the external location
       - Example: df.write.format("delta").save("s3://${aws_s3_bucket.fys_databricks_staging.id}/test/")
    
    S3 Bucket: ${aws_s3_bucket.fys_databricks_staging.id}
    IAM Role: ${aws_iam_role.databricks_cross_account_role.arn}
  EOT
  description = "Setup instructions for Databricks integration"
}
