# False-positive notes for email/calendar monitoring

This file records sender/content patterns that looked relevant at first glance but should usually be ignored during scheduled monitoring.

## Session examples

- **Nespresso** marketing mail about capsules running low: promotional; not actionable on its own.
- **Let's Get Rusty** tutorial/newsletter content: editorial/promotional, not a high-confidence alert.
- **The Pragmatic Engineer** and similar coding newsletters: useful reading, but not a monitoring alert unless they carry a direct account/billing/security notice.
- **Medium Weekly Digest** items: digest/newsletter traffic; ignore unless a specific direct account/security/payment issue is present.
- **G1 / the news** newsletters discussing government or security topics: the sender is still a media/newsletter source, so treat as irrelevant for alerting.
- If a broad inbox search returns digest/editorial sources, suppress by sender class first; do not let topical keywords rescue them.

## Filtering reminder

A keyword match such as "security", "login", "invoice", or "government" is not enough by itself. Keep the sender and message type in view, and only alert when the source is an actual account/system, biller, school, agency, or similarly high-confidence sender.