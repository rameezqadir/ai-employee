Write-Host "`n=== BRONZE TIER VERIFICATION ===" -ForegroundColor Cyan

# Check directory structure
if (Test-Path "D:\ai-employee\AI_Employee_Vault") {
    Write-Host "✅ Vault exists" -ForegroundColor Green
} else {
    Write-Host "❌ Vault missing" -ForegroundColor Red
}

# Check core files
$coreFiles = @("Dashboard.md", "CLAUDE.md", "Company_Handbook.md", "Business_Goals.md")
foreach ($file in $coreFiles) {
    if (Test-Path "D:\ai-employee\AI_Employee_Vault\$file") {
        Write-Host "✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing" -ForegroundColor Red
    }
}

# Check watcher
if (Test-Path "D:\ai-employee\ai-employee-core\watchers\filesystem_watcher.py") {
    Write-Host "✅ Filesystem watcher exists" -ForegroundColor Green
} else {
    Write-Host "❌ Watcher missing" -ForegroundColor Red
}

# Check Claude config
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $configPath) {
    Write-Host "✅ Claude MCP config exists" -ForegroundColor Green
    $config = Get-Content $configPath | ConvertFrom-Json
    if ($config.mcpServers.filesystem) {
        Write-Host "✅ Filesystem MCP configured" -ForegroundColor Green
    } else {
        Write-Host "❌ Filesystem MCP not configured" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Claude config missing" -ForegroundColor Red
}

Write-Host "`n=== Submit at: https://forms.gle/JR9T1SJq5rmQyGkGA ===" -ForegroundColor Yellow
