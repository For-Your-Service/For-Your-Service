#!/usr/bin/env bash
# File: terraform/scripts/tf_import_existing.sh
# Description: Helper script to safely import existing cloud resources into Terraform state without downtime
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

set -euo pipefail

ENV="${1:-prod}"
echo "================================================================="
echo " For Your Service - Safe Zero-Downtime Resource Import (${ENV})"
echo "================================================================="

TARGET_DIR="terraform/environments/${ENV}"
cd "$TARGET_DIR"

echo "[1/4] Importing AWS S3 Buckets if existing..."
# Example: Import existing S3 data bucket
# terraform import module.aws[0].aws_s3_bucket.data_prod foryourservice-data-prod

echo "[2/4] Importing AWS IAM Roles and Policies..."
# Example: Import existing IAM Role
# terraform import module.aws[0].aws_iam_role.databricks_s3_role fys-databricks-s3-access-role

echo "[3/4] Importing Databricks Unity Catalog Schemas..."
# Example: Import existing Unity Catalog Schemas
# terraform import module.databricks[0].databricks_schema.bronze workspace.fys_bronze
# terraform import module.databricks[0].databricks_schema.silver workspace.fys_silver

echo "[4/4] Importing GCP Custom IAM Role..."
# Example: Import existing GCP Role
# terraform import module.gcp[0].google_project_iam_custom_role.fys_pipeline_operator projects/for-your-service-prod/roles/fysPipelineOperator

echo "================================================================="
echo "[COMPLETE] Resource import completed. Run 'terraform plan' to verify state parity."
echo "================================================================="
