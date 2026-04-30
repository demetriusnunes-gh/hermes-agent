# App Store / Google Play chart research via public Appfigures pages

Use this when asked to research top-grossing mobile apps and public paid datasets (Sensor Tower/data.ai/AppMagic) are unavailable.

## Public proxy that worked

Appfigures public chart pages expose chart data in server-rendered HTML under:

```html
<script>var __appData = ...;</script>
```

Useful pages:

- iOS overall: `https://app.appfigures.com/top-apps/ios-app-store/united-states/iphone/top-overall`
- iOS category: `https://app.appfigures.com/top-apps/ios-app-store/united-states/iphone/{category-slug}`
- Google Play overall: `https://app.appfigures.com/top-apps/google-play/united-states/top-overall`
- Google Play category: `https://app.appfigures.com/top-apps/google-play/united-states/{category-slug}`

Category slugs are simple lower-case hyphen slugs such as `business`, `productivity`, `health-and-fitness`, `house-and-home`.

## Extraction pattern

1. Fetch the public HTML with a browser-like UA.
2. Parse `var __appData = (.*?);</script>` as JSON.
3. Traverse `data[6]` for dicts containing `results`.
4. Select `result['category']['subtype'] == 'topgrossing'`.
5. Read `result['entries']`: entries include `id`, `name`, `developer`, `developer_id`, `storefront`, `vendor_identifier`, and `price`.
6. Public pages generally return only ~30 entries per chart even when `total_count` says 200/500.

Python sketch:

```python
import requests, re, json
html = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=20).text
data = json.loads(re.search(r'var __appData = (.*?);\s*</script>', html, re.S).group(1))
for obj in data[6].values():
    if isinstance(obj, dict) and 'results' in obj:
        for res in obj['results']:
            if res.get('category', {}).get('subtype') == 'topgrossing':
                for rank, entry in enumerate(res['entries'], 1):
                    print(rank, entry['name'], entry.get('developer'), entry.get('vendor_identifier'))
```

## API caveat

The frontend JS references `/api/ranks/snapshots?category=...&country=...&count=...&start=...`, but direct calls returned `401 Unauthorized` without Appfigures auth. Prefer scraping the embedded `__appData` on public pages.

## Rating verification

- iOS: Apple Lookup API works without auth:

```python
https://itunes.apple.com/lookup?id={apple_track_id}&country=us
# fields: averageUserRating, userRatingCount, trackViewUrl, primaryGenreName
```

- Google Play: scrape the public detail page:

```python
https://play.google.com/store/apps/details?id={package}&hl=en_US&gl=US
# regex: aria-label="Rated ([0-5]\.[0-9]) stars out of five stars"
# reviews often nearby: <div class="g1rdde">18K reviews</div>
```

## Filtering heuristics used for Brazil solo-founder market scans

Exclude: games, giant social/media/streaming apps, marketplaces, banks/fintechs requiring licenses, hardware-first products, high-support networks, and dating/social apps.

Prioritize: niche digital subscriptions with localizable content/data, clear recurring pain, low operational burden, and app-store-proven willingness to pay. Good categories: Business, Productivity, Education, Health & Fitness, Medical trackers (non-diagnostic), Reference, House & Home, Food & Drink, Graphics & Design, Navigation niches.

Always label the result as a public-chart proxy unless the user provided paid top-1000 data access.
