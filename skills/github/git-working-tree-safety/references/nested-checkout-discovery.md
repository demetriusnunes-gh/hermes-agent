# Nested checkout discovery

This reference captures the decision tree for a parent checkout that contains a nested git repo, gitlink, or generated subdirectory.

## Quick decision tree

1. Run at the parent root:
   ```bash
   git status --porcelain --ignore-submodules=none
   git diff --name-status
   ```
2. For any suspicious path, determine whether it is its own repo:
   ```bash
   git -C <path> rev-parse --show-toplevel
   git -C <path> status --porcelain --ignore-submodules=none
   ```
3. If the nested path has its own `.git` metadata and its own status output, treat that nested repo as the default commit target.
4. Only commit the parent repo if you explicitly intend to update the parent pointer or parent-tracked files.
5. Before pushing, verify the remote branch tip and confirm the pushed commit matches:
   ```bash
   git ls-remote <remote> refs/heads/<branch>
   git rev-parse HEAD
   ```

## Session note

In this session, the parent Hermes checkout contained both generated `nova-platform/nova-platform/dist/*` artifacts and a nested `tinker-atropos/` repo. The nested repo was not a parent-tracked path; it needed its own inspection via `git -C tinker-atropos status` rather than relying on the parent status alone.