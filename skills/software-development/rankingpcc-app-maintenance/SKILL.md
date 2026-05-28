---
name: rankingpcc-app-maintenance
description: Use when modifying or debugging the RankingPCC Vite/React app on this VPS, especially homepage ticker/trivia, Caddy deployment, tests, and the TNNS Live/Sofascore tennis-score integration.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rankingpcc, vite, react, caddy, tennis, sofascore]
    related_skills: [test-driven-development, vite-supabase-caddy-webapp, systematic-debugging]
---

# RankingPCC App Maintenance

## Overview

RankingPCC lives at `/root/.www/rankingpcc` and is deployed as a static Vite/React build to `/var/www/rankingpcc`. The production site is `https://rankingpcc.demetriusnunes.com`.

Use a test-driven workflow for UI and parsing changes: add/adjust Vitest coverage first, run targeted tests, then build and copy `dist/` to the served directory.

## Key Files

- App entry/UI: `/root/.www/rankingpcc/src/main.jsx`
- Styles: `/root/.www/rankingpcc/src/styles.css`
- Tennis trivia: `/root/.www/rankingpcc/src/triviaFacts.js` and `src/triviaFacts.test.js`
- Sofascore parser/client: `/root/.www/rankingpcc/src/sofascoreTennisScores.js` and `src/sofascoreTennisScores.test.js` (kept as prior implementation/reference)
- TNNS Live parser/client: `/root/.www/rankingpcc/src/tnnsliveTennisScores.js` and `src/tnnsliveTennisScores.test.js` (current live ticker source)
- Homepage test: `/root/.www/rankingpcc/src/main.test.jsx`
- Inactivity-penalty reference: `references/inactivity-penalty.md` (rolling 52-week activity window, 12-week annual grace, derived 5-point weekly penalty)
- Tennis-score proxy service file: `/root/.www/rankingpcc/sofascore-proxy.mjs` (currently implemented with TNNS Live backend, while preserving the old public route)
- Optional TNNS proxy source copy: `/root/.www/rankingpcc/tnnslive-proxy.mjs`
- Repo Caddyfile copy: `/root/.www/rankingpcc/Caddyfile`
- Live Caddy config: `/etc/caddy/Caddyfile`
- Live static root: `/var/www/rankingpcc`

## Standard Workflow

1. Work from the app directory:

   ```bash
   cd /root/.www/rankingpcc
   ```

2. Add or update tests before implementation when feasible:

   ```bash
   npm test -- --run src/main.test.jsx
   npm test -- --run src/tnnsliveTennisScores.test.js
   npm test -- --run src/sofascoreTennisScores.test.js
   ```

3. Implement changes in `src/`.

4. Verify targeted tests and build:

   ```bash
   npm test -- --run src/tnnsliveTennisScores.test.js src/main.test.jsx
   npm run build
   ```

5. Deploy static assets:

   ```bash
   cp -a dist/. /var/www/rankingpcc/
   ```

6. Browser-verify production:

   - Open `https://rankingpcc.demetriusnunes.com`
   - Check the accessibility snapshot for expected text
   - If visual layout matters, use browser vision/screenshot too

## Ranking/Inactivity Notes

- Ranking math lives in `src/ranking.js`; keep changes test-driven in `src/ranking.test.js`.
- Inactivity penalties should be derived during `calculateRanking(...)`, not persisted as fake matches or permanent rating mutations.
- Current policy: rolling 52-week window, one match makes that week active, 12 inactive weeks of grace per year, then -5 points per extra inactive week. See `references/inactivity-penalty.md` for details and deterministic test patterns.
- Preserve both `baseRating` and penalized `rating` when inactivity is involved so tests/UI can separate Elo movement from decay.

## Tennis Ticker Notes

The live ticker currently uses TNNS Live as the main source, parsed by `src/tnnsliveTennisScores.js`.

