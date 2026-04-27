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
   - `popular-web-designs` is a good default.
   - For executive-tech minimalism, Vercel/Linear style works well: white/black palette, Geist font, strong typography, restrained cards, sparse color.

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
   - Use `browser_vision` if available for visual QA; if vision fails due environment/tool bug, still verify with browser snapshot and HTTP checks.
   - Validate required strings are present and files exist.

6. Public deployment readiness
   - Check DNS and current service state before claiming it is live:
     - `getent hosts example.com www.example.com`
     - `curl -I https://example.com/` and `curl -I https://www.example.com/`
     - `timeout 10 systemctl is-active nginx caddy apache2` where relevant; wrap systemctl/journalctl calls with `timeout` because they may hang in this environment.
   - If no web server is active, report that the static site is built but not publicly served yet.
   - Recommend Caddy for simple static hosting with automatic TLS unless the user already has nginx/apache conventions.

7. Caddy static-site deployment on this VPS
   - Prefer serving from `/var/www/<domain>` rather than `/root/.www`; Caddy runs as the `caddy` user and `/root` permissions can break access.
   - Copy files with `rsync -a --delete /root/.www/ /var/www/<domain>/`, then `chown -R caddy:caddy /var/www/<domain>` and set dirs 755/files 644.
   - The official Caddy Cloudsmith repo setup can hang/time out here; if that happens, use Ubuntu’s package (`apt-get install -y caddy`) as a reliable fallback.
   - Write `/etc/caddy/Caddyfile` via a small Python script or terminal command; file tools refuse sensitive system paths.
   - Validate and apply config: `caddy fmt --overwrite /etc/caddy/Caddyfile`, `caddy validate --config /etc/caddy/Caddyfile`, then `systemctl enable --now caddy` and `caddy reload --config /etc/caddy/Caddyfile`.
   - Important: after editing the Caddyfile, check logs or reload explicitly; Caddy may still be serving the default `:80` config until reload.
   - With Cloudflare proxied/orange-cloud DNS, Let’s Encrypt `tls-alpn-01` can fail (`Cannot negotiate ALPN protocol "acme-tls/1"`) but Caddy usually falls back to `http-01` successfully if port 80 reaches the origin. Verify final logs show `certificate obtained successfully`.
   - Once certificates are obtained, Cloudflare SSL/TLS should be `Full (strict)`.
   - Verify live deployment with `curl -sSIL https://www.<domain>/`, `curl -sSIL https://<domain>/` for redirects, and a browser load of the public URL.

## Pitfalls

- Do not block indefinitely on Firecrawl/LinkedIn. LinkedIn is often better handled through browser snapshot after dismissing modals.
- Do not describe unverifiable private career history as fact; label inferred positioning as copy or use only public/user-provided facts.
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
