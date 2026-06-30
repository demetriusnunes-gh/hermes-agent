# Hermes runtime root backup commit checklist

Use when asked to commit/push `/root/.hermes` or another live Hermes home directory.

## Target selection

- Inspect both the outer runtime root and nested code checkouts before staging.
- If `/root/.hermes/hermes-agent` is a nested repo/gitlink and is clean, do not assume it is the publish target; the user may mean the outer runtime/root backup branch.
- Verify remotes and branch on the actual repo being committed, then push with an explicit refspec such as `git push fork HEAD:push-clean`.

## Staging discipline

The outer Hermes home usually contains sensitive or noisy runtime artifacts. Do not use `git add -A` across the whole root. Stage deliberately:

1. Stage tracked updates only for intended areas, for example:
   ```bash
   git -C /root/.hermes add -u config.yaml skills
   ```
2. Add only intended new durable library content, e.g. new skill directories under `skills/`.
3. In a live `/root/.hermes` tree, start with a dry-run or name-only audit before committing:
   ```bash
   git add -n <paths...>
   git diff --cached --name-only
   git diff --cached --shortstat
   ```
   This helps confirm that the staged set is confined to durable profile/skill content instead of runtime noise.
4. Leave private/runtime paths untracked unless the user explicitly asks otherwise: `auth*.json`, token files, caches, DBs, sessions, cron output, profile homes, audio/cache folders, gateway locks/PIDs, and other live state.

## Pre-commit checks

- Run a staged diff review: `git diff --cached --stat` and `git diff --cached --name-only`.
- Run `git diff --cached --check`; if generated markdown has whitespace errors, normalize trailing spaces and extra EOF blank lines before committing.
- Parse `config.yaml` with Python/YAML if it is staged.
- Scan staged additions for obvious secrets before publishing. Redacted placeholders like `***` are acceptable; real tokens, private keys, and credentials are not.

## Verification

After pushing, verify:

```bash
git -C /root/.hermes rev-parse HEAD
git -C /root/.hermes ls-remote fork refs/heads/push-clean
git -C /root/.hermes rev-list --left-right --count fork/push-clean...HEAD
git -C /root/.hermes status --porcelain --untracked-files=no
```

A clean tracked tree with remaining untracked runtime/private files is expected in a live Hermes home backup.
