# Sync vault to GitHub
$ErrorActionPreference = 'SilentlyContinue'
cd D:\ai-employee\AI_Employee_Vault
git pull origin main 2>&1 | Out-Null
git add .
git commit -m "Auto-sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" 2>&1 | Out-Null
git push origin main 2>&1 | Out-Null
"Synced at $(Get-Date -Format 'HH:mm:ss')" | Out-File -Append D:\ai-employee\AI_Employee_Vault\Logs\sync.log
