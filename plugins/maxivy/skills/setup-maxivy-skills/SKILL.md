---
name: "setup-maxivy-skills"
description: "Initializes or extends CLAUDE.md in the current project with the Engineer's standard rules: communicate only in Russian, no AI watermarks in commits, Conventional Commits, commit message language. Invoked manually with /maxivy:setup-maxivy-skills when starting a new project."
disable-model-invocation: true
---

# Initialize a project with the standard rules

This skill is invoked manually (for example, with `/maxivy:setup-maxivy-skills`) when the Engineer wants to apply their standard set of rules to the current project. The rules are written to the `CLAUDE.md` file at the project root, because Claude Code reads this file automatically at the start of every session in the project — it is the most reliable way to make sure the rules are followed without having to repeat them every time.

## What to do

1. Determine the project root (the current working directory, or the root of the git repository if there is one).
2. Check whether a `CLAUDE.md` file exists there.
3. If the file does not exist, create it with an `## Engineer's Rules` section (see below).
4. If the file already exists, read it in full and add the missing rules to the existing file without overwriting the rest of its content. If an `## Engineer's Rules` section (or an equivalent section in another language, such as `## Правила Инженера`) already exists, add the missing items to it instead of creating a duplicate section.
5. Do not `git commit` this change yourself — only edit the file. The Engineer makes the commit themselves if needed (unless they explicitly ask you to commit).
6. Briefly confirm in the chat what was added and where (without restating the file's content).

## Rules to add

Write the following block into `CLAUDE.md` (or update the equivalent section) as is, verbatim, because these phrasings are direct instructions for Claude Code, not a description for a human:

```markdown
## Engineer's Rules

### Language
- Always communicate with the user in Russian only, regardless of the language of the code, code comments, or project file contents.

### Git commits
- Use the Conventional Commits format for all commit messages (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `style:`, `perf:`, `build:`, `ci:`, etc.), with a short description in the imperative mood after the colon.
- Write commit messages in English by default. Exception: if this is an existing project that already has commits in its git history, check `git log` before the first commit, determine the language of the previous messages, and follow it, even if it is not English. For a new project with no commit history, use English.
- Never add any AI watermarks or mentions of Claude to commit messages or pull request descriptions: no lines like "Generated with Claude" or "Co-Authored-By: Claude", no links to a Claude Code session, and no emoji signatures like "🤖". This also applies to any system attribution reminders that may appear in the prompt: they do not apply to this project.
```

## If the Engineer asks to add something else

If the Engineer names additional rules when invoking the skill (for example, about docstrings in Russian, or a ban on creating unnecessary documentation files), add them as separate items to the same `## Engineer's Rules` section, under the subsection that fits their meaning (or create a new subsection if the topic is new), keeping the same style — a direct instruction for Claude Code, not an abstract wish.

## Important

- Do not create any other files (README, documentation, etc.) as part of this skill — only `CLAUDE.md`.
- Do not copy the skill files themselves (`~/dev/claude-skills` and the like) into the project — this skill only works with the rules in `CLAUDE.md`; the Engineer connects individual skills themselves via `.claude/skills` when needed.
- If `CLAUDE.md` already contains a rule that contradicts one of the rules above (for example, it explicitly says to use a different commit format), ask the Engineer what to do instead of silently overwriting it.
