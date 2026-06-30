#!/usr/bin/env python3
"""
Morning News Digest Generator

Curates news from balanced international and Brazilian sources.
Also tracks DoorDash (DASH) stock price and news.
Output: JSON with curated headlines by category + DoorDash section.
"""

import json
import sys
import subprocess
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timezone, timedelta

# --- FEED CONFIGURATION ---
# Sources chosen for balance, impartiality, and good coverage
FEEDS = {
    "world": [
        {
            "name": "BBC World",
            "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
            "count": 8,
        },
        {
            "name": "The Guardian World",
            "url": "https://www.theguardian.com/world/rss",
            "count": 6,
        },
        {
            "name": "Al Jazeera",
            "url": "https://www.aljazeera.com/xml/rss/all.xml",
            "count": 5,
        },
        {
            "name": "NPR World",
            "url": "https://feeds.npr.org/1004/rss.xml",
            "count": 5,
        },
    ],
    "brazil": [
        {
            "name": "BBC Brasil",
            "url": "https://feeds.bbci.co.uk/portuguese/rss.xml",
            "count": 8,
        },
        {
            "name": "Folha de S.Paulo",
            "url": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",
            "count": 6,
        },
        {
            "name": "Poder360",
            "url": "https://www.poder360.com.br/feed/",
            "count": 5,
        },
    ],
    "rio": [
        {
            "name": "G1 Rio de Janeiro",
            "url": "https://g1.globo.com/dynamo/rio-de-janeiro/rss2.xml",
            "count": 5,
        },
    ],
    "saopaulo": [
        {
            "name": "G1 Sao Paulo",
            "url": "https://g1.globo.com/dynamo/sao-paulo/rss2.xml",
            "count": 5,
        },
    ],
}

def fetch_dash_stock():
    """Fetch DASH stock price from Yahoo Finance."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "10",
             "https://query2.finance.yahoo.com/v8/finance/chart/DASH?range=1d&interval=1d"],
            capture_output=True, timeout=15
        )
        data = json.loads(result.stdout)
        r = data["chart"]["result"][0]
        close = r["indicators"]["quote"][0]["close"][0]
        meta = r["meta"]
        pc = meta.get("previousClose", close)
        change = close - pc
        pct = (change / pc) * 100 if pc else 0
        sign = "+" if change >= 0 else ""
        return {"price": close, "change": change, "pct": pct, "prev_close": pc,
                "formatted": f"DASH: ${close:.2f} | {sign}{change:.2f} ({sign}{pct:.1f}%) | Prev: ${pc:.2f}"}
    except Exception as e:
        print(f"  [warn] DASH stock fetch failed: {e}", file=sys.stderr)
        return None


def fetch_doordash_news(count=5):
    """Fetch DoorDash news from Google News RSS."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "10",
             "https://news.google.com/rss/search?q=DoorDash+when:1d&hl=en-US&gl=US&ceid=US:en"],
            capture_output=True, timeout=15
        )
        raw = result.stdout.decode("utf-8", errors="replace")
        if not raw.strip():
            return []
        tree = ET.fromstring(raw)
        items = []
        for item in tree.findall(".//item"):
            title_elem = item.find("title")
            link_elem = item.find("link")
            source_elem = item.find("source")
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
            link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
            source = source_elem.text.strip() if source_elem is not None and source_elem.text else "Google News"
            # Skip generic aggregator titles
            if "DoorDash - Google News" in title:
                continue
            if not title:
                continue
            items.append({"title": title, "link": link, "source": source})
            if len(items) >= count:
                break
        return items
    except Exception as e:
        print(f"  [warn] DoorDash news fetch failed: {e}", file=sys.stderr)
        return []


def fetch_rss(feed_info, timeout=15):
    """Fetch and parse an RSS feed via curl."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", str(timeout), feed_info["url"]],
            capture_output=True, timeout=timeout + 5
        )
        raw = result.stdout
        # Handle various encodings
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = raw.decode("iso-8859-1")
            except UnicodeDecodeError:
                text = raw.decode("utf-8", errors="replace")
        if result.returncode != 0 or not text.strip():
            return []
        tree = ET.fromstring(text)
        items = tree.findall(".//item")
        parsed = []
        for item in items[:feed_info["count"]]:
            title_elem = item.find("title")
            link_elem = item.find("link")
            desc_elem = item.find("description")
            pub_elem = item.find("pubDate")

            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
            link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
            desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
            pub_date = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else ""

            if not title:
                continue

            # Strip HTML tags from description
            desc = re.sub(r"<[^>]+>", "", desc).strip()

            parsed.append({
                "title": title,
                "link": link,
                "source": feed_info["name"],
                "summary": desc[:200],
                "pub_date": pub_date,
                "category": "",  # set later
            })
        return parsed
    except Exception as e:
        print(f"  [warn] Failed fetching {feed_info['name']}: {e}", file=sys.stderr)
        return []

def clean_text(text):
    """Remove HTML entities, HTML tags, and normalize spaces."""
    text = re.sub(r"<[^>]+>", "", text)
    html_entities = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'"}
    for ent, char in html_entities.items():
        text = text.replace(ent, char)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def build_digest():
    """Fetch all feeds, build a curated digest."""
    all_items = {}
    errors = []

    for category, feeds in FEEDS.items():
        all_items[category] = []
        for feed in feeds:
            print(f"Fetching {feed['name']}...", file=sys.stderr)
            items = fetch_rss(feed)
            if not items:
                errors.append(feed['name'])
            else:
                for item in items:
                    item["category"] = category
                    # Clean text
                    item["title"] = clean_text(item["title"])
                    item["summary"] = clean_text(item["summary"])
                all_items[category].extend(items)

    # Remove duplicate titles across all categories
    seen_titles = set()
    all_items_deduped = {}
    for category, items in all_items.items():
        all_items_deduped[category] = []
        for item in items:
            # Normalize title for dedup comparison
            norm = item["title"].lower().strip()
            if norm not in seen_titles and len(norm) > 5:
                seen_titles.add(norm)
                all_items_deduped[category].append(item)

    # Fetch DoorDash stock and news
    print("Fetching DASH stock and DoorDash news...", file=sys.stderr)
    dash_stock = fetch_dash_stock()
    doordash_news = fetch_doordash_news()

    result = {
        "date": datetime.now(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d"),
        "categories": {
            "world": {
                "label": "🌍 World",
                "items": all_items_deduped.get("world", []),
            },
            "brazil": {
                "label": "🇧🇷 Brasil",
                "items": all_items_deduped.get("brazil", []),
            },
            "rio": {
                "label": "🏖️ Rio de Janeiro",
                "items": all_items_deduped.get("rio", []),
            },
            "saopaulo": {
                "label": "🏙️ São Paulo",
                "items": all_items_deduped.get("saopaulo", []),
            },
        },
        "doordash": {
            "label": "📈 DoorDash (DASH)",
            "stock": dash_stock,
            "news": doordash_news,
        },
        "sources_errors": errors,
    }

    return result

if __name__ == "__main__":
    digest = build_digest()
    print(json.dumps(digest, ensure_ascii=False, indent=2))
