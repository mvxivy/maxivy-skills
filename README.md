# maxivy-skills

A personal Claude Code plugin marketplace with the `maxivy` plugin.

## Installation

```shell
/plugin marketplace add mvxivy/maxivy-skills
/plugin install maxivy@maxivy-skills
```

To pick up newly pushed commits, refresh the marketplace, update the plugin, then restart Claude Code:

```shell
/plugin marketplace update maxivy-skills
/plugin update maxivy@maxivy-skills
```

The plugin has no `version` in `plugin.json`, so an install is pinned to a commit: a marketplace update alone, or a reinstall, keeps the old commit.

## Skills

| Command | What it does |
| --- | --- |
| `/maxivy:setup-maxivy-skills` | Adds the Engineer's standard rules to the project's `CLAUDE.md`, including the dev/stage/prod branches it finds or asks about |
| `/maxivy:feature-acceptance` | Human-in-the-loop feature acceptance: `setup` writes the convention into `docs/agents/issue-tracker.md`, `prepare` opens the feature MR with a manual-test checklist, `feedback` works through the review remarks, `help` prints the project's cheat sheet |

## Feature acceptance workflow

Agents implement and auto-review a feature ticket by ticket on a feature branch; the Engineer accepts the whole feature once, in its MR, and is the only one who merges. The process lives in two project files, `CLAUDE.md` and `docs/agents/issue-tracker.md`, which Matt Pocock's skills already read, so `/to-tickets` and `/implement` follow it without changes to those skills.

### Once per project

1. `/setup-matt-pocock-skills`, if not done yet: creates `docs/agents/issue-tracker.md` (where tickets live and how to work with them).
2. `/maxivy:setup-maxivy-skills`: finds the dev, stage and prod branches (or asks about them in a quiz) and writes the `### Branches` rule into `CLAUDE.md`: feature branches are cut from the dev branch, their MRs target it, and only the Engineer merges.
3. `/maxivy:feature-acceptance setup`: adds a `## Feature acceptance` section to `docs/agents/issue-tracker.md` with the `hitl` label, the review status (for Jira, read from your workflow), the feature branch format (e.g. `feature/PROJ-100-user-login`) and the reviewer. It shows a draft first, creates a missing label on the tracker only after you confirm, and ends by printing a cheat sheet with this project's real branches, labels, statuses and example commands. `/maxivy:feature-acceptance help` prints it again at any time, rebuilt from the current configuration.

Commit these files yourself: the skills leave them uncommitted.

### Per feature

```
/to-spec → /to-tickets → /implement × N → prepare → you review → feedback → … → you merge
```

1. `/to-spec` as usual.
2. `/to-tickets`: the proposed breakdown should end with a `Приёмка: <feature>` ticket labelled `hitl` and blocked by every other ticket. Check it at the quiz step; if it is missing, the agent skipped the section in `issue-tracker.md`, so point it there.
3. `/implement <ticket>`, one ticket at a time. The agent works on the feature branch (creating it from the dev branch if needed), and records auto-review findings it chose not to fix as a `Отложенные замечания ревью` comment on the ticket.
4. **Prepare.** When the last blocker closes, the agent runs `/maxivy:feature-acceptance prepare <acceptance ticket>` itself; otherwise run it by hand. It checks that every blocker is closed, merges the fresh dev branch into the feature branch until tests and CI are green, opens the MR into the dev branch, and moves the acceptance ticket to the review status, assigned to you. The MR description says what was done, where to look, a checklist built from the spec's user stories, what was deliberately left out, and which review findings were left.
5. **Your review.** Comment on the code in the MR and walk the checklist; a failing check is a comment too. Remarks in chat work as well.
6. `/maxivy:feature-acceptance feedback`: the agent collects open threads and shows a numbered list, each remark marked fix, ticket or reply, for you to approve. Fixes land on the feature branch, each with a test and its own commit. Large remarks become new tickets blocking acceptance, so it is `/implement` and `prepare` again. The agent replies in every thread with a commit, a ticket link or an answer; you resolve the threads.
7. **Done:** you merge into the dev branch. Promotion dev → stage → prod is yours too.

Without a mode argument the skill picks one itself: no section in the tracker file → `setup`; unanswered threads of yours on the MR → `feedback`; otherwise `prepare`. It takes the acceptance ticket from the argument or from the current branch name.

"Where to look" in the MR points to the MR's review environment when CI deploys one, otherwise to a local run from the feature branch: the feature reaches the dev stand only after your merge.

## Adding a new skill

1. Create `plugins/maxivy/skills/<skill-name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Validate: `claude plugin validate plugins/maxivy`.
3. Commit and push.
