# WhatsApp target resolution and bridge fallback

Use this when sending a WhatsApp reminder through Hermes and the normal cross-platform send path does not resolve a target cleanly.

## Observed workflow

1. Check `send_message(action='list')` output first; from shell, the equivalent is `hermes send --list whatsapp --json`.
2. Prefer the exact WhatsApp target label shown there, including any `(dm)` suffix if present.
3. If the cross-platform/CLI send path cannot resolve a stored WhatsApp LID, do not convert it to a guessed phone number. Inspect the cached channel directory or job origin for the raw WhatsApp `chatId`.
4. Verify the WhatsApp bridge is healthy by checking `GET /health` on the local bridge port before attempting a fallback send.
5. Send the message to `POST /send` with `{ chatId, message }`.
6. Confirm success from the HTTP 200 response and `{"success": true, ...}` payload. A scheduler `last_status: ok` is not sufficient if `last_delivery_error` is present.

## Notes

- The bridge accepts raw WhatsApp chat IDs such as `...@lid` or `...@g.us`.
- This fallback is useful for direct DMs when human-friendly name resolution is incomplete.
- Keep the message plain text and short for reminder use cases.
