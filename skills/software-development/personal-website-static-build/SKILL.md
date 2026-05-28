---
name: personal-website-static-build
description: Build a polished static personal/executive website from an interview, using public profile research, design-system templates, local preview, and deployment readiness checks.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [personal-website, static-site, executive-profile, portfolio, web-design]
---

# Personal Website Static Build

Use this when building or revising a personal website, executive profile, advisory landing page, portfolio, or thought-leadership homepage.

## Workflow

1. Interview for positioning before writing code
   - Primary purpose: executive profile, advisory/consulting, writing/blog, portfolio, recruiting, etc.
   - Target audience: recruiters, executives, founders, peers, conference organizers.
   - Tone: authoritative, warm, sharp/opinionated, minimalist, etc.
   - Public credibility: companies, roles, team/org scale, public achievements, writing, talks.
   - Desired CTAs: LinkedIn, contact, book call, writing, speaking invite.
   - Personal/professional balance.

2. Load a visual design skill/template when design matters
   - `impeccable-design` is the best default for revising or polishing an existing personal/executive site: classify brand vs product, diagnose AI-looking patterns, reduce generic cards/pills/gradients, and run `npx --yes impeccable detect` before and after changes.
   - `popular-web-designs` is useful when the user wants a specific known design-system direction.
   - For executive-tech minimalism, Vercel/Linear style can work, but avoid stopping at a generic white/black template. Add an ownable motif, sharper POV copy, layout variation, and specific proof points.

3. Research public profile carefully
   - Prefer Firecrawl first for normal web pages.
   - For LinkedIn, Firecrawl may hang/time out or return little content. If so, use `browser_navigate` and dismiss login/signup modals when possible.
   - Public LinkedIn profile pages can expose useful data without login through the accessibility snapshot / `document.body.innerText`, including location, followers, current company, articles, posts, publications, certifications, and recommendations.
   - Do not invent private details. Use only user-provided information or publicly visible data from tool output.

4. Generate static assets
   - Put simple static sites under the requested web root, commonly `/root/.www` on this VPS.
   - Include at minimum:
     - `index.html`
     - `robots.txt`
     - `sitemap.xml`
   - Add SEO basics: title, description, canonical URL, OpenGraph/Twitter metadata, and schema.org Person JSON-LD for personal sites.

5. Local preview and verification
   - Serve locally with `python3 -m http.server <port>` from the site directory.
   - Use `browser_navigate` to verify the page loads and accessibility snapshot contains key headings/CTAs.
   - Use `browser_vision` if available for visual QA. For design revisions, use it twice: first as a critique to identify hierarchy/layout/color/typography issues, then again after changes to catch regressions such as overly tight headline spacing, unbalanced empty areas, broken image crops, or readability issues.
   - When using Impeccable, run `npx --yes impeccable detect --fast --json <target>` before and after edits; also check for banned copy/style artifacts such as em dashes and pure `#000`/`#fff` when relevant.
   - Validate required strings are present and files exist.

6. Public deployment readiness
   - Check DNS and current service state before claiming it is live:
     - `getent hosts example.com www.example.com`
     - `curl -I https://example.com/` and `curl -I https://www.example.com/`
     - `timeout 10 systemctl is-active nginx caddy apache2` where relevant; wrap systemctl/journalctl calls with `timeout` because they may hang.
   - If no web server is active, report that the static site is built but not publicly served yet.
   - Recommend Caddy for simple static hosting with automatic TLS unless the user already has nginx/apache conventions.

7. Safe temporary third-party redesign previews
   - Use this pattern when the user is doing a favor for someone else or explicitly worries about security risk.
   - Keep it static-only: HTML/CSS/assets. Avoid JavaScript, forms, cookies, analytics, external fonts, hotlinked images, tracking pixels, service workers, and embedded third-party widgets.
   - Preserve requested brand assets by downloading them locally and serving them from the preview path, rather than hotlinking the original site.
   - Do not copy authenticated areas, partner portals, customer data, forms, private dashboards, or credentials. Only use public pages and public company/profile information.
   - Publish under an isolated temporary subdirectory such as `/var/www/<domain>/<project-redesign>/`, preferably with `robots.txt` `Disallow: /`, page-level `<meta name="robots" content="noindex, nofollow, noarchive">`, and HTTP `X-Robots-Tag: noindex, nofollow, noarchive` for the preview path.
   - Add restrictive browser/security posture where possible: no external origins, `Content-Security-Policy` like `default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`, plus existing Caddy headers (`X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`).
   - For Caddy path-specific headers under an existing site, add a matcher before the global header block, e.g. `@preview path /project-redesign*` then `header @preview { X-Robots-Tag "noindex, nofollow, noarchive"; Cache-Control "no-store, no-cache, max-age=0, must-revalidate" }`. Validate and reload Caddy.
   - Verify live headers with `curl -sSIL https://www.<domain>/<path>/` and check body markers for both languages/variants.
   - If the user wants stronger isolation, offer a random unguessable path or HTTP Basic Auth rather than making the preview discoverable.

