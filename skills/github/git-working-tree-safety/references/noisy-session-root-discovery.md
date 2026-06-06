# Noisy session-root discovery

Observed pattern for `~/.hermes`-style roots:

1. Inspect the outer root first:
   - `git status --porcelain --ignore-submodules=none`
   - `git remote -v`
   - `git branch --show-current`
2. Look for nested repos or gitlinks inside the outer tree.
3. Inspect the nested repo directly:
   - `git -C <nested> status --porcelain --ignore-submodules=none`
   - `git -C <nested> remote -v`
   - `git -C <nested> branch --show-current`
4. Commit the nested repo if the actual file changes live there; commit the parent only if you intend to publish the gitlink pointer.
5. Push with an explicit refspec rather than assuming the local branch name matches the desired remote branch:
   - `git -C <nested> push <remote> HEAD:<branch>`
   - `git -C <parent> push <remote> HEAD:<branch>`
6. Verify the remote ref after each push:
   - `git -C <repo> ls-remote <remote> refs/heads/<branch>`

Common symptom: the parent root is full of runtime artifacts, while the publishable change lives in a child repo with its own branch and remote configuration.