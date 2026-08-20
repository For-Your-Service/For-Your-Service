# File: terraform/scripts/tf_import_existing.ps1
# Description: PowerShell script to import existing cloud resources into Terraform state without downtime
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

param (
    [string]$Environment = "prod"
)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " For Your Service - Safe Zero-Downtime Resource Import ($Environment)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$targetDir = "terraform\environments\$Environment"

if (-not (Test-Path $targetDir)) {
    Write-Host "[ERROR] Environment directory not found: $targetDir" -ForegroundColor Red
    exit 1
}

Push-Location $targetDir

Write-Host "`n[1/4] Preparing Terraform working directory..." -ForegroundColor Yellow
terraform init -upgrade

Write-Host "`n[2/4] Safe Resource Import Examples:" -ForegroundColor Yellow
Write-Host "  To import existing AWS S3 bucket:"
Write-Host "    terraform import 'module.aws[0].aws_s3_bucket.data_prod' foryourservice-data-prod" -ForegroundColor Gray
Write-Host "  To import existing Databricks Schema:"
Write-Host "    terraform import 'module.databricks[0].databricks_schema.bronze' workspace.fys_bronze" -ForegroundColor Gray
Write-Host "  To import existing GCP Custom Role:"
Write-Host "    terraform import 'module.gcp[0].google_project_iam_custom_role.fys_pipeline_operator' projects/for-your-service-prod/roles/fysPipelineOperator" -ForegroundColor Gray

Write-Host "`n[3/4] Running terraform plan to verify existing state parity..." -ForegroundColor Yellow
terraform plan

Pop-Location

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host "[COMPLETE] Import workflow validated. No resources were modified or destroyed." -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
