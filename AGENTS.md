# Agent Configuration (Common Standard)

> **Reference**: Based on [Agent Skills Specification](https://agentskills.io/specification)

This file defines the common standard for agents and skills across all AI client implementations (OpenCode, Claude, Gemini, etc.).

---

## Skills

Skills are reusable behavior definitions discovered from your repo or home directory. They are loaded on-demand via the native `skill` tool. For the complete specification — frontmatter rules, naming conventions, directory layout, progressive disclosure, and design patterns — use the `skill-creator` skill or read the reference docs at `.opencode/skills/skill-creator/references/`.

---

## Subagents

Subagents are specialized assistants that can be invoked for specific tasks. They are defined using markdown files.

### File Structure
```
````

agent-name.md

```

Or:

```

agent-name/
└── AGENT.md

````

### AGENT.md Format

```yaml
---
description: Brief description of what the agent does
compatibility: Compatible platforms (optional)
metadata:
  author: creator-username
  co-author: collaborator-username (optional)
  source: URL or reference to original agent
  version: "1.0.0"
  last-updated: "2026-04-05"
  tags: comma-separated-tags
  related-with:
    skills:
      - skill-name
    agents:
      - agent-name
    commands:
      - command-name
---
The rest of the agent description is up to you.
````

**Recommendation**: Include the same metadata keys for consistency:

- `author`: Who created the agent
- `co-author`: Additional contributors (optional)
- `source`: Original source URL (if adapted from another agent)
- `version`: Track version for changes
- `last-updated`: Last modification date
- `tags`: Optional tags for categorization
- `related-with`: Related skills, agents, and commands

### Effective Subagent Design

The `description` field in the frontmatter controls both **when** it's selected and **shapes the input prompt** the main agent passes to it. Vague descriptions lead to poor delegation. Be specific about its expertise and required inputs.

When writing the Markdown body (the System Prompt), you must include:

1. **Role Definition**: Clearly state who the agent is and what its primary objective is.
2. **Specific Inputs & Outputs**: Define exactly what format the subagent expects to receive and what structured format it must return (e.g., "Return a JSON object...", "Output a structured Markdown report..."). This provides a natural stopping point and prevents the subagent from running too long.

   ```markdown
   Provide your findings in a structured format:

   1. Summary: Brief overview and overall assessment
   2. Key Findings: Most important discoveries
   3. Relevant Files: Files most relevant to this task
   4. Obstacles Encountered: Workarounds, quirks, or problems found
   ```

3. **Constraints**: Explicitly list what the agent MUST NOT do (e.g., "Do not modify files directly", "Do not write tests").
4. **Tool Utilization**: Only grant tools the subagent actually needs. Instruct the agent on _when_ and _how_ to use them effectively.
5. **Report Obstacles**: Instruct the agent to document any workarounds, environment quirks, special flags, or dependency issues found in its output so the main thread doesn't have to rediscover them.

---

## Registered Subagents

### `logbook`

The `logbook` subagent helps the user maintain structured per-project logbooks (test outcomes, AI-vs-human collaboration notes, and free-form notes). It composes the user's dictation into validated entries and delegates all persistence to the logbook-* skills.

**Trigger phrases**: `logbook`, `bitácora`, `bitacora`

**NOT triggered by**: generic note-taking, TODO tracking, changelog writing, commit messages, or any request that does not explicitly name the logbook subagent.

**Location**: `plugins/logbook/agents/logbook.md`

**Install**:
```
/plugin marketplace add <path-or-url-to-my-skills>
/plugin install logbook@my-skills
```

---

## Plugins

Plugins are self-contained bundles of one or more subagents and/or skills that install as a unit.

### Directory Convention

| Location | Purpose |
|----------|---------|
| `plugins/<plugin-name>/` (this repo) | Plugin source code — authoring and development |
| `.claude/plugins/<plugin-name>/` (consumer project) | Installed runtime copy (managed by Claude Code) |

Plugin source lives at `plugins/<plugin-name>/` in the repository root. This is the canonical location for plugin development in this repository, distinct from the consumer install path. All new plugins MUST be created under `plugins/` and registered in `.claude-plugin/marketplace.json`.

### File Structure

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json        # Manifest: name, version, description, license
├── CHANGELOG.md           # Plugin-level changelog
├── README.md              # Install and usage docs
├── LICENSE                # License reference
├── agents/                # Subagent definitions (*.md)
└── skills/
    └── <skill-name>/      # One directory per skill (SKILL.md + scripts/)
```

### Script Path Resolution

Skills reference their own scripts using `${CLAUDE_SKILL_DIR}`, which Claude Code resolves at runtime to the skill's own directory. Example: `python3 "${CLAUDE_SKILL_DIR}/scripts/my_script.py"`.

**Do not use** `$CLAUDE_PLUGIN_ROOT` — this variable is not documented in the Claude Code skills spec and is not guaranteed to be set at runtime.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
specs/002-skill-creator/plan.md
<!-- SPECKIT END -->
