# Upstream Attribution

This skill is inspired by and adapted from skill-creator tools found in other AI agent ecosystems.

## Claude Code Skill Creator

- **Source**: Anthropic Claude Code skill marketplace
- **Original Author**: Anthropic / Claude Code community
- **License**: Refer to Anthropic's terms of use for Claude Code skills
- **Inspiration**: Conversational workflow for skill authoring, progressive disclosure patterns, quality checklists

## Gemini CLI Skill Creator

- **Source**: Bundled with Google Gemini CLI
- **Original Author**: Google / Gemini CLI team
- **License**: Refer to Gemini CLI license terms
- **Inspiration**: Template-based scaffolding, `package_skill.cjs` validation approach, structured skill metadata

## Adaptation Notice

This implementation (`skill-creator` for OpenCode) is an original adaptation. It:
- Follows the OpenCode skill standard (https://opencode.ai/docs/skills.md)
- Integrates with the speckit workflow used in this project
- Uses Node.js + js-yaml instead of Python or built-in CLI tooling
- Does not include subagent/evaluation infrastructure (OpenCode does not support subagents)
- Adds Constitution-required provenance metadata

All original writing, scripts, and reference documentation in this directory are authored for this project and licensed under the terms declared in the skill's frontmatter.
