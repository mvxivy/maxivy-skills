---
name: afk-session
description: "Prepares the selected repositories together, then builds their ready tickets while the Engineer is away: the /implement flow ticket by ticket, every question decided and recorded in repository docs with a ticket link instead of asked, manual checks run against the local backend and frontend, and the feature MR opened at the end with an «AFK: проверить» block listing what to re-check."
argument-hint: "<Story, feature branch, or explicit ticket set> [skip <ticket keys>] [astra]"
disable-model-invocation: true
---

# AFK session

Prepare the whole requested scope before announcing unattended execution. Build its ready tickets on their feature branches in `Blocks` order and leave one feature MR per repository. An explicit ticket set or roadmap stage limits the session to that set; it does not select every open sibling ticket. The Engineer is AFK: each question you would have asked becomes a decision you take, apply and record in versioned repository documentation, with a link and short meaning in its ticket. What they should re-check goes to the **ledger**, which becomes the «AFK: проверить» block of the MR.

Use one orchestrator for the entire session, including multi-repository work. Delegate bounded test, implementation, review and manual-check tasks with clean contexts; do not add a per-repository orchestration layer. Reserve the slots needed by the review skill before starting it. Give each worker the fetched ticket/spec, repository/remote scope, pinned base, verified runtime and permission evidence, and owned resource state paths. Reuse that evidence until a relevant HEAD, runtime or permission context changes. Only the orchestrator owns branch switches, tracker state and the ledger; workers follow their assigned commit scope. With `astra` in the argument, the test, implementer and fix subagents are Astra runs: each one goes as [astra.md](astra.md) says.

## Project conventions

Read before starting, and follow them as written except where this file overrides them:

- `CLAUDE.local.md` (or `CLAUDE.md`): `### Branches` names the dev branch and the push rules.
- `docs/agents/implement.md`: the ticket flow (seams, tests from a clean subagent, code, commit, review).
- `docs/agents/issue-tracker.md`: every tracker operation, the `## Feature MR` section (feature branch, finishing a ticket, review status, decision records). Read `docs/agents/domain.md` when recording a decision.

A project without the `## Feature MR` section has no feature to run: tell the Engineer and stop.

## 1. Prepare the whole session

Read [preflight.md](preflight.md) and complete it once for all selected repositories before starting ticket implementation. Preparation gathers missing scope/branch approvals in one concrete request, verifies required checks on the final HEAD, and exercises runtime access and cleanup in the actual worker context. A request already authorized by the user is not asked again.

The readiness gate is `python3 <skill>/scripts/preflight.py <manifest.json>`. It checks the recorded evidence and current Git identity; it does not grant permission or prove a host policy by itself. Save its output with the session ledger. Announce unattended execution only after the gate passes. If every ticket is blocked, return the complete blocker report instead of starting workers.

After readiness, ordinary implementation choices are recorded decisions. An unexpected human-only dependency blocks that ticket and its dependents; continue independent tickets within the prepared scope. New host denials are not approval: preserve work, follow the host's required denial/escalation handling, and do not promise uninterrupted execution beyond the verified context.

## 2. Each ticket

Take the next ticket from the frontier. Record its starting commit as the **base**. Then, through the steps of `implement.md`:

1. **Start.** Fetch it, state its title, move it to `In progress` as the tracker doc says.
2. **Seams.** From the ticket's `Seams` section. Without one, pick the seams yourself, one line each (interface, what it catches, what it misses), record the choice as step 4 says and write the seams into the ticket.
3. **Tests.** Dispatch a test subagent (with `astra`, an Astra run) exactly as `implement.md` step 2 describes. It commits the tests red and reports ambiguities and the existing fixtures the new rule invalidates.
4. **Ambiguities.** Decide each one yourself: take the test's reading when it fits the ticket text; otherwise the reading closest to the ticket's acceptance criteria. Record each decision and its reason as the tracker's decision-record rule says, committed on the feature branch. Put a link and short meaning into the ticket description under `h2. AFK-решения`, and the source link into the ledger.
5. **Code.** Dispatch an implementer subagent (with `astra`, an Astra run) with the ticket key, the test commit, the decisions from 4, and the pointer to `implement.md` steps 4–5. A test that reads the spec differently from the implementer is decided and recorded by you the same way as in 4. It commits with `Product review:` paragraphs and `Перед деплоем` comments as `implement.md` says.
6. **Manual checks.** When an acceptance criterion asks for a manual or in-browser check, run it as [manual-check.md](manual-check.md) says, through a dedicated subagent.
7. **Review.** `/code-review` since the base. A fix subagent (with `astra`, an Astra run) applies every finding inside the ticket's scope, in its own commits; each finding left unfixed goes into the ticket's `Отложенные замечания ревью` comment with its reason, as the `## Feature MR` section describes.
8. **Finish.** As the tracker section says for a finished ticket. Mark it done in the ledger with its commits.

Done with a ticket when its step 3 tests were red before step 5 and are green after it, the repo's blocking checks pass on the branch and its accepted advisory baseline has not worsened in changed files, and the ledger has its line.

### A ticket that does not get done

The ticket gets two implementer attempts. When the tests are still red, or the ticket needs something only a human holds (production access, a decision the ticket leaves to a person, a secret): move its commits to `afk/<ticket key>-wip`, reset the feature branch to the base so it stays green, leave the ticket `In progress` with a comment saying where the work is and why it stopped, and log it as not done. Every ticket it blocks is skipped and logged with that reason. Then take the next ticket.

## 3. The feature MR

When the frontier is empty, stop the resources owned by this session and verify cleanup before the final report, including on interruption or failure. Keep the ledger current before each handoff.

For each repository with completed work:

1. Run the full test suite once more on the feature branch.
2. Run `/maxivy:feature-mr open <feature branch>`. Its questions have AFK answers: open the MR with the tickets that are not done (the ledger says why); when the branch is red, open it as a draft and log what is red.
3. Append the ledger to the MR description as the «AFK: проверить» block (`glab mr update <id> --description …` or `gh pr edit <id> --body …`), after «Отложенные замечания ревью». Link the session's decision documents in «Что сделано»; a short explanation of their meaning is allowed. The repository documents hold the decisions and their reasons.
4. Report in chat: the MR link, tickets done, not done, skipped, and the count of ledger lines.

If preparation excluded every ticket or the feature has no diff, report that explicitly without opening an empty MR.

Push only the feature branch and `afk/*` branches during unattended execution; every merge and every long-lived branch stay the Engineer's, as `### Branches` says.

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
- [ ] <KEY>: <remaining check or result worth a second look>; <link to the repository decision when relevant>
```

Write «нет» under an empty heading: it tells the Engineer the category was checked.
