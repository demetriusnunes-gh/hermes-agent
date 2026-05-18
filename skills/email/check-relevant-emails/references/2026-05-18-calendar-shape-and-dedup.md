# Calendar JSON shape and dedup notes

Observed in a successful run of `google_api.py calendar list`:

- The top-level payload may expose calendar entries under `events` rather than `items`.
- Treat either wrapper as valid: `items` if present, otherwise `events`.
- All-day reminders can appear as date-only `start` / `end` values and should still be considered for actionable financial/account reminders.
- Do **not** dedupe calendar items by raw Google event ID alone.
  - Prefer a stable hash built from visible fields, e.g. `sha:event:` + sha256(`"{summary}|{start}|{end}"`).
  - Optionally include calendar name if the upstream format requires it, but keep the visible-field hash as the primary key.
- Existing state can contain either bare digests or `sha:event:`-prefixed hashes; normalize both before comparison.
