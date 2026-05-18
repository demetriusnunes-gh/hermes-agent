# 2026-05-18: Google Workspace API JSON shapes and dedup-safe calendar handling

Observed during a real cron run:

## google_api.py output shapes
- `gmail search` returns a JSON object, not a bare array:
  - keys: `messages`, `query`, `resultSizeEstimate`
  - each message summary includes `id`, `from`, `subject`, `date`
- `calendar list` returns a JSON object, not a bare array:
  - keys: `count`, `events`, `timeMin`, `timeMax`
  - each event includes `id`, `summary`, `start`, `end`, `location`, `description`, `status`, `htmlLink`

## Practical implication
- Code that consumes the wrapper must unwrap `messages` / `events` before iterating.
- A direct `for item in fetch_json(...)` will fail if the tool output is a dict.

## Calendar dedup normalization
- All-day events can surface as `YYYY-MM-DD` start/end values.
- For stable event hashing, normalize date-only values before hashing:
  - start → `YYYY-MM-DDT00:00:00`
  - end → `YYYY-MM-DDT23:59:59`

## Date handling for Gmail hashes
- Gmail search dates are RFC 2822 strings, so hash generation should normalize them to ISO 8601 first when possible.
- If parsing fails, keep the original string rather than dropping the item.
