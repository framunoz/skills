# Grill Me — Django Monolith to Microservices
**Skill**: grill-me v3.0.0
**Date**: 2026-04-01
**User prompt**: "Grill me on my plan to split our Django monolith into 8 microservices over the next 6 months. We have a team of 5 devs and ~200k LOC."

---

## Phase 0 — Model Check

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

---

## Phase 1 — Research Notes

**Codebase / ADRs**: No real codebase exists and no `docs/decisions/` folder is present — this is a hypothetical plan. No prior ADRs to consult.

**WebSearch**: Permission was denied. All analysis relies on training knowledge (cutoff: August 2025). External validation would add value in the following areas:
- Current industry data on microservices migration timelines per LOC and team size
- Django-specific ORM unbundling patterns (e.g., shared-database-separate-schema approaches)
- Post-mortems from teams of similar size who attempted 6-month splits

**Training-knowledge findings applied**:
- The "8 services in 6 months with 5 devs" ratio is a well-known danger zone: each service requires its own CI/CD pipeline, observability stack, inter-service contracts, and on-call surface — all of which compound developer cognitive load multiplicatively, not additively.
- 200k LOC in a Django monolith almost certainly has a highly entangled ORM layer. Django's implicit foreign-key joins across apps routinely survive as cross-service data dependencies that become distributed transactions post-split.
- The Strangler Fig pattern is the dominant industry approach for live systems; a "big bang" rewrite has a poor track record at this scale.
- Conway's Law predicts that 8 services owned by 5 devs will result in unclear ownership, with individuals owning 1.5–2 services on average — a fragile arrangement during incidents.

---

## Phase 2 — Assumption Map

---
**Assumption Map**

| # | Assumption | Risk |
|---|---|---|
| 1 | 6 months is sufficient to extract 8 services from a 200k LOC Django monolith | 🔴 |
| 2 | The 5-dev team can absorb migration overhead AND maintain feature velocity simultaneously | 🔴 |
| 3 | Service boundaries are already well-understood and agreed upon | 🔴 |
| 4 | The existing Django ORM / database can be cleanly decomposed per service without cross-schema joins | 🔴 |
| 5 | Each of the 8 services will have a clear owner on a 5-person team | 🟡 |
| 6 | The team has existing expertise in distributed systems, service meshes, and async messaging | 🟡 |
| 7 | There is an existing CI/CD, observability, and secrets-management platform ready to serve multiple services | 🟡 |
| 8 | Inter-service communication contracts (REST / gRPC / events) have been designed | 🟡 |
| 9 | Data consistency across services (eventual vs. strong) is acceptable for all current business workflows | 🟡 |
| 10 | Stakeholders accept potential feature slowdown or increased bug risk during the migration window | 🟡 |
| 11 | The monolith's test coverage is high enough to detect regressions during extraction | 🟡 |
| 12 | Authentication/authorization can be cleanly extracted or federated across services | 🟡 |
| 13 | "8 services" is the right granularity (not too many, not too few) for this team and codebase | 🟡 |
| 14 | There is no hard regulatory, compliance, or SLA constraint that forbids a transitional dual-run period | 🟢 |
| 15 | Deployment infrastructure costs (containers, orchestration, networking) are budgeted | 🟢 |

---

> **AskUserQuestion (simulated)**: "Does this look complete? Anything missing before we start?"

---

## Phase 3 — Interrogation (First Question)

### 1. Service Boundary Definition 🔴

No codebase or ADRs exist to examine, so there is no documented evidence that the 8 service boundaries have been formally analyzed. In Django monoliths of this size, Django "apps" are the natural candidate for service extraction — but they frequently share models via direct ORM foreign keys, making a clean split impossible without either duplicating data, introducing sync jobs, or accepting eventual consistency. Industry post-mortems (e.g., Segment, Istio early adopters) consistently cite premature or poorly-reasoned boundary selection as the primary cause of failed microservices migrations.

- **Question**: How were the 8 service boundaries determined — and for each proposed boundary, have you mapped every database-level foreign key and every in-process function call that currently crosses that boundary?
  - A) Yes — we have a full dependency map (FK graph + call graph) for each proposed boundary
  - B) We've done a rough domain analysis (e.g., by Django app or team ownership) but haven't audited cross-boundary data dependencies in detail
  - C) The 8 services are aspirational / org-chart-driven; the technical boundary work hasn't been done yet
  - D) We have a partial map for the highest-priority services but not all 8

- *Recommendation*: **Option A is the minimum bar before committing to this plan.** If you're at B, C, or D, the 6-month timeline is almost certainly wrong — the boundary analysis alone typically takes 4–8 weeks for a 200k LOC Django monolith, and the findings frequently reduce the number of viable services or force a phased approach. I would strongly recommend producing a full FK + call-graph dependency map for all 8 proposed boundaries before locking in the timeline or service count. Tools like `django-extensions` graph_models and static import analysis (e.g., `pydeps`) can accelerate this.

---

> **AskUserQuestion note**: Per the skill's Phase 3 instructions, the next step is to deliver this question via `AskUserQuestion` and wait for the answer before proceeding. Since this is a simulation, the interrogation stops here after the first question. In a live session, the follow-up questions would adapt based on which option (A/B/C/D) the user selects.

---

*WebSearch was denied during Phase 1 — all findings are based on training knowledge. External validation on microservices migration benchmarks and Django-specific decomposition patterns would strengthen the analysis.*
