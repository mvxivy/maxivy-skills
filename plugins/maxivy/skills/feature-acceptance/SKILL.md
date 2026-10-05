---
name: feature-acceptance
description: "Feature acceptance, the Engineer's gate before a feature reaches the dev branch, in repos whose docs/agents/issue-tracker.md has a `## Feature acceptance` section. Use to prepare acceptance once every blocker of an acceptance ticket is closed, or to work through review feedback on a feature MR."
argument-hint: "[setup | prepare | feedback | help] [acceptance ticket]"
---

# Feature acceptance

The Engineer accepts each feature once, as a whole, before it reaches the dev branch. Agents implement and auto-review ticket by ticket on the feature branch; this skill runs the **gate** above them.

## Vocabulary

- **Acceptance ticket**: a ticket the Engineer works, not an agent. It carries the HITL label and is blocked by every ticket of the feature, so it frees itself when the last blocker closes.
- **Feature**: the set of tickets blocking an acceptance ticket. There is no separate feature or epic entity.
- **Dev branch**: the branch feature MRs target, named in the `### Branches` rules of `CLAUDE.md` (the prod branch when the project has no dev stand).
- **Feature branch**: the branch every ticket of the feature commits to, cut from the dev branch and named after the acceptance ticket.
- **Feature MR**: the merge request (a pull request on GitHub) from the feature branch into the dev branch. Its description is the acceptance report.
- **Round**: one pass of prepare → the Engineer reviews → feedback. A feature takes as many rounds as it needs; each round ends in a round note on the MR, `Раунд N: …`.
- **Green**: the typecheck and the full test suite pass locally, the branch is pushed, and CI passes on it.
- **Hand over**: move the acceptance ticket to the review status, assign it to the Engineer, and post the round note on the MR.
- **Merge gate**: the merge into the dev branch is the Engineer's click, as `### Branches` in `CLAUDE.md` says. Leave the feature MR open for them.

## Project conventions

Read both before any mode:

- The `### Branches` rules in `CLAUDE.md`: the dev branch. If they are missing, the project works without the branch flow, which acceptance needs: tell the Engineer to re-run `/maxivy:setup-maxivy-skills` and choose the branch flow, then stop.
- The `## Feature acceptance` section of `docs/agents/issue-tracker.md`: HITL label, review status, feature branch format. If `docs/agents/issue-tracker.md` is missing, tell the Engineer to run `/setup-matt-pocock-skills` and stop.

Acceptance is **opt-in** per project: it is on exactly when that section exists. Without it, only an explicit `setup` proceeds; for anything else, tell the Engineer that acceptance is off in this project and `/maxivy:feature-acceptance setup` turns it on, then stop.

Every tracker operation (fetch a ticket, list its blockers, comment, label, change status, create a ticket) goes through the workflow in `docs/agents/issue-tracker.md`.

The code host is separate from the tracker (Jira tickets with GitLab code is common). Take it from `git remote -v`:

- GitLab → `glab mr …`
- GitHub → `gh pr …`
- no remote host → **local mode**: the acceptance report and round notes go into the acceptance ticket, feedback arrives in its `## Comments` or the conversation, and the Engineer merges locally.

## Pick the mode

An explicit mode argument wins; `setup` and `help` run only on request. Otherwise:

- The feature MR has unresolved discussions whose last note is not yours, or the Engineer gave remarks in the conversation → **feedback**.
- Otherwise → **prepare**.

Find the acceptance ticket (prepare and feedback): the argument; else the key in the current branch name, matched against the branch format; else ask.

Then read and follow the mode's file:

- setup → [setup.md](setup.md)
- prepare → [prepare.md](prepare.md)
- feedback → [feedback.md](feedback.md)
- help → [cheatsheet.md](cheatsheet.md)
