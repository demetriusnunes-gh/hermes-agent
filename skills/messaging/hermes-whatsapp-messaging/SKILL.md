---
name: hermes-whatsapp-messaging
description: Send WhatsApp messages via the Baileys bridge HTTP API, verify connectivity, and set up cron jobs for WhatsApp delivery.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [WhatsApp, Messaging, Cron, Baileys, Self-chat]
---

# Hermes WhatsApp Messaging Operations

Send WhatsApp messages and set up automated WhatsApp delivery via cron.

## When to Use

- User asks to send a WhatsApp message to someone
- User wants automated WhatsApp delivery (reminders, notifications)
- Testing WhatsApp bridge connectivity

## Prerequisites

- WhatsApp bridge running on port 3000 (self-chat mode)
- Node.js available
- Bridge dependencies installed

## Step 1: Verify WhatsApp Connectivity

```bash
curl -s http://127.0.0.1:3000/health
# Expected: {"status":"connected","queueLength":0,"uptime":...}
```

If the health endpoint doesn't return "connected", the bridge isn't running. Check:
```bash
# Is the bridge process running?
pgrep -f "bridge.js"
# Check the log
cat ~/.hermes/whatsapp/bridge.log
```

If the gateway isn't running:
```bash
systemctl status hermes-gateway
systemctl start hermes-gateway
```

## Step 2: Send a WhatsApp Message

Direct HTTP API call to the bridge:

```bash
curl -s -X POST http://127.0.0.1:3000/send \
  -H "Content-Type: application/json" \
  -d '{"chatId":"5521988420759@c.us","message":"Your message here"}'
```

**Number format**: Use the full international number without `+`, followed by `@c.us`:
- Brazil: `5521XXXXXXXXX@c.us`
- Format: `{country_code}{area_code}{number}@c.us`

**Response**:
- Success: `{"success":true,"messageId":"3EB0..."}`
- Failure: `{"success":false,"error":"..."}` 

## Step 3: Cron Job for WhatsApp Delivery

When setting up a cron job that delivers via WhatsApp, use the deliver format:

```
deliver: "whatsapp:{phone_number}"
```

Example cron job:
```python
cronjob(action="create",
    name="Daily reminder",
    deliver="whatsapp:5521988420759",
    schedule="0 11 * * *",  # Always UTC!
    prompt="Send a message to X reminding them of Y")
```

**Important**: The cron scheduler runs in UTC. Convert BRT time to UTC:
- 8 AM BRT = 11 AM UTC (schedule: `0 11 * * *`)
- 10 AM BRT = 1 PM UTC (schedule: `0 13 * * *`)

## Step 4: Verify Cron Sent Successfully

```bash
# Check cron job status
cronjob(action="list")

# Check bridge logs for send activity
tail -20 ~/.hermes/whatsapp/bridge.log
```

## Self-Chat Mode

This setup uses `self-chat` mode — the bridge uses your own WhatsApp account to send messages.
This means:
- All messages appear as coming from your WhatsApp account
- The recipient sees a normal WhatsApp message from you
- No bot account needed

## Pitfalls

1. **Cron runs asynchronously** — `cronjob(action="run")` starts the job but doesn't block. The job runs in a fresh session with no current-chat context.
2. **Gateway must be running for cron WhatsApp delivery** — The bridge needs to be connected at cron execution time. If the gateway is down, the message won't send.
3. **Use the bridge HTTP API directly for immediate testing** — More reliable than relying on the cron runner to handle gateway state.
4. **Bridge port is usually 3000** — Check config.yaml `whatsapp.extra.bridge_port` if it differs.
5. **No markdown in WhatsApp messages** — WhatsApp doesn't support rich formatting via the bridge API. Keep messages plain text.
