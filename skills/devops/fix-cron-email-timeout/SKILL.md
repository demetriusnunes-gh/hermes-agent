---
name: fix-cron-email-timeout
description: Fix cron job timeouts for email checking by switching from unreliable Zapier MCP to reliable Gmail IMAP approach
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [cron, email, imap, zapier, timeout, fix]
---

# Fix Cron Job Timeouts for Email Checking

When cron jobs for email checking (like the "Email checker - relevant alerts" job) consistently time out after 10 minutes, the root cause is often the unreliable Zapier MCP approach in headless/cron environments.

## Problem

Cron job "Email checker - relevant alerts" (job ID: ef8ac0a9a456) times out after 10 minutes with:
```
TimeoutError: Cron job 'Email checker - relevant alerts' timed out after 10 minutes
```

Root cause: The Zapier MCP approach (`npx mcporter call zapier.*`) is unreliable in automated/cron environments due to:
- Persistent token/truncation issues in headless environments
- Frequent "Unknown MCP server 'zapier'" errors
- MCP calls that can hang or fail silently
- Retry logic with exponential backoff (10s→20s→40s) that can exceed timeouts when MCP is unreliable

## Solution

Switch from Zapier MCP to the Gmail IMAP fallback approach, which is proven reliable for automated email checks in cron/headless environments.

## Why IMAP Works Better

- No MCP dependency or token issues
- Works reliably in headless/cron without approval prompts
- Full header access (can also fetch body snippets)
- Uses existing deduplication state file (`~/.hermes/state/email-check-state.json`)
- No interactive approvals required
- Proven reliability in automated/cron environments

## Implementation Steps

### 1. Modify the Cron Job Prompt/Script

Replace the Zapier MCP-based email/calendar checks with direct IMAP calls. Use the IMAP fallback procedure from the `check-relevant-emails` skill:

```python
import imaplib
import email
from email.header import decode_header
import json
import os
import re
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Load state for deduplication
STATE_FILE = Path(os.path.expanduser("~/.hermes/state/email-check-state.json"))
if STATE_FILE.exists():
    state = json.loads(STATE_FILE.read_text())
else:
    state = {"last_run_at": None, "notified_ids": [], "notified_hashes": []}

notify_ids = set(state.get("notified_ids", []))
notify_hashes = set(state.get("notified_hashes", []))

# Connect using app password stored at ~/.gmail-app-password
app_pw = os.path.expanduser('~/.gmail-app-password')
if not os.path.exists(app_pw):
    print("⚠️ Gmail app password not found at ~/.gmail-app-password")
    exit(1)

app_pw = open(app_pw).read().strip()
try:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('demetriusnunes@gmail.com', app_pw)
    mail.select('INBOX')
except Exception as e:
    print(f"⚠️ Gmail connection failed: {e}")
    exit(1)

# Search recent emails (last 24 hours to be safe, then filter by time)
since_date = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime('%d-%b-%Y')
status, messages = mail.search(None, f'(SINCE "{since_date}")')

if status != 'OK':
    print("⚠️ Failed to search emails")
    mail.logout()
    exit(1)

two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)

# Process emails and apply relevance criteria (from check-relevant-emails skill)
# [Add email processing logic here - filtering for wife, kids school, government, etc.]

# After processing, update state file with new notifications and timestamp
# (Refer to the "Save State After Report" section in check-relevant-emails skill)

mail.logout()
```

### 2. Key Implementation Details

**Relevance Criteria** (same as original skill):
- Wife: Fernanda Hamacher (`fhamacher@gmail.com`)
- Kids' school: Anything from or about "Eleva"
- Government: `.gov.br` domains or specific keywords (intimação, notificação, etc.)
- Purchases/orders, recruiter outreach, financial statements, urgent subjects

**Deduplication** (preserve existing logic):
- Use `~/.hermes/state/email-check-state.json`
- Track `notified_ids` (Zapier/Gmail message IDs)
- Track `notified_hashes` (SHA-256 of `{sender_email}|{subject}|{date_iso}`)
- Only report emails not in either list
- Rotate to keep last 1000 entries max

**Important Notes**:
- Always use `BODY.PEEK` (not `BODY`) to avoid marking emails as read
- For calendar events: When MCP fails, skip calendar check silently (no IMAP equivalent)
- Only report errors if both Gmail IMAP and calendar checks fail
- Consider using Google Calendar API directly if calendar becomes critical

### 3. Verification

After implementing:
1. Test manually: `hermes run "test email check with IMAP"`
2. Check logs: `journalctl -u hermes-gateway.service -f`
3. Verify no more 10-minute timeouts
4. Confirm relevant emails are still being detected and reported via Telegram
5. Ensure deduplication still works (no duplicate alerts)

## Benefits

- Eliminates 10-minute cron job timeouts
- More reliable email checking in automated environments
- Removes MCP dependency and token issues
- Maintains all existing functionality (relevance filtering, deduplication, alerting)
- Uses proven, tested approach for headless/cron environments

## When to Use This Fix

Apply this fix when:
- Cron email jobs consistently time out after 10 minutes
- Seeing "Unknown MCP server 'zapier'" errors in logs
- Zapier MCP calls are failing or hanging in automated environments
- You need reliable email checking for cron/headless operations

## Related Skills

- `check-relevant-emails`: Original skill with both MCP and IMAP approaches
- `gmail-attachment-extraction`: Shows direct IMAP usage for attachments
- `himalaya`: Alternative IMAP-based email CLI (though user prefers to remove it)

This fix aligns with the explicit recommendation in the `check-relevant-emails` skill: "The Gmail IMAP fallback has been tested and works reliably in cron/headless environments. It provides full header access, respects the deduplication state file, and does not require interactive approvals. When MCP fails, the IMAP approach should be used as the primary method for automated email checks."