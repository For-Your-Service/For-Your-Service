# File: terraform/modules/huggingface/variables.tf
# Description: Hugging Face Module Variables
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment (dev, staging, prod)"
}

variable "space_name" {
  type        = string
  default     = "fys-matching-api"
  description = "Hugging Face Space repository name"
}

variable "space_author" {
  type        = string
  default     = "For-Your-Service"
  description = "Hugging Face organization or username"
}

variable "hardware" {
  type        = string
  default     = "cpu-basic"
  description = "Hugging Face hardware tier (free: cpu-basic, paid: cpu-upgrade, t4-small, etc.)"
}

variable "hf_token" {
  type        = string
  default     = ""
  sensitive   = true
  description = "Hugging Face User Access Token"
}

variable "databricks_host" {
  type        = string
  default     = ""
  description = "Databricks workspace server hostname"
}

variable "databricks_token" {
  type        = string
  default     = ""
  sensitive   = true
  description = "Databricks personal access token for SQL warehouse connection"
}

variable "databricks_http_path" {
  type        = string
  default     = "/sql/1.0/warehouses/fys-default"
  description = "Databricks SQL warehouse HTTP path"
}
