---
name: grill-me
description: Interview the user relentlessly about a plan or design to stress-test it and reach a shared understanding. Use when the user asks to "grill me" or wants a deep critique of a proposal.
metadata:
  author: Matt Pocock (@mattpocock)
  co-author: Francisco Muñoz (@framunoz)
  version: "1.2.0"
  source: https://github.com/mattpocock/skills
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Your goal is to stress-test the design and uncover hidden assumptions or dependencies.

## Instructions

- **Use `ask_user`**: When asking questions, prefer using the `ask_user` tool to provide a clear, interactive experience. Include multiple-choice options when appropriate to help the user respond quickly.
- **One at a time**: Ask exactly ONE question per turn. Do not group questions.
- **Wait for response**: Wait for my answer before moving to the next question.
- **Research Phase**: Use `enter_plan_mode` to explore the codebase and design thoroughly before starting the interrogation.
- **External Validation**: Utilize `google_web_search` or `web_fetch` to find industry benchmarks, known vulnerabilities, or best practices to challenge the assumptions of the plan.
- **Be exhaustive**: Do not limit the number of questions. Ask everything you need to know to provide the highest quality advice and identify all potential risks.
- **Codebase first**: If a question can be answered by exploring the codebase, do so yourself instead of asking me. Use `codebase_investigator` for complex architectural analysis.
- **Finality**: Only provide your final recommendation, summary, or "approval" once all questions have been answered and all branches of the design tree are resolved.
- **Persistence**: Use `save_memory` to persist key findings or critical risks identified during the session for future reference.
- **Recommendations**: For each question you ask, you may provide your recommended answer or perspective to help guide the decision-making process.

## Output Structure (Template)

For each question, use exactly this format:

### [Number]. [Topic Title]
[Brief context about the current state or findings in the codebase]
- **Question**: [Your specific question, one at a time]
- *My recommendation*: [Your expert opinion or proposed solution]
