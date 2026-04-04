# grill-me v3.1.0 — Eval Run 1
**Prompt**: "Grill me on my plan to split our Django monolith into 8 microservices over the next 6 months. We have a team of 5 devs and ~200k LOC."
**Date**: 2026-04-01
**Model**: claude-sonnet-4-6

---

## Phase 0 Notice

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

*(Proceeding immediately without waiting for confirmation, as instructed.)*

---

## Phase 1 — Research

### Background Agents

The skill instructs launching two background agents in parallel (`subagent_type=Explore` and `subagent_type=general-purpose`, both with `run_in_background=true`). The `Agent` tool is **not available** in this execution environment. Per the skill's fallback instructions, direct tools (`Glob`, `Grep`, `Read`, `WebSearch`) were used instead.

**Outcome summary:**

| Agent | Outcome |
|---|---|
| `Explore` agent (codebase + ADRs) | **Not available** — `Agent` tool absent. Ran `Glob` for `docs/decisions/**/*.md` directly: **no files found** (hypothetical plan, no codebase). |
| `general-purpose` agent (WebSearch) | **Not available** — `Agent` tool absent. Attempted two parallel `WebSearch` calls directly: **both denied** (permission not granted in this environment). |

**Consequence**: Research relies entirely on training knowledge. External validation (industry benchmarks on monolith→microservices migration failure rates, Fowler's Strangler Fig case studies, DORA metrics for small-team microservices rollouts) would add significant value here — flagged for future runs with WebSearch enabled.

### Research Findings (training knowledge)

Key patterns relevant to this plan:

- **Small-team bandwidth**: 5 devs splitting 8 services simultaneously is extremely aggressive. Industry experience (Martin Fowler, Sam Newman) consistently warns that microservices multiply operational surface area faster than teams expect — CI/CD pipelines, service meshes, distributed tracing, auth propagation, and on-call rotation all multiply by the number of services.
- **200k LOC baseline**: At this size, the codebase likely has significant implicit coupling — shared ORM models, shared Django middleware, cross-app imports — that is invisible until you try to cut a seam. The real migration cost is almost always 2–4x the estimate.
- **6-month timeline**: Successful monolith decompositions at this scale typically take 12–24 months. 6 months for 8 services with 5 devs has a very high probability of producing a "distributed monolith" — services that are deployed separately but still coupled via synchronous HTTP calls and a shared database.
- **Strangler Fig vs. Big Bang**: Big Bang rewrites of monoliths have a documented high failure rate. The Strangler Fig pattern (incrementally extracting services behind a facade) is the dominant industry recommendation.
- **Data ownership is the hardest problem**: Splitting a Django ORM-backed monolith means splitting the database. Shared tables, cross-service transactions, and referential integrity constraints make this the #1 source of timeline overruns.

---

## Phase 2 — Interrogation

### 1. Service Boundary Strategy 🔴

No codebase or ADRs exist to inspect. Based on training knowledge: the single most common cause of failed microservices migrations is decomposing along technical layers (e.g., "auth service", "API service") rather than along **business domain boundaries** (Domain-Driven Design bounded contexts). With 200k LOC and a shared Django ORM, the seams between your proposed 8 services almost certainly cross database tables and ORM relationships — which means the migration will require either a shared database anti-pattern or a painful data migration strategy for each cut.

- **Question**: How did you identify the boundaries for your 8 proposed microservices — are they aligned to business domain/bounded contexts (e.g., Orders, Inventory, Billing), or to technical concerns (e.g., Auth, API Gateway, Worker)? And do any two of the proposed services currently read from or write to the same Django database table?
- *Recommendation*: Boundaries should be driven by domain ownership and data ownership together. Before committing to 8 services, map every Django model to a proposed service owner. Any table with two owners is a red flag that will either block the migration or force a shared-DB anti-pattern. Start with 2–3 services maximum for the first 6 months; defer the remaining 5 to a second phase once operational patterns are proven.

---

## Overall Recommendation

Based on Phase 1 research (training knowledge only — WebSearch was denied, Agent tool unavailable), the plan as stated carries **high risk**. The combination of 5 developers, 8 services, 6 months, and 200k LOC of Django ORM code hits nearly every documented failure pattern for this class of migration.

The interrogation should continue through data ownership, deployment infrastructure, inter-service communication strategy, testing strategy, rollback plan, and team skill gaps before a final scorecard can be produced. Phase 3 (Final Scorecard) is deferred until all question branches are resolved.

---

## Tooling Outcome Summary

| Tool / Capability | Outcome |
|---|---|
| `Agent` (background, `subagent_type=Explore`) | Not available in environment |
| `Agent` (background, `subagent_type=general-purpose`) | Not available in environment |
| `WebSearch` (parallel, two queries) | Denied — permission not granted |
| `WebFetch` | Not attempted (WebSearch denied first) |
| `Glob` for `docs/decisions/` | Available, returned no results (hypothetical plan) |
| Phase 0 model notice | Delivered |
| Phase 1 research | Completed via training knowledge with noted gaps |
| Phase 2 Q1 | Delivered (see above) |
| Phase 3 scorecard | Deferred — simulation stops after Q1 per eval constraints |
