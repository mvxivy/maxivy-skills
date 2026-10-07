# Cheat sheet: this project's guide

Print a usage guide built from this project's live configuration: the `### Branches` rules in `CLAUDE.md`, the `## Feature MR` section of `docs/agents/issue-tracker.md`, the tracker type, and the code host. Print it in chat only: it is rebuilt from the configuration on every call, so it never goes stale.

Fill every template slot `<…>` with this project's real value:

- `<project>`: the repository name from `git remote -v`; with no remote, the root directory's name.
- Example keys and branch names: the project's real key prefix, taken from the tracker or from ticket references in `git log`, with made-up numbers and slug.
- `<branch format>`: the format exactly as the tracker section writes it.
- Ticket review: read the `Finishing a ticket` rule of the tracker section. Tickets go to the review status → the "обязательно" variants; tickets close at once → the "нет" variants.
- "Где смотреть": the MR's review environment when the CI config deploys one (a GitLab `environment` on merge request pipelines, a preview deploy on pull requests); otherwise the run command from the project's task runner or README.

Drop lines that do not apply: the stage hop when there is no stage stand; in local mode, the MR is a description in chat and a local merge.

Done when the guide is printed with every template slot filled and every value traced to one of these sources.

## Template

```markdown
## MR фичи: <project>

**Настройки**
- Трекер: <Jira, проект PROJ | GitLab Issues | GitHub Issues | файлы в .scratch/>; код: <GitLab | GitHub | локально>
- Ветки: фича отводится от `<dev>` и мержится в него; дальше `<dev>` → `<stage>` → `<prod>` продвигаете вы
- Ветка фичи: `<branch format>`, например `<feature/user-login>`; каждый тикет фичи несёт строку `Ветка: …`
- Ревью тикетов: <обязательно: после `/implement` тикет уходит в `<review status>` на <engineer>, закрываете вы | нет: агент закрывает тикет сам>

**Каждая фича**
1. `/to-spec`, затем `/to-tickets`: тикеты с acceptance criteria, в каждом строка `Ветка: <feature/user-login>`. Проверьте критерии на шаге опроса: это единственная проверка фичи, другой не будет.
2. `/implement <PROJ-101>` по тикету: коммиты идут в `<feature/user-login>`. Незакрытые замечания `/code-review` агент показывает в сессии; закрываете тикет без них — они уходят комментарием `Отложенные замечания ревью` в тикет. <Тикет уходит в `<review status>`: прочитайте коммиты и закройте его | Агент закрывает тикет сам>.
3. После закрытия последнего тикета — `/maxivy:feature-mr open <feature/user-login>` (агент запускает сам, если закрывал он; закрывали вы — запустите): ветка подтянута до `<dev>`, зелёная, MR в `<dev>` с описанием: что сделано, тикеты, где смотреть, что сознательно не сделано, отложенные замечания ревью чек-боксами.
4. Читаете MR: что не отметили в отложенных замечаниях, уходит в `<dev>` под вашу ответственность. Где смотреть: <review-окружение MR | локально `<run command>`>. Замечания — комментариями в MR или в чате.
5. `/maxivy:feature-mr feedback`: каждое замечание — правка с тестом или ответ в треде; агент только помечает, что похоже на отдельный инкремент, решение за вами.
6. Merge в `<dev>` — ваш клик, это и есть приёмка. Проверка на дев-стенде, дальше промоушен. Дефект после merge — баг-тикет.

**Признаки сбоя**
- После `/to-tickets` в тикетах нет строки `Ветка: …`, или `/implement` коммитит в `<dev>`: агент пропустил раздел `## Feature MR` в `docs/agents/issue-tracker.md` — укажите ему на него.

Шпаргалку в любой момент выводит `/maxivy:feature-mr help`.
```
