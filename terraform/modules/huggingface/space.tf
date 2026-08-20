# File: terraform/modules/huggingface/space.tf
# Description: Hugging Face Space Manifest & Deployment Specification
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# Generate local deployment configuration bundle for Hugging Face Space sync
resource "local_file" "space_metadata_file" {
  content  = local.space_readme_metadata
  filename = "${path.module}/dist/README.md"
}

resource "local_file" "space_env_template" {
  content  = <<-EOT
    # Hugging Face Space Environment Configuration (${var.environment})
    SPACE_NAME=${var.space_name}-${var.environment}
    HARDWARE=${var.hardware}
    APP_PORT=7860
    ENVIRONMENT=${var.environment}
  EOT
  filename = "${path.module}/dist/.env.space"
}
