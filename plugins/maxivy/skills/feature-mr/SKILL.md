---
name: feature-mr
description: "The feature MR: opens the merge request of a feature branch into the dev branch once the feature's tickets are done, or works through the review threads on it, in repos whose docs/agents/issue-tracker.md has a `## Feature MR` section."
argument-hint: "[setup | open | feedback | help] [feature branch]"
---

# Feature MR

A feature's tickets commit to one feature branch and reach the dev branch through one MR. This skill opens that MR when the tickets are done and works through the review threads on it. The merge is the Engineer's click and the only gate: tickets were checked against their acceptance criteria one by one, and nothing is re-checked at feature scale.

## Vocabulary

- **Feature**: the tickets `/to-tickets` published from one spec, as many as the Engineer found convenient, with or without business value of their own. On a local tracker, the feature's directory under `.scratch/`; on a real tracker, the tickets whose body names the feature branch.
- **Feature branch**: the branch every ticket of the feature commits to, cut from the dev branch, in the format the tracker section gives.
- **Dev branch**: the branch feature MRs target, named in the `### Branches` rules of `CLAUDE.md` (the prod branch when the project has no dev stand).
- **Feature MR**: the merge request (a pull request on GitHub) from the feature branch into the dev branch. Its description sums the feature up for the Engineer; its threads carry their remarks and your answers.
- **Deferred findings**: the `Отложенные замечания ревью` comments `/implement` left on the feature's tickets. The MR gathers them into one checkbox block; what the Engineer leaves unticked goes into the dev branch on their responsibility.
- **Green**: the typecheck and the full test suite pass locally, the branch is pushed, and CI passes on it.
- **Footprint**: what this skill writes to the tracker: only a ticket the Engineer asked for in feedback. Summaries, remarks and answers live on the MR.

## Project conventions

Read both before any mode:

- The `### Branches` rules in `CLAUDE.md`: the dev branch. If they are missing, the project works without the branch flow, which this skill needs: tell the Engineer to re-run `/maxivy:setup-maxivy-skills` and choose the branch flow, then stop.
- The `## Feature MR` section of `docs/agents/issue-tracker.md`: feature branch format, ticket review, review status. If `docs/agents/issue-tracker.md` is missing, tell the Engineer to run `/setup-matt-pocock-skills` and stop.

The flow is **opt-in** per project: it is on exactly when that section exists. Without it, only an explicit `setup` proceeds; for anything else, tell the Engineer that the feature MR flow is off in this project and `/maxivy:feature-mr setup` turns it on, then stop.

Every tracker operation (fetch a ticket, list a feature's tickets, create a ticket) goes through the workflow in `docs/agents/issue-tracker.md`.

The code host is separate from the tracker (Jira tickets with GitLab code is common). Take it from `git remote -v`:

- GitLab → `glab mr …`
- GitHub → `gh pr …`
- no remote host → **local mode**: the description and the merge command go to the chat, remarks arrive in the conversation, and the Engineer merges locally.

## Pick the mode

An explicit mode argument wins; `setup` and `help` run only on request. Otherwise:

- The feature MR has unresolved threads whose last note is not yours, or the Engineer gave remarks in the conversation → **feedback**.
- Otherwise → **open**.

Find the feature (open and feedback): the argument, a feature branch, a spec path or a slug; else the current branch, when it matches the branch format; else ask.

Then read and follow the mode's file:

- setup → [setup.md](setup.md)
- open → [open.md](open.md)
- feedback → [feedback.md](feedback.md)
- help → [cheatsheet.md](cheatsheet.md)
