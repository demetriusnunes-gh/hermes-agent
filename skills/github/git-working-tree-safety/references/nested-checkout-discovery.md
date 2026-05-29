# Nested checkout discovery

Use this when a parent checkout contains a nested directory that may itself be a Git repo.

## Quick checks

1. Confirm the current repo root.
   ```bash
   git rev-parse --show-toplevel
   ```
2. Inspect the parent tree before staging.
   ```bash
   git status --porcelain --ignore-submodules=none
   git diff --name-status
   ```
3. If a directory looks suspicious, inspect it directly.
   ```bash
   test -e path/.git && file path/.git
   git -C path status --porcelain --ignore-submodules=none
   git -C path rev-parse --show-toplevel
   ```
4. Check whether the parent tracks that path as a gitlink.
   ```bash
   git ls-files -s path
   git ls-tree HEAD path
   ```
   A mode `160000` entry means the parent is tracking a nested repo pointer, not normal files.

## Interpretation

- Parent clean + nested repo dirty: commit inside the nested repo, not the parent.
- Parent shows `M path` and the index entry is `160000`: the parent is recording a nested repo HEAD movement.
- A directory may be a real repo even when the parent does not have a `.gitmodules` entry.

## Decision rule

Treat the nested repo as the default commit target unless you explicitly intend to update the parent gitlink pointer.
