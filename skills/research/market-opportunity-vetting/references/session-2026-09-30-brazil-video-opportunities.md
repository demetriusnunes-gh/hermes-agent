# Session notes: Brazil AI video-service sweep (2026-09-30)

## Access pattern
- The configured web search and extraction backends were unavailable.
- Diagnose the provider failure once; do not retry the same failed provider in parallel.
- Use Bing only for candidate discovery, then verify claims on official pages.
- Bing's Portuguese/local queries were noisy and sometimes returned generic Brazil results. Treat search-result absence as weak evidence.
- Direct official pages exposed stronger claims in rendered accessibility text than compact search snippets. `browser_console` with `document.body.innerText` was useful for confirming rendered claims.

## Verified official proof
- OpusClip homepage (`https://www.opus.pro`): rendered claim "Used by 20M+ creators and businesses." It also describes API/workflow automation and business/team features.
- OpusClip pricing (`https://www.opus.pro/pricing`): Free plan; Starter $15/month; Pro shown at $29 monthly / $19.43 equivalent on annual billing; Business custom pricing. This is monetization-path evidence, not verified revenue.
- HeyGen homepage (`https://www.heygen.com`): rendered claims include 4.8/5 from 1,000+ reviews, "Trusted by over 1,000,000 developers and leading companies," and "Trusted by 85% of the Fortune 100."
- HeyGen pricing (`https://www.heygen.com/pricing`): "100,000+ businesses"; Creator $29/month; Pro $49/month; 175+ languages and dialects. Treat the business count as official self-reported adoption.
- Synthesia homepage (`https://www.synthesia.io`): rendered claims include over 2,000 five-star G2 reviews, 4.7/5 on G2, 50,000+ companies, 160+ languages, and training/operations/compliance use cases.

## Brazil-fit conclusions
- The strongest Brazil opportunity is not a raw clone: all three global products are already internationally available and at least some expose Portuguese/localized pages.
- Reframe the opportunity as a managed, productized recurring service: one upload/URL in, one PT-BR output bundle out, with human QA for names, slang, brand terms, and compliance-sensitive claims.
- Useful wedges are idiomatic PT-BR, WhatsApp delivery, Pix/card/boleto billing, vertical specialization, and local turnaround—not generic feature parity.
- For video services, the narrowest viable shapes were: short-form repurposing for experts/agencies; English-to-PT-BR dubbing/localization; and SOP-to-training-video production for franchises or distributed SMBs.
- Local incumbent checks were noisy; use the calibrated wording "no obvious dominant Brazilian leader found in this sweep," never "no competitors exist."
- Exclude meeting transcription/notetaker clones when a global incumbent already has PT-BR support and the category appears crowded.

## Commercial framing
- For scheduled "passive income" digests, call these semi-automated productized recurring services, not fully passive income.
- Separate verified official traction, corroborated third-party evidence, and provisional market-gap inference.
- Never turn a pricing page into a revenue claim; say "commercially validated by official adoption claims plus paid plans" when independent earnings are unavailable.
