# Ambient-noise checkout checklist

Use this when the repo root is also a long-lived agent workspace or profile directory with many unrelated runtime files.

## Signal

You see lots of `??` entries in `git status`, especially directories that are clearly runtime/cache/state artifacts rather than source:
- `cache/`, `state/`, `sessions/`, `audio_cache/`, `cron/output/`, `webui/`, `whatsapp/`
- lock files, DB files, tokens, or generated config snapshots

## Rule

Do not treat a noisy tree as a reason to use `git add -A` blindly.

## Safer flow

1. Inspect the delta first:
   ```bash
   git status --porcelain --ignore-submodules=none
   git diff --name-status
   ```
2. Stage only the intended paths:
   ```bash
   git add <explicit paths>
   ```
3. Re-run status and confirm the noisy artifacts remain untracked.
4. Commit and push only after confirming the index contains just the intended change.

## Pitfall

If the checkout is a Hermes workspace root, unrelated runtime artifacts are often permanent background noise. They should usually stay untracked unless the task explicitly concerns them.
