# Deterministic Gmail + Calendar monitoring

Use this recipe for scheduled scans that must stay conservative, deduplicated, and silent when nothing new exists.

## Fetch order

1. Check auth/backend connectivity first.
2. Load `~/.hermes/state/email-check-state.json` before scanning.
3. Fetch the smallest useful candidate set.
4. Re-fetch only the few candidates that need full-body inspection.
5. Freeze the final candidate list.
6. Write the updated state in the same run.
7. Return exactly `[SILENT]` if no new items survive deduplication.

## Recommended Google Workspace commands

- `python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail search 'in:inbox newer_than:7d' --max 50`
- `python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail get MESSAGE_ID`
- `python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py calendar list --calendar primary --start ISO_START --end ISO_END --max 50`

These produce deterministic JSON and are suitable for cron jobs and post-processing.

## Dedup keys

- Gmail
  - message id
  - stable hash of sender email + normalized subject + date
  - one alert per thread after relevance filtering
- Calendar
  - event id
  - stable hash of summary + start + end + location + description

Normalize legacy hash prefixes before comparison:
- treat bare SHA-256 digests and prefixed forms like `sha:` / `sha:event:` as equivalent

## Relevance buckets

High-confidence items include:
- account/security alerts
- sign-in notifications
- refunds, credits, charges, bills, and statements
- workspace retention, deletion, or access-change warnings
- school, family, or other clearly actionable personal calendar events
- government/public-agency notices

Be conservative with newsletters, promotions, digests, and generic calendar notifications.