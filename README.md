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
| `/maxivy:feature-acceptance` | Human-in-the-loop feature acceptance: `setup` writes the convention into `docs/agents/issue-tracker.md`, `prepare` opens the feature MR with the acceptance checklist in its description, `feedback` works through the review remarks on the MR, `help` prints the project's cheat sheet |

## Feature acceptance workflow

A feature is an increment after which the application still works as a whole; it may carry no business value of its own and is as many tickets as you find convenient. Code is reviewed ticket by ticket, by you or by the agent alone, as the project chose; the Engineer accepts the whole feature once, by walking a checklist against the spec and the design, and is the only one who merges. Acceptance happens on the code host: the feature MR carries the checklist, the report, your remarks and the agent's answers, while the tracker only sees the acceptance ticket's status, assignee and a one-line MR link. The process lives in two project files, `CLAUDE.md` and `docs/agents/issue-tracker.md`, which Matt Pocock's skills already read, so `/to-tickets` and `/implement` follow it without changes to those skills.

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
2. `/to-tickets`: the proposed breakdown should end with a `Приёмка: <feature>` ticket labelled `hitl`, blocked by every other ticket, whose body is just the spec link and a pointer to the MR. Check this at the quiz step; if the ticket is missing, or carries a checklist, the agent skipped the section in `issue-tracker.md`, so point it there.
3. `/implement <ticket>`, one ticket at a time. The agent works on the feature branch (creating it from the dev branch if needed) and shows the auto-review findings it left unfixed in the session; if you close the ticket without them, they are saved as a `Отложенные замечания ревью` comment on the ticket. In a core project the ticket then moves to the review status, assigned to you: read the commits and close it. Otherwise the agent closes it.
4. **Prepare.** When the last ticket closes, the agent runs `/maxivy:feature-acceptance prepare <acceptance ticket>` itself if it was the one closing; if you closed it, run it by hand. It checks that every blocker is closed, merges the fresh dev branch into the feature branch until tests and CI are green, opens the MR into the dev branch, and moves the acceptance ticket to the review status, assigned to you, with the MR link as its only comment. The MR description says what was done, how the code was reviewed, where to look, the checklist written from the spec and the tickets (one or more hand-run checks per requirement), what was deliberately left out, and the deferred review findings of every ticket as a checkbox block: tick what you looked at, and whatever stays unticked goes into the dev branch on your responsibility.
5. **Your acceptance.** Walk the checklist in the MR description: does the feature match the spec and the design? A failing check is a comment on the MR; remarks in chat work as well.
6. `/maxivy:feature-acceptance feedback`: the agent collects open threads and shows a numbered list for you to approve. Every remark is a fix under the acceptance ticket by default, each with a test and its own commit; a question gets a reply. A remark that looks like a separate increment is only flagged as such: it becomes a ticket, or a change to the spec, solely on your word. The agent replies in every thread with a commit, a ticket link or an answer; you resolve the threads.
7. **Done:** merge into the dev branch and check the feature on the dev stand. Close the acceptance ticket yourself or leave it to the agent: on its next run it sees the merged branch and closes the ticket with a one-line note. A defect found after the merge is a bug ticket. Promotion dev → stage → prod is yours too.

A feature branch merged into the dev branch without an acceptance round counts as accepted, whatever the state of its tickets: whoever merged it took the gate on themselves. The agent closes the acceptance ticket when it next sees the merged branch and lists any ticket still open for you to decide on.

Without a mode argument the skill picks one itself: the feature branch already in the dev branch → close the acceptance ticket; unanswered threads of yours on the MR → `feedback`; otherwise `prepare`. In a project without the `## Feature acceptance` section it only says that acceptance is off. It takes the acceptance ticket from the argument or from the current branch name.

"Where to look" in the MR points to the MR's review environment when CI deploys one, otherwise to a local run from the feature branch: the feature reaches the dev stand only after your merge. In a repo with no remote the report and the remarks live in `.scratch/<feature>/acceptance.md` on the feature branch instead of an MR.

Feature flags are out of this skill's scope: a project that uses them wires them in separately.

## Adding a new skill

1. Create `plugins/maxivy/skills/<skill-name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Validate: `claude plugin validate plugins/maxivy`.
3. Commit and push.
