terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type        = string
  description = "The GCP Project ID for the For-Your-Service project"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Target GCP region"
}

resource "google_project_iam_custom_role" "fys_pipeline_operator" {
  role_id     = "fysPipelineOperator"
  title       = "For-Your-Service Pipeline Operator"
  description = "Custom role with specific permissions for managing data ingestion, GCS buckets, and Databricks pipeline connectors."
  stage       = "GA"
  permissions = [
    "storage.buckets.get",
    "storage.buckets.list",
    "storage.objects.create",
    "storage.objects.delete",
    "storage.objects.get",
    "storage.objects.list",
    "resourcemanager.projects.get"
  ]
}
