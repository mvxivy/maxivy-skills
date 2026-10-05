# Setup: write the convention

Write the `## Feature acceptance` section into `docs/agents/issue-tracker.md`. `/to-tickets` and `/implement` already read that file, so the convention reaches them without touching those skills. Done when the section is written with every placeholder filled.

## 1. Explore

- `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`: tracker type and label vocabulary.
- The tracker itself: does a HITL label already exist? What is the review status called? Jira workflows name it per project, so look at a real ticket's transitions.

## 2. Draft and confirm

Fill the template in [tracker-section.md](tracker-section.md). Defaults when exploration found nothing:

| Placeholder | Default |
| --- | --- |
| `{{HITL_LABEL}}` | `hitl` |
| `{{BRANCH_FORMAT}}` | `feature/<acceptance key>-<slug>`; local tracker: `feature/<feature-slug>` |
| `{{REVIEW_STATUS}}` | Jira: the workflow's review status; GitHub/GitLab: label `in-review`; local: `Status: in-review` |
| `{{ENGINEER}}` | the Engineer's handle on the tracker and the code host |

Show the filled section and let the Engineer edit it.

## 3. Write

- Append the section to `docs/agents/issue-tracker.md`, or update it in place when it already exists.
- If the HITL label or the review label is missing on the tracker, offer to create it and create it only on a yes.
- Leave the commit to the Engineer.
- Finish by printing the project's cheat sheet: follow [cheatsheet.md](cheatsheet.md).
