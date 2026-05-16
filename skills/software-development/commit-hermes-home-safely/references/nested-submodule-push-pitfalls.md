# Nested submodule and push-pipeline pitfalls

Session pattern:
- Root repo: `/root/.hermes`
- Dirty top-level view was caused by nested `hermes-agent` state, not the parent repo itself.
- Inside `hermes-agent`, there were untracked nested worktrees/repositories (`nova-platform/`, `tinker-atropos/`) plus a standalone markdown artifact (`Opex_BR_Hackaton.md`).
- One runtime artifact at the root level was `webui/.login_attempts.json`; it was best handled by adding it to the root `.gitignore` rather than committing it.

Useful checks before staging a parent repo that contains a submodule or nested repo:
1. `git status --porcelain --ignore-submodules=none`
2. `git diff --submodule=log -- <submodule-path>`
3. `git -C <submodule> status --porcelain --ignore-submodules=none`
4. If the submodule contains nested repositories, run the same status check inside each nested repo.

Important outcome from this session:
- A local commit in `hermes-agent` succeeded, but `git -C hermes-agent push origin main` failed with `Permission to NousResearch/hermes-agent.git denied to demetriusnunes-gh`.
- The parent `roger-hermes` repo could still be pushed independently after recording the desired root-level changes.

Guidance:
- Treat submodule pointer changes and parent-repo commits as separate operations.
- Verify the actual remote owner for every nested repo before assuming a push failure is an auth problem.
- A clean parent repo does not guarantee a clean submodule, and a clean submodule does not guarantee its upstream is writable.
- If a runtime artifact appears during the workflow, prefer `.gitignore` updates over versioning it unless the user explicitly asked to keep it.