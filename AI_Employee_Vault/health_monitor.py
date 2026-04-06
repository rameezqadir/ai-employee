"""Health Monitor - Windows Version"""
import psutil
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

vault_path = Path(os.getenv('VAULT_PATH', r'D:\ai-employee\AI_Employee_Vault'))
log_dir = vault_path / 'Logs'
log_dir.mkdir(parents=True, exist_ok=True)

def check_health():
    """Run health checks"""
    issues = []
    
    # Check disk space
    disk = psutil.disk_usage('D:\\')
    if disk.percent > 85:
        issues.append(f'❌ Disk usage high: {disk.percent}%')
    else:
        print(f'✅ Disk usage: {disk.percent}%')
    
    # Check memory
    mem = psutil.virtual_memory()
    if mem.percent > 90:
        issues.append(f'❌ Memory usage high: {mem.percent}%')
    else:
        print(f'✅ Memory usage: {mem.percent}%')
    
    # Check vault exists
    if not vault_path.exists():
        issues.append(f'❌ Vault not found at {vault_path}')
    else:
        print(f'✅ Vault found')
    
    # Check recent activity (files modified in last hour)
    recent_files = 0
    for folder in ['Needs_Action', 'Done', 'Logs']:
        folder_path = vault_path / folder
        if folder_path.exists():
            for file in folder_path.glob('*'):
                if (datetime.now().timestamp() - file.stat().st_mtime) < 3600:
                    recent_files += 1
    
    if recent_files == 0:
        issues.append(f'⚠️  No recent activity (last hour)')
    else:
        print(f'✅ Recent activity: {recent_files} files modified in last hour')
    
    # Log results
    timestamp = datetime.now()
    
    if issues:
        # Log issues
        issue_log = log_dir / 'health_issues.txt'
        with open(issue_log, 'a', encoding='utf-8') as f:
            f.write(f'\n=== {timestamp.isoformat()} ===\n')
            f.write('\n'.join(issues) + '\n')
        
        print(f'\n⚠️  {len(issues)} issues found!')
        for issue in issues:
            print(f'   {issue}')
    else:
        # Log OK
        ok_log = log_dir / 'health_ok.txt'
        with open(ok_log, 'a', encoding='utf-8') as f:
            f.write(f'{timestamp.isoformat()} - All checks passed\n')
        
        print('\n✅ All health checks passed!')
    
    return len(issues) == 0

if __name__ == '__main__':
    check_health()
