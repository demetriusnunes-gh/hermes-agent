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
6. Browser-check both local preview and the deployed URL, including the new interaction and console errors. For positioned micro-actions on cards, verify bounding boxes programmatically so they do not overlap badges/content:

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
