# Email + calendar state hygiene

Use this when a scheduled monitoring job maintains a persistent suppression file for Gmail and Calendar.

## Goals

- prevent repeat alerts for the same item
- keep the on-disk state compact and readable
- avoid re-alerting items after a temporary scan glitch or noisy run
- stay silent when no unseen, high-confidence items remain

## Practical recipe

1. Load the suppression file before scanning.
2. Build candidate alerts conservatively.
3. Deduplicate each candidate against **both**:
   - its stable backend ID, and
   - a stable content hash
4. Remove already-seen candidates **before** any user-facing output.
5. Freeze the final candidate list.
6. Update the suppression file in the **same run** so newly accepted items cannot be re-alerted later.
7. If every candidate is already seen, emit exactly `[SILENT]`.

## Recommended hashes

- Gmail: sender + normalized subject + date, or a thread/message-level stable fingerprint
- Calendar: summary + start + end + location + description

## Cleanup guidance

- Keep only the suppression keys that are still useful for future deduplication.
- If legacy prefixes exist for stored hashes, normalize them before comparison.
- If the file has accumulated stale or noisy entries, rewrite it cleanly from the current accepted suppression set rather than appending blindly.
- Treat repeated notification of the same email or event as a bug, not a benign duplicate.

## Verification

- Re-read the saved state after writing if the run is expected to be durable.
- Confirm that a second identical scan would produce no new alerts.
- If auth/backend fails, report the failure once instead of replaying previous alerts.
