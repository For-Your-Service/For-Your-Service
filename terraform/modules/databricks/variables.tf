# File: terraform/modules/databricks/variables.tf
# Description: Databricks Module Variables
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment (dev, staging, prod)"
}

variable "project_name" {
  type        = string
  default     = "foryourservice"
  description = "Project name prefix"
}

variable "catalog_name" {
  type        = string
  default     = "workspace"
  description = "Databricks Unity Catalog name"
}

variable "aws_s3_bucket_arn" {
  type        = string
  default     = ""
  description = "AWS S3 staging bucket ARN for external location"
}

variable "aws_iam_role_arn" {
  type        = string
  default     = ""
  description = "AWS IAM Role ARN assumed by Databricks for S3 access"
}

variable "gcp_storage_bucket_name" {
  type        = string
  default     = ""
  description = "GCP Cloud Storage archive bucket name for external location"
}

variable "enable_unity_catalog" {
  type        = bool
  default     = true
  description = "Enable Unity Catalog schemas (fys_bronze, fys_silver, fys_gold)"
}

variable "enable_sql_warehouse" {
  type        = bool
  default     = true
  description = "Enable Databricks Serverless SQL Warehouse provisioning"
}

variable "enable_secrets" {
  type        = bool
  default     = true
  description = "Enable Databricks secret scopes (aws-credentials, api-keys)"
}

variable "enable_jobs" {
  type        = bool
  default     = true
  description = "Enable Databricks workflow ingestion & matching jobs"
}

variable "sql_warehouse_auto_stop_mins" {
  type        = number
  default     = 10
  description = "Minutes of inactivity before SQL Warehouse auto-stops (cost control)"
}
