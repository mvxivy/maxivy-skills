# One readiness gate for the selected scope

## Inventory before mutation

Read AGENTS.md, then AGENTS.local.md and applicable subdirectory rules. Resolve the requested tickets, blockers, repositories, remotes, feature branches, hooks and paired runtimes. Read-only access elsewhere does not add it to scope. List the exact effects before asking for any missing cross-project or configuration approval; existing authorization remains valid.

Resolve each selected Story/feature branch through the project tracker convention, fetch its tickets once, exclude Done and explicitly skipped tickets, and order the frontier by Blocks. For an explicit roadmap stage, keep only its named tickets. Create each ledger at `.git/afk/<feature branch with / replaced by ->.md`; on resume, verify its recorded commits/check outcomes and continue only unfinished tickets. Fetch the tickets once. For every acceptance criterion, identify the required environment and evidence: unit/integration, local browser, or live access. Check credentials by using the documented helper without exposing secrets. A missing live route export/access, interactive password setup, or unavailable production fixture is a ticket blocker now, not a surprise after implementation. Record blocked tickets and dependent skips; independent tickets remain candidates.

## Resolve preparation as a batch

Inspect all branch divergence before switching branches. Follow project sync rules and preserve dirty work. Collect every needed long-lived branch push with exact repository, refs and possible CI/deploy effects in one request, together with other missing preparation authorizations. Never infer push authorization from an AFK launch. Complete approved preparation, then pin the actual feature HEAD for each repository. A pending required push prevents readiness for that repository.

Discover runtime versions and required check commands from the repository and CI. Use the declared versions. Run blocking checks on the pinned HEAD; a check on an earlier HEAD is not current evidence. The existing CI should exercise the same required commands; report a missing job rather than inventing a replacement check.

Repair a pre-existing local test-harness/setup defect within the already authorized project when the required behavior is clear (for example an alias mapping, isolated test environment, or test resource cleanup). Keep assertions and product semantics intact; record the red result and separate repair commit, then rerun the affected checks and the readiness baseline on the final HEAD. Do not silently skip a test, lower a threshold, or label a blocking failure advisory. Product changes, destructive data changes or unresolved semantics are blockers, not harness repair. Two unsuccessful repair attempts stop that repository's preparation; other prepared repositories may proceed once the batch report is complete.

## Check requirements before readiness

Complete [requirements.md](requirements.md) for the selected scope before marking tickets ready. Resolve preparation questions with the Engineer while available; record unanswered product questions as ticket blockers and propagate dependent skips into the manifest. Link the requirements report from each feature ledger, including on handoff. If source-backed clarification commits change a pinned HEAD, refresh that repository's baseline evidence before the readiness gate.

## Verify capabilities in the execution context

Scope authorization and host permissions are separate. Keep the sandbox and saved allowances unchanged unless the user explicitly approves exact changes. In Codex, inspect the effective approval reviewer as well as approval policy: `on-request` with a human reviewer can interrupt runtime calls. Auto-review can handle eligible requests when selected by the user, but can still deny them; `never` denies requests rather than granting access. Do not solve this with a blanket shell/script allow rule or Full Access.

Run the concrete operations the selected work needs, using their normal helpers and command forms: tracker read, local Git write on the authorized feature branch, feature publication/PR access, required tests that bind sockets, browser connection, and runtime start/status/stop. Use read-only/dry-run checks where they establish access; record any publication capability that cannot be verified safely as unresolved. A successful read does not establish write permission. No probe may send an unrequested message, create a dummy issue/PR, change a long-lived remote branch, or mutate an unapproved project.

Dispatch one bounded clean-context worker to verify the needed capabilities under its actual inherited restrictions, including a disposable local listener started/stopped with `scripts/runtime.py`. Pass reusable facts instead of making each worker rediscover credentials or configuration. If this first worker needs human runtime approvals, resolve them during preparation and repeat the probe; do not mark readiness from an elevated parent-only result. Not-required capabilities need a reason. Record differences between CLI and desktop/managed sessions; a config file does not prove that the current session adopted it.

Use [manual-check.md](manual-check.md) to prepare the real local stack, login, migrations and cleanup. Verify migration targets and side effects; preserve pre-existing data and resources. A startup that works but cannot be stopped is a failed capability check.

## Manifest and handoff

For `astra`, verify the documented Codex login/runtime once before its first worker. Keep one manifest in the orchestrator repository's `.git/afk/`, plus each feature's ledger. Record evidence paths, not secrets. `scripts/preflight.py` accepts this structure (replace every example with observed results):

```json
{
  "scope_evidence": "user message selecting repositories and actions",
  "pending_approvals": [],
  "projects": [{
    "path": "/absolute/repo",
    "remote": "git@github.com:owner/repo.git",
    "branch": "feature/KEY-name",
    "head": "full verified SHA",
    "branch_ready": true,
    "runtime": "verified runtime versions, local DB and setup evidence path",
    "checks": [{"command": "repository check", "head": "full verified SHA", "exit_code": 0, "log": "/absolute/log"}]
  }],
  "capabilities": {
    "tracker": {"status": "passed", "worker": true, "evidence": "/path/to/receipt"},
    "publish": {"status": "passed", "worker": true, "evidence": "/path/to/receipt"},
    "git_write": {"status": "passed", "worker": true, "evidence": "/path/to/receipt"},
    "runtime_start_stop": {"status": "passed", "worker": true, "evidence": "/path/to/receipt"},
    "browser": {"status": "not_required", "reason": "selected tickets have no browser criteria"}
  },
  "tickets": [{"key": "KEY-1", "project": "/absolute/repo", "status": "ready"}, {"key": "KEY-2", "project": "/absolute/repo", "status": "blocked", "reason": "live access unavailable"}]
}
```

Capabilities must cover every selected repository/environment; record separate receipts inside the evidence document. `advisory_source` on a failed check is only for a documented non-blocking classification or an explicit user acceptance, with its source. Keep baseline worktrees clean (including untracked sources); preserve unrelated work in place and use an authorized isolated checkout when needed. Logs/receipts must be existing local files. The gate validates records, not the truth of self-reported claims: inspect the logs before setting them passed.

Exclude blocked repositories from the runnable `projects` array and record all their tickets as blocked/skipped with reasons. Report every repository's result together. A runtime or host-policy change invalidates its capability evidence; a new branch HEAD requires new baseline evidence. During implementation, run the ticket's checks normally; do not restart all preparation for each expected code commit.
