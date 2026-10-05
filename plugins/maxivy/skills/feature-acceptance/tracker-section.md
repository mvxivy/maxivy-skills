## Feature acceptance

Each feature ends in an **acceptance ticket** that the Engineer works, not an agent. A **feature** is the set of tickets that block its acceptance ticket; a ticket's feature is the acceptance ticket it blocks. Acceptance rounds run through `/maxivy:feature-acceptance`.

- **Acceptance ticket.** When `/to-tickets` publishes a feature's tickets, it publishes one more, last: title `Приёмка: <feature>`, label `{{HITL_LABEL}}` instead of `ready-for-agent`, blocked by every other ticket of the feature, body linking the spec. Agents take `ready-for-agent` tickets only; a `{{HITL_LABEL}}` ticket waits for the Engineer.
- **Feature branch.** `{{BRANCH_FORMAT}}`, keyed by the acceptance ticket, cut from `{{MAIN}}`. Before implementing a ticket, check out its feature branch; when it does not exist yet, create it from `{{MAIN}}` and push it. `/implement` commits there.
- **Closing a ticket.** Record `/code-review` findings left unfixed as a comment on the ticket headed `Отложенные замечания ревью`, one line each with the reason. When the closed ticket was the acceptance ticket's last open blocker, run `/maxivy:feature-acceptance prepare <acceptance ticket>`.
- **Review status.** {{REVIEW_STATUS}}. The acceptance ticket sits there, assigned to {{ENGINEER}}, while the Engineer reviews.
- **Stage.** {{STAGE}}
- **Merge.** The Engineer merges the feature MR into `{{MAIN}}`; agents leave it open for them.
