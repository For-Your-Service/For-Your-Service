#!/usr/bin/env bash
# File: terraform/scripts/tf_plan_all.sh
# Description: Multi-Cloud Terraform Dry-Run Plan Generator
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

set -euo pipefail

ENV="${1:-dev}"
echo "========================================================"
echo " For Your Service - Multi-Cloud Terraform Plan (${ENV})"
echo "========================================================"

TARGET_DIR="terraform/environments/${ENV}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "[ERROR] Environment directory not found: $TARGET_DIR"
    exit 1
fi

cd "$TARGET_DIR"

if [ ! -f "terraform.tfvars" ]; then
    if [ -f "terraform.tfvars.example" ]; then
        echo "[INFO] Copying terraform.tfvars.example to terraform.tfvars"
        cp terraform.tfvars.example terraform.tfvars
    fi
fi

echo "[1/2] Initializing Terraform..."
terraform init -upgrade

echo "[2/2] Generating Execution Plan..."
terraform plan -out="${ENV}.tfplan"

echo "========================================================"
echo "[SUCCESS] Plan generated: ${TARGET_DIR}/${ENV}.tfplan"
echo "Review the changes above. To apply, run:"
echo "  terraform apply \"${ENV}.tfplan\""
echo "========================================================"
