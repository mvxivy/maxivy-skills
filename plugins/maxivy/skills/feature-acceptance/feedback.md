# Feedback: close the round

Give every remark of the Engineer exactly one outcome: a **fix** on the feature branch, a new **ticket** blocking acceptance, or a **reply**. Done when every remark has its outcome and the Engineer can see it on the MR.

## 1. Collect the remarks

- **GitLab**: `glab api projects/:id/merge_requests/<iid>/discussions`; keep the unresolved ones (a diff note carries its file and line).
- **GitHub**: `gh api repos/{owner}/{repo}/pulls/<n>/comments` for line comments, `gh pr view <n> --comments` for general ones.
- **Checklist**: items the Engineer marked as failed or commented on.
- **Conversation**: remarks the Engineer gave in chat.
- **Local mode**: the acceptance ticket's `## Comments` and the conversation.

Skip threads whose last note is yours: an earlier round handled them. Number the rest.

## 2. Triage

Sort each remark:

- **Fix**: corrects code already on the branch and needs no new spec decision: a bug, a missed edge case, a wrong message, naming, structure. Fits in this session.
- **Ticket**: new or changed behaviour, a spec decision, or work big enough to be its own tracer-bullet ticket.
- **Reply**: a question, or a remark you disagree with. Answer with your reasoning and change nothing yet.

Between fix and ticket, pick ticket. Present the numbered list, each remark with its category and a one-line plan, and iterate until the Engineer approves it.

## 3. Fix

On the feature branch, for each fix:

1. Write a test that goes red on the remark, then make it green (`/tdd`). Remarks with no observable behaviour (naming, structure, wording in code) go straight to the change.
2. Commit, one commit per remark.

Then make the branch green.

## 4. Ticket

Publish each ticket through the tracker workflow in `/to-tickets`' shape (what to build, acceptance criteria), labelled `ready-for-agent`, then add it as a blocker of the acceptance ticket.

## 5. Answer on the MR

Reply in each remark's thread: a fix gets the commit SHA and the test name, a ticket gets its link, a reply gets the answer. The Engineer resolves threads: resolution is their check.

## 6. Close the round

- **Only fixes and replies**: hand over with the round note `Раунд N: правки внесены` and the list.
- **Any ticket created**: post the round note `Раунд N: заведены тикеты` with their links, and move the acceptance ticket out of the review status, since it is blocked again. When the new tickets close, prepare runs again.

In chat, report the count per outcome and the links.
