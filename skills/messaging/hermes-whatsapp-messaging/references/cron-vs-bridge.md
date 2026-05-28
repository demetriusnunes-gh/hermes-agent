# Cron vs bridge delivery for WhatsApp

Use these verified patterns:

## Immediate send (bridge)

```bash
curl -s http://127.0.0.1:3000/health
curl -s -X POST http://127.0.0.1:3000/send \
  -H 'Content-Type: application/json' \
  -d '{"chatId":"5521988490510@c.us","message":"Bom dia! Comece com gratidão: reconheça três coisas boas antes de agir."}'
```

- Health should return `{"status":"connected",...}`.
- WhatsApp `chatId` format: `{country_code}{area_code}{number}@c.us`.

## Scheduled send (cron)

Actual CLI:

```bash
hermes cron create "0 11 * * *" "Send a WhatsApp reminder" \
  --name "Daily reminder" \
  --deliver whatsapp:5521988490510
```

- `0 11 * * *` = 8:00 BRT (UTC-3) because cron runs in UTC.
- WhatsApp delivery target format: `whatsapp:{phone_number}`.
- For a different local time in BRT, add 3 hours for UTC.

## Pitfall

`cronjob(action="create", ...)` is legacy pseudo-code from old notes; prefer `hermes cron create` in this codebase.