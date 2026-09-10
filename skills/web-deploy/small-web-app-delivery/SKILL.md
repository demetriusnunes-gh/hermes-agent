---
name: small-web-app-delivery
description: Build, validate, and hand off small self-hosted web apps with local persistence, reverse-proxy routing, and honest deployment status.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [web, deployment, sqlite, reverse-proxy, dns, validation]
platforms: [linux]
triggers:
  - build a small website with a local database
  - create an RSVP or registration web app
  - deploy a self-hosted web app behind a domain
  - host a local web service with Caddy or nginx
---

# Small Web App Delivery

Use this skill for small custom websites that collect form data, persist it locally, and may need to be exposed through an existing server and domain. The goal is a working artifact plus a verifiable deployment handoff—not merely attractive HTML.

## Delivery contract

Separate the work into four independently verifiable layers:

1. **Application** — routes, validation, persistence, user-facing states.
2. **Runtime** — a repeatable process definition that survives the shell/session ending.
3. **Edge** — reverse-proxy configuration, HTTPS, headers, and routing.
4. **DNS/external reachability** — domain records and an end-to-end request from outside the host.

Never report the domain as deployed unless the runtime, edge, DNS, and external HTTPS request have all been verified. If only the application is complete, say that explicitly.

## Recommended implementation sequence

1. Inspect the workspace and existing web server before creating files. Check which ports are already occupied, which reverse proxy is active, and whether the requested hostname resolves.
2. Create an isolated app directory with a clear data directory. Keep the SQLite file out of static assets and document the schema.
3. Build the smallest complete form flow: required fields, explicit yes/no state, bounded numeric input, server-side validation, success/error feedback, and parameterized SQL.
4. Add a health endpoint that does not expose private data. Use it for local and proxy checks.
5. Run a real local smoke test: GET the page, GET the health endpoint, POST a representative valid form, query the database, then remove only the synthetic test row.
6. Verify the rendered page in a browser at desktop and mobile widths when visual quality matters. Check focus/selected states and form usability rather than relying only on source inspection.
7. Define a persistent service (systemd, container, or the host's established process manager) before claiming the app is hosted. Avoid leaving a one-off background process as the production runtime.
8. Add the smallest reverse-proxy route for the exact hostname. Validate the proxy configuration before reloading it. Preserve existing sites and do not guess at a conflicting port.
9. If using Cloudflare Tunnel, treat DNS routing and tunnel ingress as separate operations: `cloudflared tunnel route dns` creates the CNAME but does not necessarily configure the tunnel's public-hostname origin. Inspect or configure the tunnel ingress for the exact hostname before claiming it is routed. For a tunnel on the same host, point the public hostname directly to the app's HTTP listener (for example `http://127.0.0.1:8797`) unless the proxy path has been tested; pointing the tunnel at an HTTP reverse proxy that redirects to the public HTTPS URL can create a redirect loop.
10. Check DNS resolution before requesting or testing public HTTPS. If DNS is absent, provide the exact record needed and mark public deployment as blocked. For Cloudflare-managed zones, inspect the authoritative nameservers and current public A/AAAA records; give the user the exact CNAME target, proxy mode, and hostname rather than claiming the subdomain is live. Do not assume an existing apex record or Cloudflare proxy IP means the requested subdomain exists.
11. If DNS is missing but host access is available, still finish the server-side layers: install/enable the persistent service, add and validate the exact Caddy route, reload the proxy, and verify the backend plus local host-routed HTTP response. Keep certificate acquisition pending until public DNS exists; Caddy will retry ACME automatically after propagation.
12. Verify in this order: backend health, proxy request with the hostname, tunnel ingress/origin response, authoritative DNS, public HTTP redirect/HTTPS, then a real form submission through the public URL. Distinguish a backend/proxy 404 from a tunnel-ingress 404 by comparing the local response and the public response. Record the database result or a non-sensitive count. If DNS, tunnel credentials, or dashboard access prevents the last steps, report completed layers and the single concrete external action still required.

## Content and data rules

- Do not invent event date, location, pricing, or other factual content the user did not provide. Use clearly labeled placeholders.
- For Brazilian event/RSVP pages, use `pt-BR` for visible copy and document metadata when requested; preserve explicit brand or event names exactly, and remove replaced English copy rather than leaving mixed-language remnants.
- When a form field changes meaning (for example, email to WhatsApp), change the HTML name, server parsing, INSERT statement, schema for fresh databases, and a safe migration for existing SQLite databases together.
- Store only the fields required by the requested flow. Use SQL parameters, length limits, numeric bounds, and an explicit attending constraint.
- Do not leave synthetic test submissions in the production database.
- Treat system service files, reverse-proxy reloads, DNS changes, and public writes as side effects requiring appropriate authorization. If an environment approval blocks them, stop and report the exact remaining step rather than retrying through a different command.
- Keep deployment instructions in a README with the local run command, data location, port, domain prerequisites, and current stored-field names.

## Content-change verification

After content or schema edits, restart the persistent service before testing; source-only checks can pass while the running process still serves old content. Run a local HTML assertion for every requested addition and removal, exercise one representative form submission, verify the migrated field in SQLite, delete only the synthetic row, then check the public page in a browser with a cache-busting query parameter.

## Verification checklist

- `python -m py_compile` or the framework's syntax check passes.
- Local page contains the event title and form controls.
- Valid POST returns a success state and creates one SQLite row.
- Invalid/missing input does not create a row.
- Test data is removed after the smoke test.
- Service manager reports the process active after a restart.
- Reverse proxy validates and routes the exact host.
- DNS resolves to the intended server.
- Public HTTPS request succeeds and the form submission reaches the intended SQLite database.

See `references/deployment-checklist.md` for the compact handoff checklist and status language.