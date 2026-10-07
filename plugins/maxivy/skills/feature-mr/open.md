# Open: the feature MR

Turn a finished feature branch into an MR the Engineer can read in one sitting and merge. Done when the MR exists with the description below, the branch is green, and the Engineer has the link.

## 1. Tickets

List the feature's tickets with their status. For every open one, say so and ask whether to open the MR without it; the Engineer decides. A branch already in the dev branch needs no MR: say so and stop.

## 2. Green

1. Check out the feature branch and pull.
2. If the dev branch has moved, merge it into the feature branch (this direction only); resolve conflicts with `/resolving-merge-conflicts`.
3. Make it green. Fix mechanical fallout from the merge yourself; for anything else, report what is red and stop.

## 3. Material

- **Spec**: `.scratch/<feature>/spec.md`, or the spec the tickets link; the source of "what was done".
- **Every ticket**: title, comments. Collect each `Отложенные замечания ревью` comment, every finding of it, and every note of scope dropped or deferred.
- **Ticket review**: the `Finishing a ticket` rule of the tracker section says whether tickets closed after the Engineer's review or after the agent's own.
- **History**: `git log <dev>..HEAD --oneline` and `git diff <dev>...HEAD --stat`.
- **Where to look**: the MR's review environment when CI deploys one; the local run command from the project's task runner or README. The stands get the feature only after the merge.
- **Existing MR**: its description, if the MR was opened before.

## 4. Open or update

Source: the feature branch. Target: the dev branch. Title: the feature name from the spec. Write the description in the spec's language.

- **New**: `glab mr create --source-branch <branch> --target-branch <dev> --title … --description …`, or `gh pr create --head <branch> --base <dev> --title … --body …`, with the Engineer as reviewer.
- **Existing**: replace the description with a fresh one and comment what changed since the last one (commits, tickets closed, threads answered).
- **Local mode**: print the description and the merge command in chat.

## 5. Report

In chat: the MR link and one line with the ticket count and the deferred findings count.

## MR description template

```markdown
## Что сделано

<Two or three sentences: what the user can now do that they could not before.>

Тикеты:
- <KEY>: <title>

Ревью кода: <"каждый тикет закрыт после вашего ревью" | "по правилам проекта код не ревьюился человеком">

## Где смотреть

- Review-окружение: <url, or "нет">
- Локально: `<run command>` из ветки `<feature branch>`

## Что сознательно не сделано

- <scope>: <reason; follow-up ticket if one exists>

## Отложенные замечания ревью

- [ ] <KEY>: <finding> — <why it was left>

Что не отмечено, остаётся на ответственности принимающего.
```

Write "нет" under an empty section rather than dropping it: an empty section tells the Engineer it was checked.
