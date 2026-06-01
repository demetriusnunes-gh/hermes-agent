# Noisy session-root discovery

Use this when working under `~/.hermes` or another long-lived session root that may contain both runtime artifacts and one or more nested git repositories.

## Quick sequence

1. Inspect the outer root first:
   ```bash
   git status --porcelain --ignore-submodules=none
   git remote -v
   git branch --show-current
   ```
2. Enumerate nested repos before staging:
   - look for child directories that are themselves git repositories
   - check each candidate with:
     ```bash
     git -C <candidate> rev-parse --show-toplevel
     git -C <candidate> status --porcelain --ignore-submodules=none
     git -C <candidate> remote -v
     git -C <candidate> branch --show-current
     ```
3. Decide the publish target by ownership, not by path similarity.
   - Treat the noisy outer root as ambient state unless it is the intended repo.
   - Prefer the nested repo as the commit target when the actual code lives there.
4. Verify the exact remote branch before push:
   ```bash
   git -C <repo> ls-remote <remote> refs/heads/<branch>
   git -C <repo> rev-list --left-right --count <remote>/<branch>...HEAD
   ```
5. If a push to the intended remote is rejected as non-fast-forward, fetch and re-check what the remote tip is before retrying.

## Why this matters

The outer session root often contains untracked caches, locks, snapshots, or other runtime files that should not be staged. The real publishable code may be a nested repository with its own branch and remotes, even when the outer checkout looks like the active workspace.
