# ==============================================================================
# Script: scripts/setup_health_scheduler.ps1
# Description: Registers a Windows Scheduled Task to run the health monitor twice daily
# Author: Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group
# ==============================================================================

$taskName = "ForYourService-HealthCheck"
$pythonPath = "C:\Users\FreeF\projects\For-Your-Service\venv\Scripts\python.exe"
$scriptPath = "C:\Users\FreeF\projects\For-Your-Service\scripts\system_health_monitor.py"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " Registering Windows Scheduled Task: $taskName" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# Define Triggers: 09:00 AM and 09:00 PM Daily
$trigger1 = New-ScheduledTaskTrigger -Daily -At 9:00AM
$trigger2 = New-ScheduledTaskTrigger -Daily -At 9:00PM

# Define Action
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`" --push" -WorkingDirectory "C:\Users\FreeF\projects\For-Your-Service"

# Register Task
try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $taskName -Trigger @($trigger1, $trigger2) -Action $action -Description "Automated twice-daily system & application health check for For Your Service"
    Write-Host "[SUCCESS] Task '$taskName' successfully registered to run daily at 9:00 AM and 9:00 PM!" -ForegroundColor Green
} catch {
    Write-Host "[!] Note on registration: $($_.Exception.Message)" -ForegroundColor Yellow
}
