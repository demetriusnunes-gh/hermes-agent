# 2026-05-24 Session Signals

## HN Algolia query patterns that produced usable leads
Use `created_at_i%3E1777071623` for the last-30-days filter.
Useful queries from this run:
- `AI micro SaaS` → **Show HN: TalkTimer, a micro-SaaS run by an AI agent team** (weak signal; ignore for finalist selection)
- `AI agent revenue` → surfaced **Show HN: I built a marketplace where AI agents can hire humans (& other agents)**, **Show HN: Gigacatalyst**, **Show HN: Airbyte Agents**, **Show HN: AIMX**
- `Show HN AI` → surfaced a useful mix of proof pages and high-signal launches
- `Show HN proposal` → **Proposalkit.io**
- `Show HN voice AI` → mostly low-signal for this digest
- `Show HN email API` → **AgentMail**, **Email for AI Agents**, **E2a**
- `Show HN guardrails` → **Forge**, **Retroguard**, **Statewright** (good for trend awareness; not all fit passive-income criteria)

## Proof-page extraction snippets
Terminal `urllib.request` + HTML text stripping was reliable for marketing pages when browser snapshots were empty or hid pricing.

### Voker
Source: https://voker.ai/pricing
- Free: `$0 / month`, `2,000 events / month`, `30 days retention`, `Unlimited seats`
- Starter: `$80 / month`, `30 Day Free Trial`, `Up to 20,000 events / month`, `90 days data retention`
- Agent First: `$400 / month`, `30 Day Free Trial`, `2,000,000 events / month`, `1 year data retention`
- Blog post: `Voker discloses $2.2M pre-seed`

### AgentMail
Source: https://agentmail.to/pricing
- `We raised $6M in Seed Funding`
- Free: `$0 /month`, `3 inboxes`, `3,000 emails/month`
- Developer: `$20 /month`, `10 inboxes`, `10,000 emails/month`
- Startup: `$200 /month`, `150 inboxes`, `150,000 emails/month`
- Enterprise: custom pricing, bulk discounts, white-label, usage-based pricing

### Outlit
Source: https://outlit.ai/pricing
- Free: `$0`, `3 connections`, `1,000 API calls / mo`
- Builder: `$49 /mo`, `5 connections`, `3,000 API calls / mo`
- Pro: `$199 /mo`, `10 connections`, `15,000 API calls / mo`
- Enterprise: custom connections and API volume
- Homepage shows customer logos and a churn/renewal positioning

## Brazil-gap conclusions from this run
- **AgentMail**: no obvious Brazil-native exact equivalent; adjacent local players are messaging/CPaaS/email-marketing vendors. Recommend **keep, but narrow** as a Brazil-localized global infra play.
- **Voker**: no obvious Brazil-native direct equivalent, but Brazil has strong adjacent analytics/support incumbents. Recommend **keep, but narrow** around Portuguese + WhatsApp/Blip/Zenvia + agent QA/ROI.
- **Outlit**: no obvious Brazil-native direct equivalent; local CRMs and support tools are strong adjacent incumbents. Recommend **keep, but narrow** around WhatsApp-native retention workflows and LGPD-aware customer context.

## Selection heuristic reinforced
Prefer ideas that have:
1. a pricing page with concrete tiers,
2. a blog/news post with funding or traction,
3. a narrow Brazil-first wedge that avoids fighting strong local incumbents head-on.
