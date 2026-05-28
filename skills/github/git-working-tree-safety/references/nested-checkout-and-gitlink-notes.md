# Nested checkout and gitlink notes

Use this when a parent repository contains a nested checkout or a tracked gitlink path.

## Decision checklist

1. Identify the real repo root before staging.
   - Run `git rev-parse --show-toplevel` in the parent checkout.
   - Run the same command inside the nested checkout.
2. Determine whether the parent repo tracks the nested path as a gitlink.
   - If the parent status shows the nested path as modified, inspect the nested repo first.
3. Commit in the repo that owns the actual change.
   - If the nested checkout changed files, commit there.
   - If the parent only needs to update the pointer, commit the gitlink update in the parent.
4. Verify the intended remote/branch before pushing.
   - Run `git remote -v`.
   - Run `git ls-remote <remote> refs/heads/<branch>`.
5. After pushing, confirm the remote branch points to the new commit.
   - Use `git ls-remote <remote> refs/heads/<branch>` again.

## Practical cues

- A parent checkout can look dirty because a nested repo advanced HEAD, even if no parent files changed.
- Untracked runtime files in the parent checkout do not automatically belong in the commit.
- If the nested checkout is a separate repo, treat it as the primary unit of work unless the parent explicitly needs the pointer update.