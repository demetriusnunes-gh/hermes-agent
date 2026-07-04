# Session observations: Gmail/Calendar monitoring

Date: 2026-06-03

## High-confidence items that were worth alerting

- Claro bill email: `Fatura Claro` / `Sua Fatura Digital Claro chegou` with a visible due date in the body.
- Agenda Edu / Escola Eleva school notices, including:
  - `novo comunicado`
  - `cardápio`
  - `mensagem para as famílias`
- Amazon Prime account change: `Confirmation of Prime membership change` confirming a pause.

## Items that were correctly ignored

- Promotional travel/retail senders with topical subjects, including Airbnb and Booking.com.
- Media/newsletter senders, even when they mention politics, finance, or government topics.
- Generic Google Calendar digest emails like `Você não tem nenhum evento programado para hoje.`
- Public-event/news sender traffic that is not an actionable bill/account/school/security notice.

## Operational note

For monitoring runs, preserve both the raw Gmail message id and a stable visible-field hash in suppression state. Rewriting `~/.hermes/state/email-check-state.json` in the same run after the final candidate set is frozen prevented duplicate alerts.
