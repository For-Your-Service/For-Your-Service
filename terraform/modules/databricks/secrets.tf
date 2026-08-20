# File: terraform/modules/databricks/secrets.tf
# Description: Databricks Secret Scopes for AWS and Job Board API Integrations
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. AWS Credentials Secret Scope
# -----------------------------------------------------------------------------
resource "databricks_secret_scope" "aws_credentials" {
  count = var.enable_secrets ? 1 : 0
  name  = "aws-credentials"

  lifecycle {
    prevent_destroy = false
  }
}

# -----------------------------------------------------------------------------
# 2. API Keys Secret Scope (USAJOBS, JSearch, Adzuna)
# -----------------------------------------------------------------------------
resource "databricks_secret_scope" "api_keys" {
  count = var.enable_secrets ? 1 : 0
  name  = "api-keys"

  lifecycle {
    prevent_destroy = false
  }
}
