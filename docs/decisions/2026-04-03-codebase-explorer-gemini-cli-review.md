# ADR: Codebase Explorer Gemini CLI — Design Review

**Date**: 2026-04-03
**Status**: Approved with conditions

## Context

The `codebase-explorer-gemini-cli` agent delegates codebase exploration from Claude Code to Gemini CLI (Flash model). This review stress-tested the design before first real-world use. The agent had not been tested end-to-end at the time of this review.

## Key Decisions

### Motivation
- **Decided**: Gemini Flash for cost savings and larger context window vs. Claude tokens
- **Action**: Document this motivation explicitly in the agent file

### Error Handling
- **Decided**: Replace `2>/dev/null` with selective stderr capture — suppress on success, report on failure
- **Pattern**: Redirect stderr to temp file, check exit code, surface errors only on failure

### Orchestration Model
- **Decided**: Upgrade from `haiku` to `sonnet` for better query formulation
- **Rationale**: Cost savings come from Gemini Flash doing the heavy lifting, not from the orchestrator model

### JSON Output
- **Decided**: `.response` field verified correct. Add null/empty handling
- **Schema**: `{ session_id, response, stats }` — confirmed via real execution

### Fallback Strategy
- **Decided**: If Gemini CLI fails, fall back to the built-in `Explore` subagent
- **Rationale**: Maintains exploration capability at higher cost vs. total failure

### Memory Section
- **Decided**: Simplify from ~130 lines (4 types) to ~15 lines (only `user` type)
- **Rationale**: Generic template bloat; only `user` memory is relevant for exploration

### Policy Path
- **Decided**: Make path relative to repo for portability
- **Rationale**: Agent is personal but intended to be shareable

### Invocation Limit
- **Decided**: Soft limit of 5-7 Gemini CLI calls per task
- **Action**: Instruct agent to synthesize and report if limit reached

### Verification Level
- **Decided**: Verify file paths and function names with Glob/Grep; trust content summaries
- **Rationale**: Low cost, high value — prevents most hallucination-related errors

### Output Format
- **Decided**: Add a concrete few-shot example (~15 lines) to anchor expected format

### Web Tools in Policy
- **Decided**: Remove `web_fetch` and `google_web_search` from `read-only-explorer.toml`
- **Rationale**: Reduces attack surface; not needed for pure codebase exploration

### Agent Priority
- **Decided**: Add instruction in global CLAUDE.md to always prefer this agent over built-in `Explore`
- **Rationale**: User wants Gemini-based exploration as default for cost savings

## Consequences

- Agent becomes more robust (error handling, null checks, fallback)
- Slightly higher orchestration cost (sonnet vs haiku) offset by Gemini Flash savings
- More portable and shareable
- Reduced system prompt size (memory simplification)
- Tighter security (no web access in Gemini policy)

## Open Questions

- Does the `Explore` fallback subagent inherit the `sonnet` model from the parent agent?
- Real-world performance: does sonnet + Gemini Flash actually produce better results than native Explore?
- Should the invocation limit be configurable per-task?
