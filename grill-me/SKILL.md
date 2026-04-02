---
name: grill-me
description: Interview the user relentlessly about a plan or design to stress-test it and reach a shared understanding. Use when the user asks to "grill me" or wants a deep critique of a proposal.
metadata:
  author: Matt Pocock (@mattpocock)
  co-author: Francisco Muñoz (@framunoz)
  version: "3.0.0"
  source: https://github.com/mattpocock/skills
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Your goal is to stress-test the design and uncover hidden assumptions or dependencies.

## Phase 0 — Model Check

Before doing anything else, notify the user:

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

Then proceed immediately — don't wait for confirmation.

## Phase 1 — Research

Before asking any questions, explore deeply. Think through all second-order effects and hidden dependencies as you go.

- Launch the `Agent` tool with `subagent_type=Explore` **in the background** (`run_in_background=true`) if available. While it runs, proceed in parallel: check `docs/decisions/` for prior ADRs, and use `WebSearch` / `WebFetch` to find industry benchmarks, known failure modes, and best practices. When the Explore agent completes, incorporate its findings before composing the Assumption Map.
- If the `Agent` tool is not available, use `Glob`, `Grep`, and `Read` directly (no background needed).
- If `WebSearch` / `WebFetch` are unavailable, rely on your training knowledge and note where external validation would add value.
- If a question can be answered from the codebase or prior decisions, answer it yourself — don't ask the user.

## Phase 2 — Assumption Map

Before the first question, present a structured map of every assumption you detected in the plan. This gives the user a clear picture of what the plan is built on before the interrogation begins.

Use exactly this format:

---
**Assumption Map**

| # | Assumption | Risk |
|---|---|---|
| 1 | [Detected assumption] | 🔴 / 🟡 / 🟢 |

Risk levels: 🔴 blocker if wrong · 🟡 significant rework if wrong · 🟢 minor impact if wrong

---

Then ask the user: "Does this look complete? Anything missing before we start?" via `AskUserQuestion`.

## Phase 3 — Interrogation

Work through every assumption and branch of the design tree, one question at a time.

- **Think before each question**: reason through the implications and second-order effects of each possible answer before deciding what to ask next.
- **Ask one question at a time**: use the `AskUserQuestion` tool. Include multiple-choice options when appropriate. Wait for the answer before moving on.
- **Adapt**: tailor follow-up questions based on previous answers. If the user answers A, explore the consequences of A. If C, explore C. Don't follow a fixed list — follow the thread.
- **Be exhaustive**: do not limit the number of questions. Cover every assumption and risk branch until the design tree is fully resolved.
- **Recommendations**: for each question, provide your recommended answer or perspective to help guide the decision.

### Question format

Use exactly this template for every question:

### [Number]. [Topic Title] [🔴 / 🟡 / 🟢]
[Brief context: what you found in the codebase, ADRs, or research that makes this question relevant]
- **Question**: [Your specific question]
- *Recommendation*: [Your expert opinion or proposed answer]

## Phase 4 — Final Scorecard

Only deliver this once all questions have been answered and all branches are resolved.

Produce a structured scorecard followed by your overall recommendation:

---
**Design Scorecard**

| Area | Risk | Decision Made | Open Questions |
|---|---|---|---|
| [Area] | 🔴 / 🟡 / 🟢 | [What was decided] | [Anything still unresolved] |

**Overall verdict**: [Approved / Approved with conditions / Not recommended]

**Conditions / next steps** (if any):
- [Specific action or decision still needed]

---

Then, use the `Write` tool to save the scorecard and key decisions as an ADR-style file in `docs/decisions/YYYY-MM-DD-topic.md` — only if a project root with a recognizable structure exists. Each file should include: context, decisions made, consequences, and open questions.
