# 2026-05-21 session signals

Concise notes from the latest digest run.

## High-signal HN queries

Use the HN Algolia API directly with a browser User-Agent and `numericFilters=created_at_i%3E<cutoff>`.
The following queries were productive in the last 30 days:
- `Show HN AI`
- `Show HN guardrails`
- `Show HN email API`
- `Launch HN AI`
- `analytics for AI agents`
- `state machine guardrails AI agents`
- `agent inbox`

### Top items surfaced
- **AgentMail** (`https://agentmail.to/`): email inbox API for AI agents. Public pricing page showed $0 / $20 / $200 tiers; HN story `Show HN: Agent.email – sign up via curl, claim with a human OTP` had 45 points / 49 comments.
- **Voker** (`https://voker.ai/`): analytics for AI agents. Public pricing page showed $0 / $80 / $400 tiers and self-hosted enterprise options; HN launch had 59 points / 22 comments.
- **Statewright** (`https://statewright.ai/`): visual workflow builder / guardrails for AI coding agents. Public site showed free tier with 200 transitions/month; HN story had 126 points / 59 comments.

## Useful validation pattern

For candidate selection, prefer ideas with at least two concrete proof signals:
- pricing page + HN traction
- customer logos / seed funding + clear self-serve plan
- product claims + usage caps / free tier + HN traction

## Brazil-gap validation reminders

- Check whether an adjacent incumbent already owns the core workflow in Brazil before calling a market underserved.
- If Brazil has a strong incumbent, narrow the wedge to a smaller workflow rather than cloning the full US offer.
- Agent-email, analytics, and workflow-guardrail products are more likely to fit Brazil than broad content or generic AI-agency plays.

## Notes on evidence extraction

- When browser snapshots omit pricing numbers, fall back to direct HTML extraction with `urllib.request` or `curl`.
- For pricing pages, search for snippets around `pricing`, `free`, `trial`, `$`, `customers`, `self-hosted`, and `usage`.
- For GitHub-backed launches, the README often contains the clearest product thesis and proof details.
