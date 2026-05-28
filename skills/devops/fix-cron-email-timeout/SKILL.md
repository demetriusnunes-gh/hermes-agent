---
name: fix-cron-email-timeout
description: Fix cron email-check jobs by standardizing on Google Workspace gws/google_api.py instead of Zapier MCP or IMAP.
version: 2.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [cron, email, google-workspace, gws, timeout, fix]
---

# Fix Cron Job Timeouts for Email Checking

When cron jobs for email checking are unreliable, the fix in this environment is to standardize on Google Workspace via `gws` and the `google_api.py` wrapper.

Do not use:
- Zapier MCP
- IMAP / app passwords


## Problem Pattern

Email-check cron jobs may fail or become inconsistent when they rely on older access methods.

Historical causes included:
- Zapier MCP auth/token instability in headless runs
- IMAP-specific credential drift and alternate code paths
- multiple competing skills using different transports

## Current Solution

Use one transport only:
- `~/.hermes/skills/productivity/google-workspace/scripts/google_api.py`
- with auth handled by `setup.py` and token refresh via `gws_bridge.py`

## Procedure

### 1. Verify Google Workspace auth

```bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
GWORKSPACE_SKILL_DIR="$HERMES_HOME/skills/productivity/google-workspace"
PYTHON_BIN="${HERMES_PYTHON:-python3}"
if [ -x "$HERMES_HOME/hermes-agent/venv/bin/python" ]; then
  "$HERMES_HOME/hermes-agent/venv/bin/python" -m ensurepip --upgrade >/dev/null 2>&1 || true
  PYTHON_BIN="$HERMES_HOME/hermes-agent/venv/bin/python"
fi
GSETUP="$PYTHON_BIN $GWORKSPACE_SKILL_DIR/scripts/setup.py"
GAPI="$PYTHON_BIN $GWORKSPACE_SKILL_DIR/scripts/google_api.py"

$GSETUP --check
```

If this fails, repair auth first. Do not add a fallback transport.

### 2. Use the main skill

For the actual monitoring logic, follow `check-relevant-emails`.

### 3. Standardize cron behavior

Cron prompts/scripts should:
- check auth first
- search Gmail with `google_api.py gmail search "in:inbox newer_than:2h" --max 50`
- optionally widen to `newer_than:1d` for sparse inboxes
- read full messages only when needed with `google_api.py gmail get MESSAGE_ID`
- check calendar with `google_api.py calendar list ...`
- preserve dedup state in `~/.hermes/state/email-check-state.json`
- emit `[SILENT]` when there is nothing relevant

## Verification

After updating a cron workflow:
1. run it manually once
2. verify `AUTHENTICATED` succeeds
3. verify Gmail search returns JSON
4. verify no Zapier/IMAP commands remain in the cron prompt/script
5. verify dedup state still works

## Expected Benefits

- one supported auth path
- one supported email/calendar transport
- less configuration drift
- no app-password dependency
- no MCP dependency for this workflow

## Related Skills

- `check-relevant-emails`
- `google-workspace`

## Note

This skill used to recommend IMAP as the cron-safe fallback. That is now obsolete here. The correct fix is to migrate cron email checks to Google Workspace only.
