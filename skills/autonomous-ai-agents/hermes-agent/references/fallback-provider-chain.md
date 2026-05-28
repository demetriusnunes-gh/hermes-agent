# Fallback provider chain

Session-derived note for Hermes configuration and troubleshooting.

## Effective chain rules
- `fallback_providers` is the primary, ordered fallback list.
- Hermes also merges legacy `fallback_model` entries into the effective chain for backward compatibility.
- The effective chain deduplicates routes by provider/model/base_url identity.

## Migration note
When updating an older config:
1. Copy the legacy `fallback_model` entry into `fallback_providers`.
2. Remove `fallback_model` from the config so the written source of truth is unambiguous.
3. Keep the list ordered from preferred to least preferred fallback.

## Example
```yaml
fallback_providers:
- provider: openrouter
  model: openrouter/owl-alpha
- provider: openrouter
  model: nvidia/nemotron-3-super-120b-a12b:free
- provider: openrouter
  model: openai/gpt-oss-120b:free
```

## Practical reminder
If a user says “configure these as fallback models”, treat it as a `fallback_providers` edit unless they explicitly ask to preserve legacy `fallback_model` behavior.
