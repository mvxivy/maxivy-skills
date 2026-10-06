# Feedback: close the round

Give every remark of the Engineer exactly one outcome: a **fix** on the feature branch under the acceptance ticket, or a **reply**. A fix that looks like its own increment also carries a **flag**, and becomes a ticket only on the Engineer's word. Done when every remark has its outcome and the Engineer can see it on the MR.

## 1. Collect the remarks

- **GitLab**: `glab api projects/:id/merge_requests/<iid>/discussions`; keep the unresolved ones (a diff note carries its file and line).
- **GitHub**: `gh api repos/{owner}/{repo}/pulls/<n>/comments` for line comments, `gh pr view <n> --comments` for general ones.
- **Checklist**: items the Engineer marked as failed or commented on.
- **Conversation**: remarks the Engineer gave in chat.
- **Local mode**: the acceptance ticket's `## Comments` and the conversation.

Skip threads whose last note is yours: an earlier round handled them. Number the rest.

## 2. Triage

The Engineer has the last word: the list is a proposal, and the branch, the tracker, the spec and the design change only after they approve each item.

Sort each remark:

- **Fix**, the default: anything the Engineer wants changed in this feature: a defect, a missed edge case, a divergence from the spec or the design, a wrong message, naming, structure, stabilisation. It is done under the acceptance ticket.
- **Reply**: a question, or a remark you disagree with. Answer with your reasoning and change nothing yet.
- **Flag**, on top of a fix: the fix looks like its own increment: behaviour the spec does not describe, a decision the spec has to make, or more than a session of work. Mark it `похоже на отдельный инкремент` with one line of why. The Engineer chooses: still a fix, or a new ticket.

Present the numbered list, each remark with its outcome and a one-line plan, and iterate until the Engineer approves it.

## 3. Fix

On the feature branch, for each fix:

1. Write a test that goes red on the remark, then make it green (`/tdd`). Remarks with no observable behaviour (naming, structure, wording in code) go straight to the change.
2. Commit, one commit per remark, referencing the acceptance ticket.

Then make the branch green.

## 4. Ticket

Only for a flag the Engineer turned into a ticket: publish it through the tracker workflow in `/to-tickets`' shape (what to build, acceptance criteria), labelled `ready-for-agent`, then add it as a blocker of the acceptance ticket. The spec and the design stay as they are unless the Engineer asked to change them.

## 5. Answer on the MR

Reply in each remark's thread: a fix gets the commit SHA and the test name, a ticket gets its link, a reply gets the answer. The Engineer resolves threads: resolution is their check.

## 6. Close the round

- **Only fixes and replies**: hand over with the round note `Раунд N: правки внесены` and the list.
- **Any ticket created**: post the round note `Раунд N: заведены тикеты` with their links, and move the acceptance ticket out of the review status, since it is blocked again. When the new tickets close, prepare runs again.

In chat, report the count per outcome and the links.
