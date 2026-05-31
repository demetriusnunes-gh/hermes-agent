---
name: whatsapp-messaging-automation
description: Send and automate WhatsApp messages via a local bridge, including cron-driven reminders, connectivity checks, and delivery verification.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [whatsapp, messaging, automation, cron, reminders, bridge]
---

# WhatsApp Messaging Automation

Use this skill for class-level WhatsApp delivery work: one-off sends, scheduled reminders, and bridge-backed automation.

## When to Use

- Sending a WhatsApp message to a specific recipient or self-chat target
- Creating a scheduled WhatsApp reminder via cron
- Verifying the WhatsApp bridge is connected before sending
- Debugging delivery failures or confirming the last successful send

## Core Flow

1. **Confirm the bridge is healthy** before trying to send.
2. **Use the bridge HTTP API directly** for immediate sends.
3. **Use UTC cron expressions** for scheduled jobs; convert local user time to UTC first.
4. **Verify success** from the API response and, when useful, from bridge logs.

## Sending a Message

Prefer the bridge HTTP API when you need a direct send:

```bash
curl -sS -X POST http://127.0.0.1:3000/send \
  -H 'Content-Type: application/json' \
  -d '{"chatId":"<chat_id>","message":"<plain text message>"}'
```

## Schedule Conversion

Cron in Hermes runs in UTC. Convert the requested local time before creating or editing the schedule.

- 8:00 BRT (UTC-3) → `0 11 * * *`
- 9:00 BRT (UTC-3) → `0 12 * * *`
- 10:00 BRT (UTC-3) → `0 13 * * *`

## Message Style for Reminders

For recurring reminders, keep the content:

- short
- plain text
- non-questioning
- naturally varied across runs

When the user asks for a repeating reminder, rotate phrasings instead of reusing the same sentence.

## Verification

After sending or scheduling:

- confirm the bridge health endpoint reports `connected`
- check the send API returns success
- inspect bridge logs if a send looks suspicious or needs auditability

## Pitfalls

- Cron schedules must be entered in UTC, not local time.
- WhatsApp bridge messages should stay plain text; avoid markdown-heavy formatting.
- For recurring reminders, vary the wording so the output does not sound automated.
- If the recipient is represented by a WhatsApp-origin chat, use the stored origin chat id from the job record rather than guessing a new identifier.

## References

- See `references/bridge-and-cron.md` for a compact runbook, example payloads, and notes from a successful WhatsApp reminder automation.
