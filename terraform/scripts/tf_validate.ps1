# File: terraform/scripts/tf_validate.ps1
# Description: Validates and Formats all Terraform configurations across modules and environments
# Lead Architect: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

Write-Host "=== Validating For Your Service Terraform Configurations ===" -ForegroundColor Cyan

$directories = @(
    "terraform",
    "terraform\modules\aws",
    "terraform\modules\gcp",
    "terraform\modules\databricks",
    "terraform\modules\huggingface",
    "terraform\environments\dev",
    "terraform\environments\staging",
    "terraform\environments\prod"
)

$hasErrors = $false

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "`n--> Checking directory: $dir" -ForegroundColor Yellow
        Push-Location $dir
        try {
            terraform fmt -check
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Formatting issues found in $dir. Run 'terraform fmt' to fix." -ForegroundColor Red
                $hasErrors = $true
            } else {
                Write-Host "Formatting OK: $dir" -ForegroundColor Green
            }
        } catch {
            Write-Host "Error executing terraform in $dir" -ForegroundColor Red
            $hasErrors = $true
        }
        Pop-Location
    }
}

if ($hasErrors) {
    Write-Host "`n[FAIL] Validation encountered issues." -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n[SUCCESS] All Terraform files formatted and valid!" -ForegroundColor Green
}
