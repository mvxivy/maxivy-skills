# Manual check against the running stack

A ticket's acceptance criterion asks for a manual check: the frontend against the local backend, a screen in the browser, a flow end to end. The Engineer is away, so a check subagent runs it on a real local stack and drives the browser itself. The result is evidence in the ledger, never a skipped criterion.

## 1. The stack

The repos involved: the ticket's own repo and the paired one its text names (a frontend ticket names its backend pair, and the reverse). Both live next to each other under the same root.

1. Check out in each repo the branch the check needs: the feature branch here; in the paired repo, the branch carrying its paired ticket when the tracker names one, otherwise its dev branch. Leave a dirty paired repo as it is and log it as a blocker of the check.
2. Install dependencies with the package manager from `packageManager` in `package.json` (`npx --yes corepack@<version> enable` once when Corepack is missing), with the lockfile frozen.
3. Environment: copy `.env.example` to `.env` where `.env` is missing and fill what local runs need from the README. Point the frontend at the local backend (the frontend's README or `.env.example` names the variable).
4. Start what the backend needs (the database container from its README), then the backend and the frontend in parallel as background processes, with the run commands from each README. Wait until both answer.

## 2. The scenario

Drive the scenario the criterion describes through the browser tools (Playwright MCP): sign in the way the README or `.env.example` offers for local runs (a test user, a fixed OTP), walk every step the criterion names, and check what it says should happen. A failure mode the criterion names (a 502, a dropped connection) is produced by stopping or blocking the backend the scenario talks to.

Take a screenshot at each check point into `.git/afk/screens/<ticket key>-<n>.png`.

## 3. Result

- Passed: the ticket gets a comment with the scenario, the branches of both repos and the screenshot paths; the ledger gets a «Ручные проверки» line marked passed.
- Failed because of the ticket's code: hand it back to an implementer subagent as a failing case once, then run the check again; still failing → log it failed with what was seen.
- Could not run (a secret only a person holds, no way to sign in locally, the paired branch missing): log it as not run with the exact reason, so the Engineer runs it.

Stop every process this check started and remove the database container it created, so the next ticket starts clean.
