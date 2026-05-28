---
name: multica-vps-oauth-localhost-tunnel
description: Complete Multica hosted-service login when the CLI runs on a VPS and the OAuth callback incorrectly targets localhost on the remote machine. Use an SSH local port-forward to tunnel the callback from the laptop browser to the waiting CLI process on the VPS.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [multica, oauth, ssh, vps, localhost, callback]
---

# Multica VPS OAuth localhost tunnel

## When to use

Use this when:
- `multica login` is running on a remote VPS or server
- the hosted Multica service (`multica.ai`) opens an auth URL with `cli_callback=http://localhost:<port>/callback`
- the browser used for login is on a different machine from the CLI
- authentication appears stuck because the callback targets localhost

This happens because the Multica CLI starts a temporary local HTTP callback server and, for hosted/public app URLs, keeps the callback host as `localhost`. When the browser is on your laptop and the CLI is on the VPS, the callback must be tunneled back to the VPS.

## Proven workflow

### 1. Start login on the VPS

Run on the VPS:

```bash
multica login
```

Keep this process running. It will print a login URL containing something like:

```text
https://multica.ai/login?cli_callback=http%3A%2F%2Flocalhost%3A35063%2Fcallback&cli_state=...
```

Important: note the exact callback port (for example `35063`).

### 2. Create an SSH local tunnel from the laptop

Run on the laptop/browser machine:

```bash
ssh -L 35063:127.0.0.1:35063 user@your-vps
```

If SSH uses a custom port:

```bash
ssh -p 2222 -L 35063:127.0.0.1:35063 user@your-vps
```

If an SSH config alias exists:

```bash
ssh -L 35063:127.0.0.1:35063 myvps
```

Keep this SSH tunnel open until login finishes.

### 3. Open the Multica login URL in the laptop browser

Open the exact URL printed by `multica login`.

What happens:
1. the browser completes authentication at `multica.ai`
2. Multica redirects to `http://localhost:35063/callback?...`
3. the laptop receives that request
4. SSH forwards it to `127.0.0.1:35063` on the VPS
5. the waiting `multica login` process receives the callback and completes

## Quick explanation to give users

"Run `multica login` on the VPS, keep it open, then from your laptop forward the callback port with `ssh -L <port>:127.0.0.1:<port> user@vps` and open the printed login URL in your laptop browser. The localhost redirect lands on your laptop and the tunnel sends it to the CLI on the VPS."

## Practical tips

- The callback port is random; use the exact port from the printed URL.
- The CLI waits about 5 minutes, so create the tunnel and authenticate promptly.
- Use `tmux` or `screen` on the VPS so the waiting `multica login` process is not lost.
- Do not rewrite the URL except to open it exactly as printed.
- This is specifically for hosted/public Multica. Self-hosted setups may behave differently.

## Troubleshooting

### Browser says localhost refused to connect
- The SSH tunnel is not running, or the wrong port was forwarded.
- Confirm the tunnel uses the exact port from `cli_callback`.
- Confirm `multica login` is still running on the VPS.

### Login still times out
- Restart `multica login` to get a fresh URL and state.
- Recreate the tunnel with the new port.
- Ensure the browser machine is the same one where `localhost:<port>` will open.

### Need the exact command fast
Parse the callback port from the URL and tell the user the precise SSH command:

```text
ssh -L <port>:127.0.0.1:<port> user@your-vps
```

## Why this works

The Multica CLI listens on a temporary local callback server like `127.0.0.1:<port>` on the VPS. The hosted login page redirects the browser to `http://localhost:<port>/callback`. Since the browser runs on the laptop, `localhost` points to the laptop, not the VPS. SSH local port forwarding bridges laptop localhost to VPS localhost so the callback reaches the CLI.
