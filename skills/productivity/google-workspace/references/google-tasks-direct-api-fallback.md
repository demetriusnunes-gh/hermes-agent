# Google Tasks direct API fallback

Observed during a cron maintenance run:

- `gws_bridge.py tasks tasks list` works for listing Google Tasks.
- `gws_bridge.py tasks tasks update` returned `error[api]: Missing task ID` even when `--params` included both `tasklist` and `task`.
- A reliable fallback is to call the Google Tasks REST API directly with a refreshed bearer token from `~/.hermes/google_token.json`.

## Fallback recipe

1. Refresh the Hermes Google token if needed.
2. Use `PATCH https://tasks.googleapis.com/tasks/v1/lists/{tasklist}/tasks/{task}`.
3. Send a minimal JSON body such as:

```json
{"status":"completed","completed":"2026-07-05T15:36:05Z"}
```

4. Verify with a follow-up `tasks.list` call filtered to open tasks.

## Notes

- This is useful when the bridge wrapper's argument handling is stricter than the underlying REST API.
- Keep the task list ID explicit; do not assume the default list when working from cron prompts.
- Preserve the current user-facing output rules from the cron prompt: read-only unless the user explicitly asks to modify tasks.
