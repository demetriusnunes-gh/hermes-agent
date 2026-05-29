---
name: git-working-tree-safety
description: "Safely commit and push from dirty or shared Git checkouts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Git, GitHub, commits, pushes, dirty-tree, merge-conflicts, remotes]
    related_skills: [github-repo-management, github-pr-workflow]
---

# Git Working Tree Safety

Use this skill when you need to commit and push changes from a checkout that may already contain unrelated edits, generated files, submodules/gitlinks, or merge conflict markers.

## When to use

- The repository is not clean before your change.
- You are working in a shared or long-lived checkout.
- The remote target matters and must be verified explicitly.
- You need to recover from unmerged paths before committing.

## Core workflow

1. Inspect the tree before staging.
   ```bash
   git status --porcelain --ignore-submodules=none
   ```
2. Verify the exact remote and branch you intend to push to.
   ```bash
   git remote -v
   git ls-remote <remote> refs/heads/<branch>
   ```
3. Review the delta before staging.
   ```bash
   git diff --name-status
   ```
4. If Git reports unmerged paths, resolve them first; do not stage through conflict markers.
5. Stage only after review.
   ```bash
   git add -A
   ```
6. Commit with a message that describes the actual change.
   ```bash
   git commit -m "<message>"
   ```
7. Push to the verified remote/branch explicitly.
   ```bash
   git push <remote> HEAD:<branch>
   ```

## Pitfalls

- A dirty tree is not an error by itself; it is a signal to inspect before acting.
- `git add -A` should come after `git diff --name-status`, not before.
- If a checkout contains unrelated files, keep them out of the commit unless they are part of the intended change.
- If a path is a gitlink/submodule pointer, verify whether the pointer update is intentional before staging it.
- If the checkout contains a nested repo or submodule, inspect both layers before staging:
  - `git status --porcelain --ignore-submodules=none` at the parent root
  - `git -C <nested> status --porcelain`
  - commit the layer that actually owns the change, and only commit the parent if you intend to update the gitlink pointer
- When a path or directory is suspicious, inspect the actual index entry before deciding what changed:
  ```bash
  git ls-files -s <path>
  git ls-tree HEAD <path>
  ```
  A mode `160000` entry means the parent repo is tracking a nested repo pointer, not normal files.
- When working under a parent checkout that already contains nested repos or gitlinks, verify the repo root with `git rev-parse --show-toplevel` before staging so you don't commit from the wrong level.
- If the parent checkout shows an untracked directory that is itself a git repo, treat the nested repo as the likely commit target and inspect it directly with `git -C <nested> status` before assuming the parent tree is relevant.
- If the parent repo shows a path as `M` with a `-dirty` subrepo pointer, inspect the nested repo's own `git status` before touching the parent; the parent may only be recording the nested repo's HEAD movement.
- If a nested repo is present, compare `git -C <nested> rev-parse --show-toplevel` and `git -C <nested> status` with the parent checkout before deciding which repo to commit in.
- In a parent checkout that contains a nested working tree, treat the nested repo as the default commit target unless you explicitly intend to update the parent gitlink pointer.

See `references/nested-checkout-discovery.md` for a concise checklist for distinguishing parent checkouts, nested git repos, and gitlink updates.

## Verification

Before finishing, confirm:
- the commit exists locally,
- the remote branch points to the pushed commit,
- the working tree is in the expected state after the push.

## Reference

See `references/writable-checkout-playbook.md` for a concise commit/push checklist and conflict-handling notes.
See `references/nested-checkout-and-gitlink-notes.md` for a focused checklist on parent checkouts, nested repos, and gitlink hygiene.