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
- Always check page title for blocking indicators ("moment", "challenge", "captcha", "sorry")
- Visit as many accessible sources as possible - quality > quantity of sources
- Focus on: Real case studies, people who actually launched and are making money, concrete numbers, step-by-step guides

**Browser searches to perform (prioritized):**
- "autonomous AI agent business ideas 2026" (via HN Algolia)
- "AI micro SaaS" (via HN Algolia)
- "self-running AI business" (via HN Algolia)
- "AI agent revenue" (via HN Algolia)
- "automated AI services" (via HN Algolia)

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
- Prioritize Brazilian/LatAm market gaps too — less competition, local advantage
- If an idea requires heavy upfront work, be honest about it
- Include specific numbers when available (revenue, costs, conversion rates)
- Avoid generic ideas like "build an AI chatbot agency" — go deeper
- Look for problems people are actively paying to solve, not hypothetical needs
- Check Product Hunt, Hacker News "Show HN", Reddit for real launches
- If nothing interesting is found, report "nothing new tonight" briefly
- Use the browser tools — don't just rely on knowledge cutoff