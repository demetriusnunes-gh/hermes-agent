# Session note — 2026-09-27: provider fallback and rendered proof

## What worked
- When `web_search` and `web_extract` both reported no provider configured, do one diagnostic attempt each, then stop retrying them.
- Use an accessible search-results page only for candidate discovery. Bing results can be noisy or irrelevant, so do not treat snippets or absence of results as market proof.
- Open official product pages directly with the browser and inspect rendered accessibility text. `browser_snapshot(full=true)` exposed key claims; `browser_console` with `document.body.innerText` recovered claims omitted from compact snapshots.

## Evidence captured
- OpusClip homepage: “Used by 20M+ creators and businesses.” Pricing page showed $15/mo Starter, $29/mo monthly Pro, free tier, captions in 20+ languages, social publishing, API/business plans. URLs: https://www.opus.pro/ and https://www.opus.pro/pricing
- Fireflies homepage: “USED ACROSS 1 MILLION+ COMPANIES,” G2 4.8/5, 100+ languages, Portuguese (BR) listed in footer/language support, and testimonials from named companies. Pricing page showed free tier, Pro $10/seat/month annual billing, Business $19/seat/month annual billing. URLs: https://fireflies.ai/ and https://fireflies.ai/pricing
- Grammarly homepage: “Trusted by 50,000 organizations and 40 million people,” with paid Pro and Enterprise plans. URL: https://www.grammarly.com/

## Calibration
- Paid pricing demonstrates a monetization path, not verified revenue. Keep official adoption claims and paid plans separate from audited earnings.
- For Brazil incumbent sweeps, phrase noisy absence as “no obvious dominant Brazil-native leader found in this sweep,” not “no competitors exist.”
- A strong Brazil recurring-service shape is one upload/link in → one PT-BR deliverable out, with human QA for names, tone, brand terms, and compliance-sensitive claims; monthly billing can use Pix/card/boleto and delivery can use WhatsApp.
- Treat Brazil gap and payment/distribution fit as analyst inference unless independently sourced.
