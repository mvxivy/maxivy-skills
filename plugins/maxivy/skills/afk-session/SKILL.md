---
name: afk-session
description: "Builds a feature's open tickets one after another while the Engineer is away: the /implement flow ticket by ticket, every question decided and written into its ticket instead of asked, manual checks run against the local backend and frontend, and the feature MR opened at the end with an «AFK: проверить» block listing what to re-check."
argument-hint: "<feature: Story key or feature branch> [skip <ticket keys>] [astra]"
disable-model-invocation: true
---

# AFK session

The Engineer launched this and walked away. Build every open ticket of one feature on its feature branch, in the order its `Blocks` links allow, and leave a feature MR they can review in one sitting. The Engineer is AFK: each question you would have asked becomes a decision you take, apply and write into its ticket. What they should re-check goes to the **ledger**, which becomes the «AFK: проверить» block of the MR.

You are the orchestrator. Each ticket is built by subagents with a clean context, so your own window holds only the ledger and short reports. With `astra` in the argument, the test, implementer and fix subagents are Astra runs: each one goes as [astra.md](astra.md) says.

## Project conventions

Read before starting, and follow them as written except where this file overrides them:

- `CLAUDE.local.md` (or `CLAUDE.md`): `### Branches` names the dev branch and the push rules.
- `docs/agents/implement.md`: the ticket flow (seams, tests from a clean subagent, code, commit, review).
- `docs/agents/issue-tracker.md`: every tracker operation, the `## Feature MR` section (feature branch, finishing a ticket, review status).

A project without the `## Feature MR` section has no feature to run: tell the Engineer and stop.

## 1. Preflight, while the Engineer may still be at the keyboard

This is the only step that may stop the session.

1. Resolve the feature from the argument: its Story, its feature branch, its tickets that are not `Done`, minus the ones the Engineer named to skip. Order them by `Blocks` links: the **frontier** is every ticket whose blockers are done or built in this session.
2. Check out the feature branch (create it from the dev branch and push it when it does not exist), pull, and run the repo's check and test commands from its README. Start what they need (a test database container, for instance).
3. Check tracker access with one ticket fetch. With `astra`: `codex login status` reports a login.
4. Create the ledger at `.git/afk/<feature branch with / replaced by ->.md` from the template in step 4. When it already exists, this is a resumed session: continue from the tickets it does not mark done or skipped.

Red checks on the untouched branch, no tracker access, or no test database: report it and stop. Otherwise print the ordered ticket list, say the session runs to the end without questions, and start.

## 2. Each ticket

Take the next ticket from the frontier. Record its starting commit as the **base**. Then, through the steps of `implement.md`:

1. **Start.** Fetch it, state its title, move it to `In progress` as the tracker doc says.
2. **Seams.** From the ticket's `Seams` section. Without one, pick the seams yourself, one line each (interface, what it catches, what it misses), write them into the ticket and log them.
3. **Tests.** Dispatch a test subagent (with `astra`, an Astra run) exactly as `implement.md` step 2 describes. It commits the tests red and reports ambiguities and the existing fixtures the new rule invalidates.
4. **Ambiguities.** Decide each one yourself: take the test's reading when it fits the ticket text; otherwise the reading closest to the ticket's acceptance criteria. Write the decisions into the ticket description under `h2. AFK-решения`, one line each with the reason. A decision that outlives the ticket (it constrains later code, is costly to reverse, or a later reader would ask why) also gets an ADR in `docs/adr/` as `docs/agents/domain.md` says, committed on the feature branch.
5. **Code.** Dispatch an implementer subagent (with `astra`, an Astra run) with the ticket key, the test commit, the decisions from 4, and the pointer to `implement.md` steps 4–5. A test that reads the spec differently from the implementer is decided by you the same way as in 4 and written into the ticket. It commits with `Product review:` paragraphs and `Перед деплоем` comments as `implement.md` says.
6. **Manual checks.** When an acceptance criterion asks for a manual or in-browser check, run it as [manual-check.md](manual-check.md) says, through a dedicated subagent.
7. **Review.** `/code-review` since the base. A fix subagent (with `astra`, an Astra run) applies every finding inside the ticket's scope, in its own commits; each finding left unfixed goes into the ticket's `Отложенные замечания ревью` comment with its reason, as the `## Feature MR` section describes.
8. **Finish.** As the tracker section says for a finished ticket. Mark it done in the ledger with its commits.

Done with a ticket when its step 3 tests were red before step 5 and are green after it, the repo's checks pass on the branch, and the ledger has its line.

### A ticket that does not get done

The ticket gets two implementer attempts. When the tests are still red, or the ticket needs something only a human holds (production access, a decision the ticket leaves to a person, a secret): move its commits to `afk/<ticket key>-wip`, reset the feature branch to the base so it stays green, leave the ticket `In progress` with a comment saying where the work is and why it stopped, and log it as not done. Every ticket it blocks is skipped and logged with that reason. Then take the next ticket.

## 3. The feature MR

When the frontier is empty:

1. Run the full test suite once more on the feature branch.
2. Run `/maxivy:feature-mr open <feature branch>`. Its questions have AFK answers: open the MR with the tickets that are not done (the ledger says why); when the branch is red, open it as a draft and log what is red.
3. Append the ledger to the MR description as the «AFK: проверить» block (`glab mr update <id> --description …` or `gh pr edit <id> --body …`), after «Отложенные замечания ревью». Name each ADR of the session in one line with its path in «Что сделано». The decisions themselves stay in the tickets: the MR carries no list of them.
4. Report in chat: the MR link, tickets done, not done, skipped, and the count of ledger lines.

Push only the feature branch and `afk/*` branches; every merge and every long-lived branch stay the Engineer's, as `### Branches` says.

## 4. The ledger

One line per thing the Engineer re-checks, written the moment it happens, so a crash leaves a usable ledger. It is the MR block verbatim:

```markdown
## AFK: проверить

Сессия <date>, ветка `<feature branch>`. Тикеты: сделано <n>, не сделано <n>, пропущено <n>.

### Ручные проверки
- [ ] <KEY>: <scenario> — <passed | failed: what was seen>; <screenshot paths>

### Не сделано и пропущено
- [ ] <KEY>: <why>; работа в `afk/<KEY>-wip` | заблокирован <KEY>

### Прочее
- [ ] <KEY>: <seams chosen, a red check, a risky merge between tickets, anything else worth a second look>
```

Write «нет» under an empty heading: it tells the Engineer the category was checked.
