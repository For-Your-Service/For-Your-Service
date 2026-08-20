#!/usr/bin/env bash
# File: terraform/scripts/tf_apply_all.sh
# Description: Multi-Cloud Terraform Apply with Confirmation and Safety Checks
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

set -euo pipefail

ENV="${1:-dev}"
echo "========================================================"
echo " For Your Service - Multi-Cloud Terraform Apply (${ENV})"
echo "========================================================"

TARGET_DIR="terraform/environments/${ENV}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "[ERROR] Environment directory not found: $TARGET_DIR"
    exit 1
fi

cd "$TARGET_DIR"

if [ -f "${ENV}.tfplan" ]; then
    echo "[INFO] Applying verified saved plan: ${ENV}.tfplan"
    terraform apply "${ENV}.tfplan"
    rm -f "${ENV}.tfplan"
else
    echo "[INFO] Running terraform apply directly..."
    terraform apply
fi

echo "========================================================"
echo "[SUCCESS] Multi-cloud deployment complete for ${ENV}!"
echo "========================================================"
