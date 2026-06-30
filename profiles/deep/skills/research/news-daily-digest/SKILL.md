---
name: news-daily-digest
description: Curated morning news digest from balanced international and Brazilian sources. Covers world news, Brazil, Rio de Janeiro, and Sao Paulo.
version: 1.0.0
author: Demetrius Nunes
metadata:
  hermes:
    tags: [News, Digest, Morning, RSS, Brazil, World]
---

# News Daily Digest

Generates a concise, curated morning news digest from balanced, impartial sources across 4 categories: World, Brazil, Rio de Janeiro, and Sao Paulo.

## Sources

**World** — BBC World, The Guardian World, Al Jazeera, NPR World
**Brazil** — BBC Brasil, Folha de S.Paulo, Poder360
**Rio** — G1 Rio de Janeiro
**Sao Paulo** — G1 Sao Paulo
**DoorDash/DASH** — NASDAQ stock info, DoorDash company news, tech/engineering press

## DoorDash DASH Tracking

For the daily digest, add a **DD** section with:

1. **Stock price** — Fetch current DASH from Yahoo Finance or Google Finance:
```bash
curl -s 'https://query2.finance.yahoo.com/v8/finance/chart/DASH?range=1d&interval=1d' 2>&1 | python3 -c "
import sys, json
data = json.load(sys.stdin)
r = data['chart']['result'][0]
close = r['indicators']['quote'][0]['close'][0]
meta = r['meta']
pc = meta.get('previousClose', close)
change = close - pc
pct = (change / pc) * 100 if pc else 0
sign = '+' if change >= 0 else ''
print(f'DASH: \${close:.2f} | {sign}{change:.2f} ({sign}{pct:.1f}%) | Prev: \${pc:.2f}')
" 2>&1 || echo "DASH: checking Google Finance fallback..."
```

If Yahoo fails due to rate limiting, use Google Finance with proper parsing:
```bash
# Get last price and previous close from Google Finance
curl -s 'https://www.google.com/finance/quote/DASH:NASDAQ' | grep -oP 'data-last-price="[\d.]+"' | head -1 | cut -d'"' -f2
curl -s 'https://www.google.com/finance/quote/DASH:NASDAQ' | grep -oP 'data-previous-close="[\d.]+"' | head -1 | cut -d'"' -f2
```

**2026-04 finding**: Yahoo works more reliably when you send a browser User-Agent, and the most useful previous-close field may be `chartPreviousClose` rather than `previousClose`:
```bash
curl -s -H 'User-Agent: Mozilla/5.0' 'https://query2.finance.yahoo.com/v8/finance/chart/DASH?range=1d&interval=1d' | python3 -c "
import sys, json
r = json.load(sys.stdin)['chart']['result'][0]
meta = r['meta']
close = meta.get('regularMarketPrice') or r['indicators']['quote'][0]['close'][0]
pc = meta.get('chartPreviousClose') or meta.get('previousClose') or close
change = close - pc
pct = (change / pc) * 100 if pc else 0
sign = '+' if change >= 0 else ''
print(f'DASH: \${close:.2f} | {sign}{change:.2f} ({sign}{pct:.1f}%) | Prev: \${pc:.2f}')
"
```

Alternative Python approach for more reliable parsing:
```bash
python3 -c "
import requests, re
resp = requests.get('https://www.google.com/finance/quote/DASH:NASDAQ', headers={'User-Agent': 'Mozilla/5.0'})
text = resp.text
last_match = re.search(r'data-last-price=\"([\d.]+)\"', text)
prev_match = re.search(r'data-previous-close=\"([\d.]+)\"', text)
if last_match and prev_match:
    last_price = float(last_match.group(1))
    prev_close = float(prev_match.group(1))
    change = last_price - prev_close
    pct = (change / prev_close) * 100 if prev_close else 0
    sign = '+' if change >= 0 else ''
    print(f'DASH: \${last_price:.2f} | {sign}{change:.2f} ({sign}{pct:.1f}%) | Prev: \${prev_close:.2f}')
else:
    print('DASH: price unavailable')
"
```

2. **DoorDash news** — Google News RSS:
```bash
curl -s "https://news.google.com/rss/search?q=DoorDash+when:1d&hl=en-US&gl=US&ceid=US:en" | grep -oP '<title>(?!DoorDash - Google News)([^<]+)</title>' | head -5
```

3. **Filter** — Max 2 stories. Only include if meaningful:
   - Earnings, partnerships, business results
   - Engineering/tech announcements
   - Competitive moves (UberEats, Instacart)
   - Regulatory/policy impact
   - Notable price moves (>2% up/down)
   - Skip: press releases, minor features

