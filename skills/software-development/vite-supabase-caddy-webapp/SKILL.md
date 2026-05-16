---
name: vite-supabase-caddy-webapp
description: Build and deploy a Vite/React + Supabase web app on the user's Hostinger VPS behind Caddy, including local demo mode, tests, static build, DNS/HTTPS validation, and common VPS pitfalls.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vite, react, supabase, caddy, vps, deployment, webapp]
    related_skills: [writing-plans, test-driven-development, systematic-debugging, code-review]
---

# Vite + Supabase + Caddy Web App on VPS

Use this when building a small/medium public web app for the user with Vite/React, Supabase auth/data, and static hosting on the user's Hostinger VPS via Caddy.

## When to Use

- User asks to create a web app/site hosted on this VPS.
- Stack is or can be Vite/React + Supabase.
- Static frontend can be served by Caddy from `/var/www/<app>`.
- Supabase project may not exist yet, so the app should still be previewable in a local/demo mode.

## Prerequisite Skills

Load and follow:
1. `software-development/writing-plans` for requirements and implementation plan.
2. `software-development/test-driven-development` for parser/ranking/business logic.
3. `software-development/systematic-debugging` when builds, tests, package installs, DNS, or Caddy fail.
4. `software-development/code-review` before finalizing security-sensitive parts.

## Proven Workflow

### Hackathon/source-archive apps

When the user provides a hackathon brief plus a source archive/directory and asks to run it under a subdomain, treat it as both a challenge-scoring task and a deployment task:

- Read the markdown brief first and extract scoring criteria, hidden-test implications, required schemas, and any allowed output enums.
- Run existing tests/builds before edits, then add a small deterministic public scorer if fixtures or answer keys are available.
- Implement challenge logic in pure/testable modules before polishing UI.
- For apps with API/runtime behavior, deploy as a systemd Node service behind Caddy `reverse_proxy` instead of publishing only static `dist/` files.
- Verify local service health, Caddy Host-header routing, and only then public DNS/HTTPS.
- If DNS is missing, finish with the exact Cloudflare `A` record required and avoid saying the public URL is live.

See `references/hackathon-decision-platform.md` for the full captured pattern, including service/Caddy templates and final-response checklist.

### 1. Inspect Environment

```bash
pwd
node --version || true
npm --version || true
systemctl is-active caddy || true
ss -ltnp | sed -n '1,100p'
dig +short <domain> A || true
curl -4 -s https://ifconfig.me || curl -4 -s https://api.ipify.org || true
```

Notes from this VPS:
- Caddy is active and owns ports 80/443.
- Node may be missing or old from apt.
- Current good Node is installed via `n` at `/usr/local/bin/node`.

### 2. Use Modern Node

If Node is missing or Vite/Supabase packages require Node >=20, install/upgrade:

```bash
apt-get update
apt-get install -y nodejs npm
npm install -g n
n 22.13.0
hash -r
node --version
npm --version
```

Pitfall: apt Node on Ubuntu 24.04 is often v18. Modern `vite`, `@vitejs/plugin-react`, `@supabase/supabase-js`, `vitest`, and `jsdom` may require Node 20+ or 22+.

### 3. Create App Skeleton

```bash
mkdir -p /root/.www/<app>
cd /root/.www/<app>
npm init -y
npm install @vitejs/plugin-react vite react react-dom @supabase/supabase-js lucide-react
npm install -D vitest jsdom @testing-library/react @testing-library/jest-dom
```

Use:
- `type: "module"`
- scripts: `dev`, `build`, `preview`, `test`
- `index.html` with `<meta name="robots" content="noindex,nofollow" />` if public-but-not-indexed.
- `public/robots.txt` with `Disallow: /`.

### 4. Supabase-Ready But Demo-Friendly

If the user has not created Supabase yet, implement a store abstraction:

- Supabase store when `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` are present.
- Local/demo store using `localStorage` otherwise.
- Show a visible setup notice when Supabase is not configured.

This lets the user inspect and test the MVP immediately before creating cloud resources.

Files to include:
- `.env.example`
- `supabase/schema.sql`
- `README.md`

### 5. Test Business Logic First

For parsers, rankings, scoring, permissions, or transformations:
1. Write tests in `src/*.test.js` first.
2. Run `npm test` and verify failure/coverage intent.
3. Implement logic.
4. Re-run `npm test`.
5. Run `npm run build`.

