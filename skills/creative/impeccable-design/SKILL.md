---
name: impeccable-design
description: Use when designing, redesigning, critiquing, auditing, polishing, or improving frontend UI, websites, landing pages, dashboards, product flows, components, forms, onboarding, empty states, UX copy, visual hierarchy, typography, color, layout, motion, responsiveness, accessibility, or design systems. Adapted from pbakaus/impeccable.
version: 1.0.0
source: https://github.com/pbakaus/impeccable
---

# Impeccable Design

Production-grade frontend design workflow, adapted from Paul Bakaus's Impeccable project. Use this skill to avoid generic AI-looking UI and to improve design craft before editing or reviewing frontend code.

## Core idea

Impeccable provides a design vocabulary, command workflow, and anti-pattern detector for AI coding agents. It fights common LLM frontend defaults: Inter/system fonts everywhere, purple gradients, nested cards, gray-on-color text, glassmorphism, identical card grids, and generic SaaS hero/stat layouts.

## First steps on UI tasks

1. Classify the surface:
   - **brand**: marketing, landing pages, campaign pages, portfolio, long-form content; design is the product.
   - **product**: app UI, admin, dashboard, settings, tools, workflows; design serves the product.
2. Look for project context at root:
   - `PRODUCT.md`: users, brand, tone, anti-references, strategic principles. Required for serious design work.
   - `DESIGN.md`: tokens, type, color, components. Strongly recommended.
3. If the repo has Impeccable installed, run its context loader before mutations:
   - `.agents/skills/impeccable/scripts/load-context.mjs`
   - `.claude/skills/impeccable/scripts/load-context.mjs`
   - equivalent provider path if present.
4. If PRODUCT.md is missing or placeholder, ask the user to provide/generate product context before major design implementation. For small critiques, proceed but explicitly label assumptions.
5. For technical anti-pattern scans, use:
   ```bash
   npx --yes impeccable detect <file-or-dir-or-url>
   npx --yes impeccable detect --fast --json <target>
   ```

## Command vocabulary to apply

Use these as intent labels even if the user does not type an Impeccable command:

- `shape`: plan UX/UI before code. Produce scene, register, information architecture, layout, theme, color strategy, type, motion, edge states.
- `craft`: shape, get confirmation, then build end-to-end.
- `critique`: UX/design review, hierarchy, clarity, emotional resonance, cognitive load.
- `audit`: technical checks: accessibility, performance, responsive behavior, anti-patterns.
- `polish`: final shipping pass: alignment, rhythm, copy, states, design-system consistency.
- `bolder`: amplify a safe/bland design.
- `quieter`: tone down overstimulating UI.
- `distill`: remove complexity, reduce to essence.
- `harden`: handle errors, loading, empty states, i18n, text overflow, edge cases.
- `onboard`: first-run flows, activation, empty states.
- `animate`: purposeful motion.
- `colorize`: strategic color system.
- `typeset`: typography hierarchy, font pairing, line length.
- `layout`: spacing, rhythm, grids, alignment.
- `delight`: memorable micro-moments.
- `overdrive`: technically extraordinary effects when appropriate.
- `clarify`: UX copy, labels, error messages.
- `adapt`: responsive/device-specific adaptation.
- `optimize`: UI performance.
- `document`: generate DESIGN.md from existing UI.
- `extract`: pull reusable tokens/components into the design system.

## Design laws

### Color

- Prefer OKLCH. Reduce chroma near lightness extremes; high chroma near 0 or 100 looks garish.
- Avoid pure `#000` and `#fff`; tint neutrals very slightly toward the brand hue.
- Choose a color strategy before choosing colors:
  - **Restrained**: tinted neutrals plus one accent under ~10%. Product default.
  - **Committed**: one saturated color carries 30 to 60% of the surface.
  - **Full palette**: 3 to 4 named roles used deliberately.
  - **Drenched**: the surface is the color. Use for high-identity brand moments.

### Theme

Dark/light is not a category default. Write a concrete scene first: who uses this, where, under what ambient light, in what emotional state. Let the scene force the theme.

### Typography

- Body line length: 65 to 75ch.
- Hierarchy through scale and weight contrast. Use at least ~1.25 ratio between meaningful type steps.
- Avoid flat type scales and default-font laziness.

### Layout

- Vary spacing for rhythm. Equal padding everywhere is monotonous.
- Cards are not the default answer. Use them only when they are the best affordance.
- Nested cards are almost always wrong.
- Do not wrap everything in containers.

### Motion

- Do not animate layout properties.
- Prefer exponential ease-out curves, quart/quint/expo.
- Avoid bounce/elastic unless there is a very specific product reason.
- Respect reduced motion.

### Copy

- Every word earns its place.
- Avoid headings repeated as body intros.
- Avoid em dashes in UI copy, use commas, colons, semicolons, periods, or parentheses.

## Absolute bans / AI slop traps

If about to write one of these, rewrite the structure:

- Colored side-stripe borders (`border-left`/`border-right` >1px) on cards, list items, callouts, alerts.
- Gradient text via `background-clip: text`.
- Decorative glassmorphism as default.
- Generic hero metric template: big number, small label, supporting stats, gradient accent.
- Endless identical icon-heading-text card grids.
- Modal as first thought. Try inline/progressive alternatives first.
- Category reflex themes: observability dark blue, healthcare white/teal, finance navy/gold, crypto neon black, etc.

## Practical Hermes workflow

For frontend design changes:

1. Inspect current UI/code and project context.
2. Run `npx --yes impeccable detect` on the target when HTML/CSS/URL is available.
3. Produce an explicit design diagnosis: register, scene, color strategy, type, layout, motion, copy, anti-patterns.
4. If implementing: state a short preflight before editing, e.g. `IMPECCABLE_PREFLIGHT: context=pass|assumed product=pass|missing command_reference=pass shape=pass|not_required image_gate=pass|skipped:<reason> mutation=open`.
5. Modify real code, not just descriptions.
6. Verify with tests/build and, when possible, screenshot/visual inspection plus another `impeccable detect` pass.

## Installation notes for user projects

The upstream project supports Cursor, Claude Code, OpenCode, Pi, Gemini CLI, Codex CLI, GitHub Copilot, Trae, Rovo Dev, and Qoder. Easiest install: download from https://impeccable.style or copy the matching `dist/<tool>/...` directory from https://github.com/pbakaus/impeccable.

For Codex-style agents:

```bash
# project-local
cp -r dist/agents/.agents <project>/

# user-wide
mkdir -p ~/.agents/skills
cp -r dist/agents/.agents/skills/* ~/.agents/skills/
```

For Claude Code:

```bash
cp -r dist/claude-code/.claude <project>/
# or global
cp -r dist/claude-code/.claude/* ~/.claude/
```

## Linked upstream references

If deeper guidance is needed, fetch/read upstream reference files from:
`https://github.com/pbakaus/impeccable/tree/main/source/skills/impeccable/reference/`

Key references: `brand.md`, `product.md`, `shape.md`, `craft.md`, `critique.md`, `audit.md`, `polish.md`, `typography.md`, `color-and-contrast.md`, `spatial-design.md`, `motion-design.md`, `interaction-design.md`, `responsive-design.md`, `ux-writing.md`.
