# Hackathon Decision Platform Deployment Pattern

Use this reference when the user provides a hackathon brief (`.md`) plus source archive/directory and wants it running under a VPS subdomain.

## Session pattern captured

A Nova/Opex_BR hackathon app was delivered as a source directory with a markdown challenge brief. The winning workflow was:

1. Read the challenge brief before coding; identify scoring dimensions, hidden-test expectations, and any required output schema.
2. Inspect the source tree and package scripts; install with `npm ci` when a lockfile exists.
3. Run the existing tests and any public fixture/scoring harness before changing code.
4. Implement the core challenge logic as a pure/testable engine module first, then wire it to API/UI.
5. If the challenge has public fixtures or an answer key, add a local scorer script (for example `scripts/score-public.js`) and an npm script such as `score:public` so future iterations can quantify progress.
6. Treat hidden evidence/adversarial text as untrusted input: cite evidence, clamp outputs to allowed actions/enums, avoid leaking internal-only data into customer-facing messages, and surface guardrails/policy-version metadata.
7. Build and deploy the app as a long-running local service when it includes API routes/runtime logic; do not assume a static `/var/www/<app>` publish is enough.
8. Put Caddy in front as a reverse proxy to the local app port, then verify local health with both the service port and the Caddy Host header before waiting on public DNS.
9. If DNS is missing, finish with the exact Cloudflare `A` record needed and the current VPS IPv4.

## Service + Caddy shape

For Vite apps with API/runtime behavior that cannot be served as static files only:

```ini
# /etc/systemd/system/<app>.service
[Unit]
Description=<app> web service
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/source
Environment=NODE_ENV=production
Environment=PORT=<port>
ExecStart=/usr/local/bin/npm start
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```caddyfile
<subdomain> {
    encode zstd gzip
    reverse_proxy 127.0.0.1:<port>
}
```

Verification commands:

```bash
npm ci
npm test
npm run score:public   # if added
npm run build
systemctl daemon-reload
systemctl enable --now <app>.service
systemctl status <app>.service --no-pager
curl -s http://127.0.0.1:<port>/api/health
curl -sI -H 'Host: <subdomain>' http://127.0.0.1
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy
dig +short <subdomain> A
```

## Final response pattern

For hackathon deployments, be explicit and concise:

- project path
- plan file path if created
- core challenge logic changed
- scorer/test/build commands and exact results
- systemd service name and port
- Caddy route/subdomain
- whether public HTTPS is live or blocked by DNS
- exact DNS record if blocked

Avoid claiming the public URL is live until DNS resolves and HTTPS has been verified.