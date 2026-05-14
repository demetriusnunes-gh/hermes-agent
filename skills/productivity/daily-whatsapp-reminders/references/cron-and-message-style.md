# Recurring WhatsApp reminder: verified commands and style notes

## Verified cron command

```bash
hermes cron create "0 11 * * *" "Send a WhatsApp reminder"
  --name "Daily reminder"
  --deliver whatsapp:5521988490510
```

- `0 11 * * *` = 8:00 BRT (UTC-3) because Hermes cron runs in UTC.
- Delivery target format: `whatsapp:{phone_number}`.

## Verified immediate send

```bash
curl -s http://127.0.0.1:3000/health
curl -s -X POST http://127.0.0.1:3000/send \
  -H 'Content-Type: application/json' \
  -d '{"chatId":"5521988490510@c.us","message":"Bom dia! Comece com gratidão: reconheça três coisas boas antes de agir."}'
```

- Health should return `{"status":"connected",...}` before sending.
- Direct send format is `{country_code}{area_code}{number}@c.us`.

## Message style rule

For daily reminder content, keep the delivered text:

- short: 1–2 sentences max
- natural PT-BR
- no questions
- no explanations
- varied day-to-day to avoid repetition

## Good reminder variants

- `Bom dia — hoje vale começar com gratidão.`
- `Antes de tudo: respira, reconhece e agradece.`
- `Lembrete rápido: agradeça por 3 coisas antes de começar o dia.`