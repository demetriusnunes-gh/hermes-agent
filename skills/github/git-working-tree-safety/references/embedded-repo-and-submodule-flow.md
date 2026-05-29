# Embedded repo inside a submodule: commit/push flow

Observed pattern:

- Parent checkout: `/root/.hermes`
- Submodule/path tracked in parent: `hermes-agent` (gitlink)
- Inner repo inside submodule: `hermes-agent/tinker-atropos`

## Decision flow

1. Inspect the parent first:
   ```bash
   git status --porcelain --ignore-submodules=none
   git ls-files -s hermes-agent
   ```
   If the index shows mode `160000`, treat `hermes-agent` as a gitlink/submodule pointer.

2. Inspect the submodule root:
   ```bash
   git -C hermes-agent status --porcelain --ignore-submodules=none
   git -C hermes-agent rev-parse --show-toplevel
   ```

3. If the submodule itself contains another git repo directory, treat that inner repo as the primary change target:
   ```bash
   git -C hermes-agent/tinker-atropos status --porcelain --ignore-submodules=none
   git -C hermes-agent/tinker-atropos rev-parse --show-toplevel
   ```

4. Commit and push the inner repo first on its own branch.

5. Update the submodule pointer in the parent repo only after the inner push is complete.

6. Commit and push the parent repo separately.

## Verification

After both pushes, verify each remote ref explicitly:

```bash
git -C hermes-agent ls-remote fork refs/heads/<branch>
git ls-remote fork refs/heads/<parent-branch>
```

## Pitfall

A parent repo can appear dirty only because its submodule pointer moved. In that case, do not stage unrelated parent files; stage the gitlink pointer only after the nested repo commit has been created and pushed.