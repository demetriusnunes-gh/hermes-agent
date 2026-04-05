Running on a Hostinger VPS.
§
- VPS provider: Hostinger
- Telegram: bot @roger_hermes1_bot, user ID 8742978410, connected and working
- Preferences: values security, reliability, and proactive system hardening
- Wants: WhatsApp integration (Baileys), Google Workspace tools (Gmail, Calendar, Drive, etc.)
- Default model: openrouter/qwen3.6-plus-preview:free
- System: Ubuntu 24.04 VPS, 8GB RAM, 96GB disk, 8GB swap, gateway runs via systemd
§
Relevant email contacts:
- Wife: Fernanda Hamacher (fhamacher@gmail.com)
- Kids' school: Eleva
- Government: .gov.br domains, official-sounding notices
Email monitoring: checks every 120min, alerts via Telegram.
§
Environment: Hostinger VPS (Ubuntu 24.04). Hermes Gateway runs as systemd service 'hermes-gateway.service' with auto-restart. Node.js (v22) installed at /root/.hermes/node/bin. 8GB swap enabled at /swapfile. Log rotation configured for ~/.hermes/logs/. Email: Himalaya CLI configured for Gmail with App Password (stored in ~/.gmail-app-password). WhatsApp: Baileys bridge on port 3000, paired with +5521990718408. Telegram: Bot @roger_hermes1_bot configured.
§
WEB RESEARCH default: Firecrawl local (Docker, port 3002) — use FIRST for any web research/research/look up/scrape tasks. POST http://localhost:3002/v1/scrape with {"url":"...", "formats":["markdown"], "onlyMainContent":true}. Only fall back to browser_navigate if Firecrawl is down, needs interactive login, or returns garbage.
§
Zapier MCP URL with token: https://mcp.zapier.com/api/v1/connect?token=ZWZhNDQ5NGYtMmIxNC00NTNkLTgwZTMtM2MzOGNiNGMxODg2OlQxKys3T2NzQVh3c2l4ZVBCZkZxK3BnQ0JwbzYwTktQaFNEbW1LV0w3SXc9 — DO NOT OVERWRITE.
§
RECURRING BUG: mcp_servers block in config.yaml gets corrupted (indented 2 spaces too deep, becomes child of _config_version). Fix: dedent mcp_servers→col 0, zapier→2sp, url/timeout/connect_timeout→4sp.
§
BOUNTYBOOK: Wallet 0x3D0d25a104CDB2388511a35F8FCC6c1E9C786DFb (MetaMask) stored at ~/.bountybook-wallet (600). Auth via wallet-signature nonce. Earnings in USDC on Base. Note: Some jobs (e.g., flatten_dict) have buggy verifiers failing on ipfs_fetch; prefer jobs that accept raw outputData or check verifier history first.