# Noisy Session-Root Discovery

Use this when the outer workspace root is a Hermes session directory full of runtime artifacts, and the real publishable repository may be nested below it.

## Discovery sequence

1. Inspect the outer root first:
   ```bash
   git -C /root/.hermes status --porcelain --ignore-submodules=none
   git -C /root/.hermes branch --show-current
   git -C /root/.hermes remote -v
   ```
2. Look for nested repositories rather than assuming the outer root is the target. In practice, scan for `.git/` directories and `.git` files that point to gitdirs:
   ```bash
   python3 - <<'PY'
   import os
   root='/root/.hermes'
   items=[]
   for dirpath, dirnames, filenames in os.walk(root):
       if dirpath != root and '.git' in dirnames:
           items.append(dirpath)
           dirnames[:] = []
       if '.git' in filenames:
           items.append(dirpath)
   print('\n'.join(sorted(items)))
   PY
   ```
3. For each candidate repo, inspect it directly:
   ```bash
   git -C <repo> rev-parse --show-toplevel
   git -C <repo> status --porcelain --ignore-submodules=none
   git -C <repo> branch --show-current
   git -C <repo> remote -v
   ```
4. Pick the repo that actually owns the code changes and has the intended publish branch/remote. In `/root/.hermes`-style workspaces, that is often a child repo such as `/root/.hermes/hermes-agent`, not the noisy outer session root.

## Verification cues

- The outer root has many unrelated untracked runtime artifacts.
- The nested repo has a clean working tree or the intended change set.
- The nested repo's remotes point to the repository you actually want to publish.
- If the nested repo contains further submodules or gitlinks, inspect them before staging the parent pointer.

## Why this matters

Avoids committing the outer session scaffolding by accident and makes push target selection explicit before any history is published.