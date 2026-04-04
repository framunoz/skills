# Grill Me — Django Monolith to Microservices

**Skill version**: grill-me v2.0.0 (old, baseline)
**Date**: 2026-04-01
**User prompt**: "Grill me on my plan to split our Django monolith into 8 microservices over the next 6 months. We have a team of 5 devs and ~200k LOC."

---

## Pre-question notes

- No real codebase to explore — hypothetical plan.
- No `docs/decisions/` folder found — no prior ADRs to consult.
- WebSearch was attempted and denied. Proceeding on built-in knowledge.

Industry context (from training data): Decomposing a 200k LOC Django monolith with a 5-person team is an extremely high-risk undertaking. Typical industry guidance (e.g., Sam Newman's *Building Microservices*, Fowler's "MonolithFirst" pattern) warns that teams this small routinely underestimate the operational overhead (service mesh, CI/CD per service, distributed tracing, inter-service auth, data ownership boundaries) and the cost of the Strangler Fig migration pattern. 6 months for 8 services with 5 devs leaves essentially zero capacity for feature work or incidents.

---

## Question 1

### 1. Service Boundary Justification

No codebase is available to inspect, so it is unknown whether the proposed 8 service boundaries map to genuinely independent bounded contexts (in the DDD sense) or were drawn arbitrarily (e.g., by team ownership, by Django app name, or by perceived size). Shared Django ORM models that span multiple proposed services are the single most common cause of migration failure — they force either a distributed monolith (services sharing a database) or a painful, multi-month data migration before a single service can be extracted.

- **Question**: How were the 8 service boundaries determined, and can you confirm that each proposed service owns its data exclusively — meaning no other service will need to read or write its database tables directly?

  A) Yes — each service has a clean data boundary; all cross-service data access is already going through explicit APIs or events.
  B) Mostly — there are 1–3 shared tables but we have a plan to resolve them.
  C) Not yet — we haven't fully mapped data ownership; some Django models are used across what will become multiple services.
  D) We haven't analysed this in detail yet.

- *Recommendation*: If the answer is anything other than (A), the 6-month timeline is almost certainly not achievable without descoping. The first thing I would do before any code is written is produce a full data-dependency map (a directed graph of which Django apps read/write which tables). Every edge that crosses a proposed service boundary is a risk item. Services that share data must either be merged back into one service, or the data migration must be completed — and validated in production — before the service split is considered done. Until that map exists, the "8 services in 6 months" figure is a guess, not a plan.

---

*[Simulation note: In a live session the skill would use `AskUserQuestion` here and wait for the user's answer before proceeding to question 2.]*
