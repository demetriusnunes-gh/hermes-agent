# Parent checkout target selection

Use this when the apparent repo root contains one or more nested Git working trees, gitlinks, or sibling untracked directories and you need to decide where the real change belongs.

## Fast decision checklist

1. Inspect the parent first.
   ```bash
   git status --porcelain --ignore-submodules=none
   git diff --name-status
   ```
2. For any suspicious path, inspect the path itself.
   ```bash
   git -C <path> status --porcelain --ignore-submodules=none
   git -C <path> rev-parse --show-toplevel
   ```
3. Inspect the index entry at the parent.
   ```bash
   git ls-files -s <path>
   git ls-tree HEAD <path>
   ```
   `mode 160000` means the parent is tracking a gitlink (a nested repo pointer), not normal files.
4. Prefer the nested repo as the commit target when:
   - the parent is clean or only shows the directory as untracked/modified,
   - the nested path has its own `.git` metadata,
   - or the parent index entry is a gitlink.
5. Only commit the parent when you explicitly intend to update the gitlink pointer or parent-level files.

## Push verification

Before pushing from a checked-out worktree, verify the exact remote branch:

```bash
git remote -v
git ls-remote <remote> refs/heads/<branch>
```

After pushing, confirm the remote ref matches the commit you expected:

```bash
git rev-parse HEAD
git ls-remote <remote> refs/heads/<branch>
```

## Pitfall

Do not stage from the parent root first and then discover the actual change lived inside the nested repo. That turns a simple nested-repo commit into a confusing parent-pointer update.
