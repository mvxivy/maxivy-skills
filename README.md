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
| `/maxivy:feature-mr` | The feature MR: `setup` writes the convention into `docs/agents/issue-tracker.md`, `open` opens the MR of a feature branch into the dev branch with a summary and the deferred review findings, `feedback` works through the review threads on it, `help` prints the project's cheat sheet |

## Feature MR workflow

A feature is the set of tickets `/to-tickets` publishes from one spec; it may carry no business value of its own and is as many tickets as you find convenient. Its tickets commit to one feature branch and reach the dev branch through one MR, which you merge. The merge is the only gate: each ticket is checked against its own acceptance criteria after `/implement` (by you or by the agent alone, as the project chose), and nothing is re-checked at feature scale. The process lives in two project files, `CLAUDE.md` and `docs/agents/issue-tracker.md`, which Matt Pocock's skills already read, so `/to-tickets` and `/implement` follow it without changes to those skills.

### Once per project

1. `/setup-matt-pocock-skills`, if not done yet: creates `docs/agents/issue-tracker.md` (where tickets live and how to work with them).
2. `/maxivy:setup-maxivy-skills`, answering yes to the branch flow: it finds the dev, stage and prod branches (or asks about them in a quiz) and writes the `### Branches` rule into `CLAUDE.md`: feature branches are cut from the dev branch, their MRs target it, and only the Engineer merges. Simple projects answer no and skip the flow altogether.
3. `/maxivy:feature-mr setup`, the explicit opt-in (the flow stays off in a project until you run it). It asks one question: is the project a core domain for you (every ticket passes your code review before it closes) or a supporting or generic one (tickets close after the agent's own review, the merge is the only human gate)? Then it adds a `## Feature MR` section to `docs/agents/issue-tracker.md` with the feature branch format (e.g. `feature/user-login`), the ticket review rule and, for a core project, the review status (for Jira, read from your workflow). It shows a draft first, creates a missing label on the tracker only after you confirm, and ends by printing a cheat sheet with this project's real branches, statuses and example commands. `/maxivy:feature-mr help` prints it again at any time, rebuilt from the current configuration.

Commit these files yourself: the skills leave them uncommitted.

### Per feature

```
/to-spec → /to-tickets → (/implement → your review) × N → open → you read the MR → feedback → … → you merge
```

1. `/to-spec` as usual.
2. `/to-tickets`: every ticket carries its acceptance criteria and a `Ветка: <feature branch>` line. Check the criteria at the quiz step: they are the only check the feature gets. If the branch line is missing, the agent skipped the section in `issue-tracker.md`, so point it there.
3. `/implement <ticket>`, one ticket at a time. The agent works on the feature branch (creating it from the dev branch if needed) and shows the auto-review findings it left unfixed in the session; if you close the ticket without them, they are saved as a `Отложенные замечания ревью` comment on the ticket. In a core project the ticket then moves to the review status, assigned to you: read the commits and close it. Otherwise the agent closes it.
4. **Open.** When the last ticket closes, the agent runs `/maxivy:feature-mr open <feature branch>` itself if it was the one closing; if you closed it, run it by hand. It lists the feature's tickets (an open one is your call), merges the fresh dev branch into the feature branch until tests and CI are green, and opens the MR into the dev branch. The description says what was done, how the code was reviewed, where to look, what was deliberately left out, and the deferred review findings of every ticket as a checkbox block: tick what you looked at, and whatever stays unticked goes into the dev branch on your responsibility.
5. **Your read.** Read the MR; remarks are comments on it, or in chat.
6. `/maxivy:feature-mr feedback`: the agent collects open threads and shows a numbered list for you to approve. Every remark is a fix by default, each with a test and its own commit; a question gets a reply. A remark that looks like a separate increment is only flagged as such: it becomes a ticket, or a change to the spec, solely on your word. The agent replies in every thread with a commit, a ticket link or an answer; you resolve the threads.
7. **Done:** merge into the dev branch and check the feature on the dev stand. A defect found after the merge is a bug ticket. Promotion dev → stage → prod is yours too.

Without a mode argument the skill picks one itself: unanswered threads of yours on the MR → `feedback`; otherwise `open`. In a project without the `## Feature MR` section it only says that the flow is off. It takes the feature from the argument or from the current branch name.

"Where to look" in the MR points to the MR's review environment when CI deploys one, otherwise to a local run from the feature branch: the feature reaches the dev stand only after your merge. In a repo with no remote the description and the merge command go to the chat instead of an MR.

Feature flags are out of this skill's scope: a project that uses them wires them in separately.

## Adding a new skill

1. Create `plugins/maxivy/skills/<skill-name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Validate: `claude plugin validate plugins/maxivy`.
3. Commit and push.
