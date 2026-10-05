# maxivy-skills

A personal Claude Code plugin marketplace with the `maxivy` plugin.

## Installation

```shell
/plugin marketplace add mvxivy/maxivy-skills
/plugin install maxivy@maxivy-skills
```

To pick up newly pushed commits, refresh the marketplace, update the plugin, then restart Claude Code:

```shell
/plugin marketplace update maxivy-skills
/plugin update maxivy@maxivy-skills
```

The plugin has no `version` in `plugin.json`, so an install is pinned to a commit: a marketplace update alone, or a reinstall, keeps the old commit.

## Skills

| Command | What it does |
| --- | --- |
| `/maxivy:setup-maxivy-skills` | Adds the Engineer's standard rules to the project's `CLAUDE.md`, including the dev/stage/prod branches it finds or asks about |
| `/maxivy:feature-acceptance` | Human-in-the-loop feature acceptance: `setup` writes the convention into `docs/agents/issue-tracker.md`, `prepare` opens the feature MR with a manual-test checklist, `feedback` works through the review remarks |

## Adding a new skill

1. Create `plugins/maxivy/skills/<skill-name>/SKILL.md` with `name` and `description` in the frontmatter.
2. Validate: `claude plugin validate plugins/maxivy`.
3. Commit and push.
