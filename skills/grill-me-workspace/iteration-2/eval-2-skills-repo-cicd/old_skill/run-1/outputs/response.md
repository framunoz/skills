# Grill Me — CI/CD Pipeline for Evals on Every PR

> Note: I explored the codebase at `/Users/franciscomunoz/Codes/Personal/my-skills` before asking. Key findings:
> - The repo contains ~13 skills, structured as `skill-name/SKILL.md` directories plus compiled `.skill` zip artifacts (e.g. `grill-me.skill`, `python-formatter.skill`).
> - Only 5 skills have `evals/evals.json` files: `grill-me`, `kedro-authoring`, `kedro-hooks-plugins`, `kedro-migration-assistant`, `kedro-notebook-converter`. Skills like `quarto-*`, `python-formatter`, `tdd`, `write-a-prd`, etc. have **no evals at all**.
> - There is no existing CI/CD configuration (no `.github/workflows/`, no `Makefile`, no test runner config).
> - No `docs/decisions/` directory exists — no prior ADRs to consult.

---

### 1. Eval Coverage Gap

Only 5 of ~13 skills currently have `evals/evals.json` files. The quarto-*, python-formatter, tdd, write-a-prd, prd-to-issues, and improve-codebase-architecture skills have no evals defined.

- **Question**: Before wiring up a CI/CD pipeline that "auto-runs evals on every PR," how do you plan to handle the skills that have no evals yet — will the pipeline skip them silently, block the PR if evals are missing, or will adding evals for all skills be a prerequisite before CI/CD is introduced?
- *Recommendation*: Require evals to exist before a skill can be merged/modified. A pipeline that silently skips unevaluated skills creates a false sense of coverage — you'll get green checks on PRs that change `quarto-authoring` while that skill goes completely untested. I'd gate the pipeline on eval presence: if a skill directory has no `evals/evals.json`, the CI job should fail with a clear message. This forces eval authorship to be part of the skill development workflow rather than an afterthought.

*(Using AskUserQuestion tool — waiting for answer before proceeding.)*
