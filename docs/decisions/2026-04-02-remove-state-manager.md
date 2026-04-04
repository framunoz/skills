# ADR: Remove State Manager from Hooks System

**Date:** 2026-04-02  
**Status:** Approved

## Context

The hooks system used `utils/state-manager.js` (~100 lines) to share state between `py-format-silent` (PostToolUse) and `py-quality-gate` (Stop). The state tracked:
- `files`: array of modified Python file paths
- `retryCount`: number of failed quality gate attempts

However, `py-quality-gate` **never reads `state.files`** — it only checks if the state file exists (as a boolean signal) and reads `retryCount`. Diagnostics run on `.` (the entire project), not on tracked files. The `files` array was dead data.

The state-manager introduced unnecessary complexity: session-scoped JSON files, 24h cleanup, a shared module dependency, and a communication channel between hooks that served no real purpose.

## Decisions

1. **Eliminate `state-manager.js`** — the shared state abstraction is not justified by its single consumer (a retry counter).
2. **Inline retry persistence in `py-quality-gate.js`** — simple file in `/tmp/` with 24h cleanup.
3. **Run quality-gate on every Stop event** — no longer gated by state file existence. Ruff/Pyrefly are fast when no Python files exist.
4. **Keep hooks separated** — `py-format-silent` (PostToolUse) handles formatting, `py-quality-gate` (Stop) handles validation. Clear separation of concerns.
5. **Maintain `ruff check --fix`** — pragmatic auto-correction during quality gate.
6. **Fix invalid `stopReason` field** — replace with `{}` (fail-open) on max retries.
7. **Fix double `logger.finish()` calls** — only call in main flow, not inside handlers.

## Consequences

- **Simplified architecture**: Two independent hooks with no shared state module.
- **Fewer files**: `state-manager.js` deleted, `tmp/hooks/` directory no longer needed.
- **Slightly more diagnostic runs**: Quality gate runs on every Stop, even for non-Python sessions (~1-2s overhead, negligible).
- **Clearer retry logic**: Retry counter is local to the hook that uses it.

## Open Questions

None.
