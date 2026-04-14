---
name: daily-self-update
description: Daily read-only self-update routine for Hermes to review recent learning, active automations, and the highest-priority next improvements, then send Demetrius a concise summary.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [Self-Update, Daily Review, Read-Only, AI Agents, Automation]
---

# Daily Self Update

Run once per day as a read-only self-review. The goal is to keep Demetrius updated on Hermes's current state and the best next improvements without creating noise.

## Goals

- Summarize what Hermes learned recently
- Surface the most relevant active automations/routines
- Highlight one or two next improvements worth pursuing
- Keep everything concise and useful

## Rules

- Read-only only
- Do not modify skills, code, config, cron jobs, or files
- Do not repeat stale status unless it matters
- Prefer changes, deltas, and the most relevant state

## What to Review

1. Recent sessions or recent cron outputs via `session_search`
2. Current scheduled jobs via `cronjob list`
3. Any important new recurring themes from the nightly AI-agent improvement scan
4. Whether Hermes has obvious gaps in skills, sources, or workflows worth proposing

## Output Format

```text
Daily Hermes self-update — Tue, 14 Apr 2026

State:
- [one short line on current overall state]
- [one short line on the most relevant active automation or change]

Next improvements:
- [one concrete next improvement]
- [optional second improvement]
```

## Output Rules

- Keep it very short
- Max 2 state bullets
- Max 2 next-improvement bullets
- One line per bullet
- No long explanations
- If nothing changed, say so plainly and briefly

## Good Updates

Examples:
- a new nightly research theme is showing up repeatedly
- a cron routine is producing better output after a recent change
- a source/tool is proving high value and should be monitored more
- there is a clear candidate skill improvement to consider next

## Avoid

- verbose recaps
- repeating all cron jobs every day
- generic "all systems normal" filler
- recommendations with no concrete value
