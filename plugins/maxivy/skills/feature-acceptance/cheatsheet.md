# Cheat sheet: this project's guide

Print a usage guide built from this project's live configuration: the `### Branches` rules in `CLAUDE.md`, the `## Feature acceptance` section of `docs/agents/issue-tracker.md`, the tracker type, and the code host. Print it in chat only: it is rebuilt from the configuration on every call, so it never goes stale.

Fill every template slot `<…>` with this project's real value:

- `<project>`: the repository name from `git remote -v`; with no remote, the root directory's name.
- Example keys and branch names: the project's real key prefix, taken from the tracker or from ticket references in `git log`, with made-up numbers and slug.
- `<branch format>`: the format exactly as the tracker section writes it, its own `<acceptance key>`-style parts included.
- Ticket review: read the `Finishing a ticket` rule of the tracker section. Tickets go to the review status → the "обязательно" variants; tickets close at once → the "нет" variants.
- "Где смотреть": the MR's review environment when the CI config deploys one (a GitLab `environment` on merge request pipelines, a preview deploy on pull requests); otherwise the run command from the project's task runner or README.

Drop lines that do not apply: the stage hop when there is no stage stand; in local mode, MR lines become `.scratch/<feature>/acceptance.md` on the feature branch.

Done when the guide is printed with every template slot filled and every value traced to one of these sources.

## Template

```markdown
## Приёмка фич: <project>

**Настройки**
- Трекер: <Jira, проект PROJ | GitLab Issues | GitHub Issues | файлы в .scratch/>; код: <GitLab | GitHub | локально>
- Ветки: фича отводится от `<dev>` и мержится в него; дальше `<dev>` → `<stage>` → `<prod>` продвигаете вы
- Ветка фичи: `<branch format>`, например `<feature/PROJ-100-user-login>`
- Тикет приёмки: `Приёмка: <фича>`, метка `<hitl>`, заблокирован всеми тикетами фичи; в теле только ссылка на спеку. Чек-лист, отчёт и замечания — в MR, в трекер агент пишет только статус и ссылку на MR
- Ревью тикетов: <обязательно: после `/implement` тикет уходит в `<review status>` на <engineer>, закрываете вы | нет: агент закрывает тикет сам>
- На ревью: статус `<review status>`, ревьюер <engineer>

**Каждая фича**
1. `/to-spec`, затем `/to-tickets`: последний тикет в разбивке — `Приёмка: …` с меткой `<hitl>`, блокеры — все остальные. Проверьте это на шаге опроса.
2. `/implement <PROJ-101>` по тикету: коммиты идут в `<feature/PROJ-100-user-login>`. Незакрытые замечания `/code-review` агент показывает в сессии; закрываете тикет без них — они уходят комментарием `Отложенные замечания ревью` в тикет. <Тикет уходит в `<review status>`: прочитайте коммиты и закройте его | Агент закрывает тикет сам>.
3. После закрытия последнего тикета — `/maxivy:feature-acceptance prepare <PROJ-100>` (агент запускает сам, если закрывал он; закрывали вы — запустите): MR `<feature/PROJ-100-user-login>` → `<dev>` с чек-листом приёмки в описании, тикет приёмки в статусе `<review status>`.
4. Приёмка: пройдите чек-лист в описании MR — соответствие спеке и дизайну. Отдельный блок — отложенные замечания ревью со всех тикетов, с чек-боксами: что не отметили, уходит в `<dev>` под вашу ответственность. Где смотреть: <review-окружение MR | локально `<run command>`>. Замечания — комментариями в MR или в чате.
5. `/maxivy:feature-acceptance feedback`: по умолчанию каждое замечание — правка в тикете приёмки; агент только помечает, что похоже на отдельный инкремент, решение за вами. Ответы — в тредах MR.
6. Приёмка пройдена — merge в `<dev>`, проверка на дев-стенде, дальше промоушен. Тикет приёмки закройте сами или оставьте агенту: при следующем запуске он увидит влитую ветку и закроет его. Дефект после merge — баг-тикет.

**Ветка влита без приёмки**
- Приёмка считается пройденной, ответственность на том, кто влил. Агент при следующем запуске закрывает тикет приёмки одной строкой и перечисляет незакрытые тикеты фичи — решите, что с ними делать.

**Признаки сбоя**
- После `/to-tickets` нет тикета приёмки, в его теле появился чек-лист, или `/implement` коммитит в `<dev>`: агент пропустил раздел `## Feature acceptance` в `docs/agents/issue-tracker.md` — укажите ему на него.
- Агент пишет чек-лист или отчёт в тикет или его комментарии: это место MR — укажите ему на тот же раздел.

Шпаргалку в любой момент выводит `/maxivy:feature-acceptance help`.
```
