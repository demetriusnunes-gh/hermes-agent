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

Use the self-hosted Firecrawl instance (running in Docker on port 3002) to scrape web pages and convert them to clean markdown for research tasks. No API key needed.

## When to Use

- Research topics across multiple sources (Brazil sites, international, niche blogs)
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

### Brazilian Research Sources

Good Brazilian sources that work well with Firecrawl:
- Sebrae: `https://www.sebrae.com.br/...`
- G1: `https://g1.globo.com/...`
- Exame: `https://exame.com/...`
- Folha: `https://www1.folha.uol.com.br/...`
- Endeavor: `https://endeavor.org.br/...`

### Search Results

Scrape Bing for search results:
```bash
curl -s -X POST http://localhost:3002/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.bing.com/search?q=inteligencia+artificial+renda+passiva+Brasil","formats":["markdown"],"onlyMainContent":true}' \
  --max-time 30
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
- **403/404 on some sites**: Not all sites are scrapeable. Try the mobile version with `"mobile":true` as a workaround.
- **Extracted content too short**: Try removing `"onlyMainContent":true` or add `"waitFor":3000` for JS-heavy pages.
- **Parallel limit**: Don't run more than 5-7 parallel scrapes at once — the single Playwright service can get overwhelmed.
- **execute_code sandbox isolation**: The Firecrawl API runs on the host Docker network. If calling from `execute_code` (which runs in an isolated sandbox), use `host.docker.internal` instead of `localhost`, or use `terminal()` to make curl calls.