If after upgrading Node a test/build errors with missing native binding like:

```text
Cannot find module '@rolldown/binding-linux-x64-gnu'
```

Root cause is npm optional dependency install state. Fix with:

```bash
npm install
npm test
npm run build
```

If still broken, remove and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
```

### 6. Build and Publish Static Files

```bash
npm test
npm run build
install -d -o caddy -g caddy /var/www/<app>
rsync -a --delete dist/ /var/www/<app>/
chown -R caddy:caddy /var/www/<app>
test -f /var/www/<app>/index.html
```

### 7. Caddy Configuration

Preferred persistent route in `/etc/caddy/Caddyfile`:

```caddyfile
<domain> {
	root * /var/www/<app>
	encode zstd gzip
	try_files {path} /index.html
	file_server

	header {
		X-Content-Type-Options nosniff
		Referrer-Policy strict-origin-when-cross-origin
		X-Frame-Options DENY
		X-Robots-Tag "noindex, nofollow"
	}
}
```

Validate/reload:

```bash
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
```

If writing `/etc/caddy/Caddyfile` is blocked by the execution environment, create a complete Caddyfile in the app directory and load it through Caddy's admin API:

```bash
caddy validate --config /root/.www/<app>/Caddyfile --adapter caddyfile
caddy reload --config /root/.www/<app>/Caddyfile --adapter caddyfile
```

Warning: `caddy reload --config /root/.www/<app>/Caddyfile` changes runtime config and autosaves, but may not update `/etc/caddy/Caddyfile`. Persist later if possible, or the route may be lost after service restart depending on how Caddy starts.

### 8. DNS and HTTPS Verification

Before expecting HTTPS to work:

```bash
SERVER_IP=$(curl -4 -s https://ifconfig.me || curl -4 -s https://api.ipify.org)
echo "$SERVER_IP"
dig +short <domain> A
journalctl -u caddy --no-pager -n 100
```

If Caddy logs show:

```text
DNS problem: NXDOMAIN looking up A for <domain>
```

Root cause: DNS record does not exist yet. For Cloudflare-managed domains, create:

- Type: `A`
- Name: subdomain, e.g. `rankingpcc`
- Value: VPS public IPv4
- Proxy: DNS-only is simplest when Caddy should obtain/manage the public certificate directly.

For `demetriusnunes.com` on this Hostinger VPS, there is a proven `cfcli` workflow for creating and verifying these records, including the IPv4 DNS-resolution wrapper needed when the Cloudflare token is IP-restricted and the VPS tries IPv6. See `references/cloudflare-cfcli-dns-on-hostinger-vps.md` before doing manual Cloudflare DNS work or overwriting existing Cloudflare config.

If Cloudflare proxy/orange-cloud is enabled and the browser shows Cloudflare 525 SSL handshake errors, Caddy may not be serving a cert Cloudflare accepts during origin negotiation. For small internal/public apps where Cloudflare terminates public TLS, a proven fix is to use Caddy's internal CA at the origin:

```caddyfile
<domain> {
	tls internal
	root * /var/www/<app>
	encode zstd gzip
	try_files {path} /index.html
	file_server

	header {
		X-Content-Type-Options nosniff
		Referrer-Policy strict-origin-when-cross-origin
		X-Frame-Options DENY
		X-Robots-Tag "noindex, nofollow"
	}
}
```

Validate/reload and verify through Cloudflare:

```bash
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
curl -I https://<domain>
```

Caddy will obtain a public certificate automatically after DNS propagates only when Cloudflare is DNS-only or Caddy can complete ACME validation.

Local route check before DNS exists:

```bash
curl -s -I -H 'Host: <domain>' http://127.0.0.1
```

HTTPS may fail locally until Caddy obtains a real cert, or may require `-k` when using `tls internal`:

```bash
curl -skv --resolve <domain>:443:127.0.0.1 https://<domain>/
```

### 9. Browser Verification

Use Vite preview before finalizing:

```bash
npm run preview -- --port 4174
```

Open `http://127.0.0.1:4174` with browser tools and verify:
- App loads.
- Main navigation works.
- Forms/autocomplete/basic interactions work.
- No obvious console errors.

Kill preview afterward.

### 10. Iterating on Deployed UI/Business Logic

For follow-up tweaks to an already-live app, keep the business logic testable and redeploy the static build:

1. Add/adjust tests for pure helpers before touching UI, e.g. score normalization, winner-side display ordering, Elo/ranking breakdowns, permission rules.
2. Run the specific test and verify it fails for the expected missing behavior.
3. Implement pure functions in the logic module first, then wire React components to them.
4. Prefer deriving display data from canonical stored data rather than mutating stored records. Example patterns:
   - Store match score exactly as entered, but display it normalized through `formatScoreForDisplay(parsed)`.
   - If the winner can be either side, compute `winnerIds`/`loserIds` and render the winner first without changing `teamA`/`teamB` in the database.
   - For per-item “how was this calculated?” UI, expose a pure `calculate...Breakdown(...)` helper that replays historical state up to the selected item, then render the detail panel from that object.
5. Run `npm test && npm run build`.
6. Redeploy the built static files to the actual Caddy-served directory before telling the user it is live. On this VPS, Ranking PCC source lives under `/root/.www/rankingpcc`, but the public site is served from `/var/www/rankingpcc`; building `dist/` alone does not change the live page. Prefer `npx vite build && rsync -a --delete dist/ /var/www/<app>/` for follow-up tweaks, then verify the deployed URL rather than only the source tree.
7. Browser-check both local preview and the deployed URL, including the new interaction and console errors. For positioned micro-actions on cards, verify bounding boxes programmatically so they do not overlap badges/content:

```js
(() => {
  const card = document.querySelector('.match-card');
  const btn = document.querySelector('.detail-button');
  const c = card.getBoundingClientRect();
  const b = btn.getBoundingClientRect();
  return {
    bottom: Math.round(c.bottom - b.bottom),
    right: Math.round(c.right - b.right),
    hasRedundantText: document.body.innerText.includes('Vencedor:'),
  };
})()
```

UI pitfall: absolute-positioned card buttons placed at `top/right` can overlap format/date badges. Prefer bottom-right for secondary detail/help actions and reserve card padding, e.g. `padding: 15px 52px 48px 15px` with `.detail-button { position:absolute; right:12px; bottom:12px; }`. If winner-first ordering already makes the winner obvious, remove redundant text such as “Vencedor: ...” to keep compact cards clean.

Player-profile/card editing pattern used successfully in Ranking PCC:
- Reuse an existing `profile jsonb` column for flexible card fields instead of adding migrations for every stat.
- Add `updatePlayer(id, patch)` to both the Supabase and local/demo stores so the feature remains previewable offline.
- Preserve `profile` and `initialRating` in ranking rows if UI needs avatars/stats on ranking cards; pure ranking functions can carry through non-scoring metadata without affecting score calculations.
- For profile photos, an MVP-safe approach is client-side resize to max ~512px and store a JPEG data URL in `profile.photoUrl`. This avoids Supabase Storage setup for small private apps, but note that it is not ideal for large/public datasets.
- Show initials fallback via a reusable `PlayerAvatar` component so ranking and profile cards render cleanly before photos are uploaded.
- Gate edit buttons by the existing admin check; public users can see cards but cannot mutate profiles.
- For sports/player cards with many attributes, use larger card widths (`repeat(auto-fill,minmax(340px,1fr))`) and render all stat fields as reusable stat-bar rows instead of compact inline text. Pattern: build an ordered `attrs` array from `profile` keys, render `<StatBar label value>`, show `--` for missing values, clamp numeric bar width to 0–99%, and use a horizontal track/fill (`.stat-track` / `.stat-fill`) so the user can visually compare strengths.
- Keep card display fields and editor fields in sync: if the editor captures 11 tennis stats (`primeiro_saque`, `segundo_saque`, `recepcao`, `voleio`, `smash`, `forehand`, `backhand`, `slice`, `drop_shot`, `mental`, `fisico`), the visible card should show all 11, not a hand-picked subset.
- For mobile-friendly sports/player cards, compact vertical space after adding full stat bars: reduce card padding, avatar size, rating size, row padding/gaps, bar height, heading margins, and panel/app padding under a `@media(max-width:760px)` block. Verify with DOM measurements (`.player-card` height/width, stat row count, metric chip count), not just visual intuition.
- Include non-skill body metrics (`idade`, `altura_cm`, `peso_kg`) as compact chips separate from performance attributes. Pattern: render a reusable `Metric` component with label/value/suffix (`anos`, `cm`, `kg`) above stat bars, while keeping bar rows reserved for 0–99 strength-style attributes.
- For ranking-result drill-downs, keep the app single-page and derive views from existing canonical arrays rather than adding routes or database queries. Pattern used successfully: in the ranking component, maintain `selectedPlayerId` and `showAllMatches` React state; compute `sortedMatches = [...matches].sort(sortMatchesDesc)`, `visibleMatches = showAllMatches ? sortedMatches : sortedMatches.slice(0, 10)`, and `selectedPlayerMatches = sortedMatches.filter(m => [...m.teamA, ...m.teamB].includes(selectedPlayerId))`. Render player names as accessible transparent buttons (`aria-label="Ver todos os resultados de ..."`) that open a modal reusing the existing `MatchCard`, including edit/delete and Elo detail behavior. Add a full-width “mais resultados (N)” button below latest results only when there are more than the default slice, and optionally toggle to “menos resultados”. Verify in browser by clicking a player and checking the modal count/text, then expanding latest results and confirming the number of rendered `.match-card` elements and no console errors.
- If the same drill-down must work from player profile/card grids as well as ranking rows, thread `matches`, `playerById`, `onEdit`, and `onDelete` into the `Players` view and reuse the same `PlayerResultsModal` instead of duplicating rendering logic. A robust pattern is to store the selected player object in state (`selectedPlayer`) from the card click, then filter by `selectedPlayer.id`; this avoids depending on a lookup map in views where the card already has the player object. Render shared modals with `createPortal(..., document.body)` rather than inline under card/grid containers; otherwise fixed-position modal backdrops can be centered relative to transformed/contained ancestors or appear out of the viewport after scrolling deep into cards. Verify by checking `.modal-backdrop.parentElement.tagName === 'BODY'` and that `.player-results-modal.getBoundingClientRect()` is fully within `innerWidth/innerHeight`. Verify with an actual browser click on the card name (not only `element.click()` in DevTools/console), because React event handling and stale deployed bundles can make console-click checks misleading during rapid redeploys.
- When the desired interaction changes from “click player name to show games” to “click whole ranking row to open player card”, make the ranking row an accessible full-width `<button className="rank-card rank-card-button">` and show the normal player card in a portal modal (`PlayerCardModal`). Move the games-list affordance inside the card to the stats summary line under the name (`<button className="player-games-link">N jogos · WV/LV · WR%</button>`), not the name itself. If this card modal can open the results modal, close the card modal in the same handler (`setSelectedResultsPlayerId(id); setSelectedCardPlayerId(null);`) to avoid stacked modal backdrops. Watch for inherited `.modal { max-height: 92vh; overflow:auto }` causing unwanted vertical scrollbars when embedding a full player card. If the screenshot/browser check shows an internal scrollbar, make the card modal its own compact presentation instead of relying on the full grid card: set `.player-card-modal { overflow: visible; max-height: none }`, reduce modal-only avatar/rating/padding/heading/stat row sizes, optionally render stat bars in 2 columns, and verify with DOM metrics like `modal.scrollHeight <= modal.clientHeight`, `getComputedStyle(modal).overflowY`, and the modal rect fitting inside `innerHeight`.
- For lightweight client-side routing in a Vite SPA without adding React Router, map view state to History API paths, e.g. `const ROUTES = { home: '/', report: '/reportar', players: '/jogadores', rules: '/calculo' }`, initialize state from `window.location.pathname`, listen to `popstate`, and implement `navigate(view)` with `history.pushState`. Keep Caddy’s `try_files {path} /index.html` so direct deep links like `/jogadores` return the SPA. Browser-verify both direct deep links and nav clicks (`location.pathname`, active tab, console errors).
- For large static content tables such as trivia/facts/tips in a small Vite app, prefer a typed data module plus deterministic tests rather than scattering strings in components. Pattern: create `src/<content>.ts` exporting `{ id, text }[]` and a pure/random helper; if the requested count is large (e.g. 1000), a curated seed list expanded with labeled variants can keep bundle/content maintainable while satisfying exact count and uniqueness. In React, choose the random item with lazy state (`const [fact] = useState(() => getRandom...())`) so it does not change on every re-render. Test both the data contract (`toHaveLength(1000)`, uniqueness, non-empty text) and the UI; for random UI tests, mock `Math.random` with `vi.spyOn(Math, 'random').mockReturnValue(0)` and restore mocks in `afterEach`. Verify with the app’s package-filtered test and build commands.

Live sports ticker / third-party scoreboard pattern used successfully in Ranking PCC:
- For lightweight ATP/WTA live scores without paid API keys, ESPN’s tennis scoreboard page (`https://www.espn.com/tennis/scoreboard`) embeds structured JSON in `window['__espnfitt__']`; the useful data is under `page.content.scoreboard` with `tournaments`, `groupings`, and `competitions`. This is more reliable than scraping visible DOM and avoids needing a browser at runtime.
- Do not fetch ESPN directly from the browser UI; expect CORS/anti-bot/cache issues. Add a same-origin Caddy proxy route before the static SPA handler:

```caddyfile
handle /api/espn-tennis-scoreboard {
	rewrite * /tennis/scoreboard
	reverse_proxy https://www.espn.com {
		header_up Host www.espn.com
		header_up User-Agent "Mozilla/5.0 RankingPCC score ticker"
	}
	header Cache-Control "no-store, no-cache, max-age=0, must-revalidate"
}

handle {
	root * /var/www/<app>
	try_files {path} /index.html
	file_server
}
```

- Parse defensively: find the `window['__espnfitt__']=` marker, slice until `;</script>`, `JSON.parse`, then derive pure `TickerItem` objects from `scoreboard.tournaments[*].groupings[*].competitionIds` and `scoreboard.competitions[id]`.
- ESPN tennis competitors differ for singles vs doubles: singles use `competitor.nm`; doubles use `competitor.rstr[]`. Format doubles as `Player A / Player B` and detect Brazilian involvement by `logo` containing `/bra.png` plus a fallback list of common Brazilian player name hints (e.g. Beatriz Haddad Maia, João Fonseca, Thiago Monteiro, Luisa Stefani, Marcelo Melo, Rafael Matos, Carolina Alves).
- Score formatting comes from each competitor’s `lnescrs`: base set scores are `v`; tiebreak/deciding super-tiebreak values are `t`. Format sets as `6-4` or `7-6(7-4)`. If no score is present, show round/draw/status instead.
- Sort ticker items by Brazilian involvement first, then live (`state === 'in'`), then scheduled, then final/recent by date. Render a graceful loading/error/empty state so ESPN outages do not break the homepage.
- Test parser logic with a small embedded ESPN-like HTML fixture rather than network calls. Also UI-test the ticker by stubbing `fetch('/api/espn-tennis-scoreboard')`; if Supabase is configured in the test environment, the global fetch stub must return JSON-compatible responses for Supabase calls too, or the app can stay stuck loading.
- After changing Caddy proxy routing, validate and reload Caddy, then browser-verify both `/api/espn-tennis-scoreboard` and the deployed home page. On this VPS, Python `Path('/etc/caddy/Caddyfile').write_text(...)` worked when shell `cp`/`install` commands unexpectedly timed out in the tool environment.

Static asset / favicon caching pitfall with Cloudflare in front of Caddy:
- If a newly added `/favicon.ico` or other public asset returns the SPA `index.html` through Cloudflare (`content-type: text/html`, `cf-cache-status: HIT`, old `last-modified`, or the response body starts with `<!doctype html>`), Cloudflare likely cached the SPA fallback from before the file existed. First compare origin vs edge:

```bash
curl --max-time 10 -skI --resolve <domain>:443:127.0.0.1 https://<domain>/favicon.ico
curl --max-time 10 -skI https://<domain>/favicon.ico
curl --max-time 10 -skI 'https://<domain>/favicon.ico?v=<cache-bust>'
```

- If the origin is correct but the bare edge URL is stale, use a cache-busted asset link immediately, e.g. `<link rel="icon" href="/favicon.ico?v=20260428-tennis" sizes="any" />`, rebuild, and redeploy. Then verify the cache-busted URL returns `content-type: image/vnd.microsoft.icon`, `cf-cache-status: BYPASS` or non-HIT, and ICO first bytes `00 00 01 00`.
- Also set Caddy headers to prevent repeat stale SPA fallback caching for HTML and favicon/static assets:

```caddyfile
@html path / /index.html
header @html {
	Cache-Control "no-store, no-cache, max-age=0, must-revalidate"
	CDN-Cache-Control "no-store"
}

header /favicon.ico {
	Cache-Control "no-store, no-cache, max-age=0, must-revalidate"
	CDN-Cache-Control "no-store"
	Content-Type "image/vnd.microsoft.icon"
}
```

- Reload Caddy (`caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy`), rebuild/deploy the Vite app, and browser-verify with:

```js
Promise.all([
  fetch('/favicon.ico?v=<cache-bust>').then(async r => ({
    status: r.status,
    type: r.headers.get('content-type'),
    cache: r.headers.get('cf-cache-status'),
    firstBytes: Array.from(new Uint8Array(await r.arrayBuffer()).slice(0, 4)),
  })),
  document.querySelector('link[rel="icon"]')?.getAttribute('href'),
])
```

- The bare `/favicon.ico` may remain wrong until Cloudflare cache TTL expires or that exact URL is purged in Cloudflare; tell the user this explicitly rather than repeatedly changing origin files.

Batch match/result insertion pattern used successfully in Ranking PCC:
- If the user provides a text batch of results, first parse and echo back a numbered confirmation table before writing to the database. Confirm date format (`DD/MM/YYYY`), whether scores are from Team/Dupla A's perspective, and any name normalization (e.g. `Vinicius -> Vinícius`, `Marcio -> Márcio`). Do not insert until the user explicitly confirms.
- For Supabase linked projects, use `supabase db query --linked` rather than local `supabase db query`, which defaults to `--local` and fails if the local DB is not running. Example: `supabase db query --linked -o json "select id,name from public.players order by name;"`.
- Supabase CLI output with multiple SQL statements may only show the last result set clearly; use separate queries for important counts/verification, or a single final `SELECT` containing all needed values.
- Generate batch SQL from a small Node script that imports the app's real `parseScore` from `src/ranking.js`, maps canonical player names to UUIDs from `public.players`, and emits a `WITH incoming(...) AS (VALUES ...)` insert. This guarantees stored `parsed` JSON matches app logic.
- Store historical match dates at noon BRT (`YYYY-MM-DD 12:00:00-03`) to avoid date shifting across timezones.
- Make the insert idempotent with `WHERE NOT EXISTS` on `(team_a, team_b, score_text, played_at)` so reruns do not duplicate rows. Keep team arrays ordered exactly as confirmed because the score is from Team A's perspective.
- After insertion, verify: total match count, per-date counts if relevant, and recalculated ranking by fetching `players`/`matches` via Supabase JS and running the app's `calculateRanking` locally. If a temporary verifier imports `@supabase/supabase-js`, place/run it inside the app directory so Node can resolve `node_modules`.

Tooling pitfall: when modifying minified/one-line CSS or JS, do not pipe `read_file` output back into a file unless you strip line-number prefixes correctly. A bad append introduced `LINE|` prefixes into CSS and broke Vite/LightningCSS minification with `Unexpected token Delim('.')`. Prefer `patch`, `write_file`, or a small Python script using `pathlib.Path(...).read_text()` / `write_text()` for exact file content.
7. Publish with:

```bash
rsync -a --delete dist/ /var/www/<app>/
chown -R caddy:caddy /var/www/<app>
curl -sI https://<domain> | sed -n '1,12p'
```

## Supabase Auth Setup Pattern

For quick MVP admin tools, email/password auth is often faster and less fragile than Google OAuth. Configure:

- `.env` with `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, and optional app-specific admin email such as `VITE_ADMIN_EMAIL`.
- Supabase Auth Site URL: `https://<domain>`.
- Redirect URLs:
  - `https://<domain>`
  - `http://127.0.0.1:5173`
  - `http://localhost:5173`
- Enable email signups.
- For private MVPs, disable email confirmation temporarily if the user needs immediate access and accepts the lower-friction tradeoff.

App UI pattern:
- Header/login form with email, password, `Entrar`, and `Criar conta com email`.
- Use the authenticated email to check admin permissions through the `admins` table/RLS function.
- Seed the user's email into `admins` during migration when authorized.

## Supabase SQL Pattern

For public-read/admin-write MVPs:
- Tables readable by everyone via RLS `select using (true)`.
- Writes restricted by an `admins` table and `is_admin()` function based on `auth.jwt() ->> 'email'`.
- Include future `user_player_links` table if users will later associate accounts to pre-existing players.

## Final Response Checklist

Report:
- Project path.
- Implemented features.
- Test/build results.
- Public path served from `/var/www/<app>`.
- DNS/HTTPS status and exact DNS record needed if not live.
- Supabase setup steps: `.env`, SQL file, OAuth config.
- Any non-persistent Caddy caveat if runtime reload was used instead of editing `/etc/caddy/Caddyfile`.
