---
name: push-vite-supabase-app-to-github
description: Safely initialize and push a local Vite/Supabase web app to a new GitHub repo from this Hermes VPS.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, vite, supabase, secrets, deployment]
    related_skills: [github-auth, github-repo-management]
---

# Push Vite/Supabase App to GitHub

Use this when the user asks to create a new GitHub repository for a locally-built Vite/Supabase app and push the code.

## Key lessons

- On this Hermes VPS, terminal sessions may have `$HOME` unset. GitHub CLI auth and `git config --global` can falsely fail unless you run `export HOME=/root` first.
- Do not commit runtime/deployment artifacts or secret-bearing local state.
- Vite `VITE_*` values are bundled into client code if present at build time. A Supabase anon/publishable key is normally public, but the real `.env` should still stay out of git; commit only `.env.example`.
- Supabase CLI creates `supabase/.temp/`; Caddy local TLS validation can create local CA files under `caddy/`. Ignore both.

## Procedure

1. Normalize environment and check auth/status:

```bash
export HOME=/root
pwd
gh auth status
git status --short --branch || true
git config --global user.name || true
git config --global user.email || true
```

2. Add a conservative `.gitignore` before `git add`:

```gitignore
node_modules/
dist/
.vite/
coverage/
.env
.env.*
!.env.example
supabase/.temp/
caddy/
.DS_Store
*.swp
*.swo
.vscode/
.idea/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
```

3. Initialize and set identity if needed:

```bash
export HOME=/root
[ -d .git ] || git init -b main
git config --global user.name  "Demetrius Nunes"
git config --global user.email "demetriusnunes@gmail.com"
```

4. Verify ignored paths before staging:

```bash
for f in .env node_modules dist supabase/.temp caddy; do
  git check-ignore -q "$f" && echo "ignored $f" || echo "NOT ignored $f"
done
```

5. Stage and scan for accidental secrets/artifacts:

```bash
git add .
git status --short

# Abort if ignored build/secret/temp paths somehow got staged
git diff --cached --name-only | grep -E '(^|/)\.env$|node_modules|^dist/|^caddy/|supabase/\.temp' && exit 1 || true

# Optionally check for known real keys/tokens if you saw them during setup
git diff --cached | grep -E 'sb_publishable_|SUPABASE_SERVICE_ROLE|BEGIN (RSA|OPENSSH) PRIVATE KEY|gh[pousr]_' && exit 1 || true
```

6. Commit, create private repo, push:

```bash
git commit -m "Initial app commit"
GH_USER=$(gh api user --jq '.login')
gh repo create rankingpcc --private --description "Ranking PCC: doubles tennis ranking app" --source . --remote origin --push
git push -u origin main
```

7. Verify:

```bash
gh repo view --json nameWithOwner,url,visibility,defaultBranchRef --jq '{nameWithOwner,url,visibility,defaultBranch:.defaultBranchRef.name}'
git remote -v
git status --short --branch
git log -1 --oneline
```

## Notes

- If the repo already exists, set `origin` manually and push instead of running `gh repo create`.
- Prefer private repos for personal/internal apps unless the user explicitly asks for public.
- Never include `.env`, local Caddy CA material, or Supabase `.temp` files in the commit.
