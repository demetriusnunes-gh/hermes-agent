---
name: ai-passive-income-digest
description: Nightly research on autonomous AI-based microbusiness ideas for passive income. Low time commitment, high leverage opportunities.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [AI, Passive Income, Microbusiness, Research, Business, Agents]
---

# AI Passive Income Daily Digest

Researches new and trending ideas for AI-powered microbusinesses that run autonomously with minimal time investment. Delivers fresh, actionable insights every night.

## User Context

- Demetrius is a software engineering manager at DoorDash leading the Engineering Hub in Brazil
- Strong technical background — can build and deploy systems
- Lives in Rio de Janeiro, works in São Paulo
- Has a VPS (Hostinger, Ubuntu 24.04, 8GB RAM) already set up
- Already uses AI agents (Hermes) with WhatsApp, Telegram, Gmail, Calendar integration
- Time is scarce — wants something that runs mostly on autopilot
- NOT interested in: get-rich-quick schemes, generic AI content mills, recycled ideas

## Steps

### 1. Research (BROWSER-BASED WITH BOT DETECTION WORKAROUNDS)

Use the browser to search for CURRENT (last 30 days) ideas and opportunities. Focus on sources that work reliably with automated browsing:

**Effective Research Strategy:**
1. **Start with Hacker News Algolia search** - `https://hn.algolia.com/api/v1/search?query=YOUR_QUERY&tags=story&numericFilters=created_at_i>TIMESTAMP` - this works without CAPTCHA
2. **Visit promising URLs directly** - once you find interesting stories from HN, navigate to the actual URLs
3. **Use Bing search** for general queries - `https://www.bing.com/search?q=YOUR_QUERY` - may give partial results
4. **Check Brazilian news sites directly** - G1, Folha, UOL, BBC Brasil work when accessed via direct URLs
5. **Use site-restricted Bing search** for blocked sources - `site:indiehackers.com QUERY` via Bing

**What Works (No CAPTCHA):**
- Hacker News: news.ycombinator.com and direct story pages
- HN Algolia search: hn.algolia.com - best for tech/SaaS/AI trends
- Bing: bing.com/search - partial results, use for general searches
- Brazilian news sites: G1, Folha, UOL, Poder360, BBC Brasil - work with direct navigation
- Direct URLs to known articles: Most news sites work if you navigate directly
- Wikipedia, GitHub: No blocks

**What Blocks (CAPTCHA/Bot Detection):**
- Google Search → `/sorry/index` redirect
- Reddit → JS challenge page
- DuckDuckGo → CAPTCHA (even lite)
- Product Hunt → Cloudflare "Just a moment..."
- Indie Hackers → Cloudflare challenge
- Brave Search → Captcha page
- Stack Overflow → May block

