# File: variables.tf
# Description: Input variables for For Your Service AWS infrastructure
# Organization: 7 Eagle Group

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for deployment (free tier optimized)"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment (dev, staging, prod)"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

variable "databricks_aws_account_id" {
  type        = string
  default     = "414351767826"
  description = "Standard Databricks production AWS account ID for cross-account trust"
}

variable "databricks_external_id" {
  type        = string
  description = "Unique External ID from your Databricks storage credential configuration"
  sensitive   = true
  
  validation {
    condition     = length(var.databricks_external_id) > 0
    error_message = "Databricks External ID must not be empty"
  }
}

variable "project_name" {
  type        = string
  default     = "ForYourService"
  description = "Project name for tagging"
}

variable "owner" {
  type        = string
  default     = "Free Hall"
  description = "Resource owner for tagging"
}

variable "organization" {
  type        = string
  default     = "7 Eagle Group"
  description = "Organization name for tagging"
}

variable "enable_versioning" {
  type        = bool
  default     = true
  description = "Enable S3 bucket versioning for data protection"
}

variable "force_destroy" {
  type        = bool
  default     = false
  description = "Allow Terraform to destroy bucket even if not empty (use with caution)"
}
