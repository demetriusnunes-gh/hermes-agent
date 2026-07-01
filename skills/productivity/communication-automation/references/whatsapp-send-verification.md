# WhatsApp send verification recipe

Use this recipe when a scheduled job needs to send a short WhatsApp reminder and you want a deterministic verification path.

## Minimal flow

1. Check bridge health first:
   - `GET http://127.0.0.1:3000/health`
2. Send the message through the bridge:
   - `POST http://127.0.0.1:3000/send`
   - Body shape: `{ "chatId": "<target>@c.us", "message": "<plain text>" }`
3. Verify success from the HTTP response:
   - `200 OK`
   - JSON payload includes `success: true`
   - capture `messageId` or `messageIds` if present

## Message style for recurring reminders

- Keep the text short and plain.
- Prefer a single sentence, or at most two.
- Vary phrasing between runs so the reminder does not feel repetitive.
- For gratitude reminders, natural Brazilian Portuguese works best, e.g.:
  - `Bom dia! Comece com gratidão antes da correria.`
  - `Antes de tudo: respira, reconhece e agradece.`
  - `Lembrete rápido: agradeça por 3 coisas antes de começar o dia.`

## Notes

- If the send backend exposes a raw WhatsApp `chatId`, use it directly instead of guessing a human-friendly label.
- Prefer plain text over formatting unless the bridge explicitly documents richer markup support.
