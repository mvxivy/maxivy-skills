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
| `/maxivy:setup-maxivy-skills` | Adds the Engineer's standard rules to the project's `CLAUDE.md`; asks whether the project uses the branch flow (feature branches and MRs) and, if so, records its dev/stage/prod branches |
| `/maxivy:feature-acceptance` | Human-in-the-loop feature acceptance: `setup` writes the convention into `docs/agents/issue-tracker.md`, `prepare` opens the feature MR with a manual-test checklist, `feedback` works through the review remarks, `help` prints the project's cheat sheet |

## Feature acceptance workflow

A feature is an increment after which the application still works as a whole; it may carry no business value of its own and is as many tickets as you find convenient. Code is reviewed ticket by ticket, by you or by the agent alone, as the project chose; the Engineer accepts the whole feature once, by walking a checklist against the spec and the design, and is the only one who merges. The process lives in two project files, `CLAUDE.md` and `docs/agents/issue-tracker.md`, which Matt Pocock's skills already read, so `/to-tickets` and `/implement` follow it without changes to those skills.

### Once per project

1. `/setup-matt-pocock-skills`, if not done yet: creates `docs/agents/issue-tracker.md` (where tickets live and how to work with them).
2. `/maxivy:setup-maxivy-skills`, answering yes to the branch flow: it finds the dev, stage and prod branches (or asks about them in a quiz) and writes the `### Branches` rule into `CLAUDE.md`: feature branches are cut from the dev branch, their MRs target it, and only the Engineer merges. Simple projects answer no and skip acceptance altogether.
3. `/maxivy:feature-acceptance setup`, the explicit opt-in (acceptance stays off in a project until you run it). It asks one question: is the project a core domain for you (every ticket passes your code review before it closes) or a supporting or generic one (tickets close after the agent's own review, acceptance is the only human gate)? Then it adds a `## Feature acceptance` section to `docs/agents/issue-tracker.md` with the `hitl` label, the review status (for Jira, read from your workflow), the feature branch format (e.g. `feature/PROJ-100-user-login`), the reviewer and the ticket review rule. It shows a draft first, creates a missing label on the tracker only after you confirm, and ends by printing a cheat sheet with this project's real branches, labels, statuses and example commands. `/maxivy:feature-acceptance help` prints it again at any time, rebuilt from the current configuration.

Commit these files yourself: the skills leave them uncommitted.

### Per feature

```
/to-spec → /to-tickets → (/implement → your review) × N → prepare → you walk the checklist → feedback → … → you merge
```

1. `/to-spec` as usual.
2. `/to-tickets`: the proposed breakdown should end with a `Приёмка: <feature>` ticket labelled `hitl`, blocked by every other ticket, with the feature checklist in its body: one or more hand-run checks per requirement. Check both at the quiz step; if they are missing, the agent skipped the section in `issue-tracker.md`, so point it there.
3. `/implement <ticket>`, one ticket at a time. The agent works on the feature branch (creating it from the dev branch if needed) and records auto-review findings it chose not to fix as a `Отложенные замечания ревью` comment on the ticket. In a core project the ticket then moves to the review status, assigned to you: read the commits and close it. Otherwise the agent closes it.
4. **Prepare.** When the last ticket closes, the agent runs `/maxivy:feature-acceptance prepare <acceptance ticket>` itself if it was the one closing; if you closed it, run it by hand. It checks that every blocker is closed, merges the fresh dev branch into the feature branch until tests and CI are green, opens the MR into the dev branch, and moves the acceptance ticket to the review status, assigned to you. The MR description says what was done, how the code was reviewed, where to look, the checklist carried from the acceptance ticket and reconciled with what was built, what was deliberately left out, and which review findings were left.
5. **Your acceptance.** Walk the checklist: does the feature match the spec and the design? A failing check is a comment on the MR; remarks in chat work as well.
6. `/maxivy:feature-acceptance feedback`: the agent collects open threads and shows a numbered list for you to approve. Every remark is a fix under the acceptance ticket by default, each with a test and its own commit; a question gets a reply. A remark that looks like a separate increment is only flagged as such: it becomes a ticket, or a change to the spec, solely on your word. The agent replies in every thread with a commit, a ticket link or an answer; you resolve the threads.
7. **Done:** close the acceptance ticket and merge into the dev branch; check the feature on the dev stand. A defect found after the merge is a bug ticket. Promotion dev → stage → prod is yours too.

Without a mode argument the skill picks one itself: unanswered threads of yours on the MR → `feedback`; otherwise `prepare`. In a project without the `## Feature acceptance` section it only says that acceptance is off. It takes the acceptance ticket from the argument or from the current branch name.

"Where to look" in the MR points to the MR's review environment when CI deploys one, otherwise to a local run from the feature branch: the feature reaches the dev stand only after your merge.

Feature flags are out of this skill's scope: a project that uses them wires them in separately.

## Adding a new skill

1. Create `plugins/maxivy/skills/<skill-name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Validate: `claude plugin validate plugins/maxivy`.
3. Commit and push.
