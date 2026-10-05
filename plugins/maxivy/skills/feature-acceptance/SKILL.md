---
name: feature-acceptance
description: "Feature acceptance, the Engineer's gate before a feature reaches main. Use to set up the acceptance convention in a repo, to prepare acceptance once every blocker of an acceptance ticket is closed, or to work through review feedback on a feature MR."
argument-hint: "[setup | prepare | feedback] [acceptance ticket]"
---

# Feature acceptance

The Engineer accepts each feature once, as a whole, before it reaches `main`. Agents implement and auto-review ticket by ticket on the feature branch; this skill runs the **gate** above them.

## Vocabulary

- **Acceptance ticket**: a ticket the Engineer works, not an agent. It carries the HITL label and is blocked by every ticket of the feature, so it frees itself when the last blocker closes.
- **Feature**: the set of tickets blocking an acceptance ticket. There is no separate feature or epic entity.
- **Feature branch**: the branch every ticket of the feature commits to, named after the acceptance ticket.
- **Feature MR**: the merge request (a pull request on GitHub) from the feature branch into `main`. Its description is the acceptance report.
- **Round**: one pass of prepare → the Engineer reviews → feedback. A feature takes as many rounds as it needs; each round ends in a round note on the MR, `Раунд N: …`.
- **Green**: the typecheck and the full test suite pass locally, the branch is pushed, and CI passes on it.
- **Hand over**: move the acceptance ticket to the review status, assign it to the Engineer, and post the round note on the MR.
- **Merge gate**: the merge into `main` is the Engineer's click. Leave the feature MR open for them: never merge it, never push to `main`, never enable auto-merge.

## Project conventions

The project's specifics (HITL label, review status, branch format, main branch, stage) live in the `## Feature acceptance` section of `docs/agents/issue-tracker.md`. Read it before any mode. If `docs/agents/issue-tracker.md` is missing, tell the Engineer to run `/setup-matt-pocock-skills` and stop.

Every tracker operation (fetch a ticket, list its blockers, comment, label, change status, create a ticket) goes through the workflow that file describes.

The code host is separate from the tracker (Jira tickets with GitLab code is common). Take it from `git remote -v`:

- GitLab → `glab mr …`
- GitHub → `gh pr …`
- no remote host → **local mode**: the acceptance report and round notes go into the acceptance ticket, feedback arrives in its `## Comments` or the conversation, and the Engineer merges locally.

## Pick the mode

An explicit mode argument wins. Otherwise, in order:

1. No `## Feature acceptance` section in `docs/agents/issue-tracker.md` → **setup**.
2. The feature MR has unresolved discussions whose last note is not yours, or the Engineer gave remarks in the conversation → **feedback**.
3. Otherwise → **prepare**.

Find the acceptance ticket (prepare and feedback): the argument; else the key in the current branch name, matched against the branch format; else ask.

Then read and follow the mode's file:

- setup → [setup.md](setup.md)
- prepare → [prepare.md](prepare.md)
- feedback → [feedback.md](feedback.md)
