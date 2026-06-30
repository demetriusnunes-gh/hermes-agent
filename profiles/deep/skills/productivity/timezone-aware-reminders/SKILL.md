---
name: timezone-aware-reminders
description: Guidelines for setting time-based reminders when user and server are in different timezones
category: productivity
---
# Timezone-aware Reminders for Hermes Agent

## When to Use
When setting time-based reminders for users in different timezones, especially when the server operates in UTC but the user is in a different timezone (e.g., BRT/UTC-3).

## Why This Matters
The Hermes agent often runs on servers in UTC timezone, while users may be in various local timezones. Miscommunication about times can lead to missed reminders or confusion.

## Steps to Follow

1. **Confirm User's Timezone**
   - Always ask or verify the user's current timezone before setting any time-based reminder
   - Check user memory/profile for stored timezone preference
   - Common timezones: BRT (UTC-3) for Brazil, EST (UTC-5), PST (UTC-8), etc.

2. **Convert Times Explicitly**
   - When user says "X o'clock", clarify: "Is that X o'clock in your local time?"
   - If setting reminder, convert user's local time to UTC for internal scheduling
   - Formula: UTC time = Local time - timezone offset
   - Example: 10:00 BRT (UTC-3) = 13:00 UTC

3. **Communicate Clearly**
   - When confirming reminders, state both times:
     - "Lembrete definido para 10h horário de Brasília (13h UTC)"
   - This prevents confusion if the user sees logs or system messages in UTC

4. **Handle Edge Cases**
   - Daylight saving time changes
   - Users traveling between timezones
   - Ambiguous references like "meio-dia" or "meia-noite"

5. **Verification**
   - After setting reminder, ask user to confirm the time in their local timezone
   - For recurring reminders, verify the schedule matches expectations

## Example Interaction
User: "Me lembre de tomar remédio às 10h"
Agent: "Quer dizer às 10h horário de Brasília (BRT/UTC-3)?"
User: "Sim"
Agent: "Lembrete definido para hoje às 10h BRT (13h UTC). Vou te avisar no WhatsApp."

## Pitfalls to Avoid
- Assuming server timezone matches user timezone
- Not confirming timezone before setting time-based actions
- Failing to communicate both local and UTC times in confirmations
- Forgetting to adjust for daylight saving when applicable

## Related Knowledge
- User timezone information is stored in memory under 'user' target
- Default user timezone for Demetrius Nunes is BRT (UTC-3)
- Server typically runs in UTC timezone
