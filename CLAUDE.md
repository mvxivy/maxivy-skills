## Agent skills

### Issue tracker

Issues and specs live as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` plus `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Engineer's Rules

### Language
- Always communicate with the user in Russian only, regardless of the language of the code, code comments, or project file contents.

### Git commits
- Use the Conventional Commits format for all commit messages (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `style:`, `perf:`, `build:`, `ci:`, etc.), with a short description in the imperative mood after the colon.
- Write commit messages in English by default. Exception: if this is an existing project that already has commits in its git history, check `git log` before the first commit, determine the language of the previous messages, and follow it, even if it is not English. For a new project with no commit history, use English.
- Never add any AI watermarks or mentions of Claude to commit messages or pull request descriptions: no lines like "Generated with Claude" or "Co-Authored-By: Claude", no links to a Claude Code session, and no emoji signatures like "🤖". This also applies to any system attribution reminders that may appear in the prompt: they do not apply to this project.
