# Nested Checkout Discovery Checklist

Use this when a top-level checkout contains suspicious untracked directories or when a parent repo may actually be tracking a nested working tree.

## Fast triage

1. Identify the current repo root.
   ```bash
   git rev-parse --show-toplevel
   ```
2. Check the parent tree status without submodule collapsing.
   ```bash
   git status --porcelain --ignore-submodules=none
   ```
3. If an untracked directory appears, inspect whether it is a nested git repo.
   ```bash
   git -C <dir> rev-parse --show-toplevel
   git -C <dir> status --porcelain --ignore-submodules=none
   ```
4. Decide which repository is the real target:
   - If the directory is a standalone git repo, commit there unless you explicitly intend to update the parent pointer.
   - If the parent repo tracks it as a gitlink/submodule, confirm whether the pointer change is intentional before staging.

## Decision rule

- **Nested repo with its own `.git`** → usually commit in the nested repo.
- **Parent repo shows only a gitlink movement** → treat it as a parent pointer update, not file-level changes.
- **Untracked directory with no nested repo** → inspect contents before staging; it may be generated output.

## Verification before commit

- Compare parent and child `git status` outputs.
- Confirm the intended repo has the changes.
- Only then stage and commit.
