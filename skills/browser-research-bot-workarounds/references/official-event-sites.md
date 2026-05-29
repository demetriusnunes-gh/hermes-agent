# Official event-site research notes

## Worked example: Roland-Garros live results / match reports

When Bing search was noisy or irrelevant, the official Roland-Garros site worked reliably:

- Homepage: `https://www.rolandgarros.com/en-us/`
- The page exposed readable DOM text for live results, top stories, and match reports.
- `browser_console(expression='document.body.innerText')` returned a clean text dump of the current homepage/article page.
- A useful discovery technique was to enumerate anchors and filter by visible text:

```js
Array.from(document.querySelectorAll('a'))
  .map(a => ({ text: a.innerText.trim().replace(/\s+/g, ' '), href: a.href }))
  .filter(x => x.text.includes('MATCH REPORT') || x.text.includes('LIVE') || x.text.includes('PREVIEW'))
```

This surfaced direct article URLs such as:

- `https://www.rolandgarros.com/en-us/article/2026-edition-r1-monfils-gaston`
- `https://www.rolandgarros.com/en-us/article/2026-edition-r1-wawrinka-dejong`
- `https://www.rolandgarros.com/en-us/article/2026-edition-1r-svitolina-bondar`

## Practical lesson

For sports/tournament coverage:

1. Open the official site directly.
2. Read the homepage/article DOM instead of using search snippets.
3. Use `browser_console` to extract anchors, article titles, and direct hrefs.
4. Follow the direct article URL for the full report or result.

This is often faster and cleaner than trying to force Bing/Google to surface the right result.
