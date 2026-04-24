---
name: skill-creator
description: Guide users through authoring, validating, and improving OpenCode skills. Use when creating a new skill, editing an existing skill, or validating skill files. Triggered by phrases like "create a skill", "I want a skill for", "improve skill", or "validate skill".
license: MIT
compatibility: Designed for OpenCode. Requires Node.js 18+ and js-yaml for bundled scripts.
metadata:
  author: framunoz
  original-author: framunoz
  source: https://github.com/framunoz/skills/tree/main/.opencode/skills/skill-creator
  version: "0.1.0"
  last-updated: "2026-04-24"
  status: active
  replaced-by: "null"
---

# Context & Goal

This skill helps users create, edit, validate, and improve OpenCode skills following the project's standards (AGENTS.md, speckit workflow, and Constitution principles). It reduces the cognitive load of skill authoring by providing a conversational workflow, scaffolding scripts, reference documentation, and a validation harness.

The skill-creator does NOT assume a default path for new skills. It always asks the user where to save the skill.

# Step-by-Step Procedure

## Workflow A: Create a New Skill

### Step 1: Capture Intent

When the user says they want to create a skill (e.g., "I want a skill for generating changelogs"):

1. Infer a tentative `skill-name` from the purpose using hyphen-case (e.g., `changelog-generator`).
2. Infer a tentative `description` (what it does + when to use it + trigger keywords).
3. Infer what resources are needed: scripts, references, assets, or instructions-only.
4. Present the inferred values to the user for confirmation.

### Step 2: Ask Clarifying Questions (if needed)

If any critical information is missing or ambiguous, ask at most 3 questions:

- "What specific triggers should activate this skill?"
- "Should it include executable scripts, reference docs, or just instructions?"
- "Where would you like to save this skill? (e.g., `.opencode/skills/my-skill` or any path)"

Do NOT proceed until the user provides the output path.

### Step 3: Generate Draft Feature Description

Once the user confirms the purpose, name, resources, and path:

1. Generate a draft feature description ready for `/speckit.specify`.
2. Include: user stories, functional requirements, success criteria, and key entities.
3. Present the draft in a code block and instruct the user to copy-paste it into `/speckit.specify`.

### Step 4: Scaffold Files

If the project uses speckit (`.specify/` exists):
- Instruct the user to run `/speckit.specify` with the draft, then `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.
- Offer to assist during `/speckit.implement` by generating SKILL.md, scripts, references, and assets.

If speckit is NOT present:
- Run the init script to scaffold the skill:
  ```bash
  node .opencode/skills/skill-creator/scripts/init_skill.cjs <skill-name> --path <output-directory>
  ```
- Then use the `write` and `edit` tools to fill in SKILL.md body, scripts, references, and assets.

### Step 5: Fill Content

Guide the user through authoring:

1. **SKILL.md body**: Context & Goal, Step-by-Step Procedure, Usage of Resources, Constraints & Rules, Expected Output.
2. **scripts/**: Self-contained executable code with dependency declarations and error handling.
3. **references/**: Documentation loaded on demand (standards, patterns, forms).
4. **assets/**: Static resources (templates, images, data files).

### Step 6: Validate

Run the validation script on the created skill:

```bash
node .opencode/skills/skill-creator/scripts/validate_skill.cjs <path-to-skill>
```

Fix any errors reported. Re-run until status is `valid` or `valid_with_warnings`.

### Step 7: Quality Checklist

Present the following checklist to the user:

```markdown
## Quality Checklist

