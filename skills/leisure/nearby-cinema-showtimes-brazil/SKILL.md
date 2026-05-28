---
name: nearby-cinema-showtimes-brazil
description: Find cinemas near a Brazilian neighborhood/address and extract current showtimes using OSM plus chain-specific website tactics (Grupo Estação, Kinoplex, Cinesystem).
version: 1.0.0
metadata:
  hermes:
    tags: [cinema, movies, showtimes, brazil, rio-de-janeiro, local]
    related_skills: [find-nearby, browser-research-bot-workarounds]
---

# Nearby Cinema Showtimes (Brazil)

Use this when the user asks things like:
- "Tem algum filme bom no cinema passando aqui perto de X?"
- "Quais cinemas perto de Y estão com sessão hoje?"
- "O que está em cartaz perto de Z?"

This workflow is for **Brazilian cinemas**, especially Rio, where generic search engines may fail or be blocked.

## Why this skill exists

A normal web search was unreliable:
- Google hit bot protection
- DuckDuckGo also challenged
- some cinema sites return incomplete HTML to raw `requests`
- accessibility snapshots may show filters but omit loaded showtime content

The robust pattern was:
1. geocode the neighborhood/address
2. find nearby cinemas with OpenStreetMap/Overpass
3. fetch showtimes using **site-specific tactics** per chain
4. summarize only the best nearby options + a few good picks

## Step 1: Find nearby cinemas

Use Python/requests against Nominatim + Overpass.

Example:
```python
import requests, math, json
headers = {"User-Agent": "HermesAgent/1.0"}

# geocode
geo = requests.get(
    "https://nominatim.openstreetmap.org/search",
    params={"q": "Laranjeiras, Rio de Janeiro, Brazil", "format": "jsonv2", "limit": 1},
    headers=headers,
    timeout=30,
).json()
lat = float(geo[0]["lat"]); lon = float(geo[0]["lon"])

query = f'''
[out:json][timeout:25];
(
  node[amenity=cinema](around:4000,{lat},{lon});
  way[amenity=cinema](around:4000,{lat},{lon});
  relation[amenity=cinema](around:4000,{lat},{lon});
);
out center tags;
'''
res = requests.get("https://overpass-api.de/api/interpreter", params={"data": query}, headers=headers, timeout=60).json()
```

Sort by distance and keep the closest relevant cinemas.

## Step 2: Get showtimes by chain/site

### A) Grupo Estação

Important findings:
- raw `requests` to old URLs like `grupoestacao.com.br/programacao` may return **406 ModSecurity**
- browser navigation works on the modern site
- the accessibility snapshot may show the filters and heading but **not the loaded movie list**
- `document.body.innerText` via `browser_console` is often the easiest extraction method

Useful URLs:
- main: `https://grupoestacao.com.br/em-cartaz/`
- filtered: `https://grupoestacao.com.br/em-cartaz/?cinema=33&data=2026-04-12`

Observed cinema IDs on the site:
- `33` = ESTAÇÃO NET BOTAFOGO
- `34` = ESTAÇÃO NET RIO
- `506` = ESTAÇÃO NET GÁVEA

Recommended extraction flow:
1. `browser_navigate` to the filtered URL with `cinema` and ISO date
2. if snapshot lacks movie titles, run:
```js
document.body.innerText
```
3. parse titles + times from the body text
4. if needed, inspect form select options with:
```js
Array.from(document.querySelectorAll('form#sessoesselector2 select')).map(sel => ({name: sel.name, options: Array.from(sel.options).map(o => ({text: o.textContent.trim(), value: o.value}))}))
```

### B) Kinoplex

Important finding:
- the cinema page HTML contains a hidden AJAX endpoint for programming
- this is much easier than scraping the rendered page

Pattern:
- cinema page: `https://www.kinoplex.com.br/cinema/kinoplex-rio-sul/39`
- hidden showtime endpoint:
  `https://www.kinoplex.com.br/cinema/_programacao_detalhes.php?c=39&data=YYYYMMDD&f=`

How to derive the date:
- endpoint wants `YYYYMMDD`

How to extract:
- request the `_programacao_detalhes.php` URL directly
- parse repeated movie blocks
- useful regex targets:
  - movie title: `header-link`
  - room: `numero-sala`
  - labels: `label ...` (DUB, LEG, 3D, etc.)
  - times: `HH:MM`

This worked well for Kinoplex Rio Sul (`c=39`).

### C) Cinesystem / Belas Artes Botafogo

Important findings:
- `https://www.cinesystem.com.br/cinemas` is a Next.js page with useful `__NEXT_DATA__`
- that page exposes cinema names/IDs/slugs in JSON
- the cinema detail page fetched via raw requests showed mostly promo data, not the actual showtime list
- browser rendering DID expose the showtimes in `document.body.innerText`

Flow:
1. fetch `https://www.cinesystem.com.br/cinemas`
2. extract `__NEXT_DATA__`
3. find the cinema entry (example found: Belas Artes Botafogo = slug `belas-artes-botafogo`, id `1606`)
4. navigate browser to:
   `https://www.cinesystem.com.br/cinemas/belas-artes-botafogo/1606`
5. extract:
```js
document.body.innerText
```
6. parse titles, rooms, formats, ratings, and times from the rendered text

## Step 3: Recommend "good" movies, not just list everything

If the user asks broadly for a good movie, give:
- 2–4 nearby cinema options
- a few movie recommendations by vibe

Good response structure:
- closest cinemas + distance
- notable films + times
- quick recommendation buckets like:
  - more serious / "filme bom pra ver de verdade"
  - lighter / fun
  - family / kids
  - horror / suspense

## Pitfalls

- Do not rely on Google or DuckDuckGo search results alone; both may challenge bots.
- Do not assume browser accessibility snapshot contains JS-loaded showtimes.
- For Grupo Estação, raw HTTP can fail with 406 even though browser access works.
- For Cinesystem, raw page fetch may show promo JSON only; use browser-rendered text.
- For Kinoplex, prefer the hidden `_programacao_detalhes.php` endpoint over brittle DOM scraping.

## Verification

Before replying, verify:
- cinema is actually near the requested neighborhood/address
- date is current/intended
- at least one concrete title+time pair is present
- recommendations match the movies you actually extracted
