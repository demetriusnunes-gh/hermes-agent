---
name: rankingpcc-app-maintenance
description: Use when modifying or debugging the RankingPCC Vite/React app on this VPS, especially ranking formula/results UI, Caddy/static deployment, and Vitest coverage.
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rankingpcc, vite, react, caddy, elo, tennis]
    related_skills: [test-driven-development, vite-supabase-caddy-webapp, systematic-debugging]
---

# RankingPCC App Maintenance

## Overview

RankingPCC is the user's Vite/React club tennis ranking app. Work from `/root/.www/rankingpcc` when the workspace tag points there, build with Vite, and deploy static assets by copying `dist/` to `/var/www/rankingpcc`.

Use test-driven changes for formula and UI updates: add/adjust Vitest tests, run targeted tests, build, deploy, browser-verify production, then commit a revert point.

## Key Files

- App entry/UI: `src/main.jsx`
- Ranking/Elo logic: `src/ranking.js`
- Formula tests: `src/ranking.test.js`
- Homepage/results UI tests: `src/main.test.jsx`
- Styles: `src/styles.css`
- Static deployment root: `/var/www/rankingpcc`

## Current Ranking Formula Notes

The production ranking now uses a doubles Elo model plus zero-sum activity redistribution:

- Each player starts at 1000 unless `initialRating` is set.
- Team rating is the mean of the two player ratings.
- Expected score uses standard Elo: `1 / (1 + 10 ** ((oppRating - rating) / 400))`.
- K by parsed format: short set `10`, single set `20`, best-of-3 with super tiebreak `40`, full best-of-3 `60`.
- Two-set reports are intentionally treated as `best_of_3_super` for K/activity weighting.
- Game-margin multiplier is capped from `1.0x` to `1.5x`; super tiebreaks count as one Elo game for the winner and zero for the loser.
- Inactive players receive a format-scaled penalty; the total deducted from inactive players is redistributed evenly to the four participants as participation bonus.
- Keep rating changes zero-sum across the full player pool. Tests should assert total rating preservation where possible.
- Track `streak` as positive consecutive wins and negative consecutive losses, plus `lastMatch` date.

## Current UX Notes

- The homepage should show latest club ranking results as a slim, horizontally animated ticker, not an external TNNS/Sofascore live feed.
- Keep a “Resultados” page/view for all reported club results.
- Do not reintroduce the tennis curiosities widget unless explicitly asked.
- Ranking should be tabular and include simulation-style columns in this order: position, player, rating, matches, W-L, win %, **Games Δ** (game differential; do not label it “Saldo”), Elo Δ, net activity delta (`participationBonus - inactivityPenalty`), and streak. Do not include a “Último jogo” column on the main ranking table unless explicitly requested.
- Match result cards should be clickable and expand calculation details, including participation bonus and per-player before/after deltas.
- Homepage ticker result pills should be compact two-line items: first line date + format, second line winner/loser/score. Use structural wrappers such as `.slim-meta` and `.slim-main` so tests and responsive CSS can verify the line split.
- User-facing best-of-3 labels should be simplified: both `best_of_3_super` and `best_of_3_full` display as “melhor de 3” even though K/activity logic still distinguishes them internally.
- Admin edit/delete controls should only appear on the full `/resultados` match cards, not in the homepage ticker or player result modal.

## Standard Workflow

1. Inspect git status before changes.
2. Add/update tests first when feasible:
   ```bash
   npm test -- --run src/ranking.test.js src/main.test.jsx
   ```
3. Implement in `src/`.
4. Verify:
   ```bash
   npm test
   npm run build
   ```
5. Deploy:
   ```bash
   cp -a dist/. /var/www/rankingpcc/
   ```
6. Browser-verify `https://rankingpcc.demetriusnunes.com` for expected text and clickable calculation details.
7. Commit the app changes so the user has an easy revert point.

## Pitfalls

- Do not trust stored `match.parsed` when changing parsing/formats; recompute from `scoreText` so old saved matches follow current rules.
- Production does not change after `npm run build` until `dist/` is copied to `/var/www/rankingpcc/`.
- Keep unrelated Caddy/proxy changes out of formula/UI commits unless the user asked for routing changes.
- If removing obsolete widgets, remove dead imports/files/tests or update the test suite so stale feed/trivia artifacts do not keep passing accidentally.
- Browser snapshots may show only compact content at first; use DOM inspection or click a match card to confirm `.match-breakdown` text includes participation bonus.
- When a UI fixture adds multiple match cards, existing `getByText(/editar|excluir/)` tests may become ambiguous; use `getAllByText(...).length` or scope queries to a specific page/card.

## Verification Checklist

- [ ] `npm test` passes.
- [ ] `npm run build` passes.
- [ ] Static assets copied to `/var/www/rankingpcc/`.
- [ ] Production browser snapshot shows latest PCC results and ranking table columns.
- [ ] DOM inspection confirms ranking table headers exactly match the requested order and removed columns are absent.
- [ ] DOM inspection confirms ticker items have `.slim-meta` for date/format and `.slim-main` for teams/score.
- [ ] A match card expands to calculation details including participation bonus.
- [ ] Git commit created after verification.
