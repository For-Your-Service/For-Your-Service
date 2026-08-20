# File: terraform/environments/staging/main.tf
# Description: Staging Environment Multi-Cloud Deployment
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.30"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project      = "ForYourService"
      Environment  = "staging"
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

module "aws" {
  count  = var.enable_aws ? 1 : 0
  source = "../../modules/aws"

  environment               = "staging"
  project_name              = var.project_name
  aws_region                = var.aws_region
  databricks_aws_account_id = var.aws_databricks_account_id
  databricks_external_id    = var.aws_databricks_external_id
  owner_email               = var.owner_email
  organization              = var.organization
}

module "gcp" {
  count  = var.enable_gcp ? 1 : 0
  source = "../../modules/gcp"

  environment  = "staging"
  project_name = var.project_name
  project_id   = var.gcp_project_id
  region       = var.gcp_region
  owner_email  = var.owner_email
  organization = var.organization
}

module "databricks" {
  count  = var.enable_databricks ? 1 : 0
  source = "../../modules/databricks"

  environment             = "staging"
  project_name            = var.project_name
  aws_s3_bucket_arn       = var.enable_aws ? module.aws[0].s3_staging_bucket_arn : ""
  aws_iam_role_arn        = var.enable_aws ? module.aws[0].databricks_cross_account_role_arn : ""
  gcp_storage_bucket_name = var.enable_gcp ? module.gcp[0].archive_bucket_name : ""
}

module "huggingface" {
  count  = var.enable_huggingface ? 1 : 0
  source = "../../modules/huggingface"

  environment      = "staging"
  space_name       = var.hf_space_name
  hardware         = "cpu-basic"
  databricks_host  = var.databricks_host
  databricks_token = var.databricks_token
  hf_token         = var.hf_token
}
