# 2026-05-14 research notes — HN leads, proof snippets, and Brazil-gap checks

Condensed notes from the 2026-05-14 AI passive income digest. Re-check pages before citing because pricing/traction can change.

## HN leads that met the traction threshold
- **Statewright** — https://github.com/statewright/statewright
  - HN: *Show HN: Statewright – Visual state machines that make AI agents reliable* (121 points, 54 comments)
  - Proof on repo page: Free / Pro / Team / Enterprise pricing; free tier; self-hostable engine.
  - Brazil note: good PT-BR devtool fit, but keep it as workflow guardrails / run history rather than generic agent hype.

- **Libretto** — https://github.com/saffron-health/libretto
  - HN: *Show HN: Libretto – Making AI browser automations deterministic* (134 points, 56 comments)
  - Proof on repo page: deterministic browser automation toolkit; install/setup docs; Chromium onboarding.
  - Brazil note: strongest as an automation reliability layer, not a consumer app.

- **Dead Simple Email** — https://deadsimple.email/
  - HN: *Show HN: Dead Simple Email – Email API for AI Agents* (3 points, 0 comments)
  - Proof on site: purpose-built inboxes for agents; 5 inbox free tier; 100 inboxes for $29/mo; bidirectional inbound webhooks.
  - Brazil note: useful infra, but not a strong Brazil-first SMB wedge.

- **Retroguard** — https://retroguard.ai
  - HN: *Show HN: Retroguard – Verifiably secure AI guardrails* (6 points, 0 comments)
  - Proof on site: $0/mo base; first 100 blocks free; $2 per 100 blocked requests.
  - Brazil note: best for regulated B2B teams; too infra-heavy for the passive-income brief unless localized into compliance tooling.

- **Agensi** — https://www.agensi.io
  - HN: *Show HN: Agensi – Curated marketplace for AI agent skills (SKILL.md)* (1 point, 0 comments)
  - Proof on site: one-time purchase, instant download, works with Claude Code / Codex / Cursor / 20+ agents.
  - Brazil note: local wedge is selling BR-specific skills (WhatsApp, Pix, NF-e, Omie/Tiny/Bling, Nuvemshop, VTEX), not a generic global marketplace.

- **Proposly** — https://proposly.org
  - HN: *Show HN: Proposly – AI-generated client proposals for freelancers* (1 point, 0 comments)
  - Proof on site: 2 free proposals, no card required, <$1 per proposal, 30s generation time, testimonials.
  - Brazil note: viable if narrowed to PT-BR freelancers/agencies and Pix billing.

## Direct-page extraction patterns that worked
- Use `python3 + urllib.request` with a browser User-Agent to fetch pages directly.
- Strip tags with regex and search for snippets around keywords like `pricing`, `customers`, `revenue`, `hours`, `calls`, `reservations`, `proposals`.
- This was more reliable than browser snapshots for pages with dynamic content.

## Brazil incumbent checks that informed exclusion/narrowing
- **Imobiliárias / housing**: Kenlo, Jetimob, Vista, Imoview, Superlógica are strong CRMs/ERPs; viable wedge is WhatsApp-native leasing assistant, not another CRM.
- **Healthcare**: iClinic, Feegow, Doctoralia, Ninsaúde already cover agenda/PMS/marketplace; viable wedge is AI receptionist on top.
- **Restaurants**: Anota AI, Goomer, Blip, Zenvia are strong around ordering and WhatsApp; viable wedge is missed-call / phone recovery, not generic chatbot.
- **Licitações**: Effecti is strong and now markets AI; avoid broad licitação automation and narrow to auditable compliance/proposal copilot if used at all.

## Market-gap lesson
- Strong US proof alone is not enough; the idea must also survive a Brazil-gap check against adjacent incumbents.
- Prefer a narrow Brazil-first wedge that overlays an incumbent workflow rather than cloning the US product one-for-one.
