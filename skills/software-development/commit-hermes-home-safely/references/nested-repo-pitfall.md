# Nested repo / submodule pitfall

Observed during a `~/.hermes` commit workflow:

- `git status --porcelain` in the parent repo can look clean even when `hermes-agent` is dirty.
- `git config --get submodule.hermes-agent.ignore` may return `all`, which hides submodule dirt from casual checks.
- Use `git status --porcelain --ignore-submodules=none` before deciding there is nothing to commit.
- Then inspect the submodule directly:
  ```bash
  git -C hermes-agent status --porcelain --ignore-submodules=none
  git -C hermes-agent diff --stat
  ```
- If the submodule contains an intentionally present nested repo such as `tinker-atropos/`, inspect that nested repo directly too:
  ```bash
  git -C hermes-agent/tinker-atropos status --porcelain
  ```

Takeaway: a clean parent status does not prove the submodule tree is clean, and a local `submodule.hermes-agent.ignore=all` setting can mask the real state.