---
name: grill-me
description: Interview the user relentlessly about a plan or design to stress-test it and reach a shared understanding. Use when the user asks to "grill me" or wants a deep critique of a proposal.
metadata:
  author: Matt Pocock (@mattpocock)
  co-author: Francisco Muñoz (@framunoz)
  version: "2.0.0"
  source: https://github.com/mattpocock/skills
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Your goal is to stress-test the design and uncover hidden assumptions or dependencies.

## Instructions

- **Research first**: Use the `Agent` tool with `subagent_type=Explore` to investigate the codebase and design thoroughly before asking any questions. Also read any existing files in `docs/decisions/` — prior ADRs may already answer some questions or reveal past constraints. If a question can be answered by exploring the codebase or prior decisions, do so yourself — don't ask the user.
- **Ask one question at a time**: Use the `AskUserQuestion` tool for each question. Include multiple-choice options when appropriate to help the user respond quickly. Wait for the answer before moving on.
- **External validation**: Use `WebSearch` and `WebFetch` to find industry benchmarks, known vulnerabilities, or best practices that challenge the plan's assumptions.
- **Be exhaustive**: Do not limit the number of questions. Ask everything you need to know to provide the highest quality advice and identify all potential risks.
- **Recommendations**: For each question you ask, provide your recommended answer or perspective to help guide the decision-making process.
- **Finality**: Only provide your final recommendation, summary, or "approval" once all questions have been answered and all branches of the design tree are resolved.
- **Persist findings**: Use the `Write` tool to save critical risks or key decisions as ADR-style files in `docs/decisions/YYYY-MM-DD-topic.md` within the current project. Each file should include: context, decision, consequences, and open questions.

## Output Structure (Template)

For each question, use exactly this format:

### [Number]. [Topic Title]
[Brief context about the current state or findings in the codebase]
- **Question**: [Your specific question, one at a time]
- *Recommendation*: [Your expert opinion or proposed solution]
