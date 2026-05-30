# Live UI verification for timestamped ordering

Use this when a timestamp-ordering change is deployed to a real site and you need to confirm the rendered order, not just the code.

## What to check

1. **Confirm the served bundle changed**
   - fetch the page HTML and make sure the asset hash or build reference is the new one
   - if the HTML still points at the old bundle, the browser may be showing an outdated build

2. **Bypass cache when needed**
   - open the page with a cache-busting query string if the app is static
   - use a hard refresh only as a secondary check; the bundle reference is the more reliable signal

3. **Inspect the rendered list visually**
   - check the visible order of the latest/timeline/feed cards in the browser
   - verify the order matches the expected comparator output, including tie cases

4. **Check the browser snapshot, not just the DOM source**
   - the final truth is the rendered order on screen
   - this catches stale hydration, client-side sorting drift, and mismatched cached data

## Good evidence to capture

- the current bundle hash or asset path from the page HTML
- a browser snapshot or screenshot of the rendered list
- the first few visible rows in the expected order

## Pitfall

If the code change is correct but the site still shows the old order, the issue is often that the deployed static assets were not refreshed or the browser is seeing a cached bundle. Verify the served HTML first, then the rendered UI.