**Research Tips:**
- Don't waste time retrying blocked sites - switch to alternatives immediately
- For tech/AI trends, HN Algolia is consistently reliable
- HN Algolia API pages may render as `Empty page` in browser snapshots; when that happens, use `browser_console(expression='document.body.innerText')` to extract the JSON results directly instead of abandoning the search
- When constructing HN Algolia API queries, remember to URL encode the '>' symbol in numericFilters as '%3E' (e.g., `created_at_i%3ETIMESTAMP`)
- Always check page title for blocking indicators ("moment", "challenge", "captcha", "sorry")
- Visit as many accessible sources as possible - quality > quantity of sources
- Focus on: Real case studies, people who actually launched and are making money, concrete numbers, step-by-step guides
- If the browse budget is tight, spend most of it on 2-3 HN Algolia queries plus 1-2 direct visits to the strongest sources rather than broad search-engine exploration
- When browser tools fail due to bot detection or technical issues, fall back to using terminal with curl to fetch data directly from APIs and web pages
- When US traction is clear but Brazil-local competition is unclear, do a second-pass market-gap validation with `delegate_task(..., toolsets=['web'])` or equivalent web research. Ask specifically whether Brazil has an obvious local equivalent, which adjacent incumbents exist, and whether the offer should be reframed as a narrower Brazil-first wedge instead of a generic clone.
- If delegated web-research subagents time out or search results are noisy, fall back to direct `curl`/browser visits of known US proof pages and Brazil incumbent homepages; this was more reliable than generic Bing for this digest. Useful US proof pages include Slang.ai customers/pricing, Assort Health, Notable Health, EliseAI customer stories/newsroom, GovDash, AutogenAI. Useful Brazil incumbent checks include Anota AI/Goomer/Blip/Zenvia for restaurant/WhatsApp automation, iClinic/Feegow/Doctoralia/Ninsaúde for clinics, Kenlo/Jetimob/Vista/Imoview for real estate, and Effecti/ConLicitação/LicitaJá/Portal de Compras Públicas for licitações.
- Prefer browser/direct-page validation for company proof pages over broad Bing when Bing returns noisy localized results. Recent reliable direct pages: Slang.ai `/pricing` and `/customers` expose pricing, restaurant counts, call-training volume, and concrete customer metrics (e.g., calls/reservations/revenue); Assort Health homepage exposes provider/specialty and outcome metrics; EliseAI homepage exposes customer logos and product scope; GovDash exposes customer-win and proposal-time metrics; Effecti homepage exposes Brazil incumbent metrics and AI positioning. Use `browser_snapshot` or terminal `urllib`/`curl` snippets to extract titles and traction claims.
- When the browser snapshot omits numbers or a JS-heavy page times out, run `browser_console(expression='document.body.innerText')`; if that times out too, fall back to terminal `python3` + `urllib.request` with a browser User-Agent, strip tags, and search for evidence snippets. This worked for Slang AI pricing, Assort Health, EliseAI, GovDash, Effecti, Anota AI, and Kenlo.
- When HN Algolia is sparse, broaden the query family to adjacent monetized classes instead of the original phrase: pricing, guardrails, workflow automation, email infra, proposal generators, and agent marketplaces often surface better self-serve products with visible pricing or traction.
- Re-check incumbent AI positioning before calling Brazil underserved. If Brazil already has a strong adjacent incumbent, narrow the wedge or exclude the idea rather than cloning the US offer.
- Prefer finalists that survive this explicit Brazil-gap validation step; reject ideas where the US proof is strong but the Brazil fit or differentiation remains weak.
- See `references/brazil-rebuild-validation-2026-04-30.md` for reusable proof snippets and Brazil-gap notes on Slang AI, Assort Health, EliseAI, GovDash, Effecti, and the current best Brazil-first wedges. See `references/2026-05-12-brazil-gap-notes.md` for prior HN-query patterns and proof snippets. See `references/2026-05-14-digest-research-notes.md` and `references/2026-05-15-research-notes.md` for HN leads, proof snippets, and Brazil-incumbent checks.

**Research workflow refinements (2026-05-14):**
- When HN Algolia is the source of truth, use the API directly with a browser User-Agent and query-only URL encoding; keep `created_at_i%3E...` in `numericFilters`.
- If a browser snapshot is empty or omits numbers, skip to terminal `python3 + urllib.request`, strip HTML, and search for keyword-adjacent evidence snippets.
- For dynamic proof pages, direct `urllib.request` plus text extraction often beats browser snapshots. Search for concrete snippets around `pricing`, `customers`, `revenue`, `hours`, `calls`, `reservations`, `proposals`, and `edital`.
- For Brazil-gap validation, do not stop at the US proof page: quickly check adjacent Brazilian incumbents and narrow the wedge if an incumbent already owns the core workflow.
- Treat HN points/comments plus explicit pricing/customer/revenue claims as acceptable traction proxies for first-pass filtering; exclude ideas with thin or purely speculative evidence.

