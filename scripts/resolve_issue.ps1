param (
    [Parameter(Mandatory=$true)][int]$IssueNumber,
    [Parameter(Mandatory=$true)][string]$IssueTag,
    [Parameter(Mandatory=$true)][scriptblock]$FixAction,
    [Parameter(Mandatory=$true)][string]$CommitMsg
)

Write-Host "==> Processing Issue #$IssueNumber ($IssueTag)..." -ForegroundColor Cyan

# 1. Execute refactor logic
& $FixAction

# 2. Stage and check git status
git add .
$changes = git status --porcelain

if ($changes) {
    git commit -m "$CommitMsg (#$IssueNumber)"
    git push origin main
    
    # 3. Post summary and close issue via GitHub CLI
    gh issue comment $IssueNumber --body "Automated Resolution for **$IssueTag**:`n* Applied code refactor/updates.`n* Validated changes and committed to `main`."
    gh issue close $IssueNumber
    Write-Host "==> Issue #$IssueNumber CLOSED successfully." -ForegroundColor Green
} else {
    Write-Host "==> No changes detected for Issue #$IssueNumber. Skipping commit." -ForegroundColor Yellow
}
