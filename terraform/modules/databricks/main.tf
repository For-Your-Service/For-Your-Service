# File: terraform/modules/databricks/main.tf
# Description: Databricks Module Core Configuration & Provider Requirements
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.30"
    }
  }
}

locals {
  schema_prefix = var.environment == "prod" ? "fys" : "fys_${var.environment}"
  custom_tags = {
    "Project"      = "ForYourService"
    "Environment"  = var.environment
    "ManagedBy"    = "Terraform"
    "Organization" = "7 Eagle Group"
  }
}
