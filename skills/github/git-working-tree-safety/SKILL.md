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

Use this skill when you need to commit and push changes from a checkout that may already contain unrelated edits, generated files, submodules/gitlinks, nested repos, sibling working trees, or merge conflict markers.

## When to use

- The repository is not clean before your change.
- You are working in a shared or long-lived checkout.
- The remote target matters and must be verified explicitly.
- The checkout may contain a nested repo, gitlink, or generated working tree inside a parent repo, and you need to identify the real commit target.
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
  - If the checkout contains a nested repo or submodule, inspect both layers before staging:
    - `git status --porcelain --ignore-submodules=none` at the parent root
    - `git -C <nested> rev-parse --show-toplevel` to confirm the nested repo root
    - `git -C <nested> status --porcelain --ignore-submodules=none`
    - commit the layer that actually owns the change, and only commit the parent if you intend to update the gitlink pointer or parent-tracked files
    - If the parent checkout shows an untracked directory that is itself a git repo, treat the nested repo as the likely commit target and inspect it directly with `git -C <nested> status` before assuming the parent tree is relevant.
    - If the parent repo shows a path as `M` with a `-dirty` subrepo pointer, inspect the nested repo's own `git status` before touching the parent; the parent may only be recording the nested repo's HEAD movement.
    - When `git add -A` emits `warning: adding embedded git repository`, stop and verify whether the nested repo should be committed on its own or whether you intentionally want to update the parent gitlink pointer.
    - When a checkout contains a path tracked as a gitlink (`mode 160000`) or a nested working tree without `.gitmodules`, use `git ls-files -s <path>` / `git ls-tree HEAD <path>` plus `git -C <path> status` to determine whether the real change lives inside the nested repo or in the parent pointer.
    - In a parent checkout that contains a nested working tree, treat the nested repo as the default commit target unless you explicitly intend to update the parent gitlink pointer.
    - If `git push` is rejected as non-fast-forward, fetch the remote tip, rebase or merge onto it, and retry; do not force-push unless that is explicitly the intended workflow.
    - See `references/nested-checkout-discovery.md` for a concise decision checklist and push-verification sequence.
    - See `references/parent-checkout-target-selection.md` for a broader parent-vs-nested selection checklist.

## Verification

Before finishing, confirm:
- the commit exists locally,
- the remote branch points to the pushed commit,
- the working tree is in the expected state after the push.

## Reference

See `references/writable-checkout-playbook.md` for a concise commit/push checklist and conflict-handling notes.
See `references/nested-checkout-and-gitlink-notes.md` for a focused checklist on parent checkouts, nested repos, and gitlink hygiene.