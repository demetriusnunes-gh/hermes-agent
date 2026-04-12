---
name: gmail-attachment-extraction
description: Deprecated. Attachment extraction guidance in this skill still depends on legacy IMAP/app-password access and should not be used in this environment.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [Gmail, Attachments, PDF, Deprecated]
---

# Gmail Attachment Extraction

This skill is deprecated in this environment.

Reason: the previous instructions relied on IMAP, Gmail app passwords, and older mail-client assumptions. Local email access is now standardized on OAuth-based Google Workspace tooling, and the app-password file should not be recreated.

## Current Rule

Do not use this skill's old workflow.

Do not use:
- legacy CLI mail-client configs
- legacy app-password files
- IMAP/app-password attachment download flows

## What To Do Instead

1. Use `google-workspace` for Gmail access.
2. Use `check-relevant-emails` for inbox monitoring.
3. If a task specifically requires attachment contents and the current OAuth wrappers cannot fetch them directly, treat that as a tooling gap rather than reviving old IMAP instructions.
4. Prefer updating the Google Workspace tooling or using another OAuth-safe path instead of reintroducing app-password config.

## Note

Keep this skill only as a tombstone so future runs do not revive the old IMAP/app-password method.