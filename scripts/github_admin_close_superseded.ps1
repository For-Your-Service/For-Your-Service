#Requires -Version 5.1
<#
.SYNOPSIS
  Org admin: close all [SUPERSEDED] legacy issues and apply triage labels.
#>
$Repo = "For-Your-Service/For-Your-Service"
$toClose = 1..16 + 21..24

Write-Host "Closing superseded issues..."
foreach ($n in $toClose) {
  gh issue close $n --repo $Repo --comment "Closed as superseded by MASTER #112 architecture program / SPECs." 2>$null
  if ($LASTEXITCODE -eq 0) { Write-Host "Closed #$n" } else { Write-Host "Skip/fail #$n" }
}

Write-Host "Applying ready-for-agent to SPEC issues 113-125..."
113..125 | ForEach-Object {
  gh issue edit $_ --repo $Repo --add-label "ready-for-agent" 2>$null
}

Write-Host "Done. Also run scripts/github_admin_setup.ps1 if labels/milestones missing."
