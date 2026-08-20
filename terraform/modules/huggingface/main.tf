# File: terraform/modules/huggingface/main.tf
# Description: Hugging Face Module Core Configuration & Locals
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

terraform {
  required_version = ">= 1.3.0"
}

locals {
  space_title           = "For Your Service - Matching API (${var.environment})"
  space_readme_metadata = <<-EOT
---
title: ${local.space_title}
emoji: 🇺🇸
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---
  EOT
}
