# Grill-Me Skill Evaluation — skills-repo-cicd

## 1. Research / Exploration Performed

Before asking any question, the following exploration was done on the repo at `/Users/franciscomunoz/Codes/Personal/my-skills`:

**Repo structure (top-level):**
- 13 skill directories, each containing a `SKILL.md` and typically an `evals/evals.json` with prompts and expected outputs.
- Skills present: `quarto-authoring`, `quarto-migrations`, `quarto-advanced`, `kedro-authoring`, `kedro-hooks-plugins`, `kedro-migration-assistant`, `kedro-notebook-converter`, `write-a-prd`, `prd-to-issues`, `tdd`, `improve-codebase-architecture`, `python-formatter`, `grill-me`.
- Some skills also have a compiled `.skill` bundle at root (e.g. `grill-me.skill`, `python-formatter.skill`, `quarto-authoring.skill`, `quarto-advanced.skill`, `quarto-migrations.skill`).
- A `grill-me-workspace/` directory exists for eval run outputs.
- `TODO.md` tracks open tasks (improve README, group skills, push Quarto files, etc.).
- No `docs/decisions/` directory exists in the repo.

**Eval structure (per skill):**
- Evals are stored as JSON (`evals/evals.json`) with `id`, `prompt`, `expected_output`, and `files` fields.
- There is no automated CI/CD pipeline currently. Evals appear to be run manually.
- The `grill-me-workspace/` directory contains iteration-based output folders (e.g. `iteration-1/`) with `eval_metadata.json` per scenario.

**Key observations relevant to CI/CD on evals:**
- No `.github/` or any CI config files (GitHub Actions, CircleCI, etc.) were found.
- No test runner, scoring script, or automation harness exists in the repo.
- Eval `expected_output` fields are prose descriptions, not structured assertions — the `assertions` array in `eval_metadata.json` is empty for this scenario. This means automated pass/fail grading is undefined today.
- Skills vary in complexity: some have only a `SKILL.md`, others have `references/` folders with domain knowledge files that the skill relies on.
- The repo has no `package.json`, `pyproject.toml`, or dependency manifest — no runtime environment is declared.

---

## 2. First Question (following the output template)

### 1. Eval Grading Strategy

The repo's evals currently define `expected_output` as free-text prose descriptions of what a good response looks like, and the `assertions` arrays are empty (e.g. `eval_metadata.json` for this scenario has `"assertions": []`). There is no scoring rubric, automated judge, or structured pass/fail criteria in the codebase today.

- **Question**: Before building the CI/CD pipeline, how do you plan to grade whether a skill's response passes or fails an eval — will you use an LLM-as-judge comparing against the prose `expected_output`, define structured assertion criteria per eval, or something else?
- *Recommendation*: Define structured, machine-checkable assertions per eval (e.g. "response contains exactly one question", "response follows the `### [N]. [Topic]` format", "response does not contain a final verdict"). Prose-based LLM judging adds cost and non-determinism to every PR. A hybrid approach works well: a fast regex/structural check first, with LLM judging only for semantic correctness on failure. This also forces you to clarify what "correct" means before automating it.

---

## 3. AskUserQuestion Tool

**Yes** — the skill instructs use of the `AskUserQuestion` tool for each question. In a live session this question would be delivered via that tool. Since this is a simulated eval, the question is written out above instead.

---

## 4. Observations / Issues About the Skill Instructions

- **Research-first instruction is strong and appropriate**: The skill explicitly says to explore the codebase and `docs/decisions/` before asking. This is the correct behavior and the most differentiating part of the skill vs. generic "grill me" prompts.
- **No docs/decisions/ to read**: The directory doesn't exist, so no prior ADRs were found. The skill handles this gracefully by simply moving on to codebase exploration.
- **AskUserQuestion tool**: The skill relies on this tool to deliver questions interactively. In batch/eval contexts where the tool is unavailable or interaction is simulated, the skill should still produce the formatted question block — and it does, via the output template.
- **Ambiguity in "research first" tooling**: The instruction says to use `Agent` with `subagent_type=Explore`. In this evaluation context that tool was not available, so Glob/Grep/Read were used directly — producing equivalent results but worth noting as a potential gap in constrained environments.
- **Finality guard**: The skill correctly defers final recommendations until all questions are answered. The first question here appropriately opens the most foundational issue (grading strategy) without jumping to conclusions about CI/CD tooling choices.
