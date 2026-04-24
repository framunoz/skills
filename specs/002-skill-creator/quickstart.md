# Quickstart: skill-creator

**Feature**: skill-creator  
**Date**: 2026-04-23

---

## Installing the skill-creator

1. Ensure Node.js 18+ is installed:
   ```bash
   node --version
   ```

2. Install js-yaml (peer dependency):
   ```bash
   npm install -g js-yaml
   # or locally in the project
   npm install js-yaml
   ```

3. The skill-creator is project-local. OpenCode will discover it automatically from:
   ```
   .opencode/skills/skill-creator/SKILL.md
   ```

---

## Creating Your First Skill

### Step 1: Invoke the skill-creator

Tell OpenCode: "I want to create a skill for [purpose]"

Example:
> "I want to create a skill that helps me write conventional commit messages"

### Step 2: Answer clarifying questions (if any)

The skill-creator may ask up to 3 questions, such as:
- What triggers should activate this skill?
- Should it include any scripts or just instructions?
- Where would you like to save this skill?

### Step 3: Choose a path

When asked, provide the output directory. Examples:
- `.opencode/skills/conventional-commit` (project-local)
- `~/.config/opencode/skills/conventional-commit` (global)
- `/tmp/test-skill` (temporary, for testing)

### Step 4: Review the draft

If the project uses speckit (`.specify/` exists), the skill-creator will generate a draft feature description. Copy and paste it into `/speckit.specify`.

If speckit is not present, the skill-creator will scaffold files directly.

### Step 5: Fill in the content

The skill-creator will guide you through authoring:
- SKILL.md body (instructions)
- scripts/ (if needed)
- references/ (if needed)
- assets/ (if needed)

### Step 6: Validate

Run the validation script:
```bash
node .opencode/skills/skill-creator/scripts/validate_skill.cjs <path-to-your-skill>
```

Expected output:
```
Skill: conventional-commit
Status: valid
```

### Step 7: Quality check

Review the checklist presented by the skill-creator:
- Name matches directory name
- Description includes what the skill does and when to trigger
- No TODO markers remain
- Test prompts are realistic

---

## Validating an Existing Skill

To check any skill manually:

```bash
node .opencode/skills/skill-creator/scripts/validate_skill.cjs /path/to/skill-name
```

With strict mode (warnings become errors):
```bash
node .opencode/skills/skill-creator/scripts/validate_skill.cjs /path/to/skill-name --strict
```

---

## Improving an Existing Skill

Tell OpenCode: "I want to improve the skill [name]"

The skill-creator will:
1. Read the existing SKILL.md
2. Present a gap analysis
3. Propose changes
4. Apply changes with your confirmation
5. Re-run validation

---

## Next Steps

- Read `references/skill-standards.md` for the complete OpenCode skill specification
- Read `references/skill-patterns.md` for design patterns and progressive disclosure guidance
- Check `CHANGELOG.md` in the skill-creator directory for version history
