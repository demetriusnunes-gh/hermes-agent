---
name: browser-research-bot-workarounds
description: Guide for effective web research using browser tools, accounting for bot detection and CAPTCHAs. Documents which sources work and which don't on this VPS.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [Research, Browser, Bot Detection, Web Scraping, Workarounds]
prerequisites:
  tools: browser_navigate, browser_snapshot, browser_click
---

# Browser Research with Bot Detection Workarounds

Research the web effectively while working around aggressive bot detection. The Hostinger VPS residential proxy limitation means many sites will block requests.

## What Works (No CAPTCHA)

- **Hacker News**: `news.ycombinator.com` and all direct story pages
- **HN Algolia Search**: `hn.algolia.com/?q=QUERY&sort=byDate&dateRange=pastMonth` — best tech source
- **Bing**: `bing.com/search?q=QUERY` — partial results, use for general searches
- **Brazilian news sites**: G1, Folha, UOL, Poder360, BBC Brasil — RSS and web pages work
- **Direct URLs to known articles**: Most news sites work if you navigate directly
- **Wikipedia**: No blocks
- **GitHub**: No blocks

## What Blocks (CAPTCHA/Bot Detection)

- Google Search → `/sorry/index` redirect
- Reddit → JS challenge page
- DuckDuckGo → CAPTCHA (even lite.duckduckgo.com/lite/)
- Product Hunt → "Just a moment..." Cloudflare
- Indie Hackers → Cloudflare challenge
- Brave Search → Captcha page
- Stack Overflow → May block

## Research Strategy

1. **Start with HN Algolia** for tech/SaaS/AI trends:
   - `https://hn.algolia.com/?q=QUERY&sort=byDate&dateRange=pastMonth`
   - Check comments on interesting stories by visiting the item page
   
2. **Use Bing** for general web searches:
   - `https://www.bing.com/search?q=QUERY&qft=sortbydate%3d1`
   - Results may be irrelevant sometimes, try reformulating queries
   
3. **Open interesting links directly** — once you find a promising URL from HN or Bing, navigate to it directly
   
4. **Use RSS feeds** for news sites — they work reliably and often don't require browser:
   - Most major news sites have `/feed/` or `/rss/` endpoints
   - Fetch via `curl` for much faster results
   
5. **Site-restricted search via Bing**:
   - `https://www.bing.com/search?q=site:indiehackers.com+QUERY`
   - Workaround for blocked sources

## Tips

- Don't waste time retrying blocked sites — switch to alternatives immediately
- Use `full=true` on browser_snapshot for article content
- For research that needs many pages, consider using `execute_code` with curl instead of browser for RSS feeds
- Always check the page title — if it contains "moment", "challenge", "captcha", or "sorry", the site blocked you