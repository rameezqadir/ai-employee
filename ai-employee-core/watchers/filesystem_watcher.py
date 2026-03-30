"""Filesystem Watcher - Monitors drop folder"""
import time
import shutil
import logging
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
vault_path = Path(os.getenv('VAULT_PATH', r'D:\ai-employee\AI_Employee_Vault'))
watch_folder = Path(os.getenv('DROP_FOLDER', r'D:\ai-employee\drop_folder'))
needs_action = vault_path / 'Needs_Action'
processed = set()

# Logging setup
log_dir = vault_path / 'Logs'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'watcher.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Ensure directories exist
watch_folder.mkdir(parents=True, exist_ok=True)
needs_action.mkdir(parents=True, exist_ok=True)

logging.info(f'🔍 Watching: {watch_folder}')

while True:
    for f in watch_folder.glob('*'):
        if f.is_file() and str(f) not in processed:
            # Create timestamp
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Copy file to Needs_Action
            dest = needs_action / f'FILE_{ts}_{f.name}'
            shutil.copy2(f, dest)
            
            # Create metadata markdown file
            meta = dest.with_suffix('.md')
            meta_content = f'''---
type: file_drop
file: {f.name}
detected: {datetime.now().isoformat()}
status: pending
---

New file dropped: {f.name}

## Required Actions
- [ ] Review file
- [ ] Process and categorize
- [ ] Move to appropriate folder

## File Details
- Original name: {f.name}
- Size: {f.stat().st_size} bytes
- Detected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
            meta.write_text(meta_content, encoding='utf-8')
            
            # Mark as processed
            processed.add(str(f))
            
            logging.info(f'✅ Processed: {f.name} → {dest.name}')
    
    time.sleep(10)  # Check every 10 seconds
