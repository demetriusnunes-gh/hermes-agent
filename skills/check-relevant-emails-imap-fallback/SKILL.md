---
name: check-relevant-emails-imap-fallback
description: Check Gmail for relevant emails using direct IMAP connection (more reliable than Zapier MCP for cron/headless environments). Includes deduplication and relevance filtering.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Email, Gmail, IMAP, Monitoring, Personal, Automation]
---

# Check Relevant Emails via Gmail IMAP (Cron/Headless Safe)

Scans Gmail inbox for important emails using direct IMAP connection (more reliable than Zapier MCP for cron jobs). Reports only items matching priority criteria with deduplication to avoid repeat notifications.

## When to Use

- Automated email checking in cron jobs (runs every 2 hours)
- Headless environments where Zapier MCP is unreliable
- When you need guaranteed email delivery without interactive approvals

## Relevance Criteria (Same as original skill)

Flag and report emails matching ANY of these:

1. **Wife** — Fernanda Hamacher (`fhamacher@gmail.com`, name: "Fernanda Hamacher")
2. **Kids' school** — Anything from or about "Eleva"
3. **Government** — `.gov.br` sender domains, or subjects containing: intimação, notificação, comunicado, declaração, imposto, receita, INSS, detran, prefeitura, governo, multa, CNH, IPTU, IOF, IR. 
   - **False positive prevention**: The keyword `"ir"` requires checking that sender is NOT promotional/commercial (airlines, retailers, newsletters) and not part of false positive patterns like "partir", "sorrir", "vir", etc.
4. **Also flag**:
   - Purchases & orders — receipts, shipping updates, delivery confirmations, payment issues
   - Recruiter / job outreach — LinkedIn recruiters, job opportunities, hiring messages
   - Financial statements & bills — bank statements, credit card invoices, bills, financial reports
   - Urgent/action-required subjects ("urgent", "ASAP", "action required", "precisa responder", "responda")
5. **Ignore**: newsletters, promotions, social notifications, automated receipts, bulk mail

## Deduplication / State Tracking

State file: `~/.hermes/state/email-check-state.json`

```json
{
  "last_run_at": "2026-04-11T09:26:00-03:00",
  "notified_ids": ["20990", "20966", "..."],
  "notified_hashes": ["sha:abc123", "sha:def456", "..."]
}
```

- **notified_ids**: Gmail Message-IDs of emails already reported
- **notified_hashes**: SHA-256 of `"{sender_email}|{subject}|{date_iso}"` for robustness against ID changes
- Only reports emails NOT in either list
- Rotates to keep last 1000 entries max for each list

## Implementation Details

### Connection
- Uses app password from `~/.gmail-app-password` (one-time setup)
- Connects to `imap.gmail.com` via IMAP4_SSL
- Authenticates as `demetriusnunes@gmail.com`
- For historical payment/subscription audits, search All Mail instead of Inbox so archived receipts are included

### Search Strategy
1. Select the correct mailbox first:
   - For inbox monitoring: `mail.select('INBOX', readonly=True)`
   - For historical/billing scans: prefer Gmail All Mail: `mail.select('"[Gmail]/Todos os e-mails"', readonly=True)` on Portuguese accounts (or the localized All Mail name returned by `mail.list()`)
2. For broad time-window scans, use standard IMAP date search: `mail.search(None, 'SINCE', since_date)`
3. For targeted Gmail-style queries, use Gmail raw search exactly like:
   - `mail.search(None, 'X-GM-RAW', '"after:2026/03/13 from:googleplay-noreply@google.com"')`
4. Filter client-side after retrieval for final relevance / merchant / subscription logic
5. Apply deduplication before reporting

### Gmail IMAP Query Pitfalls
- `mail.search()` only works after a successful `select()`; otherwise Gmail returns: `command SEARCH illegal in state AUTH`.
- `X-GM-RAW` is powerful but fragile. Wrap the entire raw Gmail query in one quoted string passed as a single criterion.
- Queries containing nested quotes, accented characters, or complex boolean expressions may fail with `SEARCH command error: BAD [Could not parse command]`.
- When that happens, simplify aggressively:
  - prefer sender-only or sender+date queries first
  - then inspect/filter subjects and bodies client-side in Python
  - avoid relying on accented literals like `cobrança` inside IMAP search
- If you need the localized Gmail folder name, inspect it with `mail.list()` first instead of assuming English names.

### Relevance Checking
- Wife: Direct email/name match
- School: Contains "eleva" (case-insensitive) in sender or subject
- Government: 
  - Domain ends with `.gov.br`
  - Subject contains government keywords with special handling for "ir":
    * Reject if subject contains false positive patterns (partir, sorrir, vir, dirigir, etc.)
    * Reject if sender matches promotional domains (noreply@voeazul, noreply@azul.com.br, etc.)
    * Otherwise accept as government-related
- Purchases/orders: Subject contains receipt/order/purchase/shipping/delivery/payment/invoice/confirmed/shipped
- Recruiter/job: Subject or sender contains recruiter/recruitment/job/position/opportunity/hiring/headhunter/linkedin/career
- Financial: Subject contains statement/bill/invoice/fatura/extrato/cartão/credit/debit/bank/banco/itau/nubank/santander/bradesco
- Urgent: Subject contains urgent/asap/action required/precisa responder/responda/urgente/importante

### Output Format
When relevant emails found:

```
📧 Relevant emails (last 2h):

1. Sender Name (sender@example.com)
   Subject: Full subject line
   HH:MM AM/PM — Brief summary (first 200 chars)
   → [Reason why it matters]

📅 Upcoming events:
[Calendar section skipped in IMAP fallback - use Zapier MCP if calendar needed]
```

If no new relevant emails: Outputs exactly `[SILENT]`
If Gmail connection fails: Outputs `⚠️ Gmail connection failed: [error]`

### State Management
After processing:
1. Append new message IDs and hashes to state lists
2. Update `last_run_at` timestamp
3. Rotate lists to keep only last 1000 entries each
4. Write updated state back to JSON file

### Requirements
- Python 3.x
- Standard library only (imaplib, email, json, hashlib, datetime, etc.)
- App password file at `~/.gmail-app-password` containing Gmail app password

### Setup Instructions
1. Generate Gmail app password (if 2FA enabled) or use regular password
2. Save to `~/.gmail-app-password` (chmod 600 recommended)
3. Ensure `~/.hermes/state/` directory exists
4. Run manually first to test: `python check_emails_imap.py`
5. Add to cron: `0 */2 * * * /path/to/check_emails_imap.py`

### Notes
- More reliable than Zapier MCP for automated/cron use
- Does not require interactive approvals or browser flows
- Provides full header access and optional body snippet extraction
- For billing/subscription audits, fetch full messages with `RFC822` and extract `text/plain` / `text/html` parts client-side; raw partial fetches can surface MIME/base64 noise and produce poor snippets
- Always prefer `readonly=True` plus `BODY.PEEK` semantics to avoid marking messages as read
- Respects quiet hours - only outputs when relevant emails found
- Handles connection failures gracefully