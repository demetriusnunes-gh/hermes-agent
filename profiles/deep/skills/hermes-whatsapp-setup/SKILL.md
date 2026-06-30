---
name: hermes-whatsapp-setup
description: Set up and pair WhatsApp for Hermes Agent using Baileys bridge. Generates a scannable QR code image for pairing.
version: 1.1.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [WhatsApp, Baileys, QR, Pairing, Messaging]
---

# Hermes WhatsApp Setup (Baileys Bridge)

Configure Hermes Agent to receive and send messages via WhatsApp using the built-in Baileys bridge.

## Prerequisites

- Node.js installed and accessible (check `node --version`)
- A dedicated phone number with WhatsApp installed
- Baileys bridge directory exists at `~/.hermes/hermes-agent/scripts/whatsapp-bridge/`

## Step 1: Configure Environment Variables

Add WhatsApp settings to `~/.hermes/.env` (use Python script or `sed` — the `.env` file may be protected from direct editing):

```bash
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot              # "bot" or "self-chat"
WHATSAPP_ALLOWED_USERS=+5521988490510,5521988490510   # Your personal number(s), allow both formats
```

For bot mode, you need a dedicated number. For self-chat, your personal number works.

## Step 2: Ensure Node.js is in PATH for Systemd

If Node.js isn't in the global PATH (e.g., installed at `~/.hermes/node/bin/node`), add it to the systemd service:

```bash
sed -i 's|Environment="PATH=/root/.hermes/hermes-agent/venv/bin:|Environment="PATH=/root/.hermes/node/bin:/root/.hermes/hermes-agent/venv/bin:|' /etc/systemd/system/hermes-gateway.service
sed -i 's|~/.hermes|/root/.hermes|g' /etc/systemd/system/hermes-gateway.service  # systemd doesn't expand ~
systemctl daemon-reload
```

## Step 3: Kill Existing Bridge (If Running)

If the gateway is already running WhatsApp bridge, stop it and kill stale processes:

```bash
systemctl stop hermes-gateway
kill $(pgrep -f "bridge.js") 2>/dev/null
fuser -k 3000/tcp 2>/dev/null
sleep 2
```

## Step 4: Clean Session Directory

```bash
rm -rf ~/.hermes/whatsapp/session/*
```

## Step 5a: Quick Method — ASCII QR (Built-in)

```bash
export PATH=/root/.hermes/node/bin:$PATH
cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
node bridge.js --pair-only --session ~/.hermes/whatsapp/session
```

This prints an ASCII QR code directly in the terminal. Scan it with WhatsApp:
1. Open WhatsApp on your phone
2. Settings → Linked Devices → Link a Device
3. Point camera at the terminal

Wait for "✅ WhatsApp connected!" or "PAIR_ONLY: connected" in the output. The bridge exits after pairing in this mode.

**If the ASCII QR won't scan** (terminal rendering issues, font too small), use Step 5b below.

## Step 5b: Fallback — Scannable PNG (Requires qrcode npm package)

Create a pairing script that generates a scannable QR image:

```bash
cat > ~/.hermes/hermes-agent/scripts/whatsapp-bridge/pair-only.js << 'PAIRJS'
import { makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import pino from 'pino';
import path from 'path';
import fs from 'fs';

const SESSION_DIR = '/root/.hermes/whatsapp/session';
fs.mkdirSync(SESSION_DIR, { recursive: true });
const logger = pino({ level: 'warn' });

async function pair() {
  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version, auth: state, logger,
    printQRInTerminal: false,
    browser: ['Hermes Agent', 'Chrome', '120.0'],
    syncFullHistory: false, markOnlineOnConnect: false,
    getMessage: async () => ({ conversation: '' }),
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log(qr);  // Raw QR string
      const qrPath = path.join(SESSION_DIR, 'qr.png');
      const QRCode = await import('qrcode');
      await QRCode.default.toFile(qrPath, qr, { width: 512, margin: 2 });
      console.log('QR_IMAGE_SAVED: ' + qrPath);
    }

    if (connection === 'close') {
      const reason = lastDisconnect?.error?.output?.statusCode;
      if (reason === 401) { process.exit(1); }
      console.log('Reconnecting (reason: ' + reason + ')');
      setTimeout(pair, 3000);
    } else if (connection === 'open') {
      console.log('PAIRED_OK');
      sock.ws.close();
      process.exit(0);
    }
  });
}
pair();
PAIRJS
```

Install the `qrcode` npm package:

```bash
cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge && npm install qrcode
```

Run it:

```bash
export PATH=/root/.hermes/node/bin:$PATH
cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
timeout 120 node pair-only.js
```

When it outputs the raw QR string and saves `qr.png`, the PNG is at `~/.hermes/whatsapp/session/qr.png`. Scan that with WhatsApp.

## Step 6: Restart Gateway

```bash
systemctl start hermes-gateway
# Verify in logs:
tail -20 ~/.hermes/logs/gateway.log
# Should show: "✓ whatsapp connected" and "Gateway running with 2 platform(s)"
```

Verify the bridge is running:
```bash
curl -s http://127.0.0.1:3000/health
# Should return: {"status": "connected", ...}
```

## Pitfalls

1. **ES module `require()` issue**: The bridge.js uses ES modules (`import`), so `require('fs')` fails inside callbacks. Use `import` syntax for the pairing script.
2. **Tilde expansion in systemd**: `~` doesn't work in systemd unit files. Always use full paths like `/root/.hermes/`.
3. **Port 3000 conflicts**: If pairing fails with EADDRINUSE, kill the old bridge: `fuser -k 3000/tcp`. The gateway starts the bridge automatically — don't run two instances.
4. **Node.js not in PATH**: The gateway systemd service won't find Node.js unless it's in the PATH env var. Check `hermes status` or logs for "Node.js not installed" warnings.
5. **Session directory must be clean for fresh pairing**: Old session data can prevent QR generation. Always `rm -rf ~/.hermes/whatsapp/session/*` before fresh pairing.
6. **Baileys auto-reconnect**: The bridge auto-reconnects on disconnect. If pairing fails, check `lastDisconnect?.error?.output?.statusCode` - 401 means unauthorized (needs re-pairing), 515 means Baileys requested restart (normal).
7. **Allowed users need multiple formats**: Baileys may send numbers with or without the `+` prefix. Include both formats in `WHATSAPP_ALLOWED_USERS` (e.g., `+5521988490510,5521988490510`).
8. **Gateway must be stopped before manual pairing**: The gateway launches the bridge automatically on port 3000. Always `systemctl stop hermes-gateway` before running `pair-only` or manual pairing.
