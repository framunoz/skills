# Migrate codebase-explorer agent to skill

**Date:** 2026-04-03
**Status:** Approved with conditions

## Context

The `codebase-explorer-gemini-cli` agent delegates codebase exploration to Gemini CLI (Flash model) to save Claude tokens. The current architecture has three AI models in the chain: Main Claude → Sonnet subagent → Gemini Flash. The subagent orchestrates Gemini calls, synthesizes results, and returns a summary.

This design was questioned: the Sonnet subagent is an intermediary that adds latency, loses information through summarization, and adds architectural complexity. Since `gemini-explore.sh` already acts as a black box (input prompt → clean output text, no intermediate steps exposed), the subagent layer provides no additional isolation value.

## Decisions

### 1. Convert to skill, drop the subagent
- **Skill name:** `exploring-with-gemini`
- **No `context: fork`** — runs in main Claude's context
- **Gemini CLI (via `gemini-explore.sh`) is the real subagent** — it's the black box with input/output isolation
- Main Claude calls the script via Bash, reads the clean output directly, and acts on it

### 2. Minimal skill content
- ~20-30 lines: script path (`${CLAUDE_SKILL_DIR}/scripts/gemini-explore.sh`), exit codes (0-3), note that Gemini has read-only access
- No prompt-crafting guidance — trust Claude (especially Opus) to formulate good queries
- No output format enforcement — main Claude structures results based on original task context
- No orchestration logic — Claude decides how many times to call and what to ask

### 3. Description (under 250 chars)
> Delegates codebase exploration to Gemini CLI (Flash model) for understanding code structure, tracing implementations, and finding dependencies. Use when navigating unfamiliar code or investigating cross-cutting concerns.

### 4. Fallback strategy
- On Gemini CLI failure (exit codes 1-3), main Claude falls back to the built-in `Explore` subagent
- Fallback is handled by the caller (main Claude), not inside the skill

### 5. CLAUDE.md update
- Explicit instruction: redirect ALL codebase exploration to this skill instead of the `Explore` subagent
- The skill acts as a **token-saving proxy** — cheaper exploration via Gemini, with Explore as fallback

### 6. Project-level knowledge persistence
- Exploration findings saved to `docs/codebase-map/`
- File naming: path with `--` separator (e.g., `src--auth.md`, `hooks--py-quality-gate.md`)
- Format per file: Purpose, Key Components, Dependencies, Notes
- `_overview.md` for top-level architecture overview

### 7. Drop agent-level memory
- Main Claude's memory system handles user preferences
- Project knowledge goes to `docs/codebase-map/`

### 8. File organization
```
exploring-with-gemini/
├── SKILL.md
├── scripts/
│   ├── gemini-explore.sh
│   └── test-gemini-explore.sh
└── policies/
    └── read-only-explorer.toml
```

### 9. Migration strategy
- Keep old agent files (`agents/codebase-explorer-gemini-cli.md`, `agents/scripts/`, `agents/policies/`) until the skill is validated
- Delete after successful testing

## Consequences

### Positive
- **Simpler architecture:** 2 models (Claude + Gemini) instead of 3 (Claude + Sonnet + Gemini)
- **No information loss:** Main Claude sees Gemini output directly, no summarization bottleneck
- **Lower latency:** No subagent spawn overhead
- **Dual invocation:** User can `/exploring-with-gemini`, Claude can auto-invoke via Skill tool
- **Single source of truth:** One SKILL.md file, no duplication

### Negative
- **Main context token cost:** Gemini output goes into main context window (but output is typically concise)
- **No context isolation:** If Gemini returns very large output, it consumes main context. Mitigated by Gemini's own summarization.

### Neutral
- Old agent's ADR (`2026-04-03-codebase-explorer-gemini-cli-review.md`) remains as historical record

## Open Questions

1. **Auto-invocation verification:** Confirm Claude can auto-invoke skills via the Skill tool in practice (docs indicate yes)
2. **Knowledge persistence trigger:** When exactly should Claude write to `docs/codebase-map/`? Needs a light rule in the skill.
3. **Test scenarios:** Define 3 manual test scenarios before validating
