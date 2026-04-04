---
name: zapier-mcp-access
description: Connect to Zapier MCP server for Gmail and Google Calendar. The mcporter native lookup always fails - must use --http-url with full token from config.yaml.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [MCP, Zapier, Gmail, Google Calendar, Email]
---

# Zapier MCP Access

Connects to `mcp.zapier.com` for Gmail search and Google Calendar queries via the Zapier MCP server.

## Critical Gotcha

**`/root/config/mcporter.json` has a TRUNCATED token** (`ZWFaND...c9`). This means `npx mcporter call zapier.gmail_find_email` ALWAYS fails with "Unknown MCP server" or 404.

**ALWAYS use `--http-url` with the full token.**

## Full Token Location

The complete Zapier MCP URL with valid token is stored in `~/.hermes/config.yaml` under `mcp_servers.zapier.url`.

Extract it like this:

```bash
ZAPIER_URL=$(python3 -c "
import yaml
with open('/root/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
print(cfg.get('mcp_servers',{}).get('zapier',{}).get('url',''))
" 2>/dev/null)
```

## Available Tools

```bash
npx mcporter list --http-url "$ZAPIER_URL" --name zapier 2>&1
```

Currently exposed:
- `gmail_find_email` — search Gmail by query
- `google_calendar_find_events` — search Google Calendar
- `get_configuration_url` — returns Zapier MCP config URL

## Gmail Search Examples

**Search all mail from December 2025:**
```bash
npx mcporter call --http-url "$ZAPIER_URL" gmail_find_email \
  instructions="Find emails from travel@beachpark.com.br in December 2025" \
  output_hint="Show sender, subject, date, full plain text body, and list attachment filenames" \
  query="from:travel@beachpark.com.br after:2025/12/01 before:2025/12/31" \
  --output json 2>&1
```

**Search inbox only for last 2 hours:**
```bash
npx mcporter call --http-url "$ZAPIER_URL" gmail_find_email \
  instructions="Show recent emails in my inbox" \
  output_hint="Show sender, subject, date, and first 100 chars of body" \
  query="in:inbox newer_than:2h" \
  --output json 2>&1
```

### Gmail Query Syntax Reference
- `from:email@example.com` — search by sender
- `subject:keyword` — search by subject keyword
- `after:YYYY/MM/DD before:YYYY/MM/DD` — date range
- `has:attachment` — emails with attachments
- `filename:pdf` — emails with PDF attachment
- `in:inbox` — inbox only (default is all mail)
- `in:anywhere` — search all mail including archived

## Calendar Search

```bash
npx mcporter call --http-url "$ZAPIER_URL" google_calendar_find_events \
  instructions="Show today events" \
  output_hint="Show title, start_time, end_time, location" \
  end_time="today at 12:00am" \
  start_time="today at 11:59pm" \
  --output json 2>&1
```

## Token Expiration

Symptom:
```json
{"error": {"code": -31997, "message": "Invalid OAuth token - please re-authenticate"}}
```

Fix: Log into Zapier MCP dashboard at mcp.zapier.com, regenerate the Connect token, then update `mcp_servers.zapier.url` in `~/.hermes/config.yaml`.

## Common Issues

1. **"Unknown MCP server zapier"** — mcporter config has truncated token. Use --http-url.
2. **HTTP 404** — Token issue. Always use --http-url with full token from config.yaml.
3. **Empty results** — Zapier has 25 result cap. Narrow date ranges or search all mail with in:anywhere instead of in:inbox.
4. **output_hint REQUIRED** — Controls the auto-generated jq filter. Without it, results may be unstructured/raw.
5. **Case-sensitive queries** — `from:BeachPark` may fail. Use exact lowercase: `from:travel@beachpark.com.br`.
6. **Attachment contents** — Zapier only returns filenames. To download and read attachments, use Python `imaplib` with the Gmail app password at `~/.gmail-app-password`, or `himalaya attachment download <ID>`.