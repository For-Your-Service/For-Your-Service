#Requires -Version 5.1
<#
.SYNOPSIS
  Org admin: labels, milestones, and triage vocabulary for For-Your-Service.
#>
param(
    [string]$Repo = "For-Your-Service/For-Your-Service"
)

Write-Host "Setting up labels..." -ForegroundColor Cyan
$labels = @(
    @{ name = "kind/master"; color = "0E8A16"; desc = "Master program tracking issue" },
    @{ name = "kind/epic"; color = "1D76DB"; desc = "Architectural Epic" },
    @{ name = "kind/task"; color = "5319E7"; desc = "Individual execution task" },
    @{ name = "slice/1-plumbing"; color = "FBCA04"; desc = "Slice 1 infrastructure plumbing" },
    @{ name = "ready-for-agent"; color = "0E8A16"; desc = "Fully specified, ready for AFK agent" },
    @{ name = "needs-triage"; color = "FBCA04"; desc = "Needs maintainer triage" },
    @{ name = "needs-info"; color = "D93F0B"; desc = "Waiting on reporter" },
    @{ name = "ready-for-human"; color = "1D76DB"; desc = "Requires human implementation" },
    @{ name = "research"; color = "BFD4F2"; desc = "From architecture research" },
    @{ name = "P0"; color = "B60205"; desc = "Blocker / Slice 1" },
    @{ name = "P1"; color = "D93F0B"; desc = "Differentiator" },
    @{ name = "P2"; color = "C5DEF5"; desc = "Later" }
)

foreach ($l in $labels) {
    gh label create $l.name --color $l.color --description $l.desc --repo $Repo --force 2>$null
}

Write-Host "Setting up Milestones..." -ForegroundColor Cyan
$milestones = @(
    "M0 Truth & safety + org/pipelines",
    "M1 Know yourself",
    "M2 Real match substrate",
    "M3 Serve & UX",
    "M4 Campaign",
    "M5 Partner scale"
)

foreach ($m in $milestones) {
    gh api "repos/$Repo/milestones" -f title="$m" --silent 2>$null
}

Write-Host "Admin setup complete." -ForegroundColor Green
Write-Host "Next: .\scripts\github_admin_close_superseded.ps1"
