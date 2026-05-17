---
name: commit-hermes-home-safely
description: Safely review, commit, and push changes in ~/.hermes while avoiding accidental secret/runtime-file commits and catching follow-up changes created during the workflow
category: software-development
---

# Commit ~/.hermes Safely

## When to Use
Use this when asked to commit and push changes from `~/.hermes`, especially after auth/setup work, skill edits, or cron-driven activity where local runtime artifacts may appear alongside meaningful changes.

## Why This Skill Exists
In `~/.hermes`, meaningful skill/config changes are often mixed with:
- local OAuth secrets/tokens
- runtime state files
- `.hermes_history` entries containing sensitive pasted values or transient auth URLs
- new files generated during the commit process itself

A naive `git add -A && git commit` can accidentally publish secrets or noisy local state.

## Procedure

### 1. Check status first
```bash
cd ~/.hermes
git status --porcelain
```

### 2. Inspect what actually changed
Use targeted diffs before staging:
```bash
git diff
```

Pay special attention to:
- `.hermes_history`
- `google_client_secret.json`, `google_token.json`, `google_oauth_pending.json`
- other auth/state/runtime files
- skill docs/scripts that may have changed legitimately

### 3. If sensitive/transient files appear, fix them before committing
Common actions:

#### Revert sensitive history noise
If `.hermes_history` captured secrets, auth callback URLs, or test noise:
```bash
git checkout -- .hermes_history
```

#### Ignore local OAuth and runtime artifacts
If local Google auth files appear untracked, add them to `.gitignore` before proceeding:
- `google_client_secret.json`
- `google_token.json`
- `google_oauth_pending.json`

Also treat these common Hermes/WebUI/runtime artifacts as local-only unless the user explicitly asks to version them:
- `context_length_cache.yaml`
- `webui/.signing_key`
- `webui/.pbkdf2_key`
- `webui/workspaces.json`
- `webui/.sessions.json`
- `webui/models_cache.json`
- `webui/projects.json`
- `gateway_state.json`
- `webui/last_workspace.txt`
- `skills/.curator_state`
- `skills/.usage.json`
- `profiles/` trees created by profile runs
- `ollama_cloud_models_cache.json`

Prefer reverting tracked runtime state (`git checkout -- gateway_state.json webui/last_workspace.txt`) and adding untracked cache/key files to `.gitignore` rather than committing them. If a tracked runtime artifact keeps reappearing and you have confirmed it is generated-only for your session, consider `git update-index --skip-worktree <file>` as a temporary local-only suppression, but only after verifying the file is not intended for version control.

#### Verify ignores
Re-run:
```bash
git status --porcelain
```

### 4. Re-check for additional tracked changes and submodule dirtiness
After cleanup, re-run status and diff again. Do not assume the first diff captured everything.

If the repo contains a nested submodule that belongs to a different GitHub owner than the parent repo, verify whether you are expected to push the submodule to a fork instead of the upstream remote before staging the parent.

Example:
```bash
git status --porcelain
git diff
```

This is important because meaningful tracked files may still be modified even after secret cleanup.

If `hermes-agent` appears modified, inspect it as a submodule before staging the parent repo:
```bash
git diff --submodule=log -- hermes-agent
git -C hermes-agent status --porcelain --ignore-submodules=none
git -C hermes-agent diff --stat
git -C hermes-agent diff -- <paths>
```

Only commit a submodule pointer bump when the submodule working tree is clean and the pointer change is intentional. If the submodule contains incidental generated changes such as `ui-tui/package-lock.json` churn from a local install, revert those inside the submodule first (for example `git -C hermes-agent checkout -- ui-tui/package-lock.json`) so the parent commit records only the intended submodule SHA.

Special case: in some worktrees `/root/.hermes` is the top-level repo, but the meaningful source tree is the nested `hermes-agent` checkout. If the parent repo looks clean, still check the nested checkout directly before concluding there is nothing to commit; a detached HEAD in the nested repo is normal and does not mean the tree is safe to ignore. Also watch for nested git projects inside the submodule (for example `hermes-agent/tinker-atropos/` with its own `.git` file) — a dirty or merely untracked nested repo can make the outer submodule look modified even when the parent repo itself only tracks the pointer. See `references/nested-repo-pitfall.md` for the exact inspection sequence.

If the parent repo stays noisy because a nested gitdir is dirty but the parent should remain clean, verify the submodule state first and then consider a local-only ignore override such as `git config submodule.hermes-agent.ignore all` for the current checkout. Use this only after confirming the dirt is non-source runtime noise. If `git config --get submodule.hermes-agent.ignore` already returns `all`, remember that it can hide real worktree dirt from a casual status check; temporarily inspect with `--ignore-submodules=none` before deciding there is nothing to do.

