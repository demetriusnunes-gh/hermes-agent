# 2026-05-26: Calendar notification and generic-comunicado false positives

## What happened
During a Gmail/Calendar scan, two items looked superficially government-ish because they contained `notificação` / `comunicado`:
- Google Calendar notification from `calendar-notification@google.com` with a family event title.
- `Saúde Petrobras` email with `comunicados@saudepetrobras.com.br` in the sender and a credential/benefits-style subject.

Neither should be treated as government/public-agency mail.

## Updated guardrail
- `notificação` / `comunicado` alone are **not** government signals.
- Require a real public-agency sender (`.gov.br` or obvious government agency domain/name) before flagging.
- If the sender is Google Calendar, corporate benefits, insurer, employer communications, or a newsletter/media source, treat government keywords as non-authoritative unless the sender itself is clearly official.

## Practical rule
Prefer this ordering:
1. `.gov.br` or obvious agency sender → relevant
2. Keyword-only match with non-government sender → usually irrelevant
3. Newsletter/media/promotional sender discussing public topics → irrelevant
