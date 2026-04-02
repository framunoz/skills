# Grill-Me v3.1.0 — Eval 2: skills-repo-cicd

**User prompt**: "Grill me on the architecture of this skills repo — I'm thinking of adding a CI/CD pipeline that auto-runs evals on every PR."

---

## Phase 0 — Model Check

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

*(Proceeding immediately without waiting for confirmation.)*

---

## Phase 1 — Research

### Background Agent Attempts

Per the skill instructions (Phase 1), two background agents were to be launched in parallel:

1. **`subagent_type=Explore` (background, codebase + ADRs)** — The `Agent` tool is not available in this execution context. Fell back to direct `Glob`, `Grep`, and `Read` calls as instructed.
2. **`subagent_type=general-purpose` (background, WebSearch/WebFetch)** — `WebSearch` and `WebFetch` are listed as deferred tools. They were not invoked; relying on training knowledge with a note that external validation would add value for framework comparisons (e.g., promptfoo vs. braintrust vs. inspect-ai benchmarks).

**Outcome**: Both background agent launches were skipped due to tool unavailability. Direct codebase exploration was performed instead in a single parallel batch of `Glob`, `Read`, and `Bash` calls.

---

### Codebase Findings

**Explored**: `/Users/franciscomunoz/Codes/Personal/my-skills`

**Repo layout:**

| Path | What it is |
|---|---|
| `grill-me/`, `tdd/`, `python-formatter/`, `kedro-authoring/`, etc. | 12+ skill directories, each with a `SKILL.md` as the canonical definition |
| `*.skill` files at root (`grill-me.skill`, `quarto-authoring.skill`, …) | Compiled/bundled skill artifacts — **gitignored** via `.gitignore` (`*.skill`) |
| `grill-me/evals/evals.json` | Eval suite for grill-me: 3 scenarios with `id`, `prompt`, `expected_output`, and structured `assertions` array |
| `kedro-authoring/evals/evals.json`, `kedro-hooks-plugins/evals/evals.json`, etc. | Several kedro skills also have eval files — eval coverage is uneven |
| `grill-me-workspace/` | Manual output store: `iteration-N/eval-N-topic/with_skill\|without_skill/run-N/outputs/response.md` |
| `grill-me-workspace/iteration-N/eval-N/eval_metadata.json` | Per-eval structured assertions (8 items for this exact scenario in iteration-3) |
| `grill-me-workspace/skill-snapshot-v2/`, `skill-snapshot-v3/` | Historical SKILL.md snapshots for manual regression comparison |
| `.claude/settings.local.json` | Permissions: only `Bash(uv run:*)` and `Bash(open:*)` are allowed |
| `TODO.md` | Open tasks: improve README, review Matt Pocock skills — no CI/CD mentioned |
| `README.md` | 3-line stub with no architecture or contribution docs |

**Key structural observations:**

1. **No CI/CD exists.** No `.github/` directory, no GitHub Actions workflows, no CI config of any kind in the repo.
2. **No declared toolchain.** No `package.json`, `pyproject.toml`, `requirements.txt`, or `Makefile`. Zero runtime dependencies declared.
3. **Eval runner does not exist.** The `evals.json` format defines prompts and assertions, but no script anywhere reads a prompt, calls an LLM, captures the response, and checks assertions. The harness is entirely manual.
4. **Eval coverage is partial.** `grill-me`, `kedro-authoring`, `kedro-hooks-plugins`, `kedro-migration-assistant`, `kedro-notebook-converter` have eval files. `tdd/`, `improve-codebase-architecture/`, `python-formatter/`, `write-a-prd/`, `prd-to-issues/`, `quarto-*` skills have none.
5. **Outputs are markdown prose.** `response.md` files are human-readable, not machine-parseable without an LLM judge or regex.
6. **`.skill` bundles are gitignored.** A CI runner would not have compiled artifacts — it would need to use `SKILL.md` source directly or regenerate bundles.
7. **Workspace output is committed manually.** The `grill-me-workspace/` tree implies a human runs evals, writes outputs, and commits them. CI would need to replace or parallel this workflow.
8. **Permissions are locked down.** `.claude/settings.local.json` only allows `uv run` and `open` — any CI runner using this settings file could not execute arbitrary shell commands without updating permissions.
9. **No `docs/decisions/` directory.** No prior ADRs exist. This is the first architectural decision being considered for CI/CD.

---

## Phase 2 — Interrogation

### 1. Eval Execution Environment 🔴

The repo has no declared toolchain and no runner script. The skills are designed to run inside Claude Code (an interactive agent harness), not as a standalone CLI command. The `evals.json` files define prompts and assertions, but nothing executes them: there is no code that reads a prompt, calls an LLM, captures output, and checks the structured assertions in `eval_metadata.json`. The `.claude/settings.local.json` only permits `uv run` and `open` commands — any CI step would need to work within or update that constraint. Without a scriptable, headless execution path, no other CI/CD decision (triggers, secrets management, PR gating) can be resolved.

- **Question**: How do you plan to execute a skill eval in CI — will you build a custom runner script that calls the Anthropic API directly (bypassing Claude Code's interactive harness), adopt an existing LLM eval framework (e.g., `promptfoo`, `braintrust`, `inspect-ai`), or find a way to invoke Claude Code in a headless/scripted mode?

- *Recommendation*: Use an existing LLM eval framework rather than rolling your own. `promptfoo` has native support for prompt files, structured assertion types (`contains`, `regex`, `llm-rubric`), and first-class GitHub Actions integration. Your `evals.json` `assertions` array maps directly onto promptfoo's `tests` format — structural checks (e.g., "response contains exactly one question", "response uses the output template format") become fast deterministic `regex` assertions, while semantic checks (e.g., "agent explored the codebase before asking") become `llm-rubric` passes that you can gate behind a `--tag expensive` flag to keep PR feedback latency under 60 seconds. This avoids building and maintaining a bespoke runner, handles API key injection via environment variables, and keeps the CI step as a single `npx promptfoo eval` invocation. The `uv run` permission in `.claude/settings.local.json` suggests a Python-first toolchain preference — `inspect-ai` (Anthropic-native, Python) is the strongest alternative if you want to avoid Node.js.

---

*(In a live session this question would be delivered via the `AskUserQuestion` tool. This is a simulation, so it is written out directly. Only one question is posed — Phase 2 stops here per eval instructions.)*
