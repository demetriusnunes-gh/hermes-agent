# Gallery / photo archival workflow

Use this when a page is a photo gallery and the goal is to download the underlying image assets, not summarize text.

## Fast discovery pattern
1. Load the page in the browser.
2. Inspect `document.querySelectorAll('img')` for `src/currentSrc`.
3. Also inspect raw HTML for `<link rel="preload" as="image" href="...">` entries; many gallery pages expose the full image list this way even when the visible DOM is lazy-loaded.
4. Deduplicate URLs and ignore non-photo assets (logos, icons, social widgets).

## Download pattern
- Prefer direct image URLs over screenshots.
- Use `requests`/`curl` with concurrency to download all files.
- Save filenames with numeric prefixes (`001_...`, `002_...`) to preserve page order.
- Write a `source_urls.txt` manifest next to the files.

## Publish on the VPS
- Put the folder under the Caddy-served web root, e.g. `/var/www/demetriusnunes.com/<subpath>/`.
- Add a simple `index.html` gallery so the folder is browsable over HTTP.
- Verify by opening the published URL in the browser.

## When Firecrawl is the wrong tool
- Firecrawl is great for text extraction, but for asset capture use browser inspection or raw HTML parsing when the page already exposes direct media URLs.
- If the page is JS-heavy but still exposes preload image URLs in HTML, regex extraction from the raw HTML is often the shortest path.
