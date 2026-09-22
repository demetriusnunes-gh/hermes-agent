---
name: market-opportunity-vetting
description: Evaluate existing products/services as rebuild or adaptation candidates, with evidence-based selection and geography-specific fit checks.
---

# Market Opportunity Vetting

Use this skill when asked to research, shortlist, or rank business opportunities by looking at proven products in one market and judging whether they are worth rebuilding or adapting for another market.

## Goal
Produce a small, decision-ready shortlist of opportunities that are:
- already working in a large market
- supported by evidence of traction, customers, revenue, or strong adoption
- plausibly adaptable to the target market
- not obviously blocked by regulation, payments, language, or distribution

## Default workflow
1. **Anchor on proof, not vibes**
   - Prefer official company pages, customer pages, product docs, public funding announcements, and reputable business press.
   - Do not include ideas that only look interesting in theory.

2. **Filter by market fit**
   - Ask whether the product still makes sense in the target market after changing language, billing, workflows, and compliance.
   - Exclude ideas that depend on a market structure the target country does not have.

3. **Check for local incumbents**
   - If the target market already has obvious strong local leaders, only keep the idea if there is a clear wedge.
   - Prefer categories where localization is the real moat, not generic feature parity.

4. **Prefer easy rebuilds**
   - Favor products that can be rebuilt as a narrow, useful MVP.
   - Prefer workflow or content tools over deep infrastructure or enterprise-heavy platforms.

5. **Limit the shortlist**
   - Return at most 3 ideas.
   - For each finalist, include:
     - US proof point
     - why the target market looks underserved
     - why the business fits the target market
     - smallest viable target-market-first version

## Evidence standard
Use at least one strong proof signal, preferably more than one:
- official site claims about customers, usage, downloads, or scale
- reputable press coverage of funding, growth, revenue, or enterprise adoption
- recognizable customer logos or testimonials
- public usage statistics or user counts

When possible, triangulate traction using multiple sources rather than relying on a single article.

### Proof extraction tip
Many modern landing pages hide the strongest traction claim in rendered DOM or page source rather than the compact browser snapshot. If the homepage snapshot is inconclusive, inspect the live page text/source before discarding the candidate. Prefer official-site wording over third-party roundup claims.

## Earning-proof discipline
A paid pricing page proves that a product has a monetization path, not independently verified revenue. Treat evidence in this order:
1. verified official traction: named customers, usage/user counts, downloads, or published scale;
2. corroborated earning signal: reputable reporting on revenue/funding/growth, or multiple recognizable customer references;
3. official self-reported monetization: paid tiers, enterprise plans, API billing, or business pricing.
If only level 3 is available, say so explicitly and lower confidence; do not write “earning” or imply audited revenue. Put the exact source URL beside the claim.

## Output shape
When asked for a shortlist, answer in a compact table or bullets with:
- idea name
- US proof point
- target-market gap
- fit rationale
- smallest viable MVP
- brief exclusion note if relevant
- a final one-line recommendation naming the best rebuild bet and why

Keep the shortlist tight (max 3 ideas) and concise; avoid filler explanations.

## Pitfalls
- Do not treat a clever idea as a good opportunity unless there is proof of demand.
- Do not keep ideas that are strong in the US but awkward in the target market because of payment rails, language nuance, regulation, or buying behavior.
- Do not build a long list; the value is in disciplined curation.
- Do not confuse generic AI novelty with durable demand.
- If live verification is limited, say so clearly and keep confidence calibrated.

### Brazil-specific lens
When the target market is Brazil, explicitly check:
- Portuguese output quality and tone
- Pix/boleto/card payment behavior
- WhatsApp-heavy workflows
- SMB adoption patterns
- local regulatory or data handling constraints
- whether a strong Brazilian incumbent already owns the category
- whether the smallest viable version is a single-upload -> single-outcome workflow (clip, dub, photo/listing) rather than a broad platform

### Brazil incumbent sweep
Before keeping a US winner, do a quick local-incumbent sanity check for the category. If Brazil already has several visible native tools, exclude the idea unless there is a clear wedge (better WhatsApp workflow, stronger PT-BR localization, materially simpler workflow, or a distribution advantage).

Categories that are often crowded in Brazil and need a sharper wedge to survive:
- WhatsApp/voice receptionist and lead qualification
- PT-BR meeting transcription / notes / follow-up
- Ad creative generation for performance teams and agencies
- Product-photo / listing optimization for marketplaces
- AI website builders
- Help desk / customer support AI
- Review-generation / reputation tools

### Browser fallback sequence
When search configuration is unavailable: diagnose the failure once; use an accessible search results page only to discover candidates; then open the candidate’s official homepage, pricing, customer, and about pages directly. Inspect rendered accessibility text/DOM because compact snapshots often omit traction claims. Record the exact wording and URL while researching. For local incumbents, run a separate category query and preserve the calibrated conclusion “no obvious dominant leader found in this sweep” when results are noisy or incomplete.

