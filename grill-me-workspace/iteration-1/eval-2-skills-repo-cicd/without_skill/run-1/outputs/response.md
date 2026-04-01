# Response: Skills Repo CI/CD for Evals (No Skill)

Interesting plan — I explored the repo to get a feel for the architecture before weighing in.

Here's what I see:

- The repo is a **flat collection of skills**, each living in its own directory (e.g., `grill-me/`, `tdd/`, `quarto-authoring/`) alongside optional `.skill` bundle files (zip archives).
- The `grill-me` skill has a proper eval harness: `grill-me/evals/evals.json` defines prompts and expected outputs, and `grill-me-workspace/` holds iteration-level output folders (`with_skill/` and `without_skill/`).
- There's no shared eval runner, no `pyproject.toml` or `package.json`, no test framework wired up — evals appear to be run manually and outputs saved by hand.
- There are no docs/decisions/ ADRs anywhere in the repo.
- The README and TODO suggest this is still in a "personal scratchpad" phase — documentation and structure improvements are explicitly on the TODO list.

So before we talk CI/CD, I want to understand one foundational thing:

---

### 1. Eval Runner: What Actually Executes the Evals?

Right now `evals.json` defines prompts and expected outputs as plain strings, but there's no visible runner script, scoring function, or assertion logic in the repo.

- **Question**: How are evals currently being run — manually by you, through Claude Code interactively, or via some external tool (e.g., the `skill-creator` skill)? And does "auto-run evals on every PR" mean re-running the LLM and scoring the output against `expected_output`, or something lighter like a lint/schema check on the eval files?
- *Recommendation*: Before wiring up CI/CD, pin down the eval execution contract first. If evals require an LLM call (which they appear to), you'll need to decide on API key management in CI, latency budgets per PR, and a deterministic scoring rubric — otherwise "auto-run" will produce flaky, hard-to-interpret results. A lighter first step might be CI that validates the structure of `evals.json` and `SKILL.md` files on every PR, with full LLM evals gated behind a manual trigger or nightly schedule.
