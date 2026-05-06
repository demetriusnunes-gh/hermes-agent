# Model catalog and routing notes

This note captures how Hermes distinguishes configured model state from available model catalogs.

## Configured default
- `hermes config` shows the active default provider/model from `~/.hermes/config.yaml`.
- `model.default` is the session default; `model.provider` selects the backend/provider.
- Example on this VPS:
  - provider: `openai-codex`
  - default model: `gpt-5.4-mini`

## Available models
- `provider_model_ids(provider)` is the canonical lookup used by the model picker.
- For `openai-codex`, Hermes resolves live Codex models from the Codex auth/API when possible, falling back to the in-repo curated list.
- The curated Codex list comes from `hermes_cli/codex_models.py` and includes forward-compatible synthetic models synthesized from templates.

## Practical inspection flow
1. `hermes config` for current default/provider.
2. `hermes model` for the interactive picker.
3. For code-level inspection, check `hermes_cli/models.py` and `hermes_cli/codex_models.py`.

## Pitfall
- Do not assume the default model is the same thing as the available model catalog. Hermes can default to one model while exposing a larger provider catalog for manual selection or routing.
