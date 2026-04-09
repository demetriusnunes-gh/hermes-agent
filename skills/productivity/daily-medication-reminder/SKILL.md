---
name: daily-medication-reminder
description: Procedure for setting up daily medication reminders via WhatsApp for user's wife
category: productivity
---
# Daily Medication Reminder for Hermes Agent

## When to Use
When user requests a daily medication reminder for their wife (Fernanda Hamacher) via WhatsApp at a specific time each day.

## Why This Matters
This is a recurring, authorized task that needs to be set up reliably and communicated clearly to avoid medication misses.

## Prerequisites
- User has explicitly authorized sending daily medication reminders via WhatsApp to +5521988420759 (Fernanda Hamacher)
- WhatsApp bridge (Baileys) is configured and working on port 3000
- User's timezone is confirmed (typically BRT/UTC-3)

## Steps to Follow

1. **Verify Authorization**
   - Confirm user has authorized reminders to Fernanda Hamacher at +5521988420759
   - Check user memory for explicit authorization (stored in user profile)

2. **Confirm Time and Timezone**
   - Ask: "É para todos os dias às [time] horário de Brasília (BRT/UTC-3)?"
   - Get explicit confirmation of both time and timezone
   - Convert to UTC if needed for internal scheduling

3. **Set Up Reminder**
   - Use WhatsApp messaging tool to send reminder at confirmed time
   - Message content: "Lembrete de tomar o remédio, amor ❤️" (or user's preferred message)
   - Ensure message is sent via the dedicated AI WhatsApp: +5521990718408

4. **Confirm Setup**
   - Inform user: "Lembrete diário definido para [time] BRT para Fernanda via WhatsApp."
   - Offer to test immediately if user wants verification

5. **For One-Time Reminders**
   - If user specifies "só hoje" or similar, set for that specific date only
   - Confirm date and time clearly

## Example Interaction
User: "Me lembre de tomar remédio às 10h só hoje"
Agent: "É para hoje às 10h horário de Brasília (BRT/UTC-3), certo?"
User: "Sim"
Agent: "Lembrete definido para hoje às 10h BRT. Vou enviar no WhatsApp da Fernanda às 10h."

## Message Template
Use this format for medication reminders:
"Lembrete de tomar o remédio, amor ❤️"
Or customize based on user preference.

## Verification
- After sending, check that message was delivered via WhatsApp bridge logs
- For recurring reminders, verify next scheduled time matches expectation

## Related Knowledge
- User's wife: Fernanda Hamacher, WhatsApp: +5521988420759
- Dedicated AI WhatsApp number: +5521990718408
- Authorization exists in user profile for daily 9 AM BRT reminders (can be adapted for other times)
- WhatsApp communication uses Baileys bridge on port 3000