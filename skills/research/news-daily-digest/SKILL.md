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

If Yahoo fails, use:
```bash
curl -s 'https://www.google.com/finance/quote/DASH:NASDAQ' | grep -oP 'data-last-price="[\d.]+"' | head -1
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

3. Curate the digest — pick only the TOP 3 most important stories across ALL categories combined. Be ruthless. Remove celebrity gossip, minor local stories, sports, entertainment. Prioritize: geopolitical events, major policy changes, significant economic news, emergencies, anything that directly affects Demetrius's life (family, work, Rio, SP).

4. Format for delivery (see Output Format below).

5. Add a 1-line editorial note at the top with the date and any "must read" highlight.

## Output Format

```
☀️ Boa Demetrius — 3 headlines — Thu, 02 Apr 2026

🌍 Macron to Trump on Iran: "Be serious" — (BBC World)
   https://link...

🇧🇷 Trump diz que objetivos no Irã estão 'perto de alcançados' — (BBC Brasil)
   https://link...

🏖️ Rio: Helio Eichbauer morre aos 76 — (G1 Rio)
   https://link...

📈 DASH: $157.32 | +3.15 (+2.0%) — Prev: $154.17
   DoorDash launches new merchant analytics platform — (TechCrunch)
   https://link...
```

The **DD section** appears after the news stories. Include stock price always (if available), then max 2 relevant DoorDash stories. If no meaningful news and stock is flat (<1% change), skip the DD section entirely.

## Delivery

Deliver to:
- Telegram (primary)
- WhatsApp to +5521988490510 (Demetrius personal)

## When to Use

- Cron job runs daily at 8 AM BRT (11:00 UTC)
- On demand when Demetrius asks for daily digest or news recap
- Can skip if no significant news found across categories

## Tips

- Be brief — Demetrius doesn't want to read much
- Keep headlines in the original language of the source
- Don't add commentary unless something is truly noteworthy
- If a source fails, mention it at the bottom quietly
- Deduplicate: same story from multiple sources should appear only once (prefer BBC or the most reputable source)
- If G1 Rio or G1 SP feeds are empty, broaden to G1 Brasil for that category
- **Pitfall on Hostinger VPS**: `feeds.g1.globo.com` may resolve to NXDOMAIN (DNS failure). In that case, all G1 feeds will fail. The bundled script will still return empty/stale items for Rio/SP categories (it may serve cached old articles). Check pub_date — if items are not from today/yesterday, skip Rio and SP sections entirely and add a brief note at the bottom: "⚠️ G1 feeds indisponíveis hoje."
- The script handles encoding issues (ISO-8859-1 from Brazilian sources) automatically