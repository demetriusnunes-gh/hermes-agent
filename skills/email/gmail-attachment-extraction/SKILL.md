---
name: gmail-attachment-extraction
description: Download and extract PDF attachments from archived Gmail messages. Uses Python imaplib directly because himalaya can only access INBOX, and Zapier MCP only returns attachment filenames.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [Gmail, Attachments, PDF, IMAP, Zapier]
---

# Gmail Attachment Extraction

Downloads and extracts PDF attachments from Gmail messages — including archived ones that himalaya cannot reach (himalaya only searches INBOX).

## When to Use

- User asks to read details from a PDF attachment in an old/archived email
- Zapier MCP finds the email and lists filenames but cannot return file contents
- himalaya cannot find the email (it is not in INBOX)

## Steps

### 1. Find the Email

First, use Zapier MCP to find the email and confirm it has attachments:

```bash
npx mcporter call --http-url "$ZAPIER_URL" gmail_find_email \
  instructions="Find reservation confirmation emails with PDF attachments" \
  output_hint="Show sender, subject, date, full body, and list attachment filenames" \
  query="from:sender@domain.com after:2025/12/01 before:2025/12/31" \
  --output json 2>&1
```

### 2. Download Attachments via IMAP

Use Python `imaplib` to connect to Gmail and download the attachments:

```python
import os, imaplib, email
from email.header import decode_header

# Get the Gmail app password
result = subprocess.run(['cat', os.path.expanduser('~/.gmail-app-password')], capture_output=True, text=True)
password = result.stdout.strip()

# Connect to Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('demetriusnunes@gmail.com', password)

# IMPORTANT: Search in ALL mail, not just INBOX
mail.select('"[Gmail]/Todos os e-mails"')

# Search for relevant emails
status, messages = mail.search(None, '(FROM "sender@domain.com" SUBJECT "keyword")')
email_ids = messages[0].split() if status == 'OK' else []

# Download attachments
save_dir = os.path.expanduser('~/.hermes/tmp/attachments')
os.makedirs(save_dir, exist_ok=True)

for eid in email_ids:
    status, msg_data = mail.fetch(eid, '(RFC822)')
    if status != 'OK': continue
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)
    
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart': continue
        filename = part.get_filename()
        if not filename: continue
        decoded = decode_header(filename)[0]
        fname = decoded[0].decode(decoded[1] or 'utf-8') if isinstance(decoded[0], bytes) else decoded[0]
        if fname.endswith('.pdf'):
            payload = part.get_payload(decode=True)
            if payload:
                fpath = os.path.join(save_dir, fname)
                with open(fpath, 'wb') as f: f.write(payload)
                print(f"Downloaded: {fname}")

mail.close()
mail.logout()
```

### 3. Extract PDF Text

Install PyMuPDF (fitz) if needed:

```bash
uv pip install pymupdf 2>&1 | tail -3
```

Extract text:

```python
python3 << 'PYEOF'
import fitz, os

save_dir = os.path.expanduser('~/.hermes/tmp/attachments')
for pdf_name in sorted(os.listdir(save_dir)):
    if not pdf_name.endswith('.pdf'): continue
    doc = fitz.open(os.path.join(save_dir, pdf_name, pdf_name))
    for page in doc:
        text = ' '.join(page.get_text().split())
        print(text)
    doc.close()
PYEOF
```

## Pitfalls

- himalaya envelope list only searches INBOX — archived emails are invisible to himalaya
- Use `[Gmail]/Todos os e-mails` for Portuguese accounts or `[Gmail]/All Mail` for English
- `execute_code` sandbox is isolated — install pymupdf with `uv pip install pymupdf`, not `pip`
- System python3 does not have pymupdf — use the one installed via uv, or install it first
- Some PDF vouchers have images/scan text — `get_text()` may return nothing for image-based PDFs. In that case convert the first page to image and use vision_analyze.