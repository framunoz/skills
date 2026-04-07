# Gemini CLI Agent Skills Configuration

> **Reference**: See [AGENTS.md](../../AGENTS.md) for the common standard.

This file provides critical instructions for any AI agent tasked with creating or modifying a Gemini CLI skill. Follow these constraints strictly.

---

## Recommended Workflow: The `skill-creator`

If you are currently running within a Gemini CLI session and have been asked to create a new skill, **you should use the built-in `skill-creator` skill.**

You can activate it using the `activate_skill` tool with the name `"skill-creator"`. This built-in skill contains expert instructions, templates, and procedures specifically designed to bootstrap new skills correctly according to the Agent Skills standard.

---

## File Structure

A skill is not just a single file; it is a directory. The standard organization is:

```text
skill-name/
├── SKILL.md       (Required) Metadata and instructions
├── scripts/       (Optional) Executable code (e.g., JS, Python, Bash)
├── references/    (Optional) Static documentation (e.g., REFERENCE.md)
└── assets/        (Optional) Templates, resources, or example data
```

---

## File Format & Frontmatter

The `SKILL.md` file MUST begin with a YAML frontmatter block containing its configuration, followed by the Markdown body which acts as its **Instructions**.

```yaml
---
name: my-custom-skill
description: Detailed explanation of what this skill does and when the agent should activate it.
license: MIT
compatibility: Requires Python 3.10+ and the 'requests' library.
metadata:
  author: creator-name
  version: "1.0.0"
---
```

### Required Fields

| Field         | Type   | Required | Description                                                                                                                          |
| :------------ | :----- | :------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | string | **Yes**  | Unique slug. Lowercase, numbers, hyphens only. Max 64 chars. Must match directory name.                                              |
| `description` | string | **Yes**  | **CRITICAL:** This is how the agent knows when to use the `activate_skill` tool. Be explicit about its capabilities. Max 1024 chars. |

### Optional Fields

| Field           | Type   | Description                                                                        |
| :-------------- | :----- | :--------------------------------------------------------------------------------- |
| `license`       | string | License name or reference to a bundled license file.                               |
| `compatibility` | string | Environment requirements (product, packages, network access, etc.). Max 500 chars. |
| `metadata`      | object | Arbitrary key-value mapping for additional metadata (author, version, tags).       |

---

## Writing the Skill Instructions

The content below the frontmatter in `SKILL.md` becomes the skill's instructions. When an agent activates a skill, it reads this content to understand how to perform the task.

When writing this section, you must include:

1. **Context & Goal**: Explain why this skill exists and what it aims to achieve.
2. **Step-by-Step Procedure**: Provide clear, sequential instructions on how the agent should execute the task.
3. **Usage of Resources**: If the skill includes scripts, references, or assets in the subdirectories, explicitly tell the agent how and when to use them (e.g., "Run the `scripts/validate.py` script to check the output").
4. **Constraints & Rules**: Explicitly list what the agent MUST NOT do while executing this skill.
5. **Expected Output**: Define how the agent should conclude the task and present the results to the user.
