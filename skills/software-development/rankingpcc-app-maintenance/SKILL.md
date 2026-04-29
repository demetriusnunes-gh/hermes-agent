---
name: rankingpcc-app-maintenance
description: Use when modifying or debugging the RankingPCC Vite/React app on this VPS, especially homepage ticker/trivia, Caddy deployment, tests, and the Sofascore tennis-score integration.
version: 1.0.0
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
- Sofascore parser/client: `/root/.www/rankingpcc/src/sofascoreTennisScores.js` and `src/sofascoreTennisScores.test.js`
- Homepage test: `/root/.www/rankingpcc/src/main.test.jsx`
- Sofascore proxy: `/root/.www/rankingpcc/sofascore-proxy.mjs`
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
   npm test -- --run src/sofascoreTennisScores.test.js
   ```

3. Implement changes in `src/`.

4. Verify targeted tests and build:

   ```bash
   npm test -- --run src/sofascoreTennisScores.test.js src/main.test.jsx
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

## Sofascore Ticker Notes

The ticker currently expects `/api/sofascore-tennis-scoreboard`, parsed by `src/sofascoreTennisScores.js`.

Filtering rules implemented:

- Include finished results only.
- Include ATP/WTA 250+ singles results by default.
- Include lower levels, Challenger, ITF, and doubles only if a Brazilian player is involved.
- Highlight Brazilian players with a flag.
- Bold the winner via `winnerIndex`.
- Keep the ticker compact with horizontal marquee animation and no scrollbars.

Brazilian detection uses `country.alpha2 === 'BR'` plus name hints for known Brazilian players.

## Sofascore 403 Caveat

Sofascore can return HTTP 403/challenge/Forbidden from server-side requests, even with browser-like headers and `curl_cffi`. During the implementation, direct calls to endpoints like:

```text
https://api.sofascore.com/api/v1/sport/tennis/scheduled-tournaments/YYYY-MM-DD/page/1
```

returned 403 from the VPS. The app-side parser/filtering is still useful and covered by tests, but the live proxy may show “Placares Sofascore indisponíveis agora” until the upstream request issue is solved.

When debugging this, do not assume a parser bug if the UI shows unavailable. First check the proxy:

```bash
curl -i http://127.0.0.1:8791/api/sofascore-tennis-scoreboard | head -c 1000
systemctl is-active rankingpcc-sofascore-proxy.service
journalctl -u rankingpcc-sofascore-proxy.service -n 80 --no-pager
```

If Sofascore blocks server-side requests, consider these alternatives:

- Use a browser/client-side fetch only if CORS allows it.
- Find a stable tennis scores API with permissive server access.
- Fall back to ESPN parsing if acceptable to the user.
- Cache manually curated results if the ticker only needs occasional display.

## Caddy and Proxy

The live Caddy route should proxy the app path to the local service:

```caddy
handle /api/sofascore-tennis-scoreboard {
    reverse_proxy 127.0.0.1:8791
    header Cache-Control "no-store, no-cache, max-age=0, must-revalidate"
}
```

After editing `/etc/caddy/Caddyfile`, always validate and reload:

```bash
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

The proxy service is:

```bash
systemctl status rankingpcc-sofascore-proxy.service --no-pager
systemctl restart rankingpcc-sofascore-proxy.service
```

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
