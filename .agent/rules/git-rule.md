---
trigger: always_on
---

Always follow this Git & GitHub workflow for THIS repository. Never bypass it unless the user explicitly says to ignore it “just this once”.

Context and assumptions:
- This project is a Git repository with a remote "origin" on GitHub.
- The local environment has the `gh` CLI installed and authenticated.
- The default branch is `main` (if the actual default branch is different, adjust the commands accordingly).
- The user wants every coding task to go through: new branch → commit → push → pull request.

GENERAL RULES
- Never commit directly to `main` or the default branch.
- For each feature/fix/refactor task, work on a dedicated topic branch.
- At the end of a task, ensure:
  1) local changes are committed,
  2) the branch is pushed to GitHub,
  3) a pull request is created with `gh pr create`.
- If you cannot execute shell commands directly, ALWAYS output the exact commands the user should run.

WHEN STARTING A NEW CODING TASK
Whenever the user asks for a change (new feature, bug fix, refactor, etc.) in this repo, do the following BEFORE modifying code:

1. Check that the working tree is clean.
   - If there are uncommitted changes:
     - Ask the user whether to:
       - (a) commit them on the current branch,
       - (b) stash them, or
       - (c) discard them.
     - Do NOT create a new branch on top of a dirty working tree unless the user explicitly tells you to.

2. Create a new branch for this task.
   - Suggest a short, descriptive branch name based on the task. For example:
       - `feature/<short-description>`
       - `fix/<short-description>`
   - Then use this pattern (adjust `main` if needed):

       git fetch origin
       git switch main
       git pull origin main
       git switch -c <branch-name>

   - If the repo already uses another default branch name (like `master` or `develop`), adapt the commands accordingly.

3. Confirm branch context.
   - Make sure all subsequent code edits, instructions, and commands are clearly assumed to be on this new branch.
   - If you show any `git` commands afterward, they must assume the current branch is this topic branch.

IMPLEMENTATION PHASE
While implementing or modifying code on the new branch:

1. Keep changes logically grouped.
   - Try to align commits with logical units of work (e.g., “add API endpoint”, “update tests”, “refactor X”).
   - Avoid committing unrelated changes together.

2. Encourage tests and checks:
   - If the repo uses tests or linters (e.g., `pytest`, `uv run`, `npm test`, etc.), propose commands like:
       - `uv run pytest`
       - or any project-specific test command, if known.
   - Before committing, suggest running the appropriate test command.

COMMIT PHASE (AFTER IMPLEMENTATION IS COMPLETE)
When the implementation and basic tests are done for this task:

1. Show the user what will be committed:
   - Suggest commands such as:

       git status
       git diff

2. Stage the changes:
   - Prefer explicit `git add` over `git add .` unless the user prefers otherwise.
   - Example:

       git add <files>

3. Create a descriptive commit message:
   - Use a clear, concise, present-tense message describing what the change does, e.g.:
       git commit -m "Add API endpoint to list LLM responses by category"

4. Only commit when the work is in a consistent, buildable state.
   - If the work is incomplete, ask the user if they want:
     - a WIP (work-in-progress) commit, or
     - to continue without committing yet.

PUSH & PULL REQUEST PHASE
Once there is at least one commit for this task:

1. Push the branch to GitHub:

       git push -u origin <branch-name>

2. Create a pull request using `gh`:
   - Prefer using the existing commit messages / diff as the PR description:

       gh pr create --fill

   - If the user prefers to review/edit the PR in a browser, you can also propose:

       gh pr create --fill --web

3. PR title and body:
   - Ensure the PR title is clear and matches the main change (you can reuse the first commit message or a refined version).
   - The body should briefly summarize:
     - What was changed,
     - Why it was changed,
     - Any testing done.

4. Remind the user:
   - After creating the PR, remind the user that:
     - The implementation is now on branch `<branch-name>`,
     - A pull request has been created,
     - Further feedback or follow-up changes should go into the same branch until the PR is merged.

IF SOMETHING FAILS OR IS AMBIGUOUS
- If commands fail (e.g., branch already exists, push rejected, non-fast-forward), do NOT guess silently.
- Explain what likely happened and propose the exact commands or options to resolve it (for example, choosing between rebase and merge).
- When in doubt, ask the user which resolution strategy they prefer.

SUMMARY
For every coding task in this repo, always:
1. Ensure a clean working tree.
2. Create and switch to a new branch for the task.
3. Implement changes on that branch.
4. Commit the changes with a clear message.
5. Push the branch to `origin`.
6. Create a pull request via `gh pr create`.
Never skip these steps unless the user explicitly instructs you to.
