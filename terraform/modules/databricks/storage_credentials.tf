# File: terraform/modules/databricks/storage_credentials.tf
# Description: Databricks Unity Catalog Storage Credentials & External Locations
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. AWS IAM Storage Credential for Unity Catalog
# -----------------------------------------------------------------------------
resource "databricks_storage_credential" "aws_s3_cred" {
  count   = var.aws_iam_role_arn != "" ? 1 : 0
  name    = "fys-aws-s3-credential-${var.environment}"
  comment = "Storage credential for For Your Service AWS S3 Buckets (${var.environment})"

  aws_iam_role {
    role_arn = var.aws_iam_role_arn
  }
}

# -----------------------------------------------------------------------------
# 2. External Location pointing to S3 Staging / Data Lake
# -----------------------------------------------------------------------------
resource "databricks_external_location" "s3_staging" {
  count           = (var.aws_iam_role_arn != "" && var.aws_s3_bucket_arn != "") ? 1 : 0
  name            = "fys-s3-staging-${var.environment}"
  url             = "s3://${replace(var.aws_s3_bucket_arn, "arn:aws:s3:::", "")}"
  credential_name = databricks_storage_credential.aws_s3_cred[0].id
  comment         = "External location for staging data ingestion from AWS S3"
}
