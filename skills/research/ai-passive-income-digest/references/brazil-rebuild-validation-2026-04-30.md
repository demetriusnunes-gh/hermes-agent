# Brazil rebuild validation notes — 2026-04-30

Reusable evidence and market-gap notes from the 2026-04-30 AI passive income digest. Use these as seed leads, but re-check pages before citing because traction/pricing can change.

## Strong US proof pages

### Slang AI — restaurant voice AI
- Pricing page: https://www.slang.ai/pricing
- Customer stories: https://www.slang.ai/customers
- Extracted proof signals: starts at $399/location/month; claims 2,000+ full-service restaurants; platform built on 20M+ calls; customers cite 100+ hours/month saved, 96% CSAT, 700 voicemails eliminated, 15k calls / 1.5k reservations in one month, $105k+ reservations captured, 88.4% of calls handled entirely by Voice AI.
- Brazil-gap framing: Anota AI/iFood, Goomer, Saipos, Consumer, Zenvia/Blip are strong around WhatsApp ordering, menus, POS, and horizontal messaging, but no obvious Slang-style restaurant-specific AI phone layer. Best wedge is not generic restaurant chatbot; it is phone + WhatsApp missed-order recovery for pizzerias/delivery-heavy SMBs.

### Assort Health — healthcare voice AI
- Homepage: https://www.assorthealth.com/
- Extracted proof signals: trained on 125M+ interactions; trusted by thousands of providers across 20+ specialties; customer-story metrics include $2.3M new revenue captured, 89% hold-time reduction, +220% labor capacity, 81% abandonment decrease, $1.3M additional appointment revenue; 3.3M+ annual revenue per 100 providers; 4.3/5 patient rating across 344k reviews; 15+ EHR/PMS integrations.
- Brazil-gap framing: iClinic, Feegow, Doctoralia, Ninsaúde are strong PMS/agenda/marketplace incumbents. The viable wedge is a layer on top: WhatsApp/voice AI receptionist for specialty clinics handling convênio/private-pay qualification, scheduling, intake, confirmations, no-show recovery, LGPD consent, and human handoff.

### EliseAI — property-management/leasing AI
- Homepage: https://eliseai.com/
- Extracted proof signals: major housing customer logos include Greystar, AvalonBay, Equity Residential, Bozzuto, Brookfield, Invitation Homes, Cardinal Group; product scope includes text/email/chat/voice, prospect management, leasing, tours, maintenance, renewals, delinquency, integrations, and centralized property-management operations.
- Brazil-gap framing: Kenlo, Jetimob, Vista, Imoview, Superlógica, Group Software are strong CRMs/back-office/ERP/payment incumbents, while QuintoAndar/Loft are marketplace/transaction platforms. The opportunity is not another CRM; it is a WhatsApp-native AI leasing assistant that responds to rental leads, answers listing FAQs, qualifies tenants, schedules visits, writes notes back to the CRM, and follows up.

### GovDash — government contracting/proposal AI
- Homepage: https://www.govdash.com/
- Extracted proof signals: claims hundreds of businesses, $5B+ customer contract wins last year, 60% faster proposal preparation, 90% reduction in draft turnaround, 150% more weekly opportunities recommended.
- Brazil-gap caution: do not include a generic licitações assistant unless narrowed. Effecti is already strong in Brazil and now prominently markets AI (Aimê), with claims of +3,000 companies, +R$82B arrematados, +840k opportunities, +456k proposals sent. If used, frame as a niche auditable compliance/proposal copilot for a specific supplier segment, not broad licitação automation.

## Current best Brazil-first wedges
1. WhatsApp AI leasing assistant for imobiliárias: strongest risk/reward; low regulation; high WhatsApp lead volume; clear CRM-overlay positioning.
2. AI front desk for specialty clinics: strong ROI but requires LGPD/healthcare care and more onboarding.
3. AI phone + WhatsApp order taker for pizzerias: clear SMB ROI, but adjacent competition from Anota AI/iFood and restaurant tooling means the phone/missed-call wedge must be explicit.

## Research workflow note
When browser pages render but snapshots omit numbers, run `browser_console(expression='document.body.innerText')`. When browser timeouts or JS-heavy pages are slow, use terminal `python3` + `urllib.request` with a browser User-Agent, strip tags, and search for evidence snippets. This worked for EliseAI/GovDash/Effecti/Anota AI on 2026-04-30.