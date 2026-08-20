# File: terraform/modules/huggingface/secrets.tf
# Description: Hugging Face Space Secret Synchronizer Definition
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# Local manifest of required Space secrets for automated CI/CD and CLI push
resource "local_file" "space_secrets_manifest" {
  content = jsonencode({
    space = "${var.space_author}/${var.space_name}-${var.environment}"
    secrets = {
      DATABRICKS_SERVER_HOSTNAME = var.databricks_host
      DATABRICKS_HTTP_PATH       = var.databricks_http_path
      DATABRICKS_TOKEN           = var.databricks_token != "" ? "configured" : "missing"
    }
  })
  filename = "${path.module}/dist/space_secrets.json"
}
