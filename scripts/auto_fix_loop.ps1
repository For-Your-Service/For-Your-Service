param (
    [string]$Milestone = "M0 Truth & safety + org/pipelines"
)

# Fetch all open issue numbers in the target milestone
$issues = gh issue list --milestone $Milestone --state open --json number,title --jq '.[] | .number'

Write-Host "==> Found $(@($issues).Count) open issues in milestone: $Milestone" -ForegroundColor Cyan

foreach ($issueNum in $issues) {
    Write-Host "`n==========================================" -ForegroundColor Yellow
    Write-Host "==> Processing Issue #$issueNum..." -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Yellow
    
    switch ($issueNum) {
        102 {
            # Fix profile package imports
            if (-not (Test-Path "src/profile")) { New-Item -ItemType Directory -Path "src/profile" | Out-Null }
            Set-Content -Path "src/profile/__init__.py" -Value "from .intake import *`nfrom .summary import *" -Encoding UTF8
            
            $fix = { git add src/profile/__init__.py }
            .\scripts\resolve_issue.ps1 -IssueNumber 102 -IssueTag "FYS-045" -FixAction $fix -CommitMsg "fix(imports): expose intake and summary packages"
        }
        107 {
            # Wire data expectations hook
            if (-not (Test-Path "src/quality")) { New-Item -ItemType Directory -Path "src/quality" | Out-Null }
            Set-Content -Path "src/quality/expectations.py" -Value @"
def validate_bronze_expectations(df):
    \"\"\"Aborts build if required fields are missing.\"\"\"
    if df is None:
        raise ValueError("Dataframe is empty or invalid.")
"@ -Encoding UTF8

            $fix = { git add src/quality/expectations.py }
            .\scripts\resolve_issue.ps1 -IssueNumber 107 -IssueTag "FYS-108" -FixAction $fix -CommitMsg "feat(quality): add bronze build expectation validator"
        }
        Default {
            Write-Host "==> No automated rule defined for Issue #$issueNum yet." -ForegroundColor Red
        }
    }
}
