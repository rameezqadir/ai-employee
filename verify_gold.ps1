Write-Host "`n=== GOLD TIER VERIFICATION ===" -ForegroundColor Cyan

# Check business auditor
if (Test-Path "D:\ai-employee\ai-employee-core\utils\business_auditor.py") {
    Write-Host "✅ Business auditor exists" -ForegroundColor Green
} else {
    Write-Host "❌ Business auditor missing" -ForegroundColor Red
}

# Check scheduled task
$task = Get-ScheduledTask -TaskName "AIEmployee-WeeklyAudit" -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "✅ Weekly audit scheduled" -ForegroundColor Green
    Write-Host "   Next run: Sunday 7:00 PM" -ForegroundColor Gray
} else {
    Write-Host "❌ Weekly audit not scheduled" -ForegroundColor Red
}

# Check briefings
$briefings = Get-ChildItem D:\ai-employee\AI_Employee_Vault\Briefings -ErrorAction SilentlyContinue
if ($briefings) {
    Write-Host "✅ Briefings generated ($($briefings.Count) files)" -ForegroundColor Green
} else {
    Write-Host "⚠️  No briefings yet (run business_auditor.py to generate)" -ForegroundColor Yellow
}

# Check agent skills
$skills = Get-ChildItem D:\ai-employee\AI_Employee_Vault\Skills\*.md -ErrorAction SilentlyContinue
if ($skills -and $skills.Count -ge 3) {
    Write-Host "✅ Agent skills created ($($skills.Count) skills)" -ForegroundColor Green
    foreach ($skill in $skills) {
        Write-Host "   - $($skill.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ Insufficient agent skills (need 3+, found $($skills.Count))" -ForegroundColor Red
}

# Check Ralph loop
if (Test-Path "D:\ai-employee\ai-employee-core\ralph_loop.py") {
    Write-Host "✅ Ralph Wiggum Loop exists" -ForegroundColor Green
} else {
    Write-Host "❌ Ralph loop missing" -ForegroundColor Red
}

# Check LinkedIn poster
if (Test-Path "D:\ai-employee\ai-employee-core\watchers\linkedin_poster.py") {
    Write-Host "✅ LinkedIn poster exists" -ForegroundColor Green
} else {
    Write-Host "❌ LinkedIn poster missing" -ForegroundColor Red
}

Write-Host "`n=== END VERIFICATION ===" -ForegroundColor Cyan
Write-Host "Submit at: https://forms.gle/JR9T1SJq5rmQyGkGA" -ForegroundColor Yellow
