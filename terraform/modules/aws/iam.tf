# File: terraform/modules/aws/iam.tf
# Description: AWS IAM Roles, Policies, and Least-Privilege Access Controls
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# 1. Custom Least-Privilege Policy: ForYourServicePolicy
# -----------------------------------------------------------------------------
resource "aws_iam_policy" "for_your_service_policy" {
  name        = "${local.resource_prefix}-policy"
  description = "Least-privilege policy scoped strictly to ForYourService resources"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3ResourceAccess"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.project_name}-*",
          "arn:aws:s3:::${var.project_name}-*/*",
          "arn:aws:s3:::fys-*",
          "arn:aws:s3:::fys-*/*"
        ]
      },
      {
        Sid    = "DynamoDBResourceAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem"
        ]
        Resource = [
          "arn:aws:dynamodb:${var.aws_region}:*:table/${var.project_name}-*",
          "arn:aws:dynamodb:${var.aws_region}:*:table/fys-*"
        ]
      },
      {
        Sid    = "SecretsManagerAccess"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          "arn:aws:secretsmanager:${var.aws_region}:*:secret:${var.project_name}/*",
          "arn:aws:secretsmanager:${var.aws_region}:*:secret:fys/*"
        ]
      },
      {
        Sid    = "CloudWatchLogging"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda/${var.project_name}-*:*"
      }
    ]
  })

  tags = local.common_tags
}

# -----------------------------------------------------------------------------
# 2. Databricks Cross-Account STS Assume Role
# -----------------------------------------------------------------------------
resource "aws_iam_role" "databricks_s3_role" {
  name        = "${local.resource_prefix}-databricks-s3-role"
  description = "Role assumed by Databricks Unity Catalog to read/write staging and data lake S3 buckets"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.databricks_aws_account_id}:root"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.databricks_external_id
          }
        }
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_policy" "databricks_s3_policy" {
  name        = "${local.resource_prefix}-databricks-s3-policy"
  description = "Grants Databricks read/write to S3 staging & prod data buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          aws_s3_bucket.staging.arn,
          "${aws_s3_bucket.staging.arn}/*",
          aws_s3_bucket.data_prod.arn,
          "${aws_s3_bucket.data_prod.arn}/*"
        ]
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "attach_databricks_s3" {
  role       = aws_iam_role.databricks_s3_role.name
  policy_arn = aws_iam_policy.databricks_s3_policy.arn
}

# -----------------------------------------------------------------------------
# 3. Lambda Execution Role
# -----------------------------------------------------------------------------
resource "aws_iam_role" "lambda_exec_role" {
  count       = var.enable_lambda ? 1 : 0
  name        = "${local.resource_prefix}-lambda-exec-role"
  description = "Execution role for ForYourService Lambda matching and intake functions"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "attach_lambda_policy" {
  count      = var.enable_lambda ? 1 : 0
  role       = aws_iam_role.lambda_exec_role[0].name
  policy_arn = aws_iam_policy.for_your_service_policy.arn
}
