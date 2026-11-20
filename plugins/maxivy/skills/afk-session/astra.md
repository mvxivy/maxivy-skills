# Astra as the builder

The session runs with `astra`: the test, implementer and fix subagents of steps 2.3, 2.5 and 2.7 are Astra runs (OpenAI `gpt-6-astra` through Codex) instead of the host's native subagents. Seams, every decision and ADR, the ledger, `/code-review`, manual checks, the tracker and the MR stay yours.

## The sandbox is the guard

Astra runs only through `astra <brief>`, the plugin's command on `PATH`. Its sandbox keeps `.git` read-only, the network off and every MCP server unloaded, so Astra edits the working tree and runs local commands, and every git operation is yours: commit, branch, reset, fetch, push. The guard holds only through the command, so `astra` is the one way you start Astra.

What the sandbox leaves out, you run: commands that need the network or Docker (dependency installs, tests against the database container, the repo's checks that call out). Install what the ticket needs before the run that uses it.

## A run

1. Start from a clean working tree; record `HEAD`.
2. Write the brief to `.git/afk/briefs/<KEY>-<role>-<n>.md` from the template below.
3. Run `astra <brief>` in the background and wait for it to finish. It prints the report (the schema is `astra-report.schema.json`); its log sits next to the brief, read it only when the report is missing or makes no sense.
4. Compare `git status --porcelain` with `changed_files`. Revert every change outside the ticket's scope and log it under «Прочее».
5. Run every check the report marks `not_run`, then the role's gate: tests for changed behavior red on the pre-implementation base for the tests role (already-satisfied criteria follow `SKILL.md` step 2.4), the ticket's tests and the repo's checks green for the code and fix roles. Keep the tail of a failing output, never the whole of it.
6. Commit the change yourself with the report's `commit_message`, under the project's commit rules. The tests role gives the test commit of step 2.3.
7. Feed the report into the session: resolve `ambiguities` and `invalidated_fixtures` through step 2.4 and [requirements.md](requirements.md) for every role. Unresolved product decisions or human-only dependencies block the ticket immediately. Implementation failures count toward the two attempts, with the failing tail in the next brief and `blocker` recorded in the ledger when present.

Done with a run when its change is committed or reverted and the report's content sits in the ticket, the ledger, or the next brief.

## The brief

Each Astra run starts with a fresh task context and the Codex instructions available to that run. Name `AGENTS.md`, `AGENTS.local.md` and the required tracker or skill documents explicitly in the brief; the parent session's context is not inherited.

```markdown
Role: <tests | code | fix>. Repo: <path>, branch <feature branch>.

## Read first
- docs/agents/implement.md, step <2 for tests | 4–5 for code and fix>
- AGENTS.md, then AGENTS.local.md if present, plus applicable subdirectory rules: code conventions and commit rules

## Ticket <KEY>
<the ticket text, verbatim>

## Seams
<the seams from step 2.2>

## Decisions
<applicable agreed spec/domain rules and the requirements report's source references; preparation clarifications and any step 2.4 decisions, including for tests>

## Task
tests: write the tests for the seams, red for the agreed change; report already-satisfied criteria with passing coverage and leave the implementation untouched. List every ambiguity of the ticket text and every existing fixture the new rule invalidates. For a correction run, align tests with the orchestrator's source-backed decision.
code: make the tests of commit <sha> green; the tests stay as written, and one you read differently goes to ambiguities.
fix: apply these review findings, each within the ticket's scope: <findings>.
<a previous attempt: its failing output tail>

## Report
Fill every field. Edit files and run local commands only: git, the network and Docker are outside your sandbox. A command that needs them goes into checks as not_run, with the exact command. commit_message follows the commit rules above, with the `Product review:` paragraphs and `Перед деплоем` notes implement.md asks for.
```
