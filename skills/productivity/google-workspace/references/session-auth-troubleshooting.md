# Google Workspace auth troubleshooting (Hermes VPS)

Observed in this session on Ubuntu 24.04 VPS:

## Run the setup script with the Hermes venv Python

The setup script may fail with:

- `ModuleNotFoundError: No module named 'hermes_constants'`
- `externally-managed-environment` / PEP 668 when using system Python for pip installs

Known-good invocation:

```bash
export HOME=/root
export PYTHONPATH=/root/.hermes/hermes-agent:$PYTHONPATH
/root/.hermes/hermes-agent/venv/bin/python /root/.hermes/skills/productivity/google-workspace/scripts/setup.py --auth-url
```

Why this works:

- The Hermes repo module path is added via `PYTHONPATH`
- The Hermes venv already has `googleapiclient`, `google_auth_oauthlib`, and `google_auth_httplib2`
- It avoids Debian/Ubuntu system Python package restrictions

## Re-auth flow

1. Run `--auth-url` and send the printed URL to the user.
2. User authorizes in browser and pastes back either:
   - the raw `code`, or
   - the full redirect URL from `http://localhost:1/?...`
3. Run `--auth-code 'PASTED_URL_OR_CODE'`
4. Verify with `--check`

## Verification

Expected success output:

```text
AUTHENTICATED: Token valid at /root/.hermes/google_token.json
```
