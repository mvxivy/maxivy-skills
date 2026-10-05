# Prepare: open the round

Turn a finished feature into a feature MR the Engineer can accept in one sitting. Done when the MR description follows the template below and the round is handed over.

## 1. Check the blockers

Fetch the acceptance ticket and every ticket blocking it. Every blocker must be closed. If any is open, list them (key, title, status) and stop: a partial feature does not go to acceptance.

## 2. Make the feature branch green

1. Check out the feature branch and pull.
2. If the dev branch has moved, merge it into the feature branch (this direction only); resolve conflicts with `/resolving-merge-conflicts`.
3. Make it green. Fix mechanical fallout from the merge yourself; for anything else, report what is red and stop.

## 3. Gather the material

- **Spec**: linked from the acceptance ticket. Its user stories drive the checklist.
- **Every blocker**: title, acceptance criteria, comments. Collect each `Отложенные замечания ревью` comment and every note of scope dropped or deferred.
- **History**: `git log <dev>..HEAD --oneline` and `git diff <dev>...HEAD --stat`.
- **Where to look**: the MR's review environment when CI deploys one; the local run command from the project's task runner or README. The stands get the feature only after the merge.
- **Earlier rounds**: the existing feature MR and its round notes, if any.

## 4. Write the checklist

Write one or more checks per user story in the spec. A check is a concrete action with concrete input and an observable result: `Войти с неверным паролем → ошибка «Неверный логин или пароль», вход не выполнен`.

- Cover the unhappy paths the spec names (rejections, empty states, permissions, limits) alongside the happy path.
- A check that needs setup (a seeded user, a feature flag) states that setup inline.
- A user story the feature leaves uncovered goes under "Что сознательно не сделано", with the reason.

Done when every user story in the spec maps to a check or to a "not done" line.

## 5. Open or update the MR

Source: the feature branch. Target: the dev branch. Title: `<acceptance key>: <feature name>`. Write the description in the spec's language.

- **First round**: `glab mr create --source-branch <branch> --target-branch <dev> --title … --description …`, or `gh pr create --head <branch> --base <dev> --title … --body …`, with the Engineer as reviewer. Round note: `Раунд 1: готово к приёмке`.
- **Later round**: replace the description with a fresh one. Round note: `Раунд N: готово к повторной приёмке`, listing what changed since the previous round (commits, tickets closed, threads answered).
- **Local mode**: write the report into the acceptance ticket under `## Приёмка, раунд N`, with the branch name and the merge command.

## 6. Hand over

Hand over, and comment the MR link on the acceptance ticket. In chat, give the MR link and one line: tickets, checks, deferred review findings.

## MR description template

```markdown
## Что сделано

<Two or three sentences: what the user can now do that they could not before.>

Тикеты:
- <KEY>: <title>

## Где смотреть

- Review-окружение: <url, or "нет">
- Локально: `<run command>` из ветки `<feature branch>`

## Чек-лист приёмки

### <User story>
- [ ] <action with concrete input> → <expected result>

## Что сознательно не сделано

- <user story or criterion>: <reason; follow-up ticket if one exists>

## Оставленные замечания авто-ревью

- <KEY>: <finding>: <why it was left>
```

Write "нет" under an empty section rather than dropping it: an empty section tells the Engineer it was checked.
