---
name: git-working-tree-safety
description: "Safely commit, push, and publish from dirty or shared Git checkouts."
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

Use this skill when you need to commit and push changes from a checkout that may already contain unrelated edits, generated files, submodules/gitlinks, nested repos, sibling working trees, or merge conflict markers.

## When to use

- The repository is not clean before your change.
- You are working in a shared or long-lived checkout.
- The remote target matters and must be verified explicitly.
- The checkout may contain a nested repo, gitlink, or generated working tree inside a parent repo, and you need to identify the real commit target.
- You need to recover from unmerged paths before committing.

## Core workflow

1. Inspect the tree before staging.
   ```bash
   git status --porcelain --ignore-submodules=none
   ```
2. If the checkout may contain a nested repo, gitlink, or parent tracking pointer, inspect both layers before deciding where the real change lives.
   ```bash
   git ls-files -s <path>
   git -C <nested> rev-parse --show-toplevel
   git -C <nested> status --porcelain --ignore-submodules=none
   ```
   Treat the nested repo as the default commit target unless you explicitly intend to update the parent pointer.
   If `git status` and `git diff` seem to disagree, use `git status --porcelain=v2` plus `git hash-object`/`git ls-files -s` to prove which layer actually changed; see `references/status-vs-diff-discrepancy.md`.
3. Verify the exact remote and branch you intend to push to.
   ```bash
   git remote -v
   git ls-remote <remote> refs/heads/<branch>
   ```
   If you created a fork for a repo you don't own, confirm that the local remote actually points to your fork before pushing. If not, add a dedicated remote (for example `fork`) explicitly and push to that remote instead of assuming `origin` is writable.
   Before pushing, compare local HEAD to the target branch so you know whether you are fast-forwarding, already up to date, or behind:
   ```bash
   git fetch <remote>
   git rev-list --left-right --count <remote>/<branch>...HEAD
   ```
   Use the count to decide whether a push is needed (`N\t0`), unnecessary (`0\t0`), or should be preceded by a rebase/merge (`0\tN`).
4. Review the delta before staging.
   ```bash
   git diff --name-status
   ```
5. If Git reports unmerged paths, resolve them first; do not stage through conflict markers.
6. Stage only after review.
   - Prefer explicit path staging (`git add <paths...>`) when the checkout contains unrelated runtime artifacts, generated trees, or other ambient noise.
   - Use `git add -A` only when you have already confirmed the entire checkout is intended to be part of the commit.
   ```bash
   git add -A
   ```
7. If the intended files are ignored by a local `.gitignore` rule, verify that explicitly before staging.
   ```bash
   git check-ignore -v <path>
   ```
   If the path is intentionally part of the change, stage it with `git add -f <path>` rather than broadening the commit to unrelated ignored files.
8. Commit with a message that describes the actual change.
   ```bash
   git commit -m "<message>"
   ```
9. Push to the verified remote/branch explicitly.
   ```bash
   git push <remote> HEAD:<branch>
   ```
10. Verify the remote ref after push and confirm the local commit matches it.
   ```bash
   git rev-parse HEAD
   git ls-remote <remote> refs/heads/<branch>
   ```

## Secure publication and push-protection

Use this section when the repository is ready to publish but the push is blocked by permissions, branch protection, or secret-scanning rules.

### Classify the failure

- `403` / permission denied: the destination remote is not writable by the current account.
- `GH013` / push protection: GitHub detected a secret somewhere in the branch history.
- If two sibling directories look related, confirm they are distinct repositories before rewriting anything.

### Safe recovery flow

1. Identify the exact repo, branch, and remote you intend to publish.
2. If history is contaminated, rewrite it in a disposable clone or throwaway worktree rather than in the only clean checkout.
3. Remove the sensitive path or value from all reachable commits on the branch, not just the tip.
4. Verify the sanitized history before pushing.
5. Push the cleaned branch to a verified writable remote or fork.
6. Confirm the remote ref points at the sanitized tip after the push.

