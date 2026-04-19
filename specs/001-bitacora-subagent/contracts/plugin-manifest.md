# Contract: Plugin Manifest + Marketplace Catalog

Defines the two JSON files that make the `logbook` plugin discoverable and installable through Claude Code's plugin system.

## 1. Plugin manifest — `plugins/logbook/.claude-plugin/plugin.json`

Declares the `logbook` plugin bundle (subagent + six skills).

```json
{
  "name": "logbook",
  "version": "0.1.0",
  "description": "A Claude Code subagent and skill bundle for maintaining per-project logbooks (test outcomes, AI-vs-human collaboration notes, free-form notes). Invoked only by explicit user request.",
  "author": {
    "name": "Francisco Muñoz"
  },
  "homepage": "https://github.com/framunoz/skills/tree/main/plugins/logbook",
  "repository": "https://github.com/framunoz/skills",
  "license": "inherits repository LICENSE",
  "keywords": ["logbook", "bitacora", "journal", "test-outcomes", "ai-collaboration"],
  "category": "productivity"
}
```

### Required fields

| Field | Rule |
|---|---|
| `name` | Must equal `logbook` and match `^[a-z0-9]+(-[a-z0-9]+)*$` (Constitution naming). |
| `version` | SemVer; initial release `0.1.0`. Bumped per Constitution II on every change, paired with `plugins/logbook/CHANGELOG.md` update. |
| `description` | English-only (Constitution). Short; the in-depth trigger description lives in the subagent `description` frontmatter, not here. |
| `license` | String reference to repo LICENSE (Constitution V). |

### Path fields (omitted → defaults)

The plugin relies on the default layout (`agents/`, `skills/`), so no custom `agents`/`skills` override fields are needed. Adding any would only be required if the directories were renamed.

## 2. Marketplace catalog — `.claude-plugin/marketplace.json` (repo root)

Turns the `my-skills` repository root into a marketplace that Claude Code can `/plugin marketplace add`.

```json
{
  "name": "my-skills",
  "owner": {
    "name": "Francisco Muñoz"
  },
  "plugins": [
    {
      "name": "logbook",
      "source": "./plugins/logbook",
      "description": "Subagent + skills for maintaining per-project logbooks (test outcomes, AI-vs-human collaboration notes)."
    }
  ]
}
```

### Required fields

| Field | Rule |
|---|---|
| `name` | `my-skills` (matches repo). |
| `owner.name` | Human-readable maintainer. |
| `plugins[].name` | Must match the plugin's own `plugin.json` `name`. |
| `plugins[].source` | Relative path from the marketplace root to the plugin directory. |
| `plugins[].description` | Short catalog-level description (may differ from the plugin's own long-form description). |

### Rules

- **One plugin per subdirectory under `plugins/`**. Adding more plugins in the future means appending entries to `plugins[]` and creating `plugins/<new-name>/`.
- **Source paths are relative** — use `./plugins/<name>`, not absolute paths, so the catalog works when the repo is cloned locally or referenced via GitHub URL.
- **The root `.claude-plugin/` directory holds ONLY `marketplace.json`.** Do not put plugin manifests, agents, or skills there.

## Install flow (informational)

```
/plugin marketplace add <path-or-url-to-my-skills>   # reads .claude-plugin/marketplace.json
/plugin install logbook@my-skills                    # resolves plugins[0].source → plugins/logbook/
                                                     # reads plugins/logbook/.claude-plugin/plugin.json
                                                     # registers agents/logbook.md and skills/*
```

## Validation

- `plugin.json` must be valid JSON and contain `name`, `version`, `description`.
- `marketplace.json` must be valid JSON, contain `name`, `owner`, `plugins`, and every `plugins[].source` must point to a directory containing `.claude-plugin/plugin.json`.
- Both files are English-only.
