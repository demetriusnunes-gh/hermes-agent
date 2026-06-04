---
name: communication-automation
description: Automate and monitor personal communications across email, calendar, and messaging channels with conservative filtering, scheduling, deduplication, and delivery verification.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Email, Calendar, Messaging, Automation, Cron, Dedup, Verification]
---

# Communication Automation

Use this skill for class-level workflows that move information between the user's communication channels and the outside world, especially when the task needs to stay conservative, deduplicated, scheduled, and verifiable.

This skill covers two common patterns:
- inbound monitoring of Gmail/Calendar for actionable items
- outbound delivery of WhatsApp messages and reminders

## Shared principles

- Prefer conservative filtering over broad extraction.
- Deduplicate against both stable IDs and stable content hashes when available.
- Stay silent when there is nothing high-confidence to report.
- Treat scheduled jobs as UTC unless the scheduler explicitly says otherwise.
- Verify the result from the backend response or state change before reporting success.
- Keep reminder text short, plain, and naturally varied when it repeats.

## Inbound monitoring pattern: email + calendar

Use this subsection when scanning Gmail or Calendar for new actionable items.

### Workflow

1. Check authentication or backend connectivity first.
2. Load any suppression or state file before scanning.
3. Search the inbox/calendar conservatively.
4. Re-fetch noisy candidates if search snippets are messy or incomplete.
5. Collapse multi-message threads or repeated calendar hits into one alert.
6. Update the suppression state only after the final candidate set is frozen.
7. If nothing new survives filtering and deduplication, output exactly `[SILENT]`.

### Filtering guidance

- Prefer high-confidence personal, billing, shipping, school, government, job, or account/security items.
- Ignore newsletters, promos, bulk mail, and low-signal marketing.
- Do not promote a weak keyword match over an obviously promotional sender.
- Treat category labels as hints, not truth.
- When a sender class is obviously irrelevant, exclude it before topical keyword matching.

### Implementation hints

- Use stable hashes over sender/subject/date or visible event fields when raw IDs are not enough.
- Normalize legacy hash prefixes before comparing suppression entries.
- Rewrite state snapshots cleanly if the on-disk file is malformed or stale.

## Outbound delivery pattern: WhatsApp reminders and sends

Use this subsection when sending a WhatsApp message, scheduling a reminder, or verifying delivery.

### Workflow

1. Confirm the bridge or send backend is healthy.
2. Resolve the correct recipient/chat identifier explicitly.
3. Convert local times to UTC before creating cron schedules.
4. Send plain-text messages unless the bridge explicitly supports richer formatting.
5. Verify success from the API response and, if needed, bridge logs.

### Message style

- short
- plain text
- non-questioning for reminders
- varied phrasing across recurring runs

### Scheduling guidance

- Cron expressions should be treated as UTC.
- Convert local time to UTC before storing or editing the schedule.
- For recurring reminders, avoid repetitive phrasing that sounds machine-generated.

## Pitfalls

- Do not confuse a monitoring workflow with a general inbox browser.
- Do not emit multiple alerts for the same thread or event.
- Do not trust search snippets when they contain HTML-heavy or control-character noise.
- Do not assume a message was delivered just because the schedule was created.
- Do not guess a recipient identifier when a stored one exists.

## Verification checklist

- Authentication or bridge health checked first
- Relevant items filtered conservatively
- Deduplication applied before output
- State updated only after final candidate selection
- `[SILENT]` returned when nothing new remains
- Delivery or scheduling success confirmed from the backend response
- Cron timings converted to UTC
