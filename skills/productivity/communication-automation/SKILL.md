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
- Load any persistent suppression file before scanning, and remove already-seen candidates before any user-facing output.
- For state-hygiene details, see `references/email-calendar-state-hygiene.md`.
- For stale cron skill-name warnings and alias drift, see `references/legacy-skill-name-mismatch.md`.
- Stay silent when there is nothing high-confidence to report.
- Treat scheduled jobs as UTC unless the scheduler explicitly says otherwise.
- Verify the result from the backend response or state change before reporting success.
- Keep reminder text short, plain, and naturally varied when it repeats.

## Skill-name hygiene for scheduled jobs

- Treat `Skill(s) not found and skipped` as a warning that the job's skill layer was not loaded, not necessarily that the whole cron job failed.
- When a scheduled workflow is renamed or split, update the cron job metadata to the current umbrella skill name or add a compatibility alias if the old name must persist.
- Prefer one maintained umbrella skill with references over a chain of narrow legacy names in cron metadata.
- When a job already contains the full prompt logic, removing a stale `skills` entry is often cleaner than keeping a dead reference around.

## Model/provider hygiene for scheduled communication jobs

- If a recurring communication job is important or user-facing, inspect its stored `model`, `provider`, and `base_url` fields when debugging failures or creating/updating the job.
- `model: null` / `provider: null` means the job inherits the current global model config and fallback chain. That can unexpectedly route through a fallback model the user never explicitly chose for that job.
- When the user is surprised by a cron job using an unexpected model, explain the distinction between an explicit per-job override and inherited global fallback selection.
- To prevent future surprise on critical monitoring jobs, pin the intended provider/model on the job with a per-job model override after verifying the current default is the desired one.
- Do not preserve deprecated/free OpenRouter fallbacks in job-specific configuration; prefer the intended default provider/model or a maintained fallback chain.

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
- Include workspace retention, deletion, or access-change warnings as actionable alerts when they materially affect access or data retention.
- Ignore newsletters, promos, bulk mail, and low-signal marketing.
- Do not promote a weak keyword match over an obviously promotional sender.
- Treat category labels as hints, not truth.
- When a sender class is obviously irrelevant, exclude it before topical keyword matching.

### Implementation hints

- Use stable hashes over sender/subject/date or visible event fields when raw IDs are not enough.
- Normalize legacy hash prefixes before comparing suppression entries.
- For Google Workspace cron scans, prefer the CLI wrapper for deterministic JSON and re-fetch only the final candidate set.
- Keep the suppression/state update in the same run as the final filtering step.
- See `references/monitoring-workflow.md` for the concrete scan recipe.
- Rewrite state snapshots cleanly if the on-disk file is malformed or stale.

## Outbound delivery pattern: WhatsApp reminders and sends

Use this subsection when sending a WhatsApp message, scheduling a reminder, or verifying delivery.

- See `references/whatsapp-target-resolution.md` for exact WhatsApp target resolution and bridge fallback details.

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
- If the user gives only a *date* (no time), make the chosen default time explicit in the confirmation so the schedule is not ambiguous.
- When a reminder is about a one-off obligation already handled by the user (for example, "already scheduled, just verify funds"), keep the reminder short and state the verification action rather than re-explaining the task.

## Scheduled news digest pattern

Use this subsection for cron-generated morning briefings, especially when the user wants an ultra-short world/Brazil/local/business digest.

### Workflow

1. Prefer live feed/search sources over memory.
2. Query a small set of high-signal sources first; use broad news aggregation only as a fallback.
3. Prioritize the requested geography or topic window before general headlines.
4. Collapse similar stories and keep only the most consequential item from each bucket.
5. If a delivery spec says to be ruthless about brevity, emit only the minimum number of stories allowed.
6. If a requested specialized skill is unavailable, continue with the closest class-level workflow rather than stopping.
7. If nothing high-confidence or materially relevant survives filtering, return exactly `[SILENT]`.

### Source selection guidance

- Favor Reuters for world/business and G1 for Brazil/São Paulo/Rio when available.
- For regional digests, use targeted query terms such as `Brazil`, `São Paulo`, `Rio de Janeiro`, and any named company/topic like `DoorDash`.
- Treat search results and feed items as candidates, not final stories; choose only the clearest, newest, and most relevant ones.
- For market/company items, include a stock move line only when the update is materially relevant and recent.

### Formatting guidance

- Header should be date only.
- Keep the total story count within the requested cap before writing.
- One short bullet per story.
- Avoid URLs unless a story cannot be identified otherwise.
- Do not add explanation, caveats, or category subtitles unless explicitly requested.

### Verification hints

- Check that the final output matches the required line count before returning.
- Verify that any silence decision is based on the absence of materially relevant items, not on a tool failure.
- See `references/news-digesting.md` for a compact source-and-query recipe.

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
