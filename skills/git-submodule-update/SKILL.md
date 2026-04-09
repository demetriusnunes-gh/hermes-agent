---
name: git-submodule-update
description: Procedure for committing and pushing changes in ~/.hermes that include submodule updates
category: software-development
---

# Git Submodule Update Procedure

## When to Use
Use this procedure when you need to commit and push changes in the ~/.hermes directory that include:
- New or modified files in the main repository
- Changes to submodules (particularly hermes-agent)
- Both of the above scenarios

## Prerequisites\n- You have write access to the target GitHub repository\n- You are working in the ~/.hermes directory\n- Git is installed and configured

## Procedure

### 1. Check Current Status
```bash
cd ~/.hermes
git status --porcelain
```

Look for:
- Modified files in the main repository (shown as `M path/to/file`)
- Untracked files/directories (shown as `?? path/to/`)
- Submodule modifications (shown as `M submodule-name` with dirty indicator)

### 2. Investigate Submodule Changes (if any)
If you see `M submodule-name` in git status:
```bash
# Check what changed in the submodule
git diff submodule-name

# Or navigate into the submodule to see details
cd submodule-name
git status --porcelain
git diff  # or git diff --stat for summary
cd ..
```

### 3. Stage All Changes
```bash
# Stage new/modified files in main repo
git add path/to/new-or-modified-files/

# Stage new skill directories or other new files
git add skills/category/skill-name/

# Stage submodule updates (records the new commit SHA)
git add submodule-name
```

### 4. Verify Staged Changes
```bash
git status --porcelain
```
Should show:
- `A` for newly added files
- `M` for modified files (including submodules)
- No `??` entries for items you want to commit

### 5. Create Descriptive Commit Message
Use conventional commits format:
```
feat(scope): description of what was added
chore(scope): description of maintenance/update work

Optional body for additional context
```

Examples:
- `feat(skills): add daily-medication-reminder and one-time-reminder skills`
- `chore(deps): update hermes-agent submodule dependency lock`
- `feat(skills): add new skill; chore(deps): update submodule reference`

### 6. Commit and Push
```bash
git commit -m "your descriptive message here"
git push origin master
```

## Key Learnings from Experience
- The `hermes-agent` directory is a git submodule, not a regular directory
- When a submodule shows as modified (`M hermes-agent`), it means the recorded commit SHA has changed
- You must `git add hermes-agent` to record the new submodule commit in the main repo
- Always verify what changed in submodules before committing to avoid committing unintended states
- Group related changes in commit messages using conventional commits style for clarity

## Verification
After pushing, you can verify by:
1. Checking the GitHub repository shows your new commit
2. Confirming the submodule points to the correct commit
3. Ensuring new skills are visible in the skills directory

## Troubleshooting
- If you see "fatal: no submodule mapping found": Check .gitmodules file exists and is properly configured
- If push fails due to non-fast-forward: Pull first, resolve any conflicts, then push again
- If submodule shows wrong commit: Navigate to submodule, checkout correct commit, then update reference in main repo