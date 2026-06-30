---
name: git-update-existing-clone
description: Safely update an existing git checkout to the latest upstream while preserving local modifications, including resolving autostash conflicts after pull --rebase --autostash.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Git, Update, Rebase, Autostash, Conflict Resolution]
---

# Git: Update Existing Clone Safely

Use this when a repo already exists locally and you want the latest upstream code without losing intentional local edits.

## Workflow

1. Inspect local state first.
2. Fetch upstream and confirm how far behind/ahead the checkout is.
3. Review any local edits that might conflict.
4. Run `git pull --rebase --autostash`.
5. If autostash conflicts appear after the pull, keep the upstream update and manually re-apply only the desired local customizations.
6. Stage the resolved files and verify syntax/tests before considering the update complete.

## Commands

```bash
# Inspect current state
git status --short --branch
git remote -v
git rev-parse --short HEAD
git branch --show-current

# Fetch and compare with upstream
git fetch origin --prune
git rev-parse --short origin/master
git rev-list --left-right --count HEAD...origin/master

# Review local changes that may need to be preserved
git diff -- path/to/file

# Update while temporarily stashing local modifications
git pull --rebase --autostash origin master
```

## When autostash causes conflicts

A common outcome is:
- the branch fast-forwards to upstream successfully
- the autostash re-apply fails
- one or more files become unmerged
- the autostash is preserved as a normal stash entry

Check the state with:

```bash
git status
git diff --name-only --diff-filter=U
git ls-files -u
```

Conflict markers typically look like:

```text
< < < < < < < Updated upstream
...
= = = = = = =
...
> > > > > > > Stashed changes
```

## Resolution strategy

1. Start from the updated upstream file.
2. Re-apply only the local additions you still want.
3. Remove all conflict markers.
4. Stage the file with `git add path/to/file`.
5. Verify the file parses or tests pass.
6. Inspect the staged diff before finishing.

Example verification for Python:

```bash
python3 -m py_compile path/to/file.py
```

Inspect the final staged result:

```bash
git diff --cached --stat
git diff --cached -- path/to/file
```

## Pitfalls

- `git pull --rebase --autostash` can leave you on the latest upstream commit even when the stash re-apply fails.
- Do not assume a failed autostash means the pull failed.
- Do not drop the remaining stash entry until you confirm the resolved file content is correct.
- Check the actual unmerged file content, not just `git status`.
- If preserving local customizations, prefer a minimal merge that keeps upstream structure and only reintroduces the intentional local lines.

## Post-update runtime check for deployed services

If the checkout backs a running service (web UI, API, bot, daemon), updating the repo does not update the live process.

After the git update, verify whether the running process is still old:

```bash
# Find the service process
ps -fp <PID>

# Compare process start time with updated file mtimes
ps -o lstart= -p <PID>
stat -c 'server.py mtime: %y' server.py
stat -c 'important file mtime: %y' path/to/file
```

Useful confirmation pattern:
- invoke the updated code directly from the repo (for example a Python function that resolves config/models)
- compare that result to what the live service is actually serving
- if they differ and the process predates the updated files, the repo is current but the service needs a restart

Important nuance: seeing legacy/fallback options in a UI is not always proof of a bug. They may still appear because of fallback providers or stored credentials. First distinguish:
- code on disk is wrong
- live process is stale
- UI is correctly showing additional fallback providers

## Success criteria

- `git status` shows no unmerged paths.
- The target file(s) pass a syntax or test check.
- The staged diff contains only the intended local preservation changes.
- The repo is at the latest upstream commit.
- If the repo backs a running service, you verified whether the live process also reflects the update.
