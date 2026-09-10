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

The production ranking now uses pure doubles Elo only:

- Each player starts at 1000 unless `initialRating` is set.
- Team rating is the mean of the two player ratings.
- Expected score uses standard Elo: `1 / (1 + 10 ** ((oppRating - rating) / 400))`.
- K by parsed format: short set `10`, single set `20`, best-of-3 with super tiebreak `40`, full best-of-3 `60`.
- Two-set reports are intentionally treated as `best_of_3_super` for K weighting.
- No game-margin multiplier: a win/loss delta is based only on K and expected probability.
- No participation bonus or inactivity penalty. Inactive players stay unchanged; active players receive only their Elo delta.
- Track `streak` as positive consecutive wins and negative consecutive losses, `longestWinningStreak` as the largest positive win streak reached by each player, plus `lastMatch` date.

## Current UX Notes

- The homepage should show latest club ranking results as a slim, horizontally animated ticker, not an external TNNS/Sofascore live feed.
- Keep a “Resultados” page/view for all reported club results.
- Do not reintroduce the tennis curiosities widget unless explicitly asked.
- Ranking should be tabular and include columns in this order: position, player, Rating (pure Elo), matches, W-L, win %, **Games Δ** (game differential; do not label it “Saldo”), Elo Δ, and streak. Do not show `Perf` or `Atividade` columns. The Streak cell should display current streak plus longest winning streak as `+3 (5)` / `-1 (5)`; sorting should remain by current `streak`, not the parenthesized historical max. Every ranking table column should be sortable ascending/descending via its header. Do not include a “Último jogo” column on the main ranking table unless explicitly requested.
- Players with fewer than 20 matches are outside the main ranking and must appear after a `Convidados` divider at the end of the table.
- Every visible player name should navigate to `/jogador/:id`. The player profile page must include summary stats, all matches for that player, filtered individual/doubles Head 2 Head, and a filtered Elo evolution chart. In the profile match list, cards must be clearly marked from that player's perspective with green `Vitória` / red `Derrota` treatment. Profile Elo chart points must be clickable and open the same match-detail modal as the global Evolução Elo page.
- Match result cards should be clickable and expand calculation details with pure Elo before/after deltas only; player names inside result cards should navigate to player profiles without toggling the match detail. Do not show margin multiplier, participation bonus, or inactivity penalty.
- Homepage ticker result pills should be compact two-line items: first line date + format, second line winner/loser/score. Use structural wrappers such as `.slim-meta` and `.slim-main` so tests and responsive CSS can verify the line split.
- User-facing best-of-3 labels should be simplified: both `best_of_3_super` and `best_of_3_full` display as “melhor de 3” even though K weighting still distinguishes them internally.
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
5. Deploy with the app script so stale hashed assets are removed before copying the new build:
   ```bash
   npm run deploy
   ```
   If deploying manually, remove stale assets first: `rm -rf /var/www/rankingpcc/assets && cp -a dist/. /var/www/rankingpcc/`. Old CSS assets can preserve obsolete rules such as hidden player-name buttons for browsers with cached HTML.
6. Browser-verify `https://rankingpcc.demetriusnunes.com` for expected text and clickable calculation details.
7. Commit the app changes so the user has an easy revert point.

## Pitfalls

- Do not trust stored `match.parsed` when changing parsing/formats; recompute from `scoreText` so old saved matches follow current rules.
- Production does not change after `npm run build` until `dist/` is copied to `/var/www/rankingpcc/`.
- Keep unrelated Caddy/proxy changes out of formula/UI commits unless the user asked for routing changes.
- If removing obsolete widgets, remove dead imports/files/tests or update the test suite so stale feed/trivia artifacts do not keep passing accidentally.
- Browser snapshots may show only compact content at first; use DOM inspection or click a match card to confirm `.match-breakdown` text shows pure Elo deltas only.
- Player profile links use `.player-name-button`/`.player-card-name-button`; never hide these globally with `display:none`, because match cards and ticker will degrade to `/ vs /` with missing names.
- Mobile result-card CSS must not use broad descendant selectors like `.teams span { display:none }`; it hides nested `.team-names` spans and removes player names only on mobile. Give the direct `vs` separator its own `.match-vs` class and hide `.teams > .match-vs` instead. Regression tests should assert the card structure keeps `.team-names` separate from `.match-vs`.
- When a UI fixture adds multiple match cards, existing `getByText(/editar|excluir/)` tests may become ambiguous; use `getAllByText(...).length` or scope queries to a specific page/card.

## Verification Checklist

- [ ] `npm test` passes.
- [ ] `npm run build` passes.
- [ ] Static assets copied to `/var/www/rankingpcc/`.
- [ ] Production browser snapshot shows latest PCC results and ranking table columns.
- [ ] DOM inspection confirms ranking table headers exactly match the requested order, `Perf`/`Atividade` are absent, `Convidados` appears after qualified players, and header buttons sort text/numeric columns ascending/descending.
- [ ] DOM inspection confirms ticker items have `.slim-meta` for date/format and `.slim-main` for teams/score.
- [ ] A match card expands to calculation details with pure Elo deltas only.
- [ ] Git commit created after verification.
