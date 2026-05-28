---
name: firecrawl-local-research
description: Use locally-hosted Firecrawl (Docker, port 3002) to scrape and extract clean markdown from web pages for research tasks. Supports parallel scraping, Brazilian sources, and search result scraping.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [Firecrawl, Research, Web Scraping, Docker, Brazil]
---

# Firecrawl Local Research

## IMPORTANT: FIRST CHOICE FOR WEB RESEARCH

When Demetrius asks you to research something on the web, look up information, find news, read articles, or scrape any web content — **use Firecrawl FIRST, before browser tools**. Always. This is the default web research tool.

Only fall back to `browser_navigate` + `browser_snapshot` / `browser_vision` when:
- Firecrawl is down/unreachable
- The page requires interactive login or form submission
- You need to click through navigation menus
- Firecrawl returns empty/garbage content AND the page is clearly scrapeable

Use the self-hosted Firecrawl instance (running in Docker on port 3002) to scrape web pages and convert them to clean markdown for research tasks. No API key needed.

## When to Use

- Research topics across multiple sources (Brazil sites, international, niche blogs) — **DEFAULT CHOICE**
- When browser tools fail due to bot detection
- When you need clean text extraction from complex web pages
- Parallel scraping for speed

## Prerequisites

- Firecrawl running in Docker on `localhost:3002` (containers: firecrawl-api-1, firecrawl-playwright-service-1, firecrawl-rabbitmq-1, firecrawl-redis-1, firecrawl-nuq-postgres-1)
- No API key required

## API

### Single Scrape (Sync)

```bash
curl -s -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/article","formats":["markdown"],"onlyMainContent":true}'
```

Response:
```json
{
  "success": true,
  "data": {
    "markdown": "Clean markdown content...",
    "metadata": { "title": "...", "statusCode": 200, "url": "..." }
  }
}
```

### Batch Scrape (Parallel)

Run multiple scrapes in parallel with background curl:

```bash
#!/bin/bash
OUTDIR="/tmp/firecrawl_research"
mkdir -p "$OUTDIR"
API="http://localhost:3002/v1/scrape"

# Launch all in parallel
curl -s -X POST "$API" -H "Content-Type: application/json" \
  -d '{"url":"URL1","formats":["markdown"],"onlyMainContent":true}' \
  -o "$OUTDIR/1.json" --max-time 30 &

curl -s -X POST "$API" -H "Content-Type: application/json" \
  -d '{"url":"URL2","formats":["markdown"],"onlyMainContent":true}' \
  -o "$OUTDIR/2.json" --max-time 30 &

wait

# Extract and summarize results
python3 -c "
import json, os, glob
out = '/tmp/firecrawl_research'
for f in sorted(glob.glob(os.path.join(out, '*.json'))):
    data = json.load(open(f))
    md = data.get('data', {}).get('markdown', '')
    print(f'{os.path.basename(f)}: {len(md)} chars')
    print(md[:500])
    print('---')
"
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `url` | URL to scrape | required |
| `formats` | Output formats: `["markdown"]` or `["html"]` | `["markdown"]` |
| `onlyMainContent` | Strip nav, footer, sidebar | `false` |
| `waitFor` | Wait ms before extracting (for JS-heavy pages) | `0` |
| `actions` | Array of actions (click, scroll, etc) | `[]` |
| `timeout` | Max time in ms | `30000` |
| `mobile` | Use mobile viewport | `false` |

## Common Patterns

### App Store / Google Play chart research

For market-research tasks involving top-grossing mobile apps, use the Appfigures public-page extraction workflow in `references/app-store-chart-research.md`: scrape public chart pages, parse embedded `var __appData`, and verify ratings via Apple Lookup / Google Play detail pages. Treat this as a public-chart proxy unless the user provides paid Sensor Tower/data.ai/AppMagic access.

### Brazilian DETRAN / CNH test-prep research

For CNH/DETRAN test-prep market or content research, use `references/detran-cnh-public-materials.md`: public CONTRAN curriculum, DETRAN educational PDFs, official simulator caveats, useful queries, and PDF extraction pitfalls.

### Brazilian Research Sources

Good Brazilian sources that work well with Firecrawl:
- Sebrae: `https://www.sebrae.com.br/...`
- G1: `https://g1.globo.com/...`
- Exame: `https://exame.com/...`
- Folha: `https://www1.folha.uol.com.br/...`
- Endeavor: `https://endeavor.org.br/...`

### Media / Photo Gallery Extraction