### Proof gathering in practice
Prefer official landing pages, pricing pages, customer pages, case studies, and funding announcements. If the homepage snippet is thin, use the rendered page text or search-result snippet from the official site before discarding the candidate; traction claims are often surfaced there rather than in compact summaries.

### Commercial proof and recurring-service framing
For opportunity digests, distinguish clearly between:
- **official traction:** named customers, user/business counts, reviews, or published usage;
- **monetization path:** visible paid tiers, API billing, or business pricing;
- **verified earnings:** independently reported revenue, ARR, or growth.

Do not turn a pricing page into a revenue claim. If verified earnings are unavailable, say that the service is commercially validated by traction plus paid plans, and label revenue as unverified. When the user asks for “passive income,” prefer a semi-automated, productized recurring service and state that it is not fully passive.

For scheduled digests, include the research date, keep the final list to only candidates that pass all gates, and make the final recommendation one sentence naming the best rebuild bet and its decisive wedge.

When the configured search provider is unavailable, diagnose the failure once, then switch to an accessible search-engine results page (for example, Bing) and direct official product pages rather than repeatedly retrying the same provider. Do not spend the research budget issuing the same failed provider call in parallel. Inspect the rendered DOM/accessibility text on official pages for traction claims, and record the exact claim plus source URL. Prefer official homepages, pricing pages, product pages, and customer pages that expose claims in rendered text; search snippets are leads, not final evidence. Use a separate local-incumbent query for each finalist category; search-result absence is weak evidence, not proof that no competitor exists. Phrase conclusions as “no obvious dominant leader found in this sweep” unless a broader local-market check supports stronger language. Distinguish official traction from provisional gap inference in the final output.

For recurring research runs, separate the evidence into three confidence levels: (1) verified official traction, (2) corroborated third-party or customer evidence, and (3) provisional market-gap inference. Do not present level 3 as a fact.

### Run discipline when evidence is thin
- If a search backend is unavailable, diagnose it once, switch to browser/direct official pages, and do not keep retrying the same failed provider or parallelizing identical failures.
- Treat search-result absence as weak evidence. Noisy or irrelevant local results should produce a calibrated statement such as “no obvious dominant local leader found in this sweep,” never “no competitors exist.”
- A globally available product is not automatically a Brazil opportunity. Separate the underlying product’s availability from the local service wedge; the finalist must explain why a PT-BR, WhatsApp, Pix/card/boleto, vertical, or managed-service layer creates room despite global access.
- Do not pad the shortlist to three. If only one or two candidates meet the proof, Brazil-fit, and rebuildability gates, return fewer.
- If current independent traction or revenue cannot be verified, label the claim as official self-reported monetization/adoption and lower confidence—or exclude the candidate rather than implying stronger proof.
- Include source URLs beside the exact proof claim, and distinguish official traction from the analyst’s provisional gap inference in the final wording.

### High-signal Brazil rebuild archetypes
When you need a fast shortlist, prioritize categories that already have a clear US leader and a narrow Brazil-first MVP:
- WhatsApp / voice receptionist for SMB lead capture and booking
- PT-BR meeting transcription, notes, and follow-up delivery
- Ad creative generation for performance marketing teams and agencies
- Product-photo / listing optimization for marketplaces and e-commerce sellers

## Proof shortcuts

- creator/user scale claims on the product homepage
- download counts
- business/customer counts
- customer-logo pages or named case studies

## Reference material
See `references/brazil-market-shortlist.md` for a concise example of the Brazil rebuild filtering criteria and the kinds of finalists/exclusions that passed this session's review.
See `references/brazil-ai-passive-income-digest.md` for session notes on proof signals, Brazil-fit filters, and the shortlist pattern that worked here.
See `references/brazil-ai-passive-income-candidates.md` for a compact session note on the three strongest Brazil-first AI rebuild archetypes that repeatedly surfaced here.
See `references/brazil-local-incumbent-sweep.md` for a compact checklist of categories that are often already crowded in Brazil and the MVP bias that tends to work.
See `references/research-access-and-evidence.md` for browser fallback, evidence-confidence labels, and Brazil incumbent-sweep handling when search access is limited.
See `references/rendered-dom-proof-patterns.md` for exact traction/pricing extraction and calibration rules from rendered official pages.
See `references/brazil-semi-automated-video-services.md` for the recurring-service evidence pattern and source claims captured from the latest Brazil video-opportunity sweep.
See `references/session-2026-09-22-brazil-video-opportunities.md` for rendered official-page evidence, source URLs, and calibration notes from the 2026-09-22 sweep.