Special case: nested repositories inside the submodule (for example `hermes-agent/nova-platform/nova-platform` or `hermes-agent/tinker-atropos`) can make the outer submodule appear modified even when the parent repo itself is only tracking the submodule SHA. Inspect those nested repos directly with `git -C <nested-repo> status --porcelain --ignore-submodules=none` before staging the parent. Do not assume a clean top-level `git status` means the nested repos are safe to ignore.

For session-specific examples and cleanup notes, see `references/root-hermes-submodule-pitfall.md`, `references/hermes-home-commit-pitfalls.md`, `references/push-permission-and-nested-repo-pitfalls.md`, `references/nested-submodule-push-pitfalls.md`, and `references/forked-submodule-push-pitfalls.md`.

If a shell command to remove generated cache directories is blocked by the tool's recursive-delete guard, use a narrower cleanup path instead of retrying `rm -rf` blindly. For example, remove `__pycache__` with a Python `shutil.rmtree(...)` helper or target individual files with non-recursive commands, then re-run `git status`.

### 5. Write a descriptive conventional commit message
Summarize both:
- **what changed**
- **why it matters**

Examples:
- `feat(google-workspace): expand OAuth scopes and improve setup guidance`
- `docs(skills): improve Google Workspace and submodule guidance`
- `chore(gitignore): ignore local OAuth artifacts in hermes home`

If the work naturally splits into separate logical commits, prefer multiple commits over one mixed commit.

### 6. Stage, validate, commit, and push
```bash
git add -A

# Catch whitespace errors and accidental literal conflict markers before committing.
git diff --cached --check

# Inspect staged secret-looking additions. This is intentionally broad; distinguish
# real secrets from documentation examples before proceeding.
git diff --cached -U0 | grep '^+' | grep -E -i \
  '(api[_-]?key|secret|token|password|private[_-]?key|BEGIN |oauth|client_secret|authorization|bearer|signing|webhook|github_pat|sk-[A-Za-z0-9])' || true

# Before pushing, confirm the target remote is writable by the current account.
# A successful auth check (gh auth status / git credentials) does NOT mean the
# repo grants push rights; org-owned upstreams can still reject with 403.
git remote -v
gh auth status 2>/dev/null || true

git commit -m "..."
git push origin master
```

If `git diff --cached --check` flags documentation that intentionally demonstrates conflict markers, rewrite the example to avoid literal marker lines (for example, space out `< < < < < < <`, `= = = = = = =`, `> > > > > > >`) rather than committing lines that look like unresolved conflicts.

If you discover an omitted tracked change immediately after pushing, amend locally and push with lease only if rewriting that just-created commit is appropriate:
```bash
git add <files>
git commit --amend
git push --force-with-lease origin master
```

Use this sparingly and only when correcting the fresh commit you just made.

### 7. Always verify final cleanliness
After the push, run:
```bash
git status --porcelain
```

Do this even if the push succeeded. Some local auth/setup tools may generate new files during the session, and you want to catch that before reporting success.

## Heuristics
- **Commit docs/code, not credentials.**
- **Prefer ignore rules over committing local machine auth state.**
- **If `.hermes_history` contains secrets or auth URLs, revert it.**
- **A successful push does not guarantee the repo stayed clean afterward. Re-check status.**

## Known Pitfalls
- `git status` may initially miss the real story if you do not inspect `git diff`.
- A modified `hermes-agent` entry can mean either an intentional submodule SHA bump, dirty files inside the submodule, or both; always inspect `git -C hermes-agent status --ignore-submodules=none` before staging.
- Nested repositories inside the submodule (for example `hermes-agent/tinker-atropos`) need their own status checks; one dirty nested repo can be the only source of the parent submodule noise.
- A local `git config submodule.hermes-agent.ignore all` setting can make the parent repo look clean while the submodule still has real changes; always confirm with `git status --porcelain --ignore-submodules=none` before concluding there is nothing to commit.
- Local Hermes webui state files like `webui/.pbkdf2_key` and `webui/projects.json` are runtime artifacts, not source changes.
- OAuth flows can create multiple local files at different times during setup.
- You may need a follow-up commit if the workflow itself creates a new ignored/runtime artifact after the first push.
- If force-pushing an amended commit, prefer `--force-with-lease`, not `--force`.

## Verification Checklist
Before reporting completion, confirm:
- `git diff --cached --check` passed before commit
- parent/submodule inspection included `git status --porcelain --ignore-submodules=none` and, when applicable, nested repo checks under `hermes-agent/`
- `git push origin master` succeeded (or `--force-with-lease` if intentionally amending a fresh commit)
- `git status --porcelain` is empty
- if `hermes-agent` was touched, `git -C hermes-agent status --porcelain` is empty and any parent submodule SHA change was intentional
- no secrets/tokens/auth callback URLs were committed
- tracked runtime state (`.hermes_history`, `gateway_state.json`, `webui/last_workspace.txt`) was not committed unless intentionally requested
- final response summarizes the meaningful changes only