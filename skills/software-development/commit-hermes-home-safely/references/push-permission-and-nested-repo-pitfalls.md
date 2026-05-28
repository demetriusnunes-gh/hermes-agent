# Push permission and nested repo pitfalls

Session takeaway:
- `gh auth status` can succeed while `git push` still fails with 403/permission denied.
- This happens when the authenticated account has valid credentials but no write access to the target repository.
- It is common with upstream org repos and nested submodules.

Useful checks before pushing:
```bash
git remote -v
gh auth status 2>/dev/null || true
git status --porcelain --ignore-submodules=none
git -C <submodule> status --porcelain --ignore-submodules=none
```

Interpretation notes:
- A detached HEAD inside a nested repo can be normal; do not assume it is dirty without status output.
- If the parent repo points at a submodule commit and the submodule worktree is clean, a push denial is usually a permissions problem, not a commit problem.

When the push is denied:
- stop before force-pushing
- report the exact remote URL and error
- if possible, confirm whether the target repo is owned by a different org/user than the authenticated account