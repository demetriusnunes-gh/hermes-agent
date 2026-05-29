# Parent vs nested checkout target selection

Use this when a path inside a checkout may itself be a Git repository, submodule, or gitlink pointer.

## Quick decision checklist

1. Inspect the parent tree first:
   ```bash
   git status --porcelain --ignore-submodules=none
   git diff --name-status --ignore-submodules=none
   git ls-files -s <path>
   ```
2. If the path is an embedded repo or appears as a gitlink, inspect the nested repo directly:
   ```bash
   git -C <path> rev-parse --show-toplevel
   git -C <path> status --porcelain --ignore-submodules=none
   git -C <path> remote -v
   ```
3. Default rule:
   - commit the nested repo when the real changes are inside it;
   - commit the parent only when you intend to update the pointer to a specific nested commit.
4. Before pushing, verify the exact branch/ref on the selected remote:
   ```bash
   git remote -v
   git ls-remote <remote> refs/heads/<branch>
   ```
5. After pushing, confirm the remote ref matches the local commit:
   ```bash
   git rev-parse HEAD
   git ls-remote <remote> refs/heads/<branch>
   ```

## Signal to stop and inspect

If the parent checkout shows a modified path with no obvious file-level diff, assume it may be recording a nested repo movement until the nested repo status proves otherwise.
