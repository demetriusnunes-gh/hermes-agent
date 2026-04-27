---
name: nightly-agent-research-improvement
description: Nightly read-only research routine to improve Hermes's skill quality, AI tooling awareness, workflows, and source discovery with a primary focus on AI agents.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [Research, AI Agents, Self-Improvement, Workflows, Sources, Read-Only]
---

# Nightly Agent Research Improvement

Run this at night as a read-only research routine. The goal is to make Hermes better over time by finding high-signal improvements in:
- skill quality
- AI tooling awareness
- agent workflows
- research/source discovery

Primary focus: AI agents.

## User Preferences

- Demetrius wants a short summary only
- Read-only mode for now
- Focus first on AI agents
- Prioritize signal over volume

## Research Principles

- Read-only only: do not edit skills, code, config, cron jobs, or files
- Do not send noisy updates; summarize only the best findings
- Prefer current information from the last 7 days; if thin, widen to the last 30 days
- Focus on actionable improvements Hermes could plausibly adopt later
- Prefer primary sources and high-signal practitioner writeups over hype

## Sources to Prioritize

1. Official product/docs/changelogs for agent tools
2. Official cookbooks/examples/notebooks when they show concrete agent workflow patterns
3. GitHub repos, releases, and issue discussions for major agent frameworks/tools
4. Technical blog posts from credible builders
5. Hacker News discussions when they expose real workflows, failures, or tooling shifts
6. Vendor docs for APIs/models only when they materially affect agent workflows

## Topics to Look For

- New AI agent frameworks, SDKs, orchestration tools, eval tools
- Better browsing/research workflows for agents
- Better memory, skill, planning, delegation, or tool-use patterns
- Reliability improvements: retries, observability, evals, failure recovery
- New high-quality sources worth monitoring regularly
- Concrete workflow ideas Hermes could adopt later in skills or code

## How to Research

1. Start by checking recent prior runs with `session_search` so you can avoid repeating the same findings and detect what is actually new.
2. Start with Firecrawl-first research for pages that need scraping.
3. Use direct source pages when possible.
4. Use accessible search/discovery sources that work well for automation, including HN/Algolia and GitHub release pages.
5. Gather a small set of strong findings rather than many weak ones.
6. Cross-check claims before surfacing them.
7. Track whether a finding is brand-new, strengthening over multiple days, or no longer interesting.

## Source Ranking

As you research, implicitly rank sources by usefulness.

Favor sources that consistently provide:
- concrete workflow details
- changelogs/releases with real impact
- implementation examples
- postmortems, evals, reliability lessons, or benchmark evidence

Deprioritize sources that mostly provide:
- hype without implementation detail
- reposted summaries of other reporting
- generic AI news with no workflow implications

In the nightly summary, mention at most one source that seems newly high-value enough to monitor more often.

## Output

Produce a short nightly summary in this exact spirit:

```text
Nightly AI agents improvement scan — Tue, 14 Apr 2026

Top findings:
- [finding 1 in one line]
- [finding 2 in one line]
- [finding 3 in one line]

Pattern check:
- [one line on whether a theme is repeating/strengthening across nights, only if useful]

Suggested follow-ups:
- [one concrete improvement Hermes could adopt later]
- [one new source/tool worth monitoring]
```

## Output Rules

- Keep the whole message short
- Max 3 top findings
- Max 1 pattern-check line
- Max 2 suggested follow-ups
- One line per bullet
- Include links only when truly useful
- If nothing meaningful is new, say so plainly in one line
- Stay read-only: propose concrete skill/code changes only as recommendations, never as edits

## Read-Only Restriction

Do not modify anything. No file edits, no skill updates, no code changes, no cron changes, no commits. Research and summarize only.

## Good Outcomes

Examples of useful findings:
- a new agent SDK/release with a clear capability Hermes lacks
- a better evaluation or observability workflow for agent systems
- a high-quality source or repo Hermes should monitor
- a practical browser/research tactic that reduces failure rate
- a repeatable prompting/skill pattern worth testing later

## Bad Outcomes

Avoid surfacing:
- vague hype
- generic AI news with no workflow impact
- low-credibility growth hacks
- product launches with no technical substance
- repeated findings from previous nights unless there is meaningful new evidence