8. Caddy static-site deployment on this VPS
   - Prefer serving from `/var/www/<domain>` rather than `/root/.www`; Caddy runs as the `caddy` user and `/root` permissions can break access.
   - Copy files with `rsync -a --delete /root/.www/ /var/www/<domain>/`, then `chown -R caddy:caddy /var/www/<domain>` and set dirs 755/files 644.
   - The official Caddy Cloudsmith repo setup can hang/time out here; if that happens, use Ubuntu’s package (`apt-get install -y caddy`) as a reliable fallback.
   - Write `/etc/caddy/Caddyfile` via a small Python script or terminal command; file tools refuse sensitive system paths.
   - Validate and apply config: `caddy fmt --overwrite /etc/caddy/Caddyfile`, `caddy validate --config /etc/caddy/Caddyfile`, then `systemctl enable --now caddy` and `caddy reload --config /etc/caddy/Caddyfile`.
   - Important: after editing the Caddyfile, check logs or reload explicitly; Caddy may still be serving the default `:80` config until reload.
   - With Cloudflare proxied/orange-cloud DNS, Let’s Encrypt `tls-alpn-01` can fail (`Cannot negotiate ALPN protocol "acme-tls/1"`) but Caddy usually falls back to `http-01` successfully if port 80 reaches the origin. Verify final logs show `certificate obtained successfully`.
   - Once certificates are obtained, Cloudflare SSL/TLS should be `Full (strict)`.
   - Verify live deployment with `curl -sSIL https://www.<domain>/`, `curl -sSIL https://<domain>/` for redirects, and a browser load of the public URL.

## GitHub repo creation for existing personal-site files

When the user asks to create a GitHub repo for local personal website files already sitting at `/root/.www`:

1. Identify the actual static-site root before initializing git. On this VPS, the personal site may live directly in `/root/.www` with files like `index.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, favicon files, and `assets/`, while other apps such as `rankingpcc/` are nested under the same directory.
2. Do not recursively add unrelated nested apps/repos, `node_modules`, `.env`, local Caddy PKI, screenshots, or QA artifacts. Add a root `.gitignore` first, for example:

```gitignore
# Other local web apps/repos
rankingpcc/

# Local screenshots / QA artifacts
screenshot-*.png

# OS/editor noise
.DS_Store
*.swp
```

3. Add only the website files explicitly:

```bash
git init -b main
git add .gitignore README.md index.html robots.txt sitemap.xml site.webmanifest \
  favicon.ico favicon.svg favicon-16x16.png favicon-32x32.png favicon-48x48.png favicon-64x64.png \
  apple-touch-icon.png android-chrome-192x192.png android-chrome-512x512.png assets/
git commit -m "Initial personal website"
```

4. Before pushing, scan only the intended files for secrets. Avoid broad scans that include nested apps or `node_modules`, which create noisy false positives.
5. Create the repo with `gh repo create <repo-name> --public --description "..." --source . --remote origin`, then `git push -u origin main`. Use timeouts around `gh` commands on this VPS because repo-listing commands can hang.
6. Verify with `git status --short --branch`, `git log --oneline --decorate -1`, and `gh repo view <owner>/<repo> --json name,url,visibility,defaultBranchRef`.

Known successful case: `/root/.www` was initialized and pushed to `demetriusnunes-gh/demetriusnunes.com` while excluding nested `rankingpcc/` and screenshot artifacts.

## Pitfalls

- Back up live static entrypoints before direct edits, e.g. `cp /var/www/<domain>/index.html /var/www/<domain>/index.html.bak.$(date +%Y%m%d%H%M%S)`, so visual redesigns can be rolled back quickly.
- Do not block indefinitely on Firecrawl/LinkedIn. LinkedIn is often better handled through browser snapshot after dismissing modals.
- Do not describe unverifiable private career history as fact; label inferred positioning as copy or use only user-provided facts.
- Do not say a site is live just because files were written. Verify DNS, HTTPS, and server status.
- Keep CTAs aligned with the user’s stated preference. If they only want LinkedIn, do not add email/contact forms.

## Output Summary Template

After building, summarize:

- Files created/updated
- Main content sections
- Public facts used and source type (user-provided vs public profile)
- Local preview URL
- Verification performed
- Deployment status and next step
