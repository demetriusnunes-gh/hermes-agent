---
name: one-time-reminder
description: Procedure for setting up one-time reminders for specific dates and times
category: productivity
---
# One-Time Reminder for Hermes Agent

## When to Use
When user requests a reminder for a specific date and time, not recurring (e.g., "só hoje", "amanhã às 15h").

## Why This Matters
One-time reminders need clear date/time confirmation and should not be confused with recurring schedules.

## Steps to Follow

1. **Clarify Date and Time**
   - Ask for explicit date if not specified (e.g., "Você quer dizer hoje, [data atual]?")
   - Confirm time in user's local timezone
   - Example: "É para hoje às [time] horário de Brasília (BRT/UTC-3)?"

2. **Confirm Timezone**
   - Always verify timezone to avoid confusion
   - Check user memory/profile for stored timezone
   - Common: BRT (UTC-3) for Brazil users

3. **Set Up Reminder**
   - Use appropriate tool based on reminder type:
     - WhatsApp: for personal reminders to contacts
     - Telegram: for user self-reminders
     - Other: as specified by user
   - Schedule for exact date/time confirmed
   - Ensure message content is clear and matches user intent

4. **Communicate Confirmation**
   - State both local and UTC time for clarity:
     - "Lembrete definido para hoje às 10h BRT (13h UTC) via WhatsApp para Fernanda."
   - Specify that it's one-time, not recurring

5. **Verification Offer**
   - Ask if user wants a test reminder or confirmation when sent
   - For time-sensitive reminders, offer to notify when sent

## Example Interaction
User: "Me lembre de tomar remédio às 10h só hoje"
Agent: "É para hoje às 10h horário de Brasília (BRT/UTC-3), certo?"
User: "Sim"
Agent: "Lembrete definido para hoje às 10h BRT. Vou enviar no WhatsApp da Fernanda às 10h."

## Message Content
- Use user-specified message if provided
- For medication reminders: consider adding emoji or affectionate tone if appropriate
- Keep clear and actionable

## Pitfalls to Avoid
- Assuming "hoje" without confirming date (especially near midnight)
- Not confirming timezone, leading to off-by-hours errors
- Accidentally setting as recurring when user wants one-time
- Failing to specify that reminder is one-time in confirmation

## Related Knowledge
- timezone-aware-reminders skill for timezone handling
- daily-medication-reminder skill for medication-specific reminders
- User's wife contact: Fernanda Hamacher, +5521988420759 (WhatsApp)
- Dedicated AI WhatsApp: +5521990718408