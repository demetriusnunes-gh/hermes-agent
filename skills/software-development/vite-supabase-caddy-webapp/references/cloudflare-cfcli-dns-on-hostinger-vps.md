# Cloudflare DNS via `cfcli` on the Hostinger VPS

Use this reference when a deployed Caddy app needs a new `*.demetriusnunes.com` DNS record and the domain is managed in Cloudflare.

## Proven pattern

1. Install `cfcli` if missing:

```bash
npm install -g cfcli
```

2. Write `/root/.cfcli.yml` with the Cloudflare API token and zone/account details, then lock it down:

```bash
chmod 600 /root/.cfcli.yml
```

3. If Cloudflare rejects requests from the VPS IPv6 path because the token is IP-restricted, force Node to resolve IPv4 first. A durable wrapper pattern is:

```bash
mv /usr/local/bin/cfcli /usr/local/bin/cfcli.real
cat >/usr/local/bin/cfcli <<'EOF'
#!/usr/bin/env bash
export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--dns-result-order=ipv4first"
exec /usr/local/bin/cfcli.real "$@"
EOF
chmod +x /usr/local/bin/cfcli
```

4. Verify zone access before mutating DNS:

```bash
cfcli ls
```

5. Create the DNS-only A record for a Caddy-managed certificate flow:

```bash
cfcli add A <subdomain> <vps_ipv4> --ttl 1 --proxied false
```

If `cfcli` syntax differs by version, inspect `cfcli --help` and use the equivalent create/add-record command. The target state is always:

- Type: `A`
- Name: `<subdomain>` (for example `nova`, not the full domain if the tool expects zone-relative names)
- Value: VPS public IPv4
- Proxy: DNS-only / `proxied=false`

6. Verify public DNS and HTTPS:

```bash
dig +short <subdomain>.demetriusnunes.com A
curl -fsS -D - https://<subdomain>.demetriusnunes.com/ -o /tmp/<subdomain>-index.html | sed -n '1,14p'
```

## Notes

- Prefer DNS-only for simple Caddy deployments so Caddy can obtain and renew its own public ACME cert.
- Keep Cloudflare tokens out of chat replies and do not overwrite existing token-bearing config unless the user explicitly provides a replacement.
- If HTTPS is not ready immediately after DNS creation, check Caddy logs for ACME/DNS errors and retry after propagation rather than changing app files.
