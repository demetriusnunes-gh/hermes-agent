# Writable Checkout Playbook

A concise checklist for committing and pushing from a checkout that may already be dirty.

## Checklist

```bash
git status --porcelain --ignore-submodules=none
git remote -v
git ls-remote <remote> refs/heads/<branch>
git diff --name-status
# resolve any unmerged paths before proceeding
git add -A
git commit -m "<message>"
git push <remote> HEAD:<branch>
```

## Conflict-handling notes

- If `git status` reports `UU` / unmerged paths, resolve them before staging.
- Do not rely on `git add -A` to "fix" a conflicted tree.
- Re-run `git status` after resolution to ensure no conflict markers remain.

## Good hygiene

- Verify the push target before the commit if the checkout has multiple remotes.
- Keep unrelated files out of the commit unless they are intentionally part of the change.
- If the repository uses gitlinks/submodules, treat pointer updates as deliberate changes and review them with extra care.
- If push protection rejects the push, remove the offending content from the commit and push again.