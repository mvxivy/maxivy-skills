# Cheat sheet: this project's guide

Print a usage guide built from this project's live configuration: the `### Branches` rules in `CLAUDE.md`, the `## Feature acceptance` section of `docs/agents/issue-tracker.md`, the tracker type, and the code host. Print it in chat only: it is rebuilt from the configuration on every call, so it never goes stale.

Fill every `<…>` with this project's real value. Example keys use the project's real key prefix, taken from the tracker or from ticket references in `git log`; the "Где смотреть" line takes the run command from the project's task runner or README. Drop lines that do not apply: the stage hop when there is no stage stand; in local mode, MR lines become the acceptance ticket.

Done when the guide is printed with no `<…>` left and every value traced to one of the sources above.

## Template

```markdown
## Приёмка фич: <project>

**Настройки**
- Трекер: <Jira, проект PROJ | GitLab Issues | GitHub Issues | файлы в .scratch/>; код: <GitLab | GitHub | локально>
- Ветки: фича отводится от `<dev>` и мержится в него; дальше `<dev>` → `<stage>` → `<prod>` продвигаете вы
- Ветка фичи: `<branch format>`, например `<feature/PROJ-100-user-login>`
- Тикет приёмки: `Приёмка: <фича>`, метка `<hitl>`, заблокирован всеми тикетами фичи
- На ревью: статус `<review status>`, ревьюер <engineer>

**Каждая фича**
1. `/to-spec`, затем `/to-tickets`: последний тикет в разбивке — `Приёмка: …` с меткой `<hitl>`, блокеры — все остальные.
2. `/implement <PROJ-101>` по тикету: коммиты идут в `<feature/PROJ-100-user-login>`.
3. После последнего тикета агент запускает `/maxivy:feature-acceptance prepare <PROJ-100>` (не запустил — запустите сами): MR `<feature/PROJ-100-user-login>` → `<dev>`, тикет приёмки в статусе `<review status>`.
4. Ревью: код — комментариями в MR, поведение — по чек-листу. Где смотреть: <review-окружение MR | локально `<run command>`>.
5. `/maxivy:feature-acceptance feedback`: утвердите раскладку замечаний на правку / тикет / ответ.
6. Всё хорошо — merge в `<dev>`.

**Признаки сбоя**
- После `/to-tickets` нет тикета приёмки, или `/implement` коммитит в `<dev>`: агент пропустил раздел `## Feature acceptance` в `docs/agents/issue-tracker.md` — укажите ему на него.

Шпаргалку в любой момент выводит `/maxivy:feature-acceptance help`.
```