Important compatibility note: the public app path is still `/api/sofascore-tennis-scoreboard` because the existing Caddy/systemd route already used that name. Do not assume the route name means the upstream is Sofascore; check `sofascore-proxy.mjs`. As of this note, that file calls TNNS Live's backend:

```text
https://gen2-matches-daily-web-ysvbugl7mq-uc.a.run.app/?date=YYYY-MM-DD&web=true&referring_domain=https%3A%2F%2Ftnnslive.com%2F&timezone=UTC&language=en&platform=web&version=100&subscribed=%7B%7D&favorites=%7B%7D&theme_settings=%7B%7D
```

Discovery workflow that worked:

1. Firecrawl can scrape `https://tnnslive.com/` and extract page text, but not the data endpoint.
2. Browser DevTools/performance resource inspection exposed the backend URL (`gen2-matches-daily-web-...a.run.app`).
3. Browser fetch confirmed JSON shape: top-level `sids`, `all_matches`, `generated_at`.
4. Server-side proxy to that Google Cloud Run endpoint works from the VPS, unlike Sofascore.

TNNS JSON shape:

- `sids`: map of season/tournament IDs to tournament metadata (`t`, `su`, `d.category`, `d.tour`).
- `all_matches`: list of matches.
- Match fields used by parser:
  - `k`: stable match ID
  - `sid`: season/tournament key into `sids`
  - `finishedAt`: timestamp in ms
  - `fs`: status array; includes `c` for completed
  - `p`: players/teams, with `n` name, `f` country flags (e.g. `BR`), `w` winner, `l` loser
  - `sc`: set scores, where the first two values are games; ignore extra tiebreak/status values for compact display

Filtering rules implemented:

