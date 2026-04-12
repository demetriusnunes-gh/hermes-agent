---
name: check-relevant-emails-imap-fallback
description: Deprecated. Relevant email checking now uses Google Workspace gws/google_api.py only; do not use IMAP, Zapier MCP, or app passwords.
version: 2.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Email, Gmail, Google-Workspace, gws, Deprecated]
---

# Check Relevant Emails via Gmail IMAP (Deprecated)

This skill is deprecated.

Use `check-relevant-emails` instead.

## Current Rule

Relevant email checking is standardized on Google Workspace only:
- `~/.hermes/skills/productivity/google-workspace/scripts/google_api.py`
- `gws_bridge.py`
- `gws`
- token at `~/.hermes/google_token.json`

Do not use:
- IMAP
- Gmail app passwords
- Zapier MCP
- any other email access path

## Why This Skill Is Deprecated

The preferred workflow now has first-class Google Workspace auth and working Gmail/Calendar access via `gws`, so IMAP fallback is no longer the desired approach for this environment.

## Migration

When a task previously would have used this skill:
1. Load `check-relevant-emails`
2. Verify auth with Google Workspace setup `--check`
3. Use `google_api.py gmail search ...`
4. Use `google_api.py gmail get MESSAGE_ID` if needed
5. Use `google_api.py calendar list ...` for calendar checks
6. Preserve the same deduplication state file: `~/.hermes/state/email-check-state.json`

## Output Behavior

Same behavioral policy still applies through the main skill:
- only report relevant unseen items
- output `[SILENT]` when there is nothing new
- report failures if the Google Workspace path is broken

## Note

Keep this skill only as a tombstone/redirect so future runs do not revive IMAP-based behavior.
