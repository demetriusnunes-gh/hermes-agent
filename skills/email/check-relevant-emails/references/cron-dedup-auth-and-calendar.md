# Cron Run Notes: Dedup, Auth, and Calendar Relevance

Observed during a live check:

## Auth caveat
`python setup.py --check` can return:

- `AUTHENTICATED (partial): Token refreshed but missing 2 scopes`
- with missing `documents.readonly` and `drive.readonly`

For this skill, that is still acceptable if Gmail/Calendar access works. Treat it as a warning, not a hard failure.

## Dedup hash normalization
When building `sha:{sender_email}|{subject}|{date_iso}`:

- extract the raw address from the `From` header
- do **not** hash the display name
- keep the header `Date` normalized to ISO 8601 before hashing

Example:
- `Agenda Edu <no-reply@contato.agendaedu.com>` → `no-reply@contato.agendaedu.com`

## Calendar reminders
Calendar results may include all-day reminders that are still relevant when they are concrete action items, including financial/account reminders such as bill payments.

Example seen in practice:
- `Pagar Nubank` (all-day reminder) — relevant financial follow-up
