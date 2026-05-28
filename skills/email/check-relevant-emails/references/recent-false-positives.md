# Recent false-positive guards

- **Gmail delivery failures** like `Mail Delivery Subsystem` / `Delivery Status Notification (Failure)` are usually **not** relevant by themselves.
  - Only flag if the body clearly ties the bounce to a specific real order, invoice, or family/priority message that needs attention.
- **Body keywords alone are not enough** when the sender is clearly a newsletter, promo, or automated marketing source.
- `notificação` / `comunicado` inside Google Calendar notifications, general automation, or newsletters is **not** a government signal by itself.
- `IR` / `ir` should be treated as priority only when it is a standalone tax/income reference with corroborating sender/context; do not infer it from unrelated Portuguese words or finance/travel marketing.
- Shopping/payment confirmations and travel promos can share words like `compra`, `pedido`, `pagamento`, `reserva`, or `segurança`; treat them as priority only when the rest of the sender/context clearly indicates a real order or account issue.
- For school-related mail, prefer senders/subjects that clearly indicate the school itself or an actual school communication; incidental mentions of `Eleva` inside newsletters should stay unflagged.
