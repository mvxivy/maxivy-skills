# maxivy-skills

A personal Claude Code plugin marketplace with the `maxivy` plugin.

## Installation

```shell
/plugin marketplace add <github-user>/maxivy-skills
/plugin install maxivy@maxivy-skills
```

To pick up newly pushed commits:

```shell
/plugin marketplace update maxivy-skills
```

## Skills

| Command | What it does |
| --- | --- |
| `/maxivy:setup-my-skills` | Adds the Engineer's standard rules to the project's `CLAUDE.md` |

## Adding a new skill

1. Create `plugins/maxivy/skills/<skill-name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Validate: `claude plugin validate plugins/maxivy`.
3. Commit and push.
