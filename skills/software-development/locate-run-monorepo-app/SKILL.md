---
name: locate-run-monorepo-app
description: Locate a previously built local app by name in monorepo/workspace directories, inspect its package metadata, and determine how to run it when package-manager shims may be missing.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [local-app, monorepo, vite, pnpm, corepack, workspace]
    related_skills: [codebase-inspection, multica-cli]
---

# Locate and Run a Local Monorepo App

Use this when the user asks to find an app/project built locally by name, asks how to run it, or asks for a quick architecture overview of a small local frontend app.

## Workflow

1. Search by filename first from the current directory, then known app roots, then home:

```text
search_files(target='files', path='.', pattern='*<app>*')
search_files(target='files', path='/root/.www', pattern='*<app>*')
search_files(target='files', path='~', pattern='*<app>*')
```

On this VPS, small deployed web apps may have their canonical working tree under `/root/.www/<app>` even when similarly named prototype copies exist under `~/multica_workspaces/...`.

2. If filename search misses, search file contents for package/app names and variants:

```text
search_files(
  target='content',
  path='~',
  pattern='<app-name>|<app_name>|<app name>|<Title Case>|<PascalCase>',
  output_mode='content',
  context=1
)
```

This is especially useful for pnpm/npm monorepos where the directory exists under a generated workspace path such as `~/multica_workspaces/.../apps/<app-name>`.

3. Once found, list the app directory and inspect these files:

- `package.json` — scripts, package manager assumptions, app name
- root `package.json` — workspace scripts and `packageManager`
- entrypoint such as `src/main.tsx`, `src/App.tsx`, `index.html`
- config such as `vite.config.ts`, `tsconfig.json`
- storage/domain files for architecture questions

4. Check available Node package tooling before giving run commands:

```bash
printf 'node='; command -v node || true; node --version 2>/dev/null || true
printf 'pnpm='; command -v pnpm || true; pnpm --version 2>/dev/null || true
printf 'corepack='; command -v corepack || true; corepack --version 2>/dev/null || true
```

5. If `pnpm` is not on PATH but `corepack` is available, prefer:

```bash
corepack pnpm --version
corepack pnpm --filter <package-name> dev
```

or from the app directory:

```bash
corepack pnpm dev
```

6. For Vite apps, look for a script like `vite --host 0.0.0.0`. If present, tell the user:

- local URL is usually `http://localhost:5173`
- remote/VPS access uses `http://<VPS-IP>:5173` if firewall allows it
- the dev server prints the actual port if 5173 is busy

## Architecture inspection checklist

For small React/Vite apps, summarize:

- runtime/framework: React, TypeScript, Vite
- whether it is client-only or has API/backend/database dependencies
- entrypoint: usually `src/main.tsx`
- top-level UI/state owner: usually `src/App.tsx`
- pure business/domain logic files
- persistence layer, often `localStorage`
- styling approach
- tests and test framework
- data flow from user interaction to state updates and persistence
- obvious MVP limitations and next architectural step if productionizing

## Pitfalls

- Do not stop after filename search returns nothing; generated workspaces may hide the app under deep paths and content search can still find `package.json` names.
- When several similar app copies exist, prefer the user-specified path or deployed-source roots such as `/root/.www/<app>` over generated/workspace prototypes, and check `git status` before/after edits in every touched checkout.
- If you accidentally edit a lookalike checkout before the user corrects the path, revert those unintended changes after applying the work in the correct tree.
- Do not assume `pnpm` is directly on PATH; on this VPS, `corepack pnpm` may work even when `pnpm` does not.
- Avoid claiming there is a backend unless code inspection finds one. Many prototype apps are fully client-side with localStorage persistence.
