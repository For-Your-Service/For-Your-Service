# File: terraform/modules/aws/s3.tf
# Description: AWS S3 Data Lake, Staging, Resume & Model Buckets (Free Tier Optimized)
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Primary Data Lake Bucket (foryourservice-data-prod)
# -----------------------------------------------------------------------------
resource "aws_s3_bucket" "data_prod" {
  bucket        = "${var.project_name}-data-${var.environment}-${random_id.aws_suffix.hex}"
  force_destroy = var.environment != "prod"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-data-${var.environment}"
    Tier = "DataLake"
  })
}

resource "aws_s3_bucket_public_access_block" "data_prod_privacy" {
  bucket                  = aws_s3_bucket.data_prod.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_prod_encryption" {
  bucket = aws_s3_bucket.data_prod.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "data_prod_versioning" {
  bucket = aws_s3_bucket.data_prod.id

  versioning_configuration {
    status = "Enabled"
  }
}

# -----------------------------------------------------------------------------
# 2. Pipeline Staging Bucket (for Databricks / Fast ingestion)
# -----------------------------------------------------------------------------
resource "aws_s3_bucket" "staging" {
  bucket        = "${var.project_name}-staging-${var.environment}-${random_id.aws_suffix.hex}"
  force_destroy = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-staging-${var.environment}"
    Tier = "Staging"
  })
}

resource "aws_s3_bucket_public_access_block" "staging_privacy" {
  bucket                  = aws_s3_bucket.staging.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "staging_encryption" {
  bucket = aws_s3_bucket.staging.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Free tier lifecycle: auto-expire temporary staging objects after 14 days
resource "aws_s3_bucket_lifecycle_configuration" "staging_lifecycle" {
  bucket = aws_s3_bucket.staging.id

  rule {
    id     = "expire-temporary-staging-data"
    status = "Enabled"

    expiration {
      days = 14
    }
  }
}

# -----------------------------------------------------------------------------
# 3. Veteran Resumes Bucket (Secure storage)
# -----------------------------------------------------------------------------
resource "aws_s3_bucket" "resumes" {
  bucket        = "${var.project_name}-resumes-${var.environment}-${random_id.aws_suffix.hex}"
  force_destroy = var.environment != "prod"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-resumes-${var.environment}"
    Tier = "Resumes"
  })
}

resource "aws_s3_bucket_public_access_block" "resumes_privacy" {
  bucket                  = aws_s3_bucket.resumes.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "resumes_encryption" {
  bucket = aws_s3_bucket.resumes.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# -----------------------------------------------------------------------------
# 4. Neural Network Models Bucket (Model weights & artifacts)
# -----------------------------------------------------------------------------
resource "aws_s3_bucket" "models" {
  bucket        = "${var.project_name}-models-${var.environment}-${random_id.aws_suffix.hex}"
  force_destroy = var.environment != "prod"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-models-${var.environment}"
    Tier = "ModelArtifacts"
  })
}

resource "aws_s3_bucket_public_access_block" "models_privacy" {
  bucket                  = aws_s3_bucket.models.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "models_encryption" {
  bucket = aws_s3_bucket.models.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
