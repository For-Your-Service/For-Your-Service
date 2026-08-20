# File: terraform/variables.tf
# Description: Root Multi-Cloud Variables & Feature Flags
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# Global / Environment Settings
# -----------------------------------------------------------------------------
variable "environment" {
  type        = string
  default     = "dev"
  description = "Target deployment environment (dev, staging, prod)"
}

variable "project_name" {
  type        = string
  default     = "foryourservice"
  description = "Project name prefix for all cloud resources"
}

variable "owner_email" {
  type        = string
  default     = "whall4.wh@gmail.com"
  description = "Resource owner email for tagging and notifications"
}

variable "organization" {
  type        = string
  default     = "7 Eagle Group"
  description = "Organization name for resource tagging"
}

# -----------------------------------------------------------------------------
# Cloud Provider Activation Feature Flags
# -----------------------------------------------------------------------------
variable "enable_aws" {
  type        = bool
  default     = true
  description = "Enable AWS infrastructure module (S3, DynamoDB, Lambda, IAM)"
}

variable "enable_gcp" {
  type        = bool
  default     = true
  description = "Enable GCP infrastructure module (GCS, BigQuery, Cloud Functions)"
}

variable "enable_databricks" {
  type        = bool
  default     = true
  description = "Enable Databricks module (Unity Catalog, SQL Warehouse, Secrets, Jobs)"
}

variable "enable_huggingface" {
  type        = bool
  default     = true
  description = "Enable Hugging Face Space module (FastAPI Space config & secrets)"
}

# -----------------------------------------------------------------------------
# AWS Specific Variables
# -----------------------------------------------------------------------------
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS target deployment region"
}

variable "aws_databricks_account_id" {
  type        = string
  default     = "414351767826"
  description = "Databricks production AWS account ID for IAM trust"
}

variable "aws_databricks_external_id" {
  type        = string
  default     = "fys-pipeline-external-id"
  description = "Databricks STS AssumeRole external ID"
}

# -----------------------------------------------------------------------------
# GCP Specific Variables
# -----------------------------------------------------------------------------
variable "gcp_project_id" {
  type        = string
  default     = "for-your-service-prod"
  description = "GCP Project ID"
}

variable "gcp_region" {
  type        = string
  default     = "us-central1"
  description = "GCP primary region (Free tier friendly)"
}

# -----------------------------------------------------------------------------
# Databricks Specific Variables
# -----------------------------------------------------------------------------
variable "databricks_host" {
  type        = string
  default     = "https://dbc-3e95d032-684c.cloud.databricks.com"
  description = "Databricks workspace URL"
}

variable "databricks_token" {
  type        = string
  default     = ""
  sensitive   = true
  description = "Databricks Personal Access Token (or OAuth token)"
}

# -----------------------------------------------------------------------------
# Hugging Face Specific Variables
# -----------------------------------------------------------------------------
variable "hf_token" {
  type        = string
  default     = ""
  sensitive   = true
  description = "Hugging Face User Access Token"
}

variable "hf_space_name" {
  type        = string
  default     = "fys-matching-api"
  description = "Hugging Face Space repository name"
}

variable "hf_space_hardware" {
  type        = string
  default     = "cpu-basic"
  description = "Hugging Face Space hardware tier (default: free cpu-basic)"
}
