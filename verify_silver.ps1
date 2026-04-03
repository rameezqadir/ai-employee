Write-Host "`n=== SILVER TIER VERIFICATION ===" -ForegroundColor Cyan

# Check Gmail authentication
if (Test-Path "D:\ai-employee\ai-employee-core\token.json") {
    Write-Host "✅ Gmail authenticated (token.json exists)" -ForegroundColor Green
} else {
    Write-Host "❌ Gmail not authenticated" -ForegroundColor Red
}

# Check watchers
$watchers = @("filesystem_watcher.py", "gmail_watcher.py")
foreach ($watcher in $watchers) {
    if (Test-Path "D:\ai-employee\ai-employee-core\watchers\$watcher") {
        Write-Host "✅ $watcher exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $watcher missing" -ForegroundColor Red
    }
}

# Check Email MCP server
if (Test-Path "D:\ai-employee\ai-employee-core\mcp_servers\email_mcp\index.js") {
    Write-Host "✅ Email MCP server exists" -ForegroundColor Green
} else {
    Write-Host "❌ Email MCP server missing" -ForegroundColor Red
}

# Check orchestrator
if (Test-Path "D:\ai-employee\ai-employee-core\orchestrator.py") {
    Write-Host "✅ Orchestrator exists" -ForegroundColor Green
} else {
    Write-Host "❌ Orchestrator missing" -ForegroundColor Red
}

# Check approval directories
$dirs = @("Pending_Approval", "Approved", "Rejected")
foreach ($dir in $dirs) {
    if (Test-Path "D:\ai-employee\AI_Employee_Vault\$dir") {
        Write-Host "✅ $dir folder exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $dir folder missing" -ForegroundColor Red
    }
}

# Check Claude MCP config
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    if ($config.mcpServers.email) {
        Write-Host "✅ Email MCP configured in Claude Desktop" -ForegroundColor Green
    } else {
        Write-Host "❌ Email MCP not in Claude config" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Claude config not found" -ForegroundColor Red
}

Write-Host "`n=== END VERIFICATION ===" -ForegroundColor Cyan
Write-Host "Submit at: https://forms.gle/JR9T1SJq5rmQyGkGA" -ForegroundColor Yellow
