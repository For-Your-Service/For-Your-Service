# File: terraform/modules/gcp/variables.tf
# Description: GCP Module Variables
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

variable "project_id" {
  type        = string
  default     = "for-your-service-prod"
  description = "Target GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Target GCP region (Free Tier friendly: us-central1, us-east1, us-west1)"
}

variable "owner_email" {
  type        = string
  default     = "whall4.wh@gmail.com"
  description = "Resource owner email for labels"
}

variable "organization" {
  type        = string
  default     = "7 Eagle Group"
  description = "Organization name"
}

variable "enable_bigquery" {
  type        = bool
  default     = true
  description = "Enable BigQuery dataset and table provisioning"
}

variable "enable_cloud_functions" {
  type        = bool
  default     = true
  description = "Enable GCP Cloud Functions for veteran intake"
}
