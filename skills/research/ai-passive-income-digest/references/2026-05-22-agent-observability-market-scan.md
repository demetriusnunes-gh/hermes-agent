# 2026-05-22 Agent Observability / Cost-Control Market Scan

Concise notes from a successful digest run focused on agent observability, guardrails, sandboxes, and LLM spend controls. Use this as a reusable proof bank for future digests and Brazil-gap validation.

## Strong validated leads

### LLMCap
- Category: hard dollar caps / spend control proxy for LLM calls.
- Proof signals:
  - HN Show/Launch traction (recent discussion, strong engagement).
  - Live pricing page with a 3-day trial and clear self-serve tiers.
- Product details:
  - Stops requests when a dollar cap is hit; returns 429 before token consumption.
  - Supports Anthropic, OpenAI, Gemini, Mistral, Cohere.
  - Workflow surfaces: API proxy, VS Code extension, terminal CLI, Windows tray app.
- Brazil wedge hypothesis:
  - Good Brazil-first angle because spend predictability and BRL budgeting are easy to understand and self-serve.
  - Likely no obvious Brazil-local category leader with a similar hard-stop spend proxy.

### Superlog
- Category: agent observability + auto-fix loop.
- Proof signals:
  - Recent HN traction.
  - Live pricing page with Free / Developer / Pro / Enterprise.
- Product details:
  - OpenTelemetry-based observability.
  - Incident grouping, dashboards, alerts, Slack integration, and PRs for remediation.
- Brazil wedge hypothesis:
  - Could localize well for BR engineering teams adopting coding agents.
  - Stronger wedge if framed as "agent observability with remediation" rather than generic dashboards.

### Tilde.run
- Category: agent sandbox / reversible production runs.
- Proof signals:
  - Strong HN traction.
  - Live pricing page with Free / Pro / Team / Enterprise.
- Product details:
  - Versioned composable filesystem.
  - GitHub / S3 / Drive mounted into one sandboxed filesystem.
  - Emphasis on reversible runs and auditability.
- Brazil wedge hypothesis:
  - Useful for agencies, startups, and regulated teams that want agents to touch real data safely.
  - Brazil-first version should start with one narrow workflow and PT-BR onboarding.

### Retroguard
- Category: guardrails / jailbreak and leak prevention.
- Proof signals:
  - Live site with outcome-based pricing.
  - Concrete "pay per blocked request" model.
- Product details:
  - Claims secure AI guardrails with hardware attestation / Nitro Enclave messaging.
  - First 100 blocks free monthly, then per-block pricing.
- Brazil wedge hypothesis:
  - Likely best where privacy/compliance matters and usage-based pricing makes adoption low-friction.

## Secondary leads

### Torrix
- Category: self-hosted LLM observability.
- Proof signals: live product messaging with cost/privacy positioning and founder-member pricing language.
- Value: spend/latency/token visibility without forcing a large managed-stack commitment.

### Incidentary
- Category: incident root-cause / causal chain analysis.
- Proof signals: strong problem framing around when a failure began and how it spread.
- Value: a narrower wedge than generic observability, useful if the product is positioned around incident forensics.

## Validation pattern that worked

1. Start with HN Algolia queries around adjacent monetizable classes:
   - "Show HN AI"
   - "Launch HN AI"
   - "Show HN guardrails"
   - "Show HN proposal"
   - "Show HN voice AI"
   - "Show HN email API"
2. Prefer products with at least two signals:
   - HN traction + pricing page
   - pricing page + customer logos
   - explicit usage limits/caps + trial or self-serve checkout
3. When browser snapshots are sparse:
   - use `browser_snapshot` for page structure and visible numbers
   - use `browser_console(expression='document.body.innerText')` when text is missing
   - fall back to `urllib.request` / `curl` with a browser User-Agent for JS-heavy pages
4. For Brazil-gap checks:
   - verify adjacent incumbents before calling a market underserved
   - if an incumbent already owns the core workflow in Brazil, narrow the wedge instead of cloning the US product
   - prefer localizable products with clear pricing, compliance, or spend-control value

## HN/search queries that surfaced useful candidates

- "autonomous AI agent business ideas 2026"
- "AI micro SaaS"
- "self-running AI business"
- "AI agent revenue"
- "automated AI services"
- "Show HN AI"
- "Launch HN AI"
- "Show HN guardrails"
- "Show HN proposal"
- "Show HN voice AI"
- "Show HN email API"

## Reusable Brazil-local incumbent checklist

Check these before declaring a category open:
- Restaurant / WhatsApp automation: Anota AI, Goomer, Blip, Zenvia
- Clinics: iClinic, Feegow, Doctoralia, Ninsaúde
- Real estate: Kenlo, Jetimob, Vista, Imoview
- Licitações / procurement: Effecti, ConLicitação, LicitaJá, Portal de Compras Públicas

## Good localizable shapes

- hard spend caps for LLM calls
- agent observability with incident grouping and remediation
- secure guardrails with usage-based pricing
- reversible sandboxes / versioned execution for real data
- self-hosted/private observability for regulated teams
