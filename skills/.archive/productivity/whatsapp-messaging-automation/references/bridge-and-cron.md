# WhatsApp bridge and cron notes

This reference captures a proven pattern for sending a short WhatsApp reminder through the local bridge and scheduling it as a daily cron job.

## Bridge health check

```bash
curl -sS http://127.0.0.1:3000/health
```

Expected shape:

```json
{"status":"connected","queueLength":0,"uptime":...}
```

## Direct send example

```bash
curl -sS -X POST http://127.0.0.1:3000/send \
  -H 'Content-Type: application/json' \
  -d '{"chatId":"203873557991626@lid","message":"Bom dia — reconheça o que já está dando certo antes de começar."}'
```

Observed successful response:

```json
{"success":true,"messageId":"3EB0F3BC9C51320F73B855","messageIds":["3EB0F3BC9C51320F73B855"]}
```

## Cron timing

Hermes cron jobs run in UTC.

- 8:00 BRT (UTC-3) → `0 11 * * *`

## Example automation shape

- recipient name: Demetrius Nunes
- delivery target: WhatsApp origin chat (`203873557991626@lid`)
- message style: short, plain text, no questions, light natural tone in pt-BR
- daily variation: rotate phrasing instead of reusing the same sentence

## Useful verification cues

- bridge health says `connected`
- send API returns `success: true`
- bridge log records the send if you need to audit the delivery
