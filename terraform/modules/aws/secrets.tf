# File: terraform/modules/aws/secrets.tf
# Description: AWS Secrets Manager for For-Your-Service API Keys
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

resource "aws_secretsmanager_secret" "fys_secrets" {
  name                    = "${var.project_name}/api-keys-${var.environment}"
  description             = "API Keys for USAJOBS, JSearch, Adzuna, and Databricks tokens"
  recovery_window_in_days = var.environment == "prod" ? 30 : 0

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-secrets-${var.environment}"
  })
}

resource "aws_secretsmanager_secret_version" "fys_secrets_default" {
  secret_id = aws_secretsmanager_secret.fys_secrets.id
  secret_string = jsonencode({
    USAJOBS_API_KEY    = ""
    USAJOBS_USER_AGENT = "whall4.wh@gmail.com"
    JSEARCH_API_KEY    = ""
    ADZUNA_APP_ID      = ""
    ADZUNA_APP_KEY     = ""
    DATABRICKS_TOKEN   = ""
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}
