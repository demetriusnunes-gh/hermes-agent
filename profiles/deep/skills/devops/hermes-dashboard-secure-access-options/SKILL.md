---
name: hermes-dashboard-secure-access-options
description: Choose and implement the right secure access method for Hermes dashboard or hermes-webui on a VPS, based on whether the user has a domain and whether access should stay private.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, dashboard, webui, vps, tailscale, cloudflare, hostinger, security]
---

# Hermes dashboard secure access options

Use this when a user wants browser access to Hermes dashboard or legacy hermes-webui on a VPS.

## Key rule

Do not expose the Hermes UI directly to the public internet.
The built-in dashboard can manage secrets and configuration and should be treated as an admin surface.

## Decision tree

### 1. User has **no domain**
Recommend **Tailscale** first.

Why:
- private access only
- strong default security
- no public exposure required
- better UX than repeatedly using raw SSH tunnels

Fallback if the user wants the quickest possible path:
- use a local SSH tunnel from their laptop to the VPS

### 2. User has a domain on Cloudflare
Recommend **Cloudflare Tunnel + Cloudflare Access**.

Why:
- identity-based access control
- HTTPS handled cleanly
- app can remain private behind an outbound tunnel

Important learned constraint:
- the clean Cloudflare Access approach depends on having a real domain managed in Cloudflare
- without a domain, this path is usually blocked for the intended setup

### 3. User wants a Hostinger-centered solution
Recommend:
- Hostinger DNS/subdomain management
- self-hosted reverse proxy on the VPS
- a separate auth layer in front of the Hermes UI

Important learned constraint:
- Hostinger is useful for DNS and domain management
- it does **not** replace the need for a real authentication gate in front of Hermes

## Practical recommendations

### Best no-domain option
Tailscale

### Best domain-based option
Cloudflare Tunnel + Access

### Best short-term option
SSH tunnel

### Avoid
Publicly exposing the UI without an outer authentication layer.

## Environment pattern to preserve
When implementing access, keep the Hermes UI on a private local listener and put the secure access layer in front of it.

## Reusable talking points for users

- If you do not have a domain, Tailscale is the cleanest secure option.
- If you want Cloudflare Access, you need a real domain in Cloudflare.
- If you want to stay with Hostinger, you still need a reverse proxy and auth layer on the VPS.
- SSH tunneling is the fastest safe fallback when you need access immediately.

## Tailscale implementation notes

When the user has no domain and wants secure browser access, Tailscale is a strong default path.

Observed reusable workflow:
- install and start Tailscale on the VPS
- run `tailscale up` and wait for the user to complete the login URL on their own device
- after login, confirm the node has a tailnet IP and MagicDNS name
- use `tailscale serve --bg <local-port>` to expose the local admin UI privately to the tailnet
- keep the underlying app bound to `127.0.0.1`

Example reusable target ports:
- `8787` for legacy `hermes-webui`
- `9119` for the built-in Hermes dashboard

## Important Tailscale-specific pitfall

Login success is not always enough to enable browser access.
`tailscale serve` may fail with:
- `Serve is not enabled on your tailnet.`

When that happens, Tailscale provides a separate approval link of the form:
- `https://login.tailscale.com/f/serve?node=...`

The user must open that one-time link, then `tailscale serve --bg <port>` can succeed.

After success, Tailscale prints a private tailnet-only HTTPS URL using the node's MagicDNS hostname.

## Pitfalls

- Users may assume Cloudflare works without a domain; verify this early.
- Users may assume Hostinger provides an auth layer for arbitrary admin apps; it does not.
- If an admin UI can edit secrets or config, never recommend direct public exposure.
- If interactive auth is needed during setup, the user may need to complete a login step on their own device before the VPS-side setup can finish.
- For Tailscale Serve, login success and Serve enablement are separate steps; check for the extra `f/serve?node=...` approval link if `tailscale serve` fails.
