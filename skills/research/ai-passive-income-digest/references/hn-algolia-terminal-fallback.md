# HN Algolia terminal fallback for passive-income research

Use this when browser snapshots fail, pages are empty, or CAPTCHA/bot detection blocks direct browsing.

## Reliable query pattern
- Query the HN Algolia API directly with a numeric filter on `created_at_i`.
- URL-encode `>` as `%3E` in `numericFilters`.

Example:
```text
https://hn.algolia.com/api/v1/search?query=AI%20microSaaS&tags=story&numericFilters=created_at_i%3E1720000000
```

## Terminal extraction
- `python3` + `urllib.request` is often enough.
- Set a browser User-Agent header.
- Inspect `hits[]` for title, points, URL, and comments count.
- Handle missing `url` fields; some HN items are text-only or have no external link.

## When to use
- Browser snapshot says empty page.
- Browser console times out.
- Search engines are blocked or noisy.
- Need fast, low-bot-detection discovery of fresh launches.

## Validation rule
Do not surface an idea unless you have at least one concrete proof signal from the source itself or from HN traction (points/comments/launch). Prefer two proof signals when possible (e.g. pricing page + HN traction, customer logos + pricing).