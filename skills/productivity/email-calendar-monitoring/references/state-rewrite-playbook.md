# Monitoring state rewrite playbook

Use this when the scheduled Gmail/Calendar monitor reads or rewrites `~/.hermes/state/email-check-state.json`.

## Goal

Keep suppression state canonical so the same email or calendar event is never re-alerted once it has been notified.

## Reliable sequence

1. Read the state file from disk before scanning.
2. Parse the current suppression set into memory.
3. Normalize all stored IDs and hashes before comparison.
4. Build the final candidate list.
5. Remove anything already present in either suppression list.
6. Freeze the final candidate set.
7. Rewrite the entire state file from the clean in-memory snapshot.
8. Only then return user-facing output.

## Recovery notes

- If a strict JSON parse fails, recover with a tolerant parse path rather than skipping deduplication.
- If the file contains extra junk outside the main JSON object, rebuild the file from the clean in-memory snapshot instead of appending more data.
- Keep the output step separate from the state-write step so a provisional candidate never leaks into the final alert list.

## Canonicalization reminders

- Gmail: dedupe on message ID and a stable sender+subject+date hash.
- Calendar: dedupe on a stable visible-field hash such as summary+start+end(+location+description when available).
- Normalize legacy hash prefixes like `sha:`, `sha:event:`, and `sha:thread:` before comparison.
