# Grill-Me Skill Response: Django Monolith to Microservices

## 1. Research Conducted

**Codebase exploration**: No actual codebase exists for this evaluation — the plan is hypothetical. No `docs/decisions/` folder was available to consult for prior ADRs.

**WebSearch**: Attempted but permission was denied in this evaluation environment. The question and recommendation below are therefore grounded in Claude's built-in knowledge of industry benchmarks and best practices (Sam Newman's "Building Microservices", Martin Fowler's Strangler Fig pattern, and widely-reported case studies from Netflix, Shopify, Airbnb, etc.).

**Key industry context applied**:
- The "two-pizza team" rule suggests one microservice per team of 5–8; a team of 5 splitting into 8 services is a well-known anti-pattern (more services than sub-teams to own them).
- 200k LOC is a medium-large monolith. Domain boundary identification is the hardest and most consequential step.
- 6 months is an aggressive timeline; Shopify's Pods migration and Airbnb's service decomposition each took 2–4 years with much larger teams.
- Cross-cutting concerns (auth, data consistency, distributed tracing, deployment pipelines) multiply per-service overhead significantly.

---

## 2. First Question (Formatted per Skill Template)

### 1. Service Ownership and Team Capacity

No existing codebase or ADRs were available to review. Based on the stated constraints (5 developers, 8 planned microservices, 6-month window), there is a structural mismatch: your team would own more services than it has sub-teams to maintain them, before accounting for the operational overhead each service introduces (CI/CD pipeline, monitoring, on-call rotation, inter-service contract testing).

- **Question**: How do you plan to map service ownership across a 5-person team for 8 microservices — and have you accounted for the operational overhead (separate deployments, monitoring, inter-service contracts) that each new service adds on top of feature work? Specifically:
  - (A) Each developer owns 1–2 services end-to-end, and we've allocated dedicated sprint capacity (e.g., 30–40%) for migration/ops work.
  - (B) The team shares ownership collectively, with no hard per-service assignments.
  - (C) We plan to hire additional engineers in parallel with the migration.
  - (D) We haven't fully mapped this yet — the 8-service number came from the domain model, not from team capacity.

- *Recommendation*: Option A is the least risky if capacity is explicitly ring-fenced, but 8 services for 5 people is still high. Industry guidance (e.g., Sam Newman) suggests starting with 2–3 extractions that have the clearest domain boundaries and lowest coupling, then expanding the service count once the team has internalized the operational patterns. Splitting into 8 simultaneously — or even in parallel streams — dramatically increases the blast radius if a service boundary turns out to be wrong.

---

## 3. AskUserQuestion Tool

**Would use**: Yes. The skill explicitly requires using the `AskUserQuestion` tool for each question. In a live session, the question above would be delivered via `AskUserQuestion` with the four multiple-choice options embedded, and the conversation would pause until the user replied before proceeding to the next question.

---

## 4. Observations and Issues About the Skill Instructions

1. **`docs/decisions/` assumption**: The skill instructs reading `docs/decisions/` for prior ADRs, but this folder will often not exist (as here). The instruction handles absence gracefully by implication, but could be made explicit with a fallback ("if the folder does not exist, proceed without it").

2. **`Agent` tool with `subagent_type=Explore`**: The skill calls for using an `Agent` tool with a specific `subagent_type=Explore` parameter. This tool/subtype was not available in the current environment; the instruction is tightly coupled to a specific Claude Code internal capability that may not be universally accessible.

3. **WebSearch permission**: The skill requires WebSearch for external validation, but this environment denied it. In a real project context this would work; for eval sandboxes it may need a fallback note.

4. **Persist findings to `docs/decisions/`**: The skill instructs writing ADR-style files as findings accumulate. With no existing project repo, this would create files in an unexpected location. The instruction could benefit from a guard — "only write if a project root is detected."

5. **Tone calibration**: The skill title says "relentlessly" and the instructions say "be exhaustive / do not limit the number of questions." The first question appropriately prioritizes the highest-risk structural concern (team capacity vs. service count) rather than jumping to implementation details — this is consistent with good interview practice.
