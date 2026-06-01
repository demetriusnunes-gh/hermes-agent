# Monitoring state format and normalization

Use this file as the canonical reference for `~/.hermes/state/email-check-state.json`.

## Suggested fields

- `last_run_at`: ISO-8601 timestamp for the most recent scan
- `notified_ids`: bounded list of Gmail message IDs and calendar event IDs already alerted
- `notified_hashes`: bounded list of stable suppression hashes already alerted

## Normalization rules

Before comparing or storing hashes:

- lowercase
- trim whitespace
- treat bare SHA-256 digests and prefixed forms as equivalent:
  - `sha:<hex>`
  - `sha:event:<hex>`
  - `sha:thread:<hex>`
- compare against normalized values only

## Gmail hash suggestion

Prefer a stable hash of:

- sender email address
- normalized subject
- visible date string

If a thread contains multiple messages, emit one alert per thread and use the newest message as the canonical representative.

## Calendar hash suggestion

Prefer a stable hash of:

- summary
- start time
- end time
- location
- description

## Safe update pattern

1. Load current state.
2. Build the final candidate list.
3. Remove anything already present in `notified_ids` or `notified_hashes`.
4. Rewrite the state file from the deduplicated in-memory snapshot.
5. Only then return output.

This avoids duplicate alerts after partial or provisional runs.
