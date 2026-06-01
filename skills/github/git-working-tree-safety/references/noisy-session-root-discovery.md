# Noisy session-root discovery

Observed in `/root/.hermes`:

- The session root itself can be a Git repository with many runtime artifacts (`state.db`, `sessions/`, `cron/`, `profiles/`, `skills/.usage.json`, caches, locks, etc.).
- A nested repo may also exist below it (for example `/root/.hermes/hermes-agent/`), and the nested repo can be the actual code target for publish work.
- The parent repo and nested repo may each have their own remotes, branches, and `HEAD` states. Do not assume the outer repo is the codebase.

## Verification sequence

1. Check the parent root first:
   ```bash
   git -C /root/.hermes status --porcelain --ignore-submodules=none
   git -C /root/.hermes remote -v
   git -C /root/.hermes branch --show-current
   ```
2. Discover nested repos with `find /root/.hermes -name .git -type d -prune` or equivalent.
3. For any nested repo, inspect it independently:
   ```bash
   git -C /root/.hermes/hermes-agent status --porcelain --ignore-submodules=none
   git -C /root/.hermes/hermes-agent remote -v
   git -C /root/.hermes/hermes-agent branch --show-current
   ```
4. Use `git ls-remote <remote> refs/heads/<branch>` before pushing to confirm the exact publish target exists.

## Pitfall

In a noisy outer checkout, the parent tree can look like the active workspace even when the publish target is the nested repo. Verify ownership before staging or pushing anything.