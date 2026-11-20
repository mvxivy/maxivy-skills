# Requirements consistency

## Before readiness

Dispatch one bounded, read-only, clean-context subagent for the selected scope. Give it the original request and agreed spec, selected tickets with acceptance criteria and dependencies, relevant domain docs/ADRs, repository/remote scope and pinned HEADs. It may read related tickets and code to establish facts; only the orchestrator changes tickets, branches or the ledger.

Ask it to trace each agreed rule relevant to the selected work to the tickets and acceptance criteria that cover it. Check the end-to-end scenarios across those tickets: business rules and exceptions, states/transitions, data and integration contracts, and dependencies. Report missing coverage, contradictions and unsupported product assumptions, with source references and affected ticket keys. Distinguish intended behavior from current code and fixtures: existing behavior is evidence, not authority to override an agreed change.

Respect the selected slice. Rules deliberately assigned to later or excluded tickets are outside this run unless the selected work depends on them. Reading them does not authorize implementing them. A standalone ticket can supply sufficient requirements without a separate spec; unavailable sources block only work whose expected behavior cannot be established.

The orchestrator resolves findings using the rule below. Save the source references/revisions, rule-to-ticket coverage, findings and dispositions in `.git/afk/<feature branch with / replaced by ->-requirements.md`, and link it from the feature ledger. Record source-backed clarifications in repository docs and tickets through step 2.4 of `SKILL.md`. Include the applicable sources and clarifications in test, implementation and review briefs.

Done when every rule relevant to the selected work has identified coverage or a recorded blocker, and every selected ticket is ready, blocked or skipped with dependent skips propagated. A `ready-for-agent` label alone is insufficient. The orchestrator verifies this result before running the Python readiness gate; that script checks operational evidence, not requirements semantics.

## Resolve a finding or a later ambiguity

- **Supported by agreed sources:** apply the rule and cite its source. An explicit Engineer-approved change supersedes the earlier requirement it changes. Restore an omitted acceptance criterion within the selected ticket's agreed scope and record why; adding work outside that scope requires approval.
- **Implementation choice:** decide and record it when the alternatives preserve the agreed observable behavior and constraints.
- **Unresolved product behavior or conflicting requirements:** record the conflicting/missing sources, affected tickets, concrete question and possible readings. During preparation, batch these questions for the Engineer; if unanswered when they leave, block the affected tickets. During unattended execution, block them immediately and continue independent work. Neither a test author's reading nor the easiest implementation establishes a new business rule.

A missing rule for cancelling an already-paid order requires a product decision. A duplicate-submission rule explicitly present in the agreed spec but omitted from an in-scope API ticket can be restored from that source.

During implementation, use this same rule for ambiguities from any worker, manual checks or review. Consult a bounded read-only subagent if source analysis is needed; give it the disputed behavior and sources without treating either worker's reading as authoritative. Recheck only affected coverage/dependencies when requirements or relevant system facts change, including after a handoff; an ordinary implementation commit does not require a new whole-session review. Update the report, ledger and worker briefs before resuming affected work. Handle a blocked in-flight ticket through `A ticket that does not get done` in `SKILL.md` without spending implementation retries on a product decision.
