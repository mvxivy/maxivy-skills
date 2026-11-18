# Manual check against the running stack

A ticket's acceptance criterion asks for a manual check: the frontend against the local backend, a screen in the browser, a flow end to end. The Engineer is away, so a check subagent runs it on a real local stack and drives the browser itself. The result is evidence in the ledger, never a skipped criterion.

## 1. The stack

Use only repositories and runtime resources authorized and verified in the session preflight. A paired repository named by a ticket is a dependency to inspect, not automatic permission to mutate it. The orchestrator owns branch changes and shared runtimes.

1. Confirm the prepared branches/HEADs and runtime versions. Reuse the preflight setup; never switch a paired repository while another worker uses it. Preserve dirty work.
2. Install missing dependencies with the declared package manager and frozen lockfile. Use an available project-scoped executable; a global package-manager installation or configuration change needs its own authorization.
3. Verify the current login flow against implementation/README, not a stale runbook. Confirm database target, migration status and test identity without printing secrets. Use an isolated local test DB where possible; record each created resource and the initial state of reused resources. Inspect migrations before applying them to a reused DB. No production calls or password resets are implied by a local browser check.
4. Before starting a process, record its deterministic runtime state directory and stop command in the ledger. Use the bundled supervisor (POSIX + Python 3 standard library), from the same approved execution context for start and stop:

   ```sh
   python3 <skill>/scripts/runtime.py start --state <repo>/.git/afk/runtime/api --cwd <repo> -- <documented server command>
   python3 <skill>/scripts/runtime.py status --state <repo>/.git/afk/runtime/api
   python3 <skill>/scripts/runtime.py stop --state <repo>/.git/afk/runtime/api
   ```

   The supervisor persists process identity and a private control socket before reporting startup, logs to `output.log`, and stops the owned process group including watcher children. An interrupted start call can be recovered with the known state path. Start success is not HTTP readiness: verify health/login separately. Do not put secrets in command arguments or screenshots. Services must stay in the supervisor's process group (no self-daemonizing commands). A killed supervisor or unavailable socket is a cleanup blocker: inspect recorded resources, never blindly signal a stale PID. On unsupported hosts, use a host-native managed process API with equivalent ownership and cancellation, verified during preflight.

## 2. The scenario

Write conditions, actions and expected results in plain language, without assigning an executor or inventing process roles. Keep the observed result separate from the expected one.

Drive the scenario through the available browser tool verified during preflight. Sign in using the prepared local test identity, walk the criterion's steps and compare observed results with expected ones. Produce failures only in owned local resources. A live-routing criterion needs separate live evidence; local fixtures never establish it.

Take a screenshot at each check point into `.git/afk/screens/<ticket key>-<n>.png`.

## 3. Result

- Passed: the ticket gets a comment with the scenario, the branches of both repos and the screenshot paths; the ledger gets a «Ручные проверки» line marked passed.
- Failed because of the ticket's code: hand it back to an implementer subagent as a failing case once, then run the check again; still failing → log it failed with what was seen.
- Could not run (a secret only a person holds, no way to sign in locally, the paired branch missing): log it as not run with the exact reason, so the Engineer runs it.

In a finally/cleanup phase, including interruption and failed checks, stop every owned runtime and confirm its listeners are gone. Remove only containers/volumes created for this check; restore the initial running/stopped state of reused resources and preserve their data. Record applied migrations and any cleanup failure immediately, before handing control back. Passing assertions with unresolved cleanup is not a completed manual check.
