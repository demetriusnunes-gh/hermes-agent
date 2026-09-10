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

## Backend fallback and commit boundary

If `setup.py --check` succeeds but the wrapper's optional `gws` backend returns an OAuth or invalid-credentials error, retry through the bundled Python backend before reporting auth failure. Use the Hermes virtualenv interpreter and a minimal `PATH` that excludes Hermes' Node bin directory, for example:

```bash
PATH=/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
  /root/.hermes/hermes-agent/venv/bin/python \
  /root/.hermes/skills/productivity/google-workspace/scripts/google_api.py \
  gmail search "in:inbox newer_than:1d" --max 100
```

Keep scan evaluation dry until relevance and deduplication are complete. Then perform one atomic state write. Build the final notification text from the exact persisted post-dedup list; do not hand-rewrite it afterward. To verify, inspect state membership or run a non-mutating repeat, not a second committing scan.

If the state file is missing, initialize it. If it exists but fails strict JSON parsing, fail closed and report the state error concisely—never treat an empty state as permission to alert.

## Google notification exclusions

Calendar agenda digests, event invitations, and routine birthday/no-event reminders are usually duplicate representations of Calendar data. Suppress them as Gmail alerts and surface only the underlying Calendar event when it independently passes relevance and deduplication. Apply hard newsletter/media/promotional exclusions before broad keyword matching.