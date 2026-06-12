# Stateful Gmail/Calendar monitoring

When using this skill for scheduled inbox/calendar scans, treat duplicate alerts as a bug.

## Recommended pattern

1. Load persistent state before scanning, e.g. `~/.hermes/state/email-check-state.json`.
2. The state file may contain both `notified_ids` and `notified_hashes`; treat either one as sufficient to suppress a candidate.
3. Normalize hash tokens before comparison: treat bare SHA-256 digests and prefixed forms like `sha:` / `sha:event:` as equivalent so legacy state still dedupes cleanly.
4. For Gmail, dedupe on both:
   - the Gmail message id, and
   - a computed stable hash for the notification unit (prefer thread-level hash if you want one alert per thread).
5. For Calendar, dedupe on both:
   - the event id, and
   - a computed stable hash from summary/start/end/location/description (or equivalent stable fields).
6. Remove any candidate already present in either `notified_ids` or `notified_hashes` before producing user-facing output.
7. If no new candidates remain, output exactly `[SILENT]`.
8. If new candidates remain, update the same state file in the same run before returning the report.
9. If auth fails, report the auth failure once concisely instead of replaying prior alerts.

## Practical note

A thread-level hash is useful for mailing lists and multi-message threads because it prevents multiple alerts for the same conversation when Gmail surfaces several messages from the same thread.

## Session notes

- In Hermes workers, if you need to parse the on-disk state as strict JSON, read the file directly from disk in the worker/terminal instead of using the line-numbered file reader output. The file reader is excellent for inspection, but its `LINE_NUM|CONTENT` formatting is not raw JSON.
- Gmail search payloads can include raw control characters or very HTML-heavy snippets; if strict JSON parsing fails, switch to a tolerant parser and re-fetch the small final candidate set with `gmail get` before deciding relevance.
- Some calendar finder wrappers validate the ordering enum case-sensitively and require `startTime` rather than `starttime` or `updated`.
- Gmail monitoring is cleaner if you normalize on one canonical alert per thread after relevance filtering. When collapsing a thread, persist **all Gmail message IDs observed in that thread**, not just the representative message ID, so later Gmail searches cannot re-alert a sibling message from the same conversation.
- For combined Gmail + Calendar scans, keep a single post-dedup candidate list and render the final report directly from that exact list after the state file has been updated. Do not hand-rewrite or trim the report from memory, or a newly detected item can be accidentally omitted even though it was persisted.
- Treat the dedup state file as safety-critical: if `~/.hermes/state/email-check-state.json` is missing, initialize it; if it exists but cannot be parsed, fail closed with a concise state/auth-style error instead of alerting from an empty state, because duplicate notifications are worse than a missed cron run.

## False-positive guardrails seen in real runs

- Google Calendar notification emails (for example from `calendar-notification@google.com` / Google Agenda) are **not** government mail just because the subject contains `Notificação` or other generic Portuguese words.
- Treat newsletter/media senders as irrelevant even when they discuss government topics in the subject or body; the sender still needs to be an actual official source.
- Treat provider newsletters and promotional bank/financial marketing as irrelevant even if they contain generic health/security/finance words (for example Care Plus newsletters or Itaú account ads); require a concrete actionable item such as an appointment, bill, statement, due date, login/security alert, or school notice.
- When a calendar or inbox notification is clearly just a reminder/update and not a real actionable item, keep it out of the alert set unless it matches a high-confidence school/financial/security case.
