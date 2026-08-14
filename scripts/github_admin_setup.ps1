# GitHub Admin Setup Script for For-Your-Service Architecture Program
param(
    [string]$Repo = "For-Your-Service/For-Your-Service"
)

Write-Host "Setting up labels..." -ForegroundColor Cyan
$labels = @(
    @{ name = "kind/master"; color = "0E8A16"; desc = "Master program tracking issue" },
    @{ name = "kind/epic"; color = "1D76DB"; desc = "Architectural Epic" },
    @{ name = "kind/task"; color = "5319E7"; desc = "Individual execution task" },
    @{ name = "slice/1-plumbing"; color = "FBCA04"; desc = "Slice 1 infrastructure plumbing" }
)

foreach ($l in $labels) {
    gh label create $l.name --color $l.color --description $l.desc --repo $Repo --force
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
