# False-positive notes from monitoring runs

Concise notes for scheduled Gmail + Calendar monitoring.

## Patterns to reject

- Promotional senders that contain security/account-like words in the subject or snippet.
- Google Calendar notification emails that say things like "notificação" or "Você não tem nenhum evento programado para hoje" unless they are clearly actionable and high-confidence.
- Commercial newsletters or promos that mention government topics; treat the sender context as decisive.
- Calendar entries or reminders that are only generic reminders without a clear task.

## Patterns to keep

- Direct family contacts.
- School communications from the school or school-domain senders.
- Real security alerts for an actual account.
- Shipping / order / payment notices with clear transaction context.

## Dedup reminder

Before producing user-facing output, remove every candidate already present in either:
- `notified_ids`
- `notified_hashes`

If nothing survives, output `[SILENT]`.
