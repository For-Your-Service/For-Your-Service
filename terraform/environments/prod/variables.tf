# File: terraform/environments/prod/variables.tf
# Description: Production Environment Variables
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

variable "project_name" {
  type    = string
  default = "foryourservice"
}

variable "owner_email" {
  type    = string
  default = "whall4.wh@gmail.com"
}

variable "organization" {
  type    = string
  default = "7 Eagle Group"
}

variable "enable_aws" {
  type    = bool
  default = true
}

variable "enable_gcp" {
  type    = bool
  default = true
}

variable "enable_databricks" {
  type    = bool
  default = true
}

variable "enable_huggingface" {
  type    = bool
  default = true
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "aws_databricks_account_id" {
  type    = string
  default = "414351767826"
}

variable "aws_databricks_external_id" {
  type    = string
  default = "fys-pipeline-external-id"
}

variable "gcp_project_id" {
  type    = string
  default = "for-your-service-prod"
}

variable "gcp_region" {
  type    = string
  default = "us-central1"
}

variable "databricks_host" {
  type    = string
  default = "https://dbc-3e95d032-684c.cloud.databricks.com"
}

variable "databricks_token" {
  type      = string
  default   = ""
  sensitive = true
}

variable "hf_token" {
  type      = string
  default   = ""
  sensitive = true
}

variable "hf_space_name" {
  type    = string
  default = "fys-matching-api"
}
