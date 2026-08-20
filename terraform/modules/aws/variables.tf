# File: terraform/modules/aws/variables.tf
# Description: AWS Module Variables
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

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS deployment region"
}

variable "databricks_aws_account_id" {
  type        = string
  default     = "414351767826"
  description = "Databricks production AWS account ID for cross-account assume role"
}

variable "databricks_external_id" {
  type        = string
  default     = "fys-pipeline-external-id"
  description = "Databricks external ID for STS trust verification"
}

variable "owner_email" {
  type        = string
  default     = "whall4.wh@gmail.com"
  description = "Resource owner email for tagging and budget alerts"
}

variable "organization" {
  type        = string
  default     = "7 Eagle Group"
  description = "Organization name"
}

variable "enable_dynamodb" {
  type        = bool
  default     = true
  description = "Enable DynamoDB table provisioning"
}

variable "enable_lambda" {
  type        = bool
  default     = true
  description = "Enable Lambda matching API provisioning"
}

variable "enable_budget_alert" {
  type        = bool
  default     = true
  description = "Enable AWS zero-spend free tier budget alert"
}
