---
name: daily-whatsapp-reminders
description: Recurring personal reminders delivered via WhatsApp, including morning habits, gratitude prompts, and medication reminders.
category: productivity
---
# Daily WhatsApp Reminders

Use this skill for recurring reminders that should be delivered via WhatsApp on a daily schedule.

## When to Use

- User wants a message sent every day at a specific local time
- The reminder should be brief, natural, and human-sounding
- The recipient is either the user or an explicitly authorized contact

## Core Rules

1. **Confirm schedule in the user's timezone**
   - Treat the user’s stated time as local time unless they say otherwise
   - For BRT/UTC-3, convert to UTC for cron scheduling
   - 8:00 BRT = 11:00 UTC

2. **Prefer short, natural Portuguese**
   - Keep the message to 1–2 sentences max
   - Use PT-BR, light and natural tone
   - Do not add questions, explanations, or trailing commentary
   - Avoid sounding repetitive; vary the phrasing across days

3. **Choose the delivery path correctly**
   - Immediate send: use the WhatsApp bridge HTTP API
   - Recurring send: use `hermes cron create` with a WhatsApp delivery target

4. **Use the WhatsApp delivery format**
   - Scheduled jobs use `--deliver whatsapp:{phone_number}`
   - Bridge sends use `{country_code}{area_code}{number}@c.us`

## Typical Workflow

1. Confirm the time and timezone
2. Confirm the target number or contact is authorized
3. Generate a short message in PT-BR
4. Send immediately via bridge, or schedule via `hermes cron create`
5. Verify delivery or next run time

## Message Style Guide

- Good: `Bom dia — hoje vale começar com gratidão.`
- Good: `Antes de tudo: respira, reconhece e agradece.`
- Good: `Lembrete rápido: agradeça por 3 coisas antes de começar o dia.`
- Bad: long explanations, questions, markdown, or stiff/robotic wording

## Pitfalls

- Do not confuse recurring jobs with one-time reminders
- Do not assume UTC when the user gave a local time in BRT
- Do not reuse the same phrasing every day
- Do not over-explain in the delivered message

## References

- See `references/cron-and-message-style.md` for the verified cron/bridge commands and the preferred reminder phrasing pattern.
