# Contract: Skills `logbook-init` and `logbook-list`

Two small deterministic skills that round out the logbook toolset. Both use Haiku and are wrappers over a single Python script each. Both reside at `claude/plugins/logbook/skills/<name>/`.

## `logbook-init`

Creates a new logbook: empty directory, `meta.json`, empty `entries.jsonl`.

**`SKILL.md` frontmatter**:

```yaml
---
name: logbook-init
description: Create a new logbook under logbook/<slug>/ with a declared schema type (tests, collaboration, free). Only invoke on explicit user/subagent request to create a logbook.
model: haiku
effort: low
disable-model-invocation: true
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/<commit-sha>/plugins/logbook/skills/logbook-init
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, init, create
---
```

### Script

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/init.py" \
  --logbook <slug> \
  [--title "<title>"] \
  [--description "<description>"] \
  [--project-root <path>]
```

### Preconditions

- `<slug>` matches `^[a-z0-9]+(-[a-z0-9]+)*$`.
- `logbook/<slug>/` does NOT already exist (refuse to overwrite).

### Postconditions

- `logbook/<slug>/meta.json` created with `slug`, `created_at`, `format_version: 1` (no `schema_type` — logbooks are typeless containers).
- `logbook/<slug>/entries.jsonl` created empty.

### stdout (success)

```json
{"ok": true, "logbook": "<slug>", "path": "logbook/<slug>/", "schema_type": "<type>"}
```

### Error codes

| Exit | Reason |
|---|---|
| 0 | Success. |
| 16 | `<slug>` invalid. |
| 17 | Logbook already exists. |
| 18 | Invalid `--type`. |
| 20 | I/O error. |

---

## `logbook-list`

Lists all logbooks in the current project with their schema type and entry count.

**`SKILL.md` frontmatter**:

```yaml
---
name: logbook-list
description: List logbooks in the current project with schema type and entry count. Any Claude Code agent may invoke this skill to enrich its context with an inventory of available logbooks.
model: haiku
effort: low
allowed-tools: Bash(python3 *), Read
metadata:
  author: franciscomunoz
  original-author: franciscomunoz
  source: https://github.com/framunoz/skills/tree/<commit-sha>/plugins/logbook/skills/logbook-list
  version: "0.1.0"
  last-updated: "2026-04-18"
  status: active
  replaced-by: null
  license: inherits repository LICENSE
  tags: logbook, list, inventory
---
```

### Script

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/list.py" \
  [--project-root <path>]
```

### Output

stdout on success:

```json
{"ok": true, "logbooks": [
  {"slug": "tests-login", "entries": 12, "last_entry_at": "2026-04-18T12:00:00Z"},
  {"slug": "collab-v1",   "entries": 3,  "last_entry_at": "2026-04-17T09:15:00Z"}
]}
```

Empty project → `logbooks: []`. Not an error.

### Error codes

| Exit | Reason |
|---|---|
| 0 | Success (including empty list). |
| 20 | I/O error. |
