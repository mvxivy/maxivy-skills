---
name: feature-acceptance
description: "Feature acceptance, the Engineer's gate before a feature reaches the dev branch, in repos whose docs/agents/issue-tracker.md has a `## Feature acceptance` section. Use to prepare acceptance once every blocker of an acceptance ticket is closed, or to work through review feedback on a feature MR."
argument-hint: "[setup | prepare | feedback | help] [acceptance ticket]"
---

# Feature acceptance

The Engineer accepts each feature once, as a whole, before it reaches the dev branch: they walk the checklist in the feature MR and confirm the feature matches the spec and the design. Code is reviewed earlier, ticket by ticket, by the Engineer or by the agent alone, as the project chose; this skill runs the **gate** above that. The gate lives on the code host: the MR carries the checklist, the report, the remarks and the round notes; the tracker only tracks the acceptance ticket's state.

## Vocabulary

- **Acceptance ticket**: a ticket the Engineer works, not an agent. It carries the HITL label and is blocked by every ticket of the feature, so it frees itself when the last blocker closes. Its body is the spec link and one line pointing to the MR; it carries no checklist and no report.
- **Feature**: an increment after which the application still works as a whole, with or without business value of its own. On the tracker, the set of tickets blocking an acceptance ticket; there is no separate feature or epic entity.
- **Checklist**: the `## Чек-лист приёмки` in the feature MR description. Prepare writes it from the spec and the tickets; the Engineer walks it on the MR.
- **Ticket review**: the project's choice, recorded in the `Finishing a ticket` rule of the tracker section: a core project sends every ticket to the Engineer's review before it closes; a supporting or generic project closes tickets after the agent's own review.
- **Dev branch**: the branch feature MRs target, named in the `### Branches` rules of `CLAUDE.md` (the prod branch when the project has no dev stand).
- **Feature branch**: the branch every ticket of the feature commits to, cut from the dev branch and named after the acceptance ticket.
- **Feature MR**: the merge request (a pull request on GitHub) from the feature branch into the dev branch. Its description is the acceptance report; its threads carry the Engineer's remarks and your answers.
- **Round**: one pass of prepare → the Engineer walks the checklist → feedback. A feature takes as many rounds as it needs; each round ends in a round note on the MR, `Раунд N: …`.
- **Green**: the typecheck and the full test suite pass locally, the branch is pushed, and CI passes on it.
- **Footprint**: all that acceptance writes to the tracker: the acceptance ticket's status and assignee, plus two one-line comments over the feature's life, the MR link when the MR opens and the merge note when the ticket closes. Checklists, reports, round notes and replies go on the MR. The `Отложенные замечания ревью` comment that `/implement` leaves on a feature ticket is the one other tracker write of the flow; prepare carries it into the MR.
- **Hand over**: move the acceptance ticket to the review status, assign it to the Engineer, and post the round note on the MR.
- **Merge gate**: the merge into the dev branch is the Engineer's click, as `### Branches` in `CLAUDE.md` says. Leave the feature MR open for them. A feature branch already in the dev branch has passed the gate: see "Merged feature".

## Project conventions

Read both before any mode:

- The `### Branches` rules in `CLAUDE.md`: the dev branch. If they are missing, the project works without the branch flow, which acceptance needs: tell the Engineer to re-run `/maxivy:setup-maxivy-skills` and choose the branch flow, then stop.
- The `## Feature acceptance` section of `docs/agents/issue-tracker.md`: HITL label, review status, feature branch format, ticket review. If `docs/agents/issue-tracker.md` is missing, tell the Engineer to run `/setup-matt-pocock-skills` and stop.

Acceptance is **opt-in** per project: it is on exactly when that section exists. Without it, only an explicit `setup` proceeds; for anything else, tell the Engineer that acceptance is off in this project and `/maxivy:feature-acceptance setup` turns it on, then stop.

Every tracker operation (fetch a ticket, list its blockers, comment, label, change status, create a ticket) goes through the workflow in `docs/agents/issue-tracker.md`, and stays within the footprint.

The code host is separate from the tracker (Jira tickets with GitLab code is common). Take it from `git remote -v`:

- GitLab → `glab mr …`
- GitHub → `gh pr …`
- no remote host → **local mode**: the acceptance report, the round notes and the Engineer's remarks live in `.scratch/<feature>/acceptance.md` on the feature branch (`<feature>` is the feature's directory when the tracker is local, the acceptance key otherwise), and the Engineer merges locally.

## Pick the mode

An explicit mode argument wins; `setup` and `help` run only on request. Otherwise:

- The feature branch is in the dev branch → **merged feature**, below.
- The feature MR has unresolved discussions whose last note is not yours, or the Engineer gave remarks in the conversation → **feedback**.
- Otherwise → **prepare**.

Find the acceptance ticket (prepare and feedback): the argument; else the key in the current branch name, matched against the branch format; else ask.

Then read and follow the mode's file:

- setup → [setup.md](setup.md)
- prepare → [prepare.md](prepare.md)
- feedback → [feedback.md](feedback.md)
- help → [cheatsheet.md](cheatsheet.md)

## Merged feature

Check this once the acceptance ticket is known, before prepare or feedback. The feature is merged when the feature MR is merged (`glab mr view <branch>`, `gh pr view <branch> --json state,mergedBy,mergeCommit`) or, with no MR, when the feature branch is an ancestor of the dev branch (`git fetch`, then `git merge-base --is-ancestor <feature branch> <dev>`).

A merged feature has passed acceptance, whatever the state of its tickets: whoever merged it took the gate on themselves. Close the acceptance ticket with the one-line comment `Приёмка засчитана: ветка влита в <dev> (<merge commit>, <who merged>)`; the MR stays as it is. In chat, name the merger and the merge commit, list any blocker still open so the Engineer decides what becomes of it, and say that a defect found from now on is a bug ticket. Then stop. An acceptance ticket already closed needs nothing: say so and stop.
