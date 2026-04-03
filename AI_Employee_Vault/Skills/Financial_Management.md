# Financial Management Skill

## Description
Handle invoices, payments, and revenue tracking with strict approval controls.

## Rules & Thresholds

### Approval Required
- Any amount over 100 dollars
- Any new recipient
- International payments
- Subscription cancellations

### Auto-Flagged
- Amounts over 1000 dollars
- Duplicate invoices
- Unusual payment timing
- New vendor setup

## Invoice Processing

### Step 1: Receive Invoice
- Check for invoice number and amount
- Verify sender legitimacy
- Extract key details

### Step 2: Validation
- Cross-check with Business_Goals.md budget
- Verify vendor in approved list
- Check for duplicate invoice number

### Step 3: Create Payment Approval
Create approval request in /Pending_Approval with:
- Vendor name
- Amount
- Invoice number
- Description
- Due date
- Justification
- Budget impact

### Step 4: After Approval
- Log payment in /Accounting
- Update cash flow tracker
- Schedule reminder for receipt
- Move invoice to /Done

## Revenue Tracking

### Incoming Payments
1. Detect payment notification
2. Extract amount and source
3. Match to invoice if applicable
4. Log in /Accounting/Revenue
5. Update Dashboard.md
6. Update Business_Goals.md progress

## Budget Monitoring

### Weekly Check
- Total spend vs budget
- Category breakdown
- Alert if over 80 percent of budget used
- Forecast end-of-month status

## Safety Rules

NEVER do without approval:
- Process payment
- Issue refund
- Update bank details
- Cancel subscription
- Commit to contract

ALWAYS required:
- Approval for payments over 100 dollars
- Logging every transaction
- Monthly reconciliation
- Receipt archiving
