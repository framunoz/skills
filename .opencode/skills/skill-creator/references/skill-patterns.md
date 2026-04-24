# Skill Patterns

Design patterns for authoring effective OpenCode skills.

---

## Progressive Disclosure

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup
2. **Instructions** (< 5000 tokens): Full `SKILL.md` body when activated
3. **Resources** (as needed): Files in `scripts/`, `references/`, `assets/` loaded on demand

Keep the SKILL.md body concise. Move detailed reference material into `references/` and load it only when needed.

---

## Domain Organization

Organize skills by domain rather than by tool:

- **Good**: `api-designer` (covers REST, GraphQL, gRPC patterns)
- **Bad**: `rest-tool`, `graphql-tool`, `grpc-tool` (fragmented, hard to discover)

A single well-organized skill with conditional logic is better than many narrow skills.

---

## Conditional Details

When a skill covers multiple scenarios, use conditional instructions rather than long monolithic procedures:

```markdown
## Step 2: Choose the appropriate approach

**If the user provided a database schema:**
1. Read the schema file
2. Generate entity models from tables

**If the user provided API specs:**
1. Read the OpenAPI spec
2. Generate DTOs from endpoints
```

This keeps the instructions scannable and reduces cognitive load.

---

## Output Patterns

Define a clear output format to prevent the agent from running too long:

```markdown
Provide your findings in a structured format:

1. Summary: Brief overview and overall assessment
2. Key Findings: Most important discoveries
3. Relevant Files: Files most relevant to this task
4. Obstacles Encountered: Workarounds, quirks, or problems found
```

---

## Trigger Keywords

The `description` field should include trigger keywords that help the agent identify when to use the skill:

- **Good**: "Use when reviewing code for readability, refactoring complex logic, or designing new functions."
- **Bad**: "This skill helps with functions."

Include domain terms, action verbs, and scenario phrases.

---

## File References

Use relative paths from skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.
scripts/extract.py
```

Agents resolve these relative to the skill directory.

---

## Script Design

Scripts in `scripts/` should:

1. Declare dependencies at the top (e.g., `// Requires: js-yaml`)
2. Exit with non-zero code on error
3. Print usage when called incorrectly
4. Support `--dry-run` for safe preview when applicable
5. Be executable or have a shebang line

Example header:

```javascript
#!/usr/bin/env node
// Requires: Node.js 18+, js-yaml
// Usage: node validate_skill.cjs <path> [--strict]
```
