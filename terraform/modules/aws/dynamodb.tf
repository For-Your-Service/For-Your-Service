# File: terraform/modules/aws/dynamodb.tf
# Description: AWS DynamoDB Tables for Veterans & Jobs (On-Demand / Free Tier Optimized)
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Veteran Profiles Table
# -----------------------------------------------------------------------------
resource "aws_dynamodb_table" "veterans" {
  count        = var.enable_dynamodb ? 1 : 0
  name         = "${var.project_name}-veterans-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "veteran_id"

  attribute {
    name = "veteran_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  ttl {
    attribute_name = "session_expiry"
    enabled        = true
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-veterans-${var.environment}"
  })
}

# -----------------------------------------------------------------------------
# 2. Job Postings Table
# -----------------------------------------------------------------------------
resource "aws_dynamodb_table" "jobs" {
  count        = var.enable_dynamodb ? 1 : 0
  name         = "${var.project_name}-jobs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "job_id"

  attribute {
    name = "job_id"
    type = "S"
  }

  attribute {
    name = "source"
    type = "S"
  }

  attribute {
    name = "posted_date"
    type = "S"
  }

  global_secondary_index {
    name            = "source-date-index"
    hash_key        = "source"
    range_key       = "posted_date"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  ttl {
    attribute_name = "job_expiry"
    enabled        = true
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-jobs-${var.environment}"
  })
}
