# Noisy parent-root / nested-repo checkout notes

Observed workflow from a Hermes cron session rooted at `/root/.hermes`:

- the parent root contained many runtime artifacts and was not the code target
- the actual publishable repository lived at `/root/.hermes/hermes-agent`
- the nested repo had its own `.git`, branch, and remotes
- the correct commit target was the nested repo, not the parent runtime workspace

## Verification sequence

1. Inspect parent root status for noise.
2. Identify the nested checkout with `git rev-parse --show-toplevel` in the suspected repo.
3. Check the nested repo's branch and remotes.
4. Stage/commit/push only inside the nested repo unless you explicitly intend to update the parent pointer.

## Why this matters

A parent runtime checkout can contain lots of transient files, while the actual source repo is nested one directory down. Committing from the wrong layer risks dragging in unrelated artifacts or updating the wrong `.git` target.