### Pitfalls specific to publication

- Do not force-push contaminated history to a protected remote.
- Do not assume `origin` is writable when a fork remote may be required.
- Do not leave secret values in commit messages, logs, or notes.
- Do not rewrite the only working copy unless that is explicitly intended.
- If a push is rejected as non-fast-forward, fetch the remote tip and rebase or merge before retrying.
- If push protection blocks the branch, stop retrying the same ref; create a sanitized branch instead and verify that the offending path or blob is absent from history.

## Pitfalls

- A dirty tree is not an error by itself; it is a signal to inspect before acting.
- `git add -A` should come after `git diff --name-status`, not before.
- If a checkout contains unrelated files, keep them out of the commit unless they are part of the intended change.
- If a path is a gitlink/submodule pointer, verify whether the pointer update is intentional before staging it.
- If the checkout contains a nested repo or submodule, inspect both layers before staging:
  - `git status --porcelain --ignore-submodules=none` at the parent root
  - `git -C <nested> rev-parse --show-toplevel` to confirm the nested repo root
  - `git -C <nested> status --porcelain --ignore-submodules=none`
  - commit the layer that actually owns the change, and only commit the parent if you intend to update the gitlink pointer or parent-tracked files
  - If the parent checkout shows an untracked directory that is itself a git repo, treat the nested repo as the likely commit target and inspect it directly with `git -C <nested> status` before assuming the parent tree is relevant.
- In noisy session-root checkouts like `/root/.hermes`, the real code checkout may be the parent root itself or a nested repo below it; verify the owning repo's branch, remotes, and `HEAD` before staging or pushing anything.
  - If the parent repo shows a path as `M` with a `-dirty` subrepo pointer, inspect the nested repo's own `git status` before touching the parent; the parent may only be recording the nested repo's HEAD movement.
  - When `git add -A` emits `warning: adding embedded git repository`, stop and verify whether the nested repo should be committed on its own or whether you intentionally want to update the parent gitlink pointer.
  - When a checkout contains a path tracked as a gitlink (`mode 160000`) or a nested working tree without `.gitmodules`, use `git ls-files -s <path>` / `git ls-tree HEAD <path>` plus `git -C <path> status` to determine whether the real change lives inside the nested repo or in the parent pointer.
  - In a parent checkout that contains a nested working tree, treat the nested repo as the default commit target unless the user's wording clearly targets the outer runtime root (for example “commit code under `/root/.hermes`” and the nested repo is clean). In that case, commit the outer root but keep the nested repo/gitlink untouched unless its pointer actually changed.
  - In `~/.hermes`-style roots, assume the outer tree may contain session/runtime noise until the nested repo is inspected directly. If the outer root itself is the target, use tracked-path/allowlist staging rather than broad `git add -A`: stage durable tracked config/skills and explicit new skill directories, while leaving auth files, tokens, caches, DBs, sessions, cron output, profile homes, lock/PID files, and other live state untracked.
  - Before committing a live Hermes root backup, review `git diff --cached --stat`/`--name-only`, run `git diff --cached --check`, parse any staged YAML config, and scan staged additions for obvious secrets. Fix whitespace warnings in generated markdown before committing; do not publish real credentials even if a config file is otherwise intended.
  - Before pushing, verify the exact remote branch mapping on the repo you are about to publish with `git -C <nested> ls-remote <remote> refs/heads/<branch>`.
  - If the nested repo's current local branch is not the branch that should be published, push the correct local branch/HEAD pair explicitly (for example `git -C <nested> push <remote> HEAD:<branch>`) instead of assuming `git push <remote> <local-branch>` targets the right remote ref. The same explicit refspec pattern is useful for outer Hermes-root backup branches (for example `git -C /root/.hermes push fork HEAD:push-clean`).
  - If the parent root and nested repo each have changes, publish the nested repo first, then update and push the parent gitlink pointer after verifying the nested remote ref.
  - If a recurring cron-style publish task names a previously observed nested repo or branch (for example a branch-specific checkout under `/root/.hermes/hermes-agent/...`), verify the path still exists before treating it as the target. Remember that nested repos/worktrees may store `.git` as a **file** (`gitdir: ...`), not a directory; `test -d path/.git` or directory-only discovery will falsely report them missing. Use `git -C <path> rev-parse --show-toplevel`, `git -C <path> status`, or check `test -e <path>/.git` before deciding a nested checkout is absent. If the nested checkout is absent but its remote branch exists, fetch/push/verify the remote branch explicitly from a containing repo with that remote instead of failing the job or staging unrelated runtime files.
  - For the recurring “roger hermes code under `/root/.hermes`” publish shape, inspect and verify all relevant layers before deciding there is nothing to commit: outer `/root/.hermes` (`push-clean`), nested `/root/.hermes/hermes-agent` (`local/package-lock-sync`), and the `tinker-atropos` nested checkout when present (`roger-hermes`). Keep live runtime/auth/cache/session files in the outer root unstaged unless explicitly requested.
  - If the parent repo contains a submodule that itself contains another git repository, commit/push the inner repo first, then update and push the parent gitlink pointer.
  - If `git push` is rejected as non-fast-forward, fetch the remote tip and rebase or merge before retrying; do not force-push unless that is explicitly the intended workflow.
  - If GitHub push protection blocks a push because a secret exists anywhere in reachable history, stop retrying the same ref and rewrite a sanitized branch that removes the offending path or blob from history before pushing again. Verify the rewritten branch no longer contains the secret path/blobs, then push the sanitized ref.
  - See `references/nested-checkout-discovery.md` for a concise decision checklist and push-verification sequence.
  - See `references/parent-checkout-target-selection.md` for a broader parent-vs-nested selection checklist.
  - See `references/embedded-repo-and-submodule-flow.md` for the observed flow when a parent repo contains a submodule that itself contains a nested git repository.
  - See `references/nested-repo-without-gitmodules.md` for a worked example of a gitlink-style nested repo with no `.gitmodules` entry and the verification steps used to publish both layers cleanly.
  - See `references/push-protection-remediation.md` for a minimal history-rewrite and verification recipe when push protection blocks a publish.
  - See `references/status-vs-diff-discrepancy.md` for a hash-based way to resolve tracked-file status/diff mismatches in noisy workspaces.
