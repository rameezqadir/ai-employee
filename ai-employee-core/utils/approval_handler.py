"""Approval Handler - Creates and manages approval requests"""
from pathlib import Path
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

load_dotenv()

vault_path = Path(os.getenv('VAULT_PATH', r'D:\ai-employee\AI_Employee_Vault'))
pending_approval = vault_path / 'Pending_Approval'
approved = vault_path / 'Approved'
rejected = vault_path / 'Rejected'

# Create directories
for directory in [pending_approval, approved, rejected]:
    directory.mkdir(parents=True, exist_ok=True)

def create_approval_request(action_type, details, expires_hours=24):
    """
    Create an approval request
    
    Args:
        action_type: Type of action (e.g., 'send_email', 'make_payment')
        details: Dict of action details
        expires_hours: Hours until approval expires (default: 24)
    
    Returns:
        Path to created approval file
    """
    timestamp = datetime.now()
    expires_at = timestamp + timedelta(hours=expires_hours)
    
    # Format details
    detail_lines = []
    for key, value in details.items():
        detail_lines.append(f'- **{key.replace("_", " ").title()}**: {value}')
    
    detail_text = '\n'.join(detail_lines)
    
    # Create approval content
    content = f'''---
type: approval_request
action: {action_type}
created: {timestamp.isoformat()}
expires: {expires_at.isoformat()}
status: pending
---

# Approval Request: {action_type.replace("_", " ").title()}

## Action Details

{detail_text}

## How to Approve

1. Review the details above carefully
2. If approved: Move this file to `/Approved` folder
3. If rejected: Move this file to `/Rejected` folder

⏰ **Expires:** {expires_at.strftime("%Y-%m-%d %H:%M")}

## Safety Notes

- This action requires human approval
- Once approved, it will be executed automatically
- Rejected requests will be logged and archived
'''
    
    # Create filename
    safe_action = action_type.replace(' ', '_').replace('/', '_')
    filename = f'APPROVAL_{safe_action}_{timestamp.strftime("%Y%m%d_%H%M%S")}.md'
    
    # Save file
    filepath = pending_approval / filename
    filepath.write_text(content, encoding='utf-8')
    
    print(f'✅ Approval request created: {filename}')
    print(f'📁 Location: {filepath}')
    print(f'⏰ Expires: {expires_at.strftime("%Y-%m-%d %H:%M")}')
    
    return filepath

# Example usage for testing
if __name__ == '__main__':
    # Test: Create sample approval requests
    
    # Example 1: Email approval
    create_approval_request(
        action_type='send_email',
        details={
            'to': 'client@example.com',
            'subject': 'Re: Invoice #1234',
            'preview': 'Thank you for your inquiry. The invoice amount of $500...',
            'reason': 'New email recipient requires approval'
        }
    )
    
    # Example 2: Payment approval
    create_approval_request(
        action_type='make_payment',
        details={
            'recipient': 'Vendor XYZ',
            'amount': '$750.00',
            'invoice_number': 'INV-2024-001',
            'reason': 'Amount exceeds $100 threshold'
        },
        expires_hours=48
    )
    
    print('\n✅ Test approval requests created!')
    print(f'📁 Check: {pending_approval}')
