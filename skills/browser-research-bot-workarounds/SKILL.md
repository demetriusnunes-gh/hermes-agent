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

1. **Start with HN Algolia API** for tech/SaaS/AI trends (most reliable):
   - Use the API endpoint: `https://hn.algolia.com/api/v1/search?query=QUERY&tags=story&numericFilters=created_at_i>TIMESTAMP`
   - For last 30 days: `numericFilters=created_at_i>$(date -d '30 days ago' +%s)`
   - Check comments on interesting stories by visiting the item page directly
   
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
- For marketing and pricing pages, try `browser_snapshot` first: many sites expose the key numbers directly in the DOM without needing extra scraping.
- If the snapshot is sparse or omits prices, run `browser_console(expression='document.body.innerText')` before giving up; this often reveals the hidden text on JS-heavy pages.
- For HN Algolia API pages that render as an empty browser page, use `browser_console(expression='document.body.innerText')` to extract the JSON payload directly.

## Media-gallery workaround (Fotto / Gabby)

Some photo gallery sites render only low-res thumbnails in the DOM, while the real usable asset list is embedded in the server-rendered HTML.

Procedure:
1. Fetch the page HTML directly.
2. Search for `self.__next_f.push(...)` / embedded JSON blobs.
3. Extract the `medias` array and collect the `preview` URLs first.
4. Only treat the browser DOM `<img>` URLs as thumbnails unless the page explicitly exposes a higher-res field.
5. Do **not** waste time guessing `thumb` → `full` URL transformations unless the HTML or app bundle shows those paths exist.

For the Gabby Produções event page we verified:
- `thumbnail` = low-res thumb
- `image` = higher-res public preview
- full-res/original was not publicly reachable from the page HTML

See `references/fotto-gallery-downloads.md` for a concise extraction recipe and observed URL patterns.