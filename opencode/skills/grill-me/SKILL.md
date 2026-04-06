---
name: grill-me
description: Interview the user relentlessly about a plan or design to stress-test it and reach a shared understanding. Use when the user asks to "grill me" or wants a deep critique of a proposal.
compatibility: OpenCode
metadata:
  author: Matt Pocock (@mattpocock)
  co-author: Francisco Muñoz (@framunoz)
  source: https://github.com/mattpocock/skills
  version: "3.2.0"
  last-updated: "2026-04-05"
  tags: interview,critique,design-review,stress-test
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Your goal is to stress-test the design and uncover hidden assumptions or dependencies.

## Phase 1 — Research

Before asking any questions, explore deeply. Think through all second-order effects and hidden dependencies as you go.

**Answer from codebase first**: If a question can be answered from the codebase or prior decisions (ADRs, interviews), answer it yourself — don't ask the user.

If useful (optional):
- Delegate to an `explore` subagent to explore the codebase for relevant files
- Run `websearch` / `webfetch` queries to gather industry benchmarks, known failure modes, best practices

Incorporate all findings before the first question.

## Phase 2 — Interrogation

Work through every assumption and branch of the design tree.

**Be exhaustive**: do not limit the number of questions. Cover every assumption and risk branch until the design tree is fully resolved.

- **Multiple questions allowed**: you don't need to ask one question at a time. Ask multiple questions in parallel when they explore independent branches. Each question can open new branches.
- **Look it up before asking**: before putting a question to the user, check if it can be resolved through a lookup — `websearch`, `webfetch`, `glob`, `read`. If yes, do it yourself and incorporate the finding into the context block.
- **Think before each question**: reason through the implications and second-order effects of each possible answer before deciding what to ask next.
- **Ask questions**: use the `question` tool. Include multiple-choice options when appropriate. Wait for the answers before moving on.
- **Adapt**: tailor follow-up questions based on previous answers. If the user answers A, explore the consequences of A. If C, explore C. Don't follow a fixed list — follow the thread.
- **Recommendations**: for each question, provide your recommended answer or perspective to help guide the decision.
- **Visual tree**: Use an ASCII tree to visualize the question/answer branches as they unfold:

```
[Topic]
├── Q1. [Risk] Question text?
│   ├── A → [Follow-up branch]
│   │   └── Q1.1. ...
│   └── B → [Follow-up branch]
└── Q2. [Risk] Question text?
    └── ...
```

### Question format

Use exactly this template for every question:

### [Number]. [🔴 / 🟡 / 🟢] [Topic Title]
[Brief context: what you found in the codebase, ADRs, or research that makes this question relevant]
- **Question**: [Your specific question]
- *Recommendation*: [Your expert opinion or proposed answer]

## Phase 3 — Final Scorecard

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

Ask the user if they want to save the scorecard. If yes, use the `edit` tool to save it as an interview-style file in `docs/interviews/YYYY-MM-DD-topic.md` — only if a project root with a recognizable structure exists. Each file should include: context, decisions made, consequences, and open questions.