**Browser searches to perform (prioritized):**
- "autonomous AI agent business ideas 2026" (via HN Algolia)
- "AI micro SaaS" (via HN Algolia)
- "self-running AI business" (via HN Algolia)
- "AI agent revenue" (via HN Algolia)
- "automated AI services" (via HN Algolia)
- If those are sparse, broaden immediately to `Show HN AI`, `Launch HN AI`, `Show HN proposal`, `Show HN voice AI`, `Show HN email API`, and `Show HN guardrails`.

### 2. Filter & Prioritize

For each idea found, evaluate against:
- **Autonomy**: Can it run with <2 hours/week maintenance?
- **Startup cost**: Can it start with <$100/month in infra?
- **Time to revenue**: Can it start generating within 30-60 days?
- **Uniqueness**: Is it differentiated or everyone is doing it?
- **Leverage**: Does it use existing AI capabilities effectively?
- **Scalability**: Can revenue grow without proportional time investment?

Score each idea 1-5 on these criteria.

### 3. Format Output

Only surface the TOP 3 ideas. Format:

```
🤖 AI Passive Income — Tue, 02 Apr 2026

1. [IDEA NAME]
   What: One-line description
   How it works: 2-3 sentences on the mechanics
   Revenue model: How it makes money
   Effort: X hrs/week to maintain after setup
   Start: What you'd need to build this (tools, APIs, cost)
   Source: <link to source>
   Score: autonomy X/5, cost X/5, time X/5

2. [IDEA NAME]
   ...

3. [IDEA NAME]
   ...

💡 Best bet tonight: One sentence on which idea has the best risk/reward ratio and why.
```

## Tips

- Do NOT recycle ideas from previous days — each day should be fresh research
- Strongly prioritize services already proven to earn in the US market that appear to have no strong Brazil-local equivalent yet
- Only include ideas that plausibly fit Brazilian customer behavior, regulation, payments, and language/localization realities
- Prefer easy-to-implement rebuilds/adaptations over novel-from-scratch concepts — the key question is: "Is this already working in the US, and can Demetrius localize it credibly for Brazil?"
- For every finalist, explicitly state why the US proof point is credible and why Brazil still appears underserved
- Prioritize Brazilian/LatAm market gaps too — less competition, local advantage
- If an idea requires heavy upfront work, be honest about it
- Include specific numbers when available (revenue, costs, conversion rates)
- Treat public pricing, free-trial tiers, usage limits, customer counts, and HN Launch/Show HN engagement (points/comments) as valid traction proxies when explicit revenue is unavailable
- Prefer finalists with at least two concrete proof signals, e.g. pricing page + HN Launch traction, or customer stats + testimonial/customer logos
- When research is thin, favor narrow B2B workflow tools with visible pricing over broad platform plays; they are easier to rebuild credibly for Brazil
- Avoid generic ideas like "build an AI chatbot agency" — go deeper
- Look for problems people are actively paying to solve, not hypothetical needs
- Check Product Hunt, Hacker News "Show HN", Reddit for real launches
- If the browser snapshot is empty or blocked, use the HN Algolia terminal fallback in `references/hn-algolia-terminal-fallback.md` before abandoning the query
- Do not use an idea unless the source itself or HN traction provides a concrete proof signal; if the evidence is thin, exclude it rather than guessing
- If nothing interesting is found, report "nothing new tonight" briefly
- If you need to deliver the digest through a local WhatsApp curl endpoint, avoid embedding a long multi-line message with URLs directly in the shell command; write the JSON payload to a temp file and send with `curl --data-binary @file` to avoid shell escaping issues and security-scan false positives
- Use the browser tools — don't just rely on knowledge cutoff
- Only surface services that are already working and earning in the US market, with evidence of traction, customers, or revenue.
- For each finalist, explicitly explain: 1) the US proof point, 2) why Brazil appears underserved, 3) why the business should fit the Brazilian market, 4) what the smallest viable Brazil-first version would be.
- Finish with exactly one line: 'Best Brazil rebuild bet:' plus the strongest option and why — no extra text or emojis.