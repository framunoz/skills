---
name: exploring-with-gemini
description: "Delegates codebase exploration to Gemini CLI (Flash model) for understanding code structure, tracing implementations, and finding dependencies. Use when navigating unfamiliar code, investigating cross-cutting concerns, searching for how a feature works, finding where a class or function is used, or understanding data flow. Prefer this skill over the built-in Explore subagent for any substantial codebase exploration task."
argument-hint: "[exploration prompt]"
---

# Exploring with Gemini

Explore the codebase by delegating to Gemini CLI, a cheaper and faster model with a larger context window. This saves Claude tokens for heavy exploration tasks.

## Usage

```bash
${CLAUDE_SKILL_DIR}/scripts/gemini-explore.sh "<your exploration prompt>"
```

The script invokes Gemini in read-only mode and returns only the final response text — no intermediate steps or tool calls are exposed.

The model defaults to `gemini-2.5-flash` and can be overridden with the `GEMINI_EXPLORE_MODEL` env var.

## Parallel exploration

Run Bash calls with `run_in_background: true` to launch multiple explorations simultaneously. This is useful when a task requires understanding several unrelated parts of the codebase at once. Keep concurrency at **3 or fewer** to stay within Gemini API rate limits.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success — stdout contains Gemini's response |
| 1 | Gemini CLI error (auth, network, bad prompt) |
| 2 | Gemini returned null/empty response |
| 3 | Missing dependency (`gemini`, `jq`, or policy file) |

## On failure

If the script fails (exit code != 0), fall back to the built-in `Explore` subagent via the Agent tool with `subagent_type=Explore`.

## Knowledge persistence

When an exploration yields findings that would be useful in future sessions (e.g., what a module does, how components connect, non-obvious architectural patterns), save them to `docs/codebase-map/` in the project root.

- One file per module/component, named by path with `--` separator (e.g., `src--auth.md`, `hooks--py-quality-gate.md`)
- Use `_overview.md` for top-level architecture
- Format per file:

```markdown
# module-name

## Purpose
One-line summary.

## Key components
- `function_name` — what it does

## Dependencies
- Depends on: X, Y
- Used by: A, B

## Notes
Any non-obvious behavior or gotchas.
```
