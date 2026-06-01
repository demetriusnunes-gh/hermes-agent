# Browser DOM extraction for ranking analysis

Use this when you need to verify a live ranking/timeline UI and compute summaries from the rendered page.

## Practical pattern

- If a static app looks blank when opened via `file:///.../index.html`, serve the directory over HTTP and open `http://127.0.0.1:PORT/` instead.
- After the app renders, use browser console queries against the live DOM rather than scraping source bundles.
- For list-based UIs, inspect repeated cards with selectors like `main article`, then extract `innerText` into structured rows.

## Example extraction shape

- `date`
- `match type`
- `team1`
- `team2`
- `score`

## Analysis tips

- Count results by date to see when activity clustered.
- Count matches per player to spot volume leaders.
- Compare wins/losses and game differential to identify the month’s standout performer.
- If the UI has a "latest results" view and a full results view, confirm both share the same order logic before trusting the summary.
