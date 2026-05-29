# Stateful Gmail/Calendar monitoring

When using this skill for scheduled inbox/calendar scans, treat duplicate alerts as a bug.

## Recommended pattern

1. Load persistent state before scanning, e.g. `~/.hermes/state/email-check-state.json`.
2. For Gmail, dedupe on both:
   - the Gmail message id, and
   - a computed stable hash for the notification unit (prefer thread-level hash if you want one alert per thread).
3. For Calendar, dedupe on both:
   - the event id, and
   - a computed stable hash from summary/start/end/location/description (or equivalent stable fields).
4. Remove any candidate already present in either `notified_ids` or `notified_hashes` before producing user-facing output.
5. If no new candidates remain, output exactly `[SILENT]`.
6. If new candidates remain, update the same state file in the same run before returning the report.
7. If auth fails, report the auth failure once concisely instead of replaying prior alerts.

## Practical note

A thread-level hash is useful for mailing lists and multi-message threads because it prevents multiple alerts for the same conversation when Gmail surfaces several messages from the same thread.

## False-positive guardrails seen in real runs

- Google Calendar notification emails (for example from `calendar-notification@google.com` / Google Agenda) are **not** government mail just because the subject contains `Notificação` or other generic Portuguese words.
- Treat newsletter/media senders as irrelevant even when they discuss government topics in the subject or body; the sender still needs to be an actual official source.
- When a calendar or inbox notification is clearly just a reminder/update and not a real actionable item, keep it out of the alert set unless it matches a high-confidence school/financial/security case.
