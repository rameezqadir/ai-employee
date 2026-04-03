# Task Processing Skill

## Description
Systematic processing of tasks from /Needs_Action folder.

## Workflow

### Step 1: Scan for Tasks
Check /Needs_Action for new files

Priority order:
1. HIGH priority first
2. MEDIUM priority
3. LOW priority

### Step 2: Categorize Task
File types:
- EMAIL_*.md → Email task
- FILE_*.md → File processing
- TASK_*.md → General task

### Step 3: Determine Action

Simple Tasks (complete immediately):
- Read-only requests
- Information lookup
- File organization
- Status updates

Complex Tasks (needs planning):
- Multi-step processes
- Research required
- Create PLAN_ file in /Plans

Sensitive Tasks (needs approval):
- Financial transactions
- External communications
- Create APPROVAL_ file in /Pending_Approval

### Step 4: Execute

For simple tasks:
1. Execute action
2. Log to /Logs
3. Move to /Done
4. Update Dashboard.md

For complex tasks:
1. Create plan in /Plans
2. Break into sub-tasks
3. Execute sequentially
4. Move to /Done when complete

For sensitive tasks:
1. Create approval request
2. Wait for human approval
3. Check /Approved folder
4. Execute approved action
5. Log and move to /Done

## Priority Detection

HIGH priority keywords:
- urgent, asap, critical
- invoice, payment, deadline
- client, customer, meeting
- emergency, important, help

## Best Practices

1. Always read CLAUDE.md first for context
2. Check Company_Handbook.md for rules
3. Update Dashboard.md after each task
4. Log everything to /Logs
5. Never skip approvals for sensitive tasks
