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

Example:
```bash
git status --porcelain
git diff
```

This is important because meaningful tracked files may still be modified even after secret cleanup.

If `hermes-agent` appears modified, inspect it as a submodule before staging the parent repo:
```bash
git diff --submodule=log -- hermes-agent
git -C hermes-agent status --porcelain
git -C hermes-agent diff --stat
git -C hermes-agent diff -- <paths>
```

Only commit a submodule pointer bump when the submodule working tree is clean and the pointer change is intentional. If the submodule contains incidental generated changes such as `ui-tui/package-lock.json` churn from a local install, revert those inside the submodule first (for example `git -C hermes-agent checkout -- ui-tui/package-lock.json`) so the parent commit records only the intended submodule SHA.

Special case: in some worktrees ` /root/.hermes ` is the top-level repo, but the meaningful source tree is the nested `hermes-agent` checkout. If the parent repo looks clean, still check the nested checkout directly before concluding there is nothing to commit; a detached HEAD in the nested repo is normal and does not mean the tree is safe to ignore.

If the parent repo stays noisy because a nested gitdir is dirty but the parent should remain clean, verify the submodule state first and then consider a local-only ignore override such as `git config submodule.hermes-agent.ignore all` for the current checkout. Use this only after confirming the dirt is non-source runtime noise.

See `references/root-hermes-submodule-pitfall.md` for the exact check sequence and examples.

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
- A modified `hermes-agent` entry can mean either an intentional submodule SHA bump, dirty files inside the submodule, or both; always inspect `git -C hermes-agent status` before staging.
- Local Hermes webui state files like `webui/.pbkdf2_key` and `webui/projects.json` are runtime artifacts, not source changes.
- OAuth flows can create multiple local files at different times during setup.
- You may need a follow-up commit if the workflow itself creates a new ignored/runtime artifact after the first push.
- If force-pushing an amended commit, prefer `--force-with-lease`, not `--force`.

## Verification Checklist
Before reporting completion, confirm:
- `git diff --cached --check` passed before commit
- `git push origin master` succeeded (or `--force-with-lease` if intentionally amending a fresh commit)
- `git status --porcelain` is empty
- if `hermes-agent` was touched, `git -C hermes-agent status --porcelain` is empty and any parent submodule SHA change was intentional
- no secrets/tokens/auth callback URLs were committed
- tracked runtime state (`.hermes_history`, `gateway_state.json`, `webui/last_workspace.txt`) was not committed unless intentionally requested
- final response summarizes the meaningful changes only