# File: terraform/modules/huggingface/outputs.tf
# Description: Hugging Face Module Resource Outputs
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

output "space_url" {
  value       = "https://${var.space_author}-${var.space_name}-${var.environment}.hf.space"
  description = "Hugging Face Space public application URL"
}

output "space_repo_url" {
  value       = "https://huggingface.co/spaces/${var.space_author}/${var.space_name}-${var.environment}"
  description = "Hugging Face Space repository URL"
}

output "space_config_manifest" {
  value       = local.space_readme_metadata
  description = "Hugging Face Space README metadata configuration"
}
