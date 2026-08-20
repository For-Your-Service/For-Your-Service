# File: terraform/modules/aws/lambda.tf
# Description: AWS Lambda Function for Serverless Matching & Intake API
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

# -----------------------------------------------------------------------------
# Archive inline Lambda payload
# -----------------------------------------------------------------------------
data "archive_file" "lambda_dummy_zip" {
  count       = var.enable_lambda ? 1 : 0
  type        = "zip"
  output_path = "${path.module}/lambda_dummy.zip"

  source {
    content  = <<-EOT
      import json

      def handler(event, context):
          return {
              "statusCode": 200,
              "headers": {"Content-Type": "application/json"},
              "body": json.dumps({
                  "status": "healthy",
                  "service": "For Your Service - Serverless Matching API",
                  "version": "1.0.0"
              })
          }
    EOT
    filename = "index.py"
  }
}

# -----------------------------------------------------------------------------
# Lambda Function: foryourservice-match-api
# -----------------------------------------------------------------------------
resource "aws_lambda_function" "match_api" {
  count         = var.enable_lambda ? 1 : 0
  function_name = "${var.project_name}-match-api-${var.environment}"
  role          = aws_iam_role.lambda_exec_role[0].arn
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256

  filename         = data.archive_file.lambda_dummy_zip[0].output_path
  source_code_hash = data.archive_file.lambda_dummy_zip[0].output_base64sha256

  environment {
    variables = {
      ENVIRONMENT         = var.environment
      DYNAMODB_VETERANS   = var.enable_dynamodb ? aws_dynamodb_table.veterans[0].name : ""
      DYNAMODB_JOBS       = var.enable_dynamodb ? aws_dynamodb_table.jobs[0].name : ""
      S3_DATA_BUCKET      = aws_s3_bucket.data_prod.id
      S3_MODELS_BUCKET    = aws_s3_bucket.models.id
    }
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-match-api-${var.environment}"
  })
}

# -----------------------------------------------------------------------------
# CloudWatch Log Group with 14-day retention for Free Tier compliance
# -----------------------------------------------------------------------------
resource "aws_cloudwatch_log_group" "lambda_logs" {
  count             = var.enable_lambda ? 1 : 0
  name              = "/aws/lambda/${aws_lambda_function.match_api[0].function_name}"
  retention_in_days = 14

  tags = local.common_tags
}
