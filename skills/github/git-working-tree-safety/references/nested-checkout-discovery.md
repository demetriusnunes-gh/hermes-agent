# Nested checkout discovery checklist

Use this when a repo contains a nested working tree, submodule, or other git-linked directory and you need to decide which level should be committed.

## Quick checks

1. Confirm the top-level repo root.
   ```bash
   git rev-parse --show-toplevel
   ```
2. Inspect the parent tree.
   ```bash
   git status --porcelain --ignore-submodules=none
   git diff --name-status
   ```
3. If a path looks like a repo, inspect it directly.
   ```bash
   git -C <nested> rev-parse --show-toplevel
   git -C <nested> status --porcelain
   ```
4. Check whether the parent is tracking a gitlink.
   ```bash
   git ls-files -s <path>
   git ls-tree HEAD <path>
   ```
   A mode `160000` entry means the parent is storing a nested repo pointer, not normal files.
5. Decide the commit target before staging:
   - If the nested repo owns the content change, commit inside the nested repo.
   - If the parent should record the nested repo’s new SHA, commit the parent gitlink update.
   - If the parent tree itself changed, commit the parent only.

## Common pitfall

Do not stage the parent tree first and then discover the actual change was inside a nested repo. That usually turns a simple nested-repo update into a confusing parent-pointer commit.