## Verification

Before finishing, confirm:
- the commit exists locally,
- the remote branch points to the pushed commit,
- the working tree is in the expected state after the push.

## Reference

- See `references/writable-checkout-playbook.md` for a concise commit/push checklist and conflict-handling notes.
- See `references/nested-checkout-and-gitlink-notes.md` for a focused checklist on parent checkouts, nested repos, and gitlink hygiene.
- See `references/parent-vs-nested-target-selection.md` for a short decision checklist when a parent checkout may contain the real target repo.
- See `references/embedded-repo-and-submodule-flow.md` for the observed flow when a parent repo contains a submodule that itself contains a nested git repository.
- See `references/ambient-noise-checkout.md` for staging discipline in noisy workspace roots with lots of runtime artifacts.
- See `references/noisy-parent-root-nested-repo.md` for the `/root/.hermes`-style case where the parent is just runtime noise and the real code checkout is nested below it.
- See `references/noisy-session-root-discovery.md` for a compact discovery sequence when the outer session root is noisy and a nested repo is the real publish target.
- See `references/hermes-runtime-root-backup.md` for the allowlist staging, secret-scan, whitespace-check, and push-verification sequence when the outer Hermes home itself is the backup/publish target.
- See `references/roger-hermes-root-publish.md` for the recurring `/root/.hermes` publish checklist and the outer-root allowlist staging rule.
- See the new `references/noisy-session-root-discovery.md` note for the parent-vs-nested inspection and explicit push-refspec sequence.
- In `~/.hermes`-style workspaces, inspect the outer root and every nested repo before staging; the outer root is often ambient runtime noise, while the publishable code lives in a child repo with its own branch/remotes.
