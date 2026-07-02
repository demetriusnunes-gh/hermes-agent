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

### Proof gathering in practice
Prefer official landing pages, pricing pages, customer pages, case studies, and funding announcements. If the homepage snippet is thin, use the rendered page text or search-result snippet from the official site before discarding a candidate; traction claims are often surfaced there rather than in compact summaries.

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
