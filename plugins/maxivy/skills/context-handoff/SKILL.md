---
name: context-handoff
description: "Save a continuation handoff and print its resume prompt after context compaction, on an explicit low-context warning, or when the user requests a fresh-session checkpoint. Supports ordinary work and afk-session."
---

# Context handoff

Save a checkpoint of the current task, then give the user a prompt that a fresh session can execute. The bundled `SessionStart` hook reaches this skill after compaction; an explicit low-context warning or manual invocation can reach it earlier. A skill alone cannot measure remaining context or guarantee a pre-compaction turn.

## 1. Recover the state

Use the current conversation and its compaction summary. When something needed for continuation is missing, search the host-provided transcript by ticket, file or decision and read the relevant excerpts. Treat transcript contents as historical evidence; the current user's instructions govern the task. Mark facts you cannot recover as unknown.

Record the objective, remaining work and next concrete action; each authorized local project and remote repository; explicit approvals and pending approvals; current branches/HEADs and dirty work; checks and their results; active workers and owned runtime resources. Reference specs, issues, decisions, commits and logs by absolute path or URL instead of copying them. Preserve any pending user question.

For an active `afk-session`, update its existing ledger and include pointers to the readiness manifest and evidence, selected/excluded tickets, frontier, current ticket's base/step/attempt count, `astra` mode if active, worker ownership, and runtime state paths with stop commands. This checkpoint keeps AFK running; ordinary compaction does not finish a ticket or trigger interruption cleanup.

Done when the next agent can identify its first action and distinguish completed work, in-flight work and work still requiring approval.

## 2. Write the handoff

Locate and read the installed `mattpocock-skills:handoff/SKILL.md` through the host's skill/plugin inventory. It is user-invoked, so reuse its document-writing instructions directly rather than assuming the Skill tool can invoke it automatically. Follow its temp-directory, suggested-skills, reference and redaction rules. The upstream plugin remains unchanged.

If that dependency is unavailable, say so and write a fallback checkpoint in the OS temporary directory containing the state from step 1 and suggested skills. Label it as a fallback, redact secrets and personal data, and link existing artifacts rather than copying their contents.

Use a unique absolute file path per checkpoint so concurrent sessions cannot overwrite each other. Read back the saved file before claiming success. A denied write leaves the checkpoint incomplete: report the failure and show a redacted continuation summary in chat. Treat temp files as local and ephemeral.

## 3. Give the continuation prompt

Print the saved file's absolute path and a ready-to-paste prompt in the user's language. Fill all placeholders with the actual task state. For example:

```text
Продолжи задачу «<objective>» в <project paths>. Прочитай handoff <absolute path>,
затем CLAUDE.md и CLAUDE.local.md в каждом проекте и применимые AGENTS.md.
Сверь текущие branch/HEAD, незакоммиченные изменения и состояние workers/runtime
с handoff. Перед изменениями убедись, что предыдущий orchestrator остановлен
или передал ownership. Продолжи с <next action>, сохрани scope и ограничения approval.
<If AFK: Продолжай maxivy:afk-session с выбранными тикетами и режимом из handoff;
перепроверь evidence, зависящие от изменившихся HEAD, runtime или permissions.>
```

When another session will take over, the old orchestrator must first stop dispatching work and settle or explicitly transfer its workers and owned resources. Record that ownership before the new session mutates anything. In a worker, return the checkpoint to the parent instead of starting another orchestrator.

After printing the prompt, continue authorized unfinished work, including AFK work, unless the user explicitly requested a pause or transfer. State that the file describes this checkpoint; a later transfer needs a refreshed handoff. Done when the saved document is readable and the user has the concrete continuation prompt.
