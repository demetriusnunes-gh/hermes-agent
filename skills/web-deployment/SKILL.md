---
name: web-deployment
description: Deploy web files and small self-hosted applications with verified hosting status.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
tags: [web, deployment, hosting, reverse-proxy, dns, validation]
triggers:
  - download files and make them available through a web server
  - build and deploy a small self-hosted web application
  - configure a web service behind a domain or reverse proxy
---

# Web Deployment

Use this umbrella skill for two related delivery classes: publishing downloaded/static files through an existing web server, and delivering small form-backed self-hosted applications. Choose the narrowest applicable procedure below, then verify the result through the serving layer rather than treating copied files or a running process as deployment.

## When to Use

- Use **Static file publishing** for a file that must be downloaded from a URL and served from a web root.
- Use **Small application delivery** for a custom website with routes, form input, local persistence, or a domain/reverse-proxy handoff.
- Do not claim public deployment until the relevant serving path has been tested end to end.

## Prerequisites

- Confirm the target web root, service owner, and existing server before changing files.
- For applications, identify a free loopback port, persistence location, runtime manager, proxy, and requested hostname.
- Treat service changes, proxy reloads, DNS changes, and public writes as authorized side effects.

## Static file publishing

1. Download with redirect following and a deterministic destination filename using `terminal`.
2. Verify the command succeeded, the file is complete, and its size/type are reasonable before publishing it.
3. Copy the file into the intended document root with permissions that allow the web server to read it; do not overwrite an unrelated file without checking ownership.
4. Verify the destination path and file metadata.
5. Test the actual HTTP URL with a HEAD request, following redirects only when expected. Confirm a 200 response or the documented redirect and the expected content type.
6. Report the source URL, destination path, public URL, and verification result. Use absolute paths for the web root.

## Small application delivery

Separate delivery into four independently verifiable layers:

1. **Application** — routes, validation, persistence, and user-facing states.
2. **Runtime** — a repeatable process definition that survives the shell/session ending.
3. **Edge** — reverse-proxy configuration, HTTPS, headers, and routing.
4. **DNS/external reachability** — records and an end-to-end request from outside the host.

### Procedure

1. Inspect the workspace and existing web server before creating files. Check occupied ports, active proxy, and hostname resolution.
2. Create an isolated app and data directory. Keep SQLite outside static assets and document the schema.
3. Build the smallest complete form flow: required fields, explicit yes/no state, bounded numeric input, server-side validation, success/error feedback, and parameterized SQL.
4. Add a private-data-safe health endpoint.
5. Run a local smoke test: GET the page and health endpoint, POST one representative valid form, query the database, test invalid input, then remove only the synthetic row.
6. Inspect the rendered page at desktop and mobile widths when visual quality matters; check focus, selected states, and usability.
7. Define a persistent service (systemd, container, or the host's established process manager) before calling the app hosted.
8. Add the smallest reverse-proxy route for the exact hostname. Validate before reloading; preserve existing sites and do not guess at a conflicting port.
9. If using Cloudflare Tunnel, treat DNS routing and tunnel ingress as separate operations. Configure the exact public hostname and point it directly to the tested app listener unless the proxy path has been verified; avoid redirect loops.
10. Check authoritative DNS before public HTTPS. If DNS is absent, provide the exact record needed and mark public deployment blocked.
11. If DNS is pending but host access exists, finish service, proxy validation, and local host-routed checks; leave certificate acquisition pending.
12. Verify in order: backend health, host-routed request, tunnel ingress/origin if applicable, authoritative DNS, public HTTP/HTTPS, and one real public form submission. Distinguish backend/proxy 404s from tunnel-ingress 404s.

### Content and data rules

- Do not invent event dates, locations, pricing, or other facts; use labeled placeholders.
- When a field changes meaning, update HTML names, server parsing, INSERT statements, fresh schema, and safe existing-database migration together.
- Store only required fields. Use SQL parameters, length limits, numeric bounds, and explicit attending constraints.
- Never leave synthetic test submissions in production.
- Keep a README with the local run command, data location, port, domain prerequisites, and current fields.
- After content or schema edits, restart the persistent service before testing and use a cache-busting browser query when checking public content.

## Hosting status language

- **Built locally:** app files and schema exist; local smoke tests pass.
- **Running locally:** a process answers on loopback; this is not durable hosting.
- **Configured for hosting:** persistent service and proxy are installed and validated; external DNS/HTTPS may still be pending.
- **Deployed:** persistent service, proxy, DNS, public HTTPS, and a public form submission have all been verified.

## Pitfalls

- An incomplete download can look valid; verify exit status, metadata, and HTTP serving.
- A one-off background process is not a production runtime.
- A DNS CNAME does not necessarily configure tunnel ingress.
- An HTTP proxy redirecting a same-host tunnel origin to the public HTTPS URL can loop.
- An existing apex record or proxy IP does not prove the requested subdomain exists.
- An occupied port requires identifying its owner before reuse.
- Authorization failures on service/system changes are blockers; do not bypass them with alternate destructive commands.

## Verification

For static files, confirm the destination exists, the server can read it, and the public URL returns the expected status and content type. For applications, confirm syntax checks, page/form markers, valid and invalid submissions, database cleanup, active service state after restart, exact-host proxy routing, DNS resolution, public HTTPS, and an end-to-end submission. Report completed layers and the single concrete external action still required when deployment is blocked.

See `references/static-file-checklist.md` and `references/application-deployment-checklist.md` for compact checklists and handoff language.
