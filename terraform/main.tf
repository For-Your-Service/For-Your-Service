# File: terraform/main.tf
# Description: Multi-Cloud Master Orchestration for For Your Service
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# Provider Instances
# -----------------------------------------------------------------------------
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project      = "ForYourService"
      Environment  = var.environment
      ManagedBy    = "Terraform"
      Owner        = var.owner_email
      Organization = var.organization
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

provider "databricks" {
  host  = var.databricks_host
  token = var.databricks_token
}

# -----------------------------------------------------------------------------
# Module 1: AWS Infrastructure (S3, DynamoDB, Lambda, IAM, Secrets)
# -----------------------------------------------------------------------------
module "aws" {
  count  = var.enable_aws ? 1 : 0
  source = "./modules/aws"

  environment               = var.environment
  project_name              = var.project_name
  aws_region                = var.aws_region
  databricks_aws_account_id = var.aws_databricks_account_id
  databricks_external_id    = var.aws_databricks_external_id
  owner_email               = var.owner_email
  organization              = var.organization
}

# -----------------------------------------------------------------------------
# Module 2: GCP Infrastructure (GCS, BigQuery, IAM, Cloud Functions)
# -----------------------------------------------------------------------------
module "gcp" {
  count  = var.enable_gcp ? 1 : 0
  source = "./modules/gcp"

  environment  = var.environment
  project_name = var.project_name
  project_id   = var.gcp_project_id
  region       = var.gcp_region
  owner_email  = var.owner_email
  organization = var.organization
}

# -----------------------------------------------------------------------------
# Module 3: Databricks Infrastructure (Unity Catalog, SQL Warehouse, Secrets, Jobs)
# -----------------------------------------------------------------------------
module "databricks" {
  count  = var.enable_databricks ? 1 : 0
  source = "./modules/databricks"

  environment               = var.environment
  project_name              = var.project_name
  aws_s3_bucket_arn         = var.enable_aws ? module.aws[0].s3_staging_bucket_arn : ""
  aws_iam_role_arn          = var.enable_aws ? module.aws[0].databricks_cross_account_role_arn : ""
  gcp_storage_bucket_name   = var.enable_gcp ? module.gcp[0].archive_bucket_name : ""
}

# -----------------------------------------------------------------------------
# Module 4: Hugging Face Space & Deployment
# -----------------------------------------------------------------------------
module "huggingface" {
  count  = var.enable_huggingface ? 1 : 0
  source = "./modules/huggingface"

  environment      = var.environment
  space_name       = var.hf_space_name
  hardware         = var.hf_space_hardware
  databricks_host  = var.databricks_host
  databricks_token = var.databricks_token
  hf_token         = var.hf_token
}
