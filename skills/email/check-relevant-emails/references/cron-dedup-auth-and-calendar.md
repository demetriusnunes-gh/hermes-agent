# Live notes: auth, dedup, and calendar quirks

Captured from a successful cron run of the relevant-email/calendar checker.

## Auth
- `python3 ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check` returned `AUTHENTICATED` after token refresh.
- Treat `AUTHENTICATED (partial)` as usable for this workflow if Gmail and Calendar calls succeed.

## Deduplication
- Gmail message dedup remains `notified_ids` plus `sha256("{sender_email}|{subject}|{date_iso}")`.
- Calendar dedup should use stable hashes from the visible event fields, typically:
  - `sha:event:` + sha256(`"{summary}|{start}|{end}"`)
  - optionally also `sha:event:` + sha256(`"{calendar}|{summary}|{start}|{end}"`)
- Do **not** include location in the calendar dedup hash unless the upstream state format changes.
- Existing state files may already contain `sha:event:`-prefixed hashes for prior notifications.

## Calendar shape
- `calendar list` can return all-day items with date-only `start` / `end` values (for example `2026-05-10` → `2026-05-11`).
- These all-day reminders should still be treated as actionable when they are clearly financial/account tasks such as `Pagar Nubank`.

## Filter hygiene
- Broadening Gmail search from `newer_than:2h` to `newer_than:1d` increases newsletter noise; keep the relevance filter conservative and dedupe before reporting.
- Newsletters and promotional mail are still irrelevant even when they mention topical government news or school-adjacent keywords incidentally.
