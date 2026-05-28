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
- If push protection or secret scanning rejects the push, fix the commit content and re-push; do not retry the same tree unchanged.

## Verification

Before finishing, confirm:
- the commit exists locally,
- the remote branch points to the pushed commit,
- the working tree is in the expected state after the push.

## Reference

See `references/writable-checkout-playbook.md` for a concise commit/push checklist and conflict-handling notes.