- [ ] Skill `name` matches the directory name exactly
- [ ] `description` states what the skill does AND when to use it
- [ ] `description` includes trigger keywords for agent selection
- [ ] No `TODO` markers remain in any file under the skill directory
- [ ] `metadata` includes Constitution-required fields: author, original-author, source, version, last-updated, status, replaced-by
- [ ] `CHANGELOG.md` exists with an initial version entry
- [ ] Scripts declare dependencies and exit non-zero on error
- [ ] SKILL.md body includes all 5 required sections
```

## Workflow B: Edit or Improve an Existing Skill

When the user wants to improve an existing skill (e.g., "improve the skill changelog-generator"):

### Step 1: Read Existing Skill

1. Read the existing `SKILL.md` from the skill directory.
2. Read any scripts, references, and assets if relevant.

### Step 2: Present Gap Diagnosis

Analyze the skill for common gaps and present findings:

1. **Metadata gaps**: Missing author, source, version, status, or replaced-by.
2. **Description gaps**: Unclear triggers, missing "when to use it", too vague.
3. **Body gaps**: Missing required sections (Context & Goal, Step-by-Step, Usage of Resources, Constraints & Rules, Expected Output).
4. **Resource gaps**: Missing scripts, references, or assets when the skill would benefit from them.
5. **Progressive disclosure gaps**: All content crammed into SKILL.md instead of using references/ for detail.
6. **TODO markers**: Any remaining TODOs in files.

### Step 3: Propose Changes

Based on the diagnosis, propose specific changes with before/after examples.

### Step 4: Apply Changes with Confirmation

Do NOT modify files without explicit user confirmation for each proposed change.

1. Present the proposed changes.
2. Wait for user approval.
3. Apply changes using `write` or `edit` tools.
4. Re-run validation after each batch of changes.

## Workflow C: Validate a Manually Created Skill

When the user wants to validate skill files they created by hand:

1. Ask for the path to the skill directory.
2. Run:
   ```bash
   node .opencode/skills/skill-creator/scripts/validate_skill.cjs <path>
   ```
3. Interpret the report for the user:
   - `valid`: No action needed.
   - `valid_with_warnings`: TODOs exist; recommend fixing them.
   - `invalid`: List specific errors and suggest fixes.
4. If the user wants strict validation:
   ```bash
   node .opencode/skills/skill-creator/scripts/validate_skill.cjs <path> --strict
   ```

# Speckit Integration

The skill-creator integrates with the speckit workflow when `.specify/` exists in the project root.

**If `.specify/` exists:**
1. Generate a draft feature description for `/speckit.specify`.
2. Instruct the user to paste it and run `/speckit.specify`.
3. Offer to assist in subsequent speckit phases (plan, tasks, implement).
4. During `/speckit.implement`, generate the actual skill files (SKILL.md, scripts, references, assets).

**If `.specify/` does NOT exist:**
1. Skip the speckit draft step.
2. Run `init_skill.cjs` directly after capturing intent.
3. Use `write`/`edit` tools to fill content immediately.
4. Run `validate_skill.cjs` to verify.

# Usage of Resources

## Scripts

- `scripts/init_skill.cjs`: Scaffold a new skill directory with SKILL.md template, CHANGELOG.md, and example subdirectories.
  - Usage: `node init_skill.cjs <skill-name> --path <output-directory>`
  - Run this after the user confirms the skill name and output path.
- `scripts/validate_skill.cjs`: Validate an existing skill's structure, frontmatter, and content.
  - Usage: `node validate_skill.cjs <path-to-skill-directory> [--strict]`
  - Run this after content is filled to catch errors and TODOs.

## References

- `references/skill-standards.md`: Complete OpenCode skill specification — frontmatter rules, naming conventions, length limits, directory layout. Read this when the user asks about standards or when authoring frontmatter.
- `references/skill-patterns.md`: Design patterns — progressive disclosure, domain organization, conditional details, output patterns. Read this when structuring a skill's instructions.
- `references/upstream-attribution.md`: License and attribution for adapted work (Claude and Gemini skill-creator sources). Read this when documenting provenance.

## Assets

- `assets/skill-template.md`: Template injected by `init_skill.cjs` into new SKILL.md files. Contains frontmatter placeholders and required section boilerplate.

# Constraints & Rules

- **ALWAYS ask for the output path** before scaffolding or creating files. Never assume a default path.
- **NEVER modify existing skills without explicit user confirmation.** Present a diagnosis and wait for approval.
- **Maximum 3 clarifying question turns** during intent capture. If still unclear, ask the user to rephrase.
- **All content MUST be in English.** This includes SKILL.md body, scripts, references, and assets.
- **Scripts MUST exit with non-zero code on error** and print clear error messages.
- **Do NOT create a package.json** for skills unless explicitly requested. Skills are documentation + script bundles, not Node projects.
- **Do NOT assume the user wants speckit.** Detect `.specify/` presence and adapt the workflow accordingly.
- **Preserve upstream attribution** when adapting skills from external sources (Constitution Principle IV).
- **Include Constitution-required metadata** in every skill's frontmatter: author, original-author, source, version, last-updated, status, replaced-by.
- **Skills MUST have a CHANGELOG.md** with semver entries (Constitution Principle II).

# Expected Output

When the user finishes creating or improving a skill, present:

1. **Validation report**: Output from `validate_skill.cjs` showing `valid` or `valid_with_warnings`.
2. **Quality checklist**: A markdown checklist with checkboxes for the user to verify manually.
3. **Test prompts**: 2-3 example user prompts that should trigger the new skill correctly, with expected behavior.

Example test prompts:

- **Prompt**: "I want to create a skill for generating conventional commit messages"
  - **Expected**: Skill-creator infers name `conventional-commit`, asks clarifying questions if needed, scaffolds files in user-provided path, validates successfully.
- **Prompt**: "Improve the skill changelog-generator"
  - **Expected**: Skill-creator reads existing SKILL.md, presents gaps (missing metadata, vague description, etc.), proposes changes, applies with confirmation, re-validates.
- **Prompt**: "Validate my hand-written skill at /tmp/my-skill"
  - **Expected**: `validate_skill.cjs` reports status, lists any errors or TODO warnings with file paths and line numbers.