For gallery-style pages where the goal is to archive the actual photos:
- First inspect the raw HTML for `<link rel="preload" as="image" href="...">` tags; many gallery sites expose the full image list there even when the visible DOM is lazy-loaded.
- In the browser, `document.querySelectorAll('img')` plus `currentSrc`/`src` is a fast way to enumerate the visible assets.
- Prefer direct image URLs over screenshots, and deduplicate aggressively to exclude logos/widgets.
- Save the download set with numeric prefixes (`001_...`, `002_...`) and a `source_urls.txt` manifest so the order and provenance are preserved.
- If the task also requires publishing the assets on the VPS, place them under the Caddy-served web root and add a minimal `index.html` gallery so the folder is browsable over HTTP.
- See `references/gallery-photo-archival.md` for a compact end-to-end recipe.

### Search Results

Scrape Bing for search results:
```bash
curl -s -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.bing.com/search?q=inteligencia+artificial+renda+passiva+Brasil","formats":["markdown"],"onlyMainContent":true}' \
  --max-time 30
```

If Bing returns irrelevant/garbage results (for example, mostly Chinese dictionary/Zhihu/Baidu pages unrelated to the query), switch to DuckDuckGo HTML and parse result links directly. This worked better for niche product/service discovery queries such as WhatsApp group AI bots:
```bash
python3 - <<'PY'
import urllib.parse, urllib.request, re, html
queries = ['WhatsApp group management bot AI', 'WhatsApp group bot expenses events']
for q in queries:
    print('\n==', q)
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    text = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
    for m in re.finditer(r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>', text, re.S):
        title = html.unescape(re.sub('<.*?>', '', m.group(2)))
        href = html.unescape(m.group(1))
        print('-', title, '|', href)
PY
```

### JS-Heavy Pages (wait for render)

```bash
curl -s -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","formats":["markdown"],"onlyMainContent":true,"waitFor":3000}' \
  --max-time 45
```

## Debugging

### Check if Firecrawl is running

```bash
docker ps | grep firecrawl
curl -s http://localhost:3002/v1/scrape -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","formats":["markdown"]}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('success'))"
```

### Important failure mode: container looks healthy but API resets connections

Sometimes `docker ps` shows `firecrawl-api-1` as Up, but requests to `http://localhost:3002/` or `/v1/scrape` fail with curl exit 52/56 or `Recv failure: Connection reset by peer`.

Quick checks:
```bash
curl -sv http://localhost:3002/ 2>&1 | tail -n 20
curl -s -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","formats":["markdown"],"onlyMainContent":true}' \
  --max-time 20
docker logs firecrawl-api-1 --tail 50
```

If you see connection resets even though the containers are running:
1. Treat Firecrawl as down for this task.
2. Fall back immediately to another research path instead of retrying repeatedly:
   - `web` research / delegated web research when available
   - `browser_navigate` only if the target site is likely scrapeable without bot challenges
3. Note the failure mode in your final reasoning so future sessions don't waste time on the same dead path.

### Failure mode: Empty API response with no error

If `curl` requests to `/v1/scrape` return empty output (no JSON body, exit code 0), Firecrawl is completely unresponsive. This is a total failure, not a transient issue. Immediately fall back to `browser_navigate` + `browser_snapshot` for the target URL, as retrying will not resolve the problem.

### View logs

```bash
docker logs firecrawl-api-1 --tail 20
docker logs firecrawl-playwright-service-1 --tail 20
```

### Restart if stuck

```bash
cd /path/to/firecrawl-docker-compose  # wherever docker-compose.yml lives
docker compose restart api
```

## Pitfalls

- **Timeout on Brazilian sites**: Some Brazilian news sites are slow or aggressive. Use `--max-time 30` on curl to avoid hanging forever. If a single URL times out, skip it and try alternatives.
- **403/404 on some sites**: Not all sites are scrapeable. Try the mobile version with `\"mobile\":true` as a workaround.
- **Extracted content too short**: Try removing `\"onlyMainContent\":true` or add `\"waitFor\":3000` for JS-heavy pages.
- **Parallel limit**: Don't run more than 5-7 parallel scrapes at once — the single Playwright service can get overwhelmed.
- **execute_code sandbox isolation**: The Firecrawl API runs on the host Docker network. If calling from `execute_code` (which runs in an isolated sandbox), use `host.docker.internal` instead of `localhost`, or use `terminal()` to make curl calls.
- **Anti-scraping sites**: Some sites like YouTube have strong anti-scraping measures that block both Firecrawl and browser tools. For video platforms, consider using specialized tools like `yt-dlp` when standard scraping approaches fail.