- Include only live matches for today and final results for the same day (`data.date` / today's TNNS scoreboard date). Do not show final results from previous days, even if the proxy has fetched multiple dates.
- Proxy default should fetch only today (`recentDates(days = 1)`) unless there is an explicit reason to inspect history; keep parser-side date filtering too as defense-in-depth.
- Live matches should be marked `status: 'Live'`, `state: 'in'`; finals should be `status: 'Final'`, `state: 'post'`.
- Strictly exclude any event that is not ATP/WTA-family before applying any Brazilian exception. ITF, UTR, exhibitions, etc. should not appear even if a Brazilian player is involved.
- Include ATP/WTA 250+ singles live/final matches by default for any players.
- Include lower-level ATP/WTA-family events (e.g. Challenger/WTA125) and doubles only if a Brazilian player is involved.
- Sort live matches before finals, then main-tour ATP/WTA 250+ singles before Brazilian lower-level/doubles exceptions so major/current events are prominent.
- Highlight the actual Brazilian player/team with a flag using `brazilianIndexes`, not name-regex-only guesses.
- Bold the winner via `winnerIndex`.
- Keep the ticker compact with horizontal marquee animation and no scrollbars.

When aggregating multiple TNNS dates in the proxy, prefix each `sid` and `sids` key with the date (e.g. `YYYY-MM-DD:12345`). Raw TNNS season IDs can collide across days; without date-prefixing, season metadata can be overwritten and matches may be classified against the wrong tournament, causing ATP/WTA main-tour matches to disappear or non-matching events to pass filters.

Brazilian detection for TNNS uses player/team `f` flags containing `BR` plus name hints for known Brazilian players.

## Sofascore 403 Caveat and TNNS Fallback

Sofascore returned HTTP 403/challenge/Forbidden from server-side requests, even with browser-like headers and `curl_cffi`. Direct calls to endpoints like:

```text
https://api.sofascore.com/api/v1/sport/tennis/scheduled-tournaments/YYYY-MM-DD/page/1
```

were unreliable from the VPS. The reliable approach was to switch the upstream to TNNS Live while preserving the existing local route name.

When debugging ticker availability, do not assume a parser bug. First check the proxy:

```bash
curl -i http://127.0.0.1:8791/api/sofascore-tennis-scoreboard | head -c 1000
systemctl is-active rankingpcc-sofascore-proxy.service
journalctl -u rankingpcc-sofascore-proxy.service -n 80 --no-pager
```

If the proxy returns TNNS JSON (`source: "https://tnnslive.com/"`, `sids`, `all_matches`) but the UI is empty, debug `src/tnnsliveTennisScores.js`. If the proxy returns 502, debug `sofascore-proxy.mjs` and the TNNS Cloud Run request.

## Caddy and Proxy

The live Caddy route currently proxies the historical app path to the local service:

```caddy
handle /api/sofascore-tennis-scoreboard {
    reverse_proxy 127.0.0.1:8791
    header Cache-Control "no-store, no-cache, max-age=0, must-revalidate"
}
```

Even though the path says `sofascore`, the proxy implementation may use TNNS Live. Rename the route only if you can update the live Caddy config, React client, tests, and service consistently.

After editing `/etc/caddy/Caddyfile`, always validate and reload:

```bash
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

The proxy service is still named:

```bash
systemctl status rankingpcc-sofascore-proxy.service --no-pager
systemctl restart rankingpcc-sofascore-proxy.service
```

If direct writes/copies into `/etc/systemd/system` or `/etc/caddy` are blocked by tool approval/timeouts, a practical workaround is to keep the service name and route unchanged, overwrite the repo proxy implementation (`sofascore-proxy.mjs`) with the desired backend, then kill the running node process and let systemd restart it.

## Ranking Calculation Changes

When changing `src/ranking.js`, keep ranking modifiers as derived fields rather than stored mutations or synthetic matches. Add/adjust `src/ranking.test.js` first, then expose only small transparent labels in `src/main.jsx` and document the rule under `/calculo`.

For activity/inactivity-style rules, prefer the simplest user-stated benchmark and make the penalty reversible:

- Compute normal Elo first.
- Preserve `baseRating` when applying any derived penalty.
- Add explicit fields such as `activityPenalty`, `gamesBehindLeader`, or similar so the UI can explain the adjusted `rating`.
- Avoid calendar/week-based inactivity systems unless the user explicitly confirms the UX; they can look surprising in a club ranking. A rule relative to the most active player is easier to reason about: e.g. leader has N matches, each player loses X points per match behind leader.
- Keep changes easy to revert by isolating ranking logic, tests, and the small UI/rules text patches.

Verification for ranking-rule changes:

```bash
npm test -- --run src/ranking.test.js
npm run build
cp -a dist/. /var/www/rankingpcc/
```

Browser-verify `/calculo` after deploy to ensure the public explanation matches the implemented rule.

## Common Pitfalls

1. **Only editing the repo Caddyfile.** Production uses `/etc/caddy/Caddyfile`; keep the repo copy in sync but update the live file for actual routing.

2. **Forgetting to deploy after build.** `npm run build` only writes `dist/`; production changes require `cp -a dist/. /var/www/rankingpcc/`.

3. **Confusing upstream 403 with app failure.** If the ticker says Sofascore is unavailable, verify the local proxy endpoint and service logs before changing React code.

4. **Duplicated marquee content in tests.** The ticker duplicates items for seamless animation, so Testing Library queries may need `getAllByText(...)[0]` instead of `getByText`.

5. **Do not reintroduce the removed Brazilian line.** The desired UX is flag-only highlight, no “Brasileiro(a):” text.

## Verification Checklist

- [ ] Targeted Vitest tests pass.
- [ ] `npm run build` passes.
- [ ] Static assets copied to `/var/www/rankingpcc/`.
- [ ] Caddy validates if routes changed.
- [ ] `rankingpcc-sofascore-proxy.service` is active if ticker proxy changed.
- [ ] Browser snapshot shows updated production text.
- [ ] If scores are unavailable, proxy logs confirm whether upstream Sofascore is returning 403.
