---
name: google-workspace-token-renewal
description: Use when you need to renew the Google Workspace OAuth token by generating an auth URL, completing the browser consent flow, exchanging the returned code, and verifying authentication.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Google, Workspace, OAuth, token, Gmail, Calendar, Drive, renewal]
    related_skills: [productivity/google-workspace, mcp/zapier-mcp-access]
---

# Google Workspace Token Renewal

## Overview

Use this skill when the Google Workspace OAuth token needs to be refreshed or recreated in the browser. It covers the exact renewal flow used by Hermes: generate an authorization URL, complete consent in a browser, paste back the redirect URL or code, and verify the saved token.

This is the safe path for Gmail, Calendar, Drive, Contacts, Sheets, Docs, Slides, and Tasks access when the stored token has expired or been revoked.

## When to Use

- `--check` reports `NOT_AUTHENTICATED`, `REFRESH_FAILED`, or an invalid token
- The user asks for the Google auth URL to renew access in the browser
- The browser consent flow is complete and you need to exchange the returned redirect URL/code
- You want to verify that `/root/.hermes/google_token.json` is valid

Do not use for:

- Creating Google Cloud OAuth credentials from scratch
- Sending emails or modifying calendar events without user confirmation
- Zapier MCP auth; that uses a different flow and token source

## Quick Recipe

### 1) Generate the auth URL

Use the Google Workspace setup script:

```bash
export HOME=/root
export PYTHONPATH=/root/.hermes/hermes-agent:$PYTHONPATH
PYTHON_BIN=/root/.hermes/hermes-agent/venv/bin/python
$PYTHON_BIN /root/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-url
```

This prints a Google consent URL. Send that URL to the user or open it in the browser.

### 2) Complete consent in the browser

After login, Google redirects to a localhost URL like:

```text
http://localhost:1/?state=...&iss=https://accounts.google.com&code=...&scope=...
```

Copy the full redirected URL exactly as shown.

### 3) Exchange the code

Pass the full redirected URL to `--auth-code`:

```bash
export HOME=/root
export PYTHONPATH=/root/.hermes/hermes-agent:$PYTHONPATH
PYTHON_BIN=/root/.hermes/hermes-agent/venv/bin/python
$PYTHON_BIN /root/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-code 'PASTE_THE_FULL_REDIRECT_URL_HERE'
```

Expected success message:

```text
OK: Authenticated. Token saved to /root/.hermes/google_token.json
```

### 4) Verify the token

```bash
export HOME=/root
export PYTHONPATH=/root/.hermes/hermes-agent:$PYTHONPATH
PYTHON_BIN=/root/.hermes/hermes-agent/venv/bin/python
$PYTHON_BIN /root/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
```

Expected success message:

```text
AUTHENTICATED: Token valid at /root/.hermes/google_token.json
```

## Common Pitfalls

1. **Pasting only the code when the script expects the full redirect URL.**
   If the script accepts either, fine; otherwise paste the entire localhost redirect URL from the browser address bar.

2. **Forgetting the Hermes venv / `PYTHONPATH` fix.**
   On this VPS, the safest invocation is the one above with `/root/.hermes/hermes-agent/venv/bin/python` and `PYTHONPATH=/root/.hermes/hermes-agent`.

3. **Using the wrong token file.**
   The current token is stored at `/root/.hermes/google_token.json`.

4. **Confusing Google Workspace OAuth with Zapier MCP auth.**
   They are separate systems. Zapier MCP auth comes from `~/.hermes/config.yaml`, not from the Google token file.

5. **Skipping verification.**
   Always run `--check` after exchanging the code.

## Verification Checklist

- [ ] Auth URL generated successfully
- [ ] Browser consent completed
- [ ] Redirect URL or code exchanged with `--auth-code`
- [ ] `setup.py --check` returns `AUTHENTICATED`
- [ ] Token exists at `/root/.hermes/google_token.json`
