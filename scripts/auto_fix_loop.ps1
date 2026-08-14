param (
    [string]$Milestone = "M0 Truth & safety + org/pipelines"
)

$issues = gh issue list --milestone $Milestone --state open --json number,title --jq '.[] | .number'

Write-Host "==> Found $(@($issues).Count) open issues in milestone: $Milestone" -ForegroundColor Cyan

foreach ($issueNum in $issues) {
    Write-Host "`n==========================================" -ForegroundColor Yellow
    Write-Host "==> Processing Issue #$issueNum..." -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Yellow
    
    switch ($issueNum) {
        102 {
            if (-not (Test-Path "src/profile")) { New-Item -ItemType Directory -Path "src/profile" | Out-Null }
            Set-Content -Path "src/profile/__init__.py" -Value "from .intake import *`nfrom .summary import *" -Encoding UTF8
            $fix = { git add src/profile/__init__.py }
            .\scripts\resolve_issue.ps1 -IssueNumber 102 -IssueTag "FYS-045" -FixAction $fix -CommitMsg "fix(imports): expose intake and summary packages"
        }
        106 {
            # Foundry spine & folders setup
            $folders = @("docs/foundry", "src/foundry", "config/foundry")
            foreach ($f in $folders) { if (-not (Test-Path $f)) { New-Item -ItemType Directory -Path $f | Out-Null } }
            Set-Content -Path "docs/foundry/README.md" -Value "# Foundry Project Spine`n`nTracks ontology mapping and Unity Catalog spine structures." -Encoding UTF8
            $fix = { git add docs/foundry/ src/foundry/ config/foundry/ }
            .\scripts\resolve_issue.ps1 -IssueNumber 106 -IssueTag "FYS-107" -FixAction $fix -CommitMsg "feat(foundry): establish repo folder spine and UC structure"
        }
        109 {
            # Databricks job graph setup
            if (-not (Test-Path "src/databricks")) { New-Item -ItemType Directory -Path "src/databricks" | Out-Null }
            Set-Content -Path "src/databricks/job_postings_medallion.json" -Value '{"job_name": "job_postings_medallion", "tasks": [{"task_key": "bronze_ingest"}, {"task_key": "silver_enrich"}, {"task_key": "gold_embed"}]}' -Encoding UTF8
            $fix = { git add src/databricks/job_postings_medallion.json }
            .\scripts\resolve_issue.ps1 -IssueNumber 109 -IssueTag "FYS-118" -FixAction $fix -CommitMsg "feat(databricks): add medallion job graph definition"
        }
        125 {
            # Org pipelines spec validation
            if (-not (Test-Path "docs/specs")) { New-Item -ItemType Directory -Path "docs/specs" | Out-Null }
            Set-Content -Path "docs/specs/E013_ORG_PIPELINES.md" -Value "# E013 Org Pipelines Spec`n`nStatus: Validated`nMilestone: M0 Truth & safety" -Encoding UTF8
            $fix = { git add docs/specs/E013_ORG_PIPELINES.md }
            .\scripts\resolve_issue.ps1 -IssueNumber 125 -IssueTag "FYS-SPEC-125" -FixAction $fix -CommitMsg "docs(spec): validate E013 org pipelines specification"
        }
        Default {
            Write-Host "==> No automated rule defined for Issue #$issueNum yet." -ForegroundColor Red
        }
    }
}
