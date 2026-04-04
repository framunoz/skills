# grill-me v3.0.0 — Eval 2: Skills Repo CI/CD

---

## Phase 0 — Model Check

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

---

## Phase 1 — Research

Explored the codebase at `/Users/franciscomunoz/Codes/Personal/my-skills`. Key findings:

**Repo structure**
- Flat layout: each skill is a top-level directory (e.g., `grill-me/`, `kedro-authoring/`, `quarto-authoring/`) plus some loose `.skill` files (e.g., `grill-me.skill`, `python-formatter.skill`).
- Skills follow an informal convention: `SKILL.md` (the prompt injected into the agent), optional `evals/evals.json`, optional `assets/`, `references/`, and `scripts/` subdirectories.
- No `docs/decisions/` ADR directory exists — no prior architectural decisions are recorded.
- No CI config files found (no `.github/workflows/`, no `Makefile`, no `pyproject.toml`, no test runner config).
- The only automation hint is `.claude/settings.local.json` which permits `Bash(uv run:*)` and `Bash(open:*)` — suggesting `uv` is the intended Python runner.
- `grill-me/evals/evals.json` is the most mature eval file; others exist for kedro skills. Eval format is JSON: each entry has an `id`, `prompt`, `expected_output`, and an `assertions` array of plain-text strings.
- There is a `grill-me-workspace/` tree for iterative benchmarking across skill versions (`iteration-1`, `iteration-2`, `iteration-3`), with grading JSON and timing JSON per run — this is the existing "eval harness" and it is entirely manual.
- No shared eval runner script exists. Evals are run by a separate agent (the skill-creator skill) on demand, not automatically.
- Skills have no versioning convention beyond the `metadata.version` field inside `SKILL.md` front matter.
- `README.md` is a single line: "A collection of my customized skills for agents." — essentially no documentation.

**Second-order effects of adding CI/CD**
1. Evals call an LLM (the agent itself). Running on every PR means LLM API costs scale with PR frequency × number of evals × number of skills touched.
2. Assertions are free-text strings graded by a grader LLM — non-deterministic. Flaky CI will erode trust quickly.
3. There is no isolation between skills; a PR could touch multiple skills and the pipeline needs to know which evals to run (no dependency graph exists).
4. The `.skill` loose files and `SKILL.md` files are the unit of change — the pipeline needs to detect which skill changed per PR.
5. No existing test runner: the team would need to build or adopt one (e.g., the skill-creator skill's runner, or a custom script using `uv run`).
6. Secret management: the pipeline needs an Anthropic API key available as a CI secret.
7. PR review latency: LLM eval runs can take 30–120 seconds per eval; with multiple skills and multiple runs per eval, wall-clock time per PR could be several minutes to tens of minutes.

---

## Phase 2 — Assumption Map

---
**Assumption Map**

| # | Assumption | Risk |
|---|---|---|
| 1 | The existing `evals/evals.json` assertion format is sufficient to gate PRs (text-match grading is reliable enough for pass/fail) | 🔴 |
| 2 | Running evals on every PR is affordable — LLM API costs at CI scale are acceptable | 🔴 |
| 3 | The CI system will be GitHub Actions (the most natural fit for a GitHub-hosted repo) | 🟡 |
| 4 | A skill change can be detected by diffing which `SKILL.md` or `.skill` files changed, and only the affected skill's evals need to run | 🟡 |
| 5 | The eval runner (currently manual via skill-creator) can be scripted into a single CLI invocation (e.g., `uv run eval.py`) | 🟡 |
| 6 | Non-determinism in LLM outputs is acceptable — a single run per eval is enough to pass/fail | 🔴 |
| 7 | Secrets (Anthropic API key) can be safely stored in CI without additional access controls | 🟢 |
| 8 | PRs will come from a trusted source (no fork PRs from unknown contributors executing arbitrary LLM calls) | 🟡 |
| 9 | The repo structure (flat, convention-based) will remain stable enough that the CI pipeline doesn't need frequent updating | 🟢 |
| 10 | There is consensus on what "passing" means — a numeric score threshold, all assertions green, or something else | 🔴 |

---

Does this look complete? Anything missing before we start?

*(Simulated AskUserQuestion — in a live session this would be an interactive pause.)*

---

## Phase 3 — Interrogation (First Question)

### 1. Eval Reliability & Pass/Fail Definition 🔴

From exploring the repo, assertions in `evals/evals.json` are plain-text strings like `"Response contains exactly one question, not multiple"` — they are graded by a separate LLM call, which introduces non-determinism. The existing benchmark runs in `grill-me-workspace/` show per-run `grading.json` files, suggesting that grading varies between runs. There is no defined threshold (e.g., "4 of 7 assertions must pass") documented anywhere in the repo.

If the CI pipeline blocks a PR merge on a flaky or ambiguous assertion, developers will quickly start ignoring or bypassing it — making the whole system worthless.

- **Question**: Before building the pipeline, what is your pass/fail definition? Specifically: (A) all assertions must pass, (B) a fixed percentage threshold (e.g., ≥80%), (C) a weighted score where 🔴 assertions are blocking and 🟡/🟢 are advisory only, or (D) something else?
- *Recommendation*: Go with **option C** — treat 🔴 assertions as hard blockers and 🟡/🟢 as warnings surfaced in the PR comment but non-blocking. This mirrors how linters work (errors vs. warnings) and tolerates the inherent non-determinism of LLM grading without turning CI into a flakiness treadmill. Also run each eval at least twice and require both runs to agree on 🔴 failures before blocking, to filter out one-off model variance.
