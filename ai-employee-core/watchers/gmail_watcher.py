"""Gmail Watcher - Monitors important emails"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from pathlib import Path
import base64
import re
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
vault_path = Path(os.getenv('VAULT_PATH', r'D:\ai-employee\AI_Employee_Vault'))
needs_action = vault_path / 'Needs_Action'
needs_action.mkdir(parents=True, exist_ok=True)

# Logging
log_dir = vault_path / 'Logs'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'gmail_watcher.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Gmail setup
creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)
processed_emails = set()

def get_email_body(message):
    """Extract email body from message"""
    try:
        payload = message.get('payload', {})
        
        # Check for parts (multipart email)
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        # Single part email
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        # Fallback to snippet
        return message.get('snippet', '')
    except Exception as e:
        logging.error(f"Error extracting body: {e}")
        return message.get('snippet', '')

def detect_priority(subject, body):
    """Detect email priority based on keywords"""
    keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency', 
                'immediate', 'critical', 'important']
    
    text = (subject + ' ' + body).lower()
    
    for keyword in keywords:
        if keyword in text:
            return 'high'
    
    return 'medium'

def create_email_task(message):
    """Create a task file for the email"""
    # Extract headers
    headers = {h['name']: h['value'] for h in message['payload']['headers']}
    sender = headers.get('From', 'Unknown')
    subject = headers.get('Subject', 'No Subject')
    
    # Get email body
    body = get_email_body(message)
    
    # Detect priority
    priority = detect_priority(subject, body)
    
    # Create safe filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_subject = re.sub(r'[^\w\s-]', '_', subject)[:40]
    filename = f'EMAIL_{timestamp}_{safe_subject}.md'
    
    # Create task content
    content = f'''---
type: email
from: {sender}
subject: {subject}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
---

**From:** {sender}
**Subject:** {subject}
**Priority:** {priority.upper()}

## Email Content

{body[:500]}{"..." if len(body) > 500 else ""}

## Required Actions

- [ ] Read and understand email
- [ ] Draft professional reply
- [ ] Create approval request in /Pending_Approval
- [ ] Wait for approval before sending

## Notes

Add any notes or context here.
'''
    
    # Save task file
    filepath = needs_action / filename
    filepath.write_text(content, encoding='utf-8')
    
    logging.info(f'📧 New email task created: {subject} (Priority: {priority})')
    return filepath

def check_gmail():
    """Check Gmail for new important unread emails"""
    try:
        # Query for unread important emails
        results = service.users().messages().list(
            userId='me',
            q='is:unread is:important',
            maxResults=5
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            logging.debug('No new important emails')
            return
        
        for msg_ref in messages:
            msg_id = msg_ref['id']
            
            # Skip if already processed
            if msg_id in processed_emails:
                continue
            
            # Get full message
            message = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            # Create task
            create_email_task(message)
            
            # Mark as processed
            processed_emails.add(msg_id)
        
    except Exception as e:
        logging.error(f'❌ Error checking Gmail: {e}')

def main():
    """Main watcher loop"""
    logging.info('🚀 Gmail Watcher started')
    logging.info(f'📁 Vault path: {vault_path}')
    logging.info(f'⏱️  Checking every 2 minutes for important emails')
    
    while True:
        try:
            check_gmail()
            time.sleep(120)  # Check every 2 minutes
        except KeyboardInterrupt:
            logging.info('👋 Gmail Watcher stopped by user')
            break
        except Exception as e:
            logging.error(f'❌ Unexpected error: {e}')
            time.sleep(120)

if __name__ == '__main__':
    main()
