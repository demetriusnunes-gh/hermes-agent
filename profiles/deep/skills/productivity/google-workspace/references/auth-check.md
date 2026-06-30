# Google Workspace Auth Check

To verify that Google Workspace authentication is current and valid, run:

```bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}" && \
GWORKSPACE_SKILL_DIR="$HERMES_HOME/skills/productivity/google-workspace" && \
PYTHON_BIN="${HERMES_PYTHON:-python3}" && \
[ -x "$HERMES_HOME/hermes-agent/venv/bin/python" ] && PYTHON_BIN="$HERMES_HOME/hermes-agent/venv/bin/python" && \
GSETUP="$PYTHON_BIN $GWORKSPACE_SKILL_DIR/scripts/setup.py" && \
$GSETUP --check
```

Expected output when authenticated:
```
AUTHENTICATED: Token valid at /root/.hermes/google_token.json
```

If the output shows `NOT_AUTHENTICATED`, re-run the OAuth setup steps (see the main SKILL.md for details).

This check uses the same setup script that handles token refresh via the gws bridge.
