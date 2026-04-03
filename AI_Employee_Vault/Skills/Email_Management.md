# Email Management Skill

## Description
Professional email handling with approval workflow.

## When to Use
- New email detected in /Needs_Action with type: email
- User requests email reply or draft
- Scheduled email campaigns

## Process Flow

### 1. Analyze Email
- Read email from task file
- Identify sender, subject, content
- Determine priority (urgent keywords)
- Check if sender is known contact

### 2. Draft Reply
- Use professional tone
- Address all points from original email
- Keep concise (under 200 words)
- Include clear call-to-action
- Add signature

### 3. Create Approval Request
Always create approval for:
- New email recipients
- Emails containing financial info
- Client communications
- Any email marked "important"

### 4. Execute (After Approval)
- Move approved email to /Approved
- Use email MCP tool: send_email
- Log sent email to /Logs
- Mark original as complete
- Move task to /Done
- Update Dashboard.md

## Safety Rules

NEVER send without approval:
- Emails to new contacts
- Emails mentioning money
- Emails with attachments
- Marketing emails

ALWAYS required:
- Approval for every send
- Logging every action
- Updating dashboard
- Professional tone
