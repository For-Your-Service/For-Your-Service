# File: versions.tf
# Description: Terraform and provider version constraints
# Organization: 7 Eagle Group

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }

  # Optional: Backend configuration for remote state
  # Uncomment and configure for team collaboration
  # backend "s3" {
  #   bucket         = "fys-terraform-state"
  #   key            = "aws/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "fys-terraform-locks"
  # }
}
