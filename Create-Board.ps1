Set-Location "$HOME\Projects\for-your-service"

$ProjectOwner = "FreeFades2Black"
$ProjectTitle = "For Your Service - Operational Roadmap"

Write-Host "Creating GitHub Project Board..." -ForegroundColor Cyan
$project = gh project create --owner $ProjectOwner --title $ProjectTitle --format json | ConvertFrom-Json
$ProjectNum = $project.number

Write-Host "Project Created! Project Number: $ProjectNum" -ForegroundColor Green

$DoneTasks = @(
    "Repository Foundation - Base structure, STATUS.md, and architectural README.md",
    "Databricks Analytics Engine - PySpark vector transform, tensor match, Delta exporter",
    "Databricks Workflow Spec - Created config/databricks_job.json pipeline configuration",
    "GCP Ingestion Microservices - Built main.py, anonymizer.py, and validator.py"
)

$InProgressTasks = @(
    "GCP Cloud Function Deployment - Deploy src/ingestion to GCP and create gs://fys-landing-dev bucket"
)

$BacklogTasks = @(
    "Windows Task Scheduler Daemon - Finalize local_ops/Show-Status.ps1 for local 2-hour popups",
    "End-to-End Test Payload - Send dummy JSON through Cloud Function into Databricks Delta Lake"
)

Write-Host "Populating task cards..." -ForegroundColor Cyan

foreach ($task in $DoneTasks) {
    gh project item-create $ProjectNum --owner $ProjectOwner --title "[DONE] $task"
}

foreach ($task in $InProgressTasks) {
    gh project item-create $ProjectNum --owner $ProjectOwner --title "[IN PROGRESS] $task"
}

foreach ($task in $BacklogTasks) {
    gh project item-create $ProjectNum --owner $ProjectOwner --title "[BACKLOG] $task"
}

Write-Host "All tasks successfully auto-populated into your GitHub Project board!" -ForegroundColor Green