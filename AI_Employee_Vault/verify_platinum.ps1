Write-Host "`n=== PLATINUM TIER VERIFICATION ===" -ForegroundColor Cyan

# Check service (if using NSSM)
$service = Get-Service -Name "AIEmployee" -ErrorAction SilentlyContinue
if ($service -and $service.Status -eq 'Running') {
    Write-Host "✅ Windows Service running" -ForegroundColor Green
} else {
    Write-Host "⚠️  Service not running (check NSSM setup)" -ForegroundColor Yellow
}

# Check vault sync
if (Test-Path "D:\ai-employee\AI_Employee_Vault\.git") {
    Write-Host "✅ Vault git enabled" -ForegroundColor Green
} else {
    Write-Host "❌ Vault not git repo" -ForegroundColor Red
}

# Check sync task
$syncTask = Get-ScheduledTask -TaskName "AIEmployee-VaultSync" -ErrorAction SilentlyContinue
if ($syncTask) {
    Write-Host "✅ Auto-sync scheduled (every 5 min)" -ForegroundColor Green
} else {
    Write-Host "❌ Sync not scheduled" -ForegroundColor Red
}

# Check health monitoring
$healthTask = Get-ScheduledTask -TaskName "AIEmployee-HealthCheck" -ErrorAction SilentlyContinue
if ($healthTask) {
    Write-Host "✅ Health monitoring scheduled (every 15 min)" -ForegroundColor Green
} else {
    Write-Host "❌ Health not scheduled" -ForegroundColor Red
}

Write-Host "`n=== PLATINUM COMPLETE! ===" -ForegroundColor Green
Write-Host "Submit: https://forms.gle/JR9T1SJq5rmQyGkGA" -ForegroundColor Yellow
