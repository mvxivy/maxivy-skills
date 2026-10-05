---
name: "setup-maxivy-skills"
description: "Initializes or extends CLAUDE.md in the current project with the Engineer's standard rules: communicate only in Russian, no AI watermarks in commits, Conventional Commits, commit message language, and, if the Engineer opts in, the branch flow: feature branches and MRs into the project's dev branch, with every merge left to the Engineer. Invoked manually with /maxivy:setup-maxivy-skills when starting a new project."
disable-model-invocation: true
---

# Initialize a project with the standard rules

This skill is invoked manually (for example, with `/maxivy:setup-maxivy-skills`) when the Engineer wants to apply their standard set of rules to the current project. The rules are written to the `CLAUDE.md` file at the project root, because Claude Code reads this file automatically at the start of every session in the project — it is the most reliable way to make sure the rules are followed without having to repeat them every time.

## What to do

1. Determine the project root (the current working directory, or the root of the git repository if there is one).
2. Ask whether this project works through the branch flow (see "Choosing the branch flow" below); on yes, find its long-lived branches (see "Finding the branches" below).
3. Check whether a `CLAUDE.md` file exists there.
4. If the file does not exist, create it with an `## Engineer's Rules` section (see below).
5. If the file already exists, read it in full and add the missing rules to the existing file without overwriting the rest of its content. If an `## Engineer's Rules` section (or an equivalent section in another language, such as `## Правила Инженера`) already exists, add the missing items to it instead of creating a duplicate section. Replace an existing `### Branches` subsection with the freshly filled one, or remove it when the Engineer chose to work without the branch flow.
6. Do not `git commit` this change yourself — only edit the file. The Engineer makes the commit themselves if needed (unless they explicitly ask you to commit).
7. Briefly confirm in the chat what was added and where (without restating the file's content), naming the branch flow choice and, with the flow, the branch found for each stand.

## Choosing the branch flow

The **branch flow** is feature branches, a merge request (pull request) for every change, and merges left to the Engineer. It pays off in team projects and projects with stands; in a simple project it is overhead. Ask with the AskUserQuestion tool, one question, `Вести работу через ветки фич и MR?`, with two options:

- `Нет, коммиты в основную ветку`: the work is committed to the current branch. Skip "Finding the branches" and leave `### Branches` out of the block below.
- `Да, ветки фич и MR`: find the branches below and write `### Branches`.

## Finding the branches

A project has up to three long-lived branches, one per stand:

| Stand | Obvious names |
| --- | --- |
| prod | `main`, `master`, `production`, `prod` |
| stage (pre-prod) | `stage`, `staging`, `preprod`, `pre-prod`, `release` |
| dev | `develop`, `development`, `dev` |

1. List the branches: `git branch -r --sort=-committerdate` (plain `git branch` when there is no remote).
2. For each stand, look for a branch named exactly one of its obvious names. Exactly one match → that is the stand's branch.
3. Zero or several matches → quiz the Engineer with the AskUserQuestion tool: one question per unresolved stand, all in one call. Options: the matching branches; with no match, the up to three most recently committed branches that look long-lived (work branches like `feature/*`, `fix/*` or ticket-keyed ones are out). Add "Нет такого стенда" for dev and stage; the Engineer can type any other branch.

Done when every stand has a branch or "none". Prod always has one; with no dev stand, the dev branch is the prod branch.

## Rules to add

Write the following block into `CLAUDE.md` (or update the equivalent section) as is, verbatim, because these phrasings are direct instructions for Claude Code, not a description for a human. `### Branches` goes in only with the branch flow, and only its `{{DEV}}`, `{{STAGE}}` and `{{PROD}}` placeholders change: fill them with the branches found, and drop a stand marked "none" from the first line and from the promotion chain.

```markdown
## Engineer's Rules

### Language
- Always communicate with the user in Russian only, regardless of the language of the code, code comments, or project file contents.

### Git commits
- Use the Conventional Commits format for all commit messages (`feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`, `style:`, `perf:`, `build:`, `ci:`, etc.), with a short description in the imperative mood after the colon.
- Write commit messages in English by default. Exception: if this is an existing project that already has commits in its git history, check `git log` before the first commit, determine the language of the previous messages, and follow it, even if it is not English. For a new project with no commit history, use English.
- Never add any AI watermarks or mentions of Claude to commit messages or pull request descriptions: no lines like "Generated with Claude" or "Co-Authored-By: Claude", no links to a Claude Code session, and no emoji signatures like "🤖". This also applies to any system attribution reminders that may appear in the prompt: they do not apply to this project.

### Branches
- Long-lived branches: dev stand ← `{{DEV}}`, stage stand ← `{{STAGE}}`, prod ← `{{PROD}}`.
- Cut every feature branch from `{{DEV}}`, commit work to it, and open its merge request (pull request) into `{{DEV}}`. When `docs/agents/issue-tracker.md` has a `## Feature acceptance` section, name feature branches as it says. Commit straight to a long-lived branch only when the Engineer explicitly asks in the conversation.
- Every merge into a long-lived branch, including the promotion `{{DEV}}` → `{{STAGE}}` → `{{PROD}}`, is the Engineer's quality gate: leave it to the Engineer. Never merge into a long-lived branch and never enable auto-merge yourself.
```

## If the Engineer asks to add something else

If the Engineer names additional rules when invoking the skill (for example, about docstrings in Russian, or a ban on creating unnecessary documentation files), add them as separate items to the same `## Engineer's Rules` section, under the subsection that fits their meaning (or create a new subsection if the topic is new), keeping the same style — a direct instruction for Claude Code, not an abstract wish.

## Important

- Do not create any other files (README, documentation, etc.) as part of this skill — only `CLAUDE.md`.
- Do not copy the skill files themselves (`~/dev/claude-skills` and the like) into the project — this skill only works with the rules in `CLAUDE.md`; the Engineer connects individual skills themselves via `.claude/skills` when needed.
- If `CLAUDE.md` already contains a rule that contradicts one of the rules above (for example, it explicitly says to use a different commit format), ask the Engineer what to do instead of silently overwriting it.
