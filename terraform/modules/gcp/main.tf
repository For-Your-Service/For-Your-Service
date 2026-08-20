# File: terraform/modules/gcp/main.tf
# Description: GCP Module Core Configuration and Random Suffix
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

terraform {
  required_version = ">= 1.3.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

resource "random_id" "gcp_suffix" {
  byte_length = 4
}

locals {
  resource_prefix = "${var.project_name}-${var.environment}"
  common_labels = {
    project      = var.project_name
    environment  = var.environment
    managed_by   = "terraform"
    owner        = replace(replace(var.owner_email, "@", "-at-"), ".", "-dot-")
    organization = "7-eagle-group"
  }
}
