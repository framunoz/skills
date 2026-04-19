# logbook plugin

A Claude Code subagent and skill bundle for maintaining per-project logbooks: test outcomes, AI-vs-human collaboration notes, and free-form notes.

## Overview

The `logbook` plugin ships a thin orchestrator subagent (`logbook`) and six co-located skills:

| Skill | Purpose |
|---|---|
| `logbook-init` | Create a new logbook with a declared schema type |
| `logbook-push` | Append one validated entry to a logbook |
| `logbook-format` | Render `entries.jsonl` to `rendered.md` |
| `logbook-list` | List all logbooks in the project |
| `logbook-query` | Filter and summarize entries by date, tag, or type |
| `logbook-schema` | Reference: schema definitions loaded by the subagent |

Each logbook lives at `logbook/<slug>/` inside the **consumer project** (not this repo). The plugin only ships code.

## Install

```
/plugin marketplace add <path-or-url-to-my-skills>
/plugin install logbook@my-skills
```

## Verify

After install, confirm everything is registered:

```
/logbook-list
/logbook-init --logbook smoke --type tests
/logbook-push --logbook smoke --type tests
```

## Usage

### Create a logbook

```
Tell logbook to create a new tests logbook called "login-tests"
```

Or directly:
```
/logbook-init --logbook login-tests --type tests
```

### Record an entry

Dictate to the `logbook` subagent in natural language:

```
logbook: smoke test passed. OAuth redirect works. Refresh loop fails on stale cookie.
```

The subagent composes a validated `tests` entry and calls `/logbook-push`.

### Render to Markdown

```
/logbook-format --logbook login-tests
```

### List logbooks

```
/logbook-list
```

### Query entries

```
logbook: show me all auth-tagged entries from last week
```

## Plugin layout

```
plugins/logbook/
├── .claude-plugin/plugin.json      # plugin manifest
├── CHANGELOG.md
├── README.md
├── LICENSE
├── agents/
│   └── logbook.md                  # subagent (sonnet, cyan, background)
└── skills/
    ├── logbook-push/               # SKILL.md + scripts/push.py + _schemas.py
    ├── logbook-format/             # SKILL.md + scripts/format.py
    ├── logbook-init/               # SKILL.md + scripts/init.py
    ├── logbook-list/               # SKILL.md + scripts/list.py
    ├── logbook-query/              # SKILL.md + scripts/query.py
    └── logbook-schema/             # SKILL.md + references/schemas.md
```
