---
name: email-calendar-monitoring
description: "Scheduled Gmail inbox + Google Calendar monitoring with strict deduplication and [SILENT] on empty runs."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Email, Gmail, Calendar, Monitoring, Dedup, Google-Workspace, Cron]
---

# Email + Calendar Monitoring

Use this skill for recurring scans of a user's Gmail inbox and Google Calendar when the goal is to surface only new, high-confidence items and stay silent otherwise.

This is a monitoring workflow, not a general inbox browser. It should be conservative, deduplicated, and quiet on empty.

## Primary backend

Use the Google Workspace skill for all data access:
- `productivity/google-workspace`
- `scripts/google_api.py`
- `scripts/setup.py --check`
- `references/session-notes.md` for session-proven parsing and dedup pitfalls

## Triggers

Use this skill when the user asks for:
- "check my email"
- "any important emails?"
- scheduled inbox/calendar scans
- actionable reminders from Gmail or Calendar

## Workflow

1. Check Google auth first.
2. Load `~/.hermes/state/email-check-state.json` before scanning.
3. Scan Gmail and Calendar using Google Workspace only.
4. Decide relevance conservatively.
5. Deduplicate against both prior message/event ids and stable hashes before output.
6. If nothing new survives deduplication, output exactly `[SILENT]`.
7. If there are new items, update the state file in the same run before returning the report.

## Deduplication rules

- Gmail:
  - dedupe on Gmail message id
  - also dedupe on a stable hash of sender email + subject + date
  - when a thread contains multiple messages, collapse it to one alert per thread and choose the newest message as the canonical report item
- Calendar:
  - dedupe on a stable visible-field hash such as summary + start + end
  - do not rely only on raw event ids when a visible-field hash is available
- Normalize legacy hashes before comparison:
  - treat bare SHA-256 digests and prefixed forms like `sha:` / `sha:event:` / `sha:thread:` as equivalent
- Treat the state file as the source of truth for suppression:
  - load it before scanning
  - filter candidates against both `notified_ids` and `notified_hashes` before any user-facing output
  - update the same file in the same run only after the final candidate set is frozen
  - keep the persistent lists bounded; trim old entries rather than allowing unbounded growth

## Practical implementation note

If a monitoring worker needs to repair or normalize old suppression state, rewrite the state file from a deduplicated in-memory snapshot rather than appending ad hoc. This prevents duplicate re-alerts when the same message or event is seen again in a later run.

If a provisional scan surfaced low-signal items, do not keep them in the final suppression set. Rebuild the final candidate list from the conservative relevance filter, then rewrite the state from that final snapshot before reporting.

## Implementation pitfalls

- If a Hermes read of the state file returns an "unchanged since last read" stub, read the file directly from disk in the worker code before deduplicating or updating it.
- Gmail search output can contain raw control characters or HTML-heavy snippets that break strict JSON parsing; use a tolerant parser, and if the search payload is messy, re-fetch the handful of candidate messages with `gmail get` before final relevance/dedup decisions.
- For Gmail monitoring, do a thread-level canonicalization pass after relevance filtering so one conversation does not emit multiple alerts.
- For Zapier calendar lookups in this environment, use the exact case-sensitive `ordering` value `startTime`.

## Relevance rules

Flag only high-confidence items, such as:
- direct family contacts
- school-related messages/events
- government/public-agency messages
- receipts, shipping, delivery, payment issues
- real account/security alerts tied to an existing account or reservation
- job/recruiter outreach
- bills, statements, collection notices, investor/fund communications

Be conservative:
- ignore newsletters, promotions, bulk mail, and low-signal marketing
- ignore generic calendar notifications unless the sender or content clearly indicates a real actionable item
- do not treat a keyword match alone as sufficient when the sender is obviously promotional or media/newsletter traffic
- media/newsletter senders stay irrelevant even when the subject discusses government, security, or finance topics
- a promotional sender about an existing hobby or purchase history is still promotional unless the message is clearly an actionable account, billing, delivery, or security notice
- when a broad inbox query returns digest/editorial senders, exclude them by sender class first; do not let topical keywords (for example security/finance/government) override the sender-type filter

## Output rules

- If no new relevant items remain after deduplication: `[SILENT]`
- If auth fails: report the auth failure once, concisely
- Otherwise: report only the new items that survived deduplication

## Notes

This skill pairs with the Google Workspace auth/setup flow.
For session-specific false-positive patterns and normalization examples, see `references/false-positive-notes.md`.
For state-format and suppression normalization details, see `references/state-format.md`.