## How It Works

1. Run the bundled Python script to fetch all RSS feeds:
```bash
python3 ~/.hermes/skills/research/news-daily-digest/scripts/news_digest.py
```
(Note: skill lives under `research/` category directory.)

2. Parse the JSON output. Each category has `label` and `items` array with `title`, `link`, `source`, `summary`, `pub_date`.
   - **2026-04 finding**: when you supplement with Google News RSS directly, `source` may come back empty in some parsers. Fall back to extracting the outlet from the title suffix (`Headline - Outlet`) if the XML source tag is missing.

3. **Filter stale data**: Check `pub_date` and skip items from previous years (especially 2018 stale cache from G1 feeds). Only process items from today/yesterday.

4. Curate the digest.
   - **Default mode**: pick only the TOP 3 most important stories across ALL categories combined.
   - **Default style**: ultra-concise. One short line per story. No summaries, no extra commentary, no blank lines between items.
   - **If the user explicitly asks for per-category counts** (for example 5–8 world, 4–6 Brazil, 3–4 Rio, 3–4 São Paulo), follow that request instead of the default top-3 format.
   - In either mode, be ruthless. Remove celebrity gossip, minor local stories, sports, entertainment. Prioritize: geopolitical events, major policy changes, significant economic news, emergencies, anything that directly affects Demetrius's life (family, work, Rio, SP).

5. Sort all stories by date (most recent first) and select top 3.

6. Format for delivery (see Output Format below).

7. Add a very short top line with date only. No editorial paragraph unless there is a single truly critical item.

8. **DoorDash section**: include only if materially relevant today. Compress to a single line. If there is no meaningful DoorDash update, omit the section entirely.

## Output Format

Default daily format:

```
🗞️ Tue, 14 Apr 2026
• 🌍 Trump tariff talks stall with China — BBC
• 🇧🇷 Governo Lula revisa regra fiscal após market pressure — Poder360
• 🏙️ SP expands anti-crime operation in downtown — G1
• 📈 DASH +2.4% on partnership news
```

Rules:
- Max 4 lines total after the header.
- Usually 3 news lines total.
- Add a 4th line for DoorDash only if it is materially relevant.
- No URLs by default.
- No paragraph summaries.
- Keep each line under ~110 characters when possible.
- If there is one truly critical story, you may add a leading `MUST READ:` on that line, but still keep it to one line.

The **DD section** is optional and should be only one compressed line. If no meaningful news and stock is flat (<1% change), skip it entirely.

## Delivery

Deliver to:
- Telegram (primary)
- WhatsApp to +5521988490510 (Demetrius personal)

**Note for automation**: When sending via WhatsApp bridge API, ensure proper JSON escaping of the message content, particularly for non-ASCII characters and quotes.

## When to Use

- Cron job runs daily at 8 AM BRT (11:00 UTC)
- On demand when Demetrius asks for daily digest or news recap
- Can skip if no significant news found across categories

## Tips

- Be extremely brief — Demetrius wants a scan, not a read
- Prefer one-line headlines over explanation
- Keep headlines in the original language of the source when readable
- Don't add commentary unless something is truly noteworthy
- If a source fails, mention it at the bottom quietly only if needed
- Deduplicate: same story from multiple sources should appear only once (prefer BBC or the most reputable source)
- **Always filter by date**: Check pub_date and skip items from previous years (especially 2018 stale cache from G1 feeds). Only process items from today/yesterday. If G1 Rio or G1 SP feeds contain only stale items, skip those sections entirely.
- If G1 Rio or G1 SP feeds are empty after filtering, broaden to G1 Brasil for that category
- If G1 Rio or G1 SP feeds are stale/unusable, a better fallback than leaving sections empty is to use **Google News RSS search constrained to Rio/São Paulo topics** and then manually filter out weather, sports, entertainment, listicles, and low-quality aggregators.
- **Pitfall on Hostinger VPS**: `feeds.g1.globo.com` may resolve to NXDOMAIN (DNS failure). In that case, all G1 feeds will fail. Check pub_date — if items are not from today/yesterday, skip Rio and SP sections entirely or fill via Google News fallback, and add a brief note at the bottom: "⚠️ G1 feeds indisponíveis hoje."
- The script handles encoding issues (ISO-8859-1 from Brazilian sources) automatically
- For DoorDash stock price: Yahoo Finance may rate limit; use Google Finance with proper parsing as fallback
- For DoorDash news, be stricter than the raw RSS: skip SEO bait, product listings, generic consumer advice, and low-signal finance rewrites; prefer competition/platform/infrastructure/regulatory stories
