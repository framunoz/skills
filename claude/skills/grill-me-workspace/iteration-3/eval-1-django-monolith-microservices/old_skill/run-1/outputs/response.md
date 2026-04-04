# Grill Me — Django Monolith to Microservices

**Skill version**: grill-me v3.0.0 (baseline)
**Prompt**: "Grill me on my plan to split our Django monolith into 8 microservices over the next 6 months. We have a team of 5 devs and ~200k LOC."
**Date**: 2026-04-01

---

## Phase 0 — Model Check

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

---

## Phase 1 — Research

No codebase, ADRs, or prior decisions are available for this hypothetical plan. Drawing on training knowledge:

**Industry context:**
- Monolith-to-microservices migrations are among the highest-risk architectural changes. The "strangler fig" pattern (incrementally extracting services) is the dominant best practice over a "big bang" rewrite.
- 200k LOC Django monolith with 5 devs over 6 months is an aggressive scope. Industry data (e.g., Sam Newman's "Building Microservices") suggests teams routinely underestimate by 2–3x.
- 8 services implies 8 independent deployment pipelines, 8 data stores to consider, and a combinatorial explosion of inter-service contracts.
- Common failure modes: distributed data consistency (lost transactions across service boundaries), shared database anti-pattern (services secretly still coupling through the DB), test environment complexity, and developer velocity collapse during the transition period.
- With 5 devs, the operational overhead of microservices (CI/CD per service, observability, on-call surface area) often consumes more bandwidth than the migration itself.

---

## Phase 2 — Assumption Map

---
**Assumption Map**

| # | Assumption | Risk |
|---|---|---|
| 1 | The 8 service boundaries are clearly defined and correspond to genuine bounded contexts with minimal cross-cutting data | 🔴 |
| 2 | The team has prior experience operating microservices (Kubernetes/Docker, distributed tracing, service mesh) | 🔴 |
| 3 | The monolith's database can be decomposed — each service will own its own data store | 🔴 |
| 4 | 6 months is sufficient for 5 devs to extract 8 services while keeping the monolith in production | 🔴 |
| 5 | Existing test coverage is high enough to validate each extraction without introducing regressions | 🟡 |
| 6 | The 200k LOC is evenly distributed such that ~25k LOC per service is a reasonable unit of work | 🟡 |
| 7 | Inter-service communication strategy (REST, gRPC, async messaging) has been decided | 🟡 |
| 8 | A strangler fig / incremental approach will be used rather than a full rewrite | 🟡 |
| 9 | Organizational structure (team ownership of services) is aligned with the proposed split | 🟡 |
| 10 | Deployment infrastructure (container orchestration, secrets management, networking) is already in place or accounted for in the timeline | 🟡 |
| 11 | The business will tolerate a likely reduction in feature velocity during the 6-month migration window | 🟡 |
| 12 | Authentication/authorization cross-cutting concerns have been addressed in the microservices design | 🟡 |
| 13 | Data consistency requirements (transactions that currently span what will become multiple services) are understood | 🔴 |
| 14 | Monitoring, alerting, and distributed tracing tooling is available or planned | 🟡 |
| 15 | There is a rollback or abort plan if the migration stalls or fails | 🟢 |

---

**[AskUserQuestion]**

Does this look complete? Anything missing before we start?

---

## Phase 3 — Interrogation

### 1. Service Boundary Definition 🔴

No codebase or ADRs are available to inspect, so there is no evidence that the 8 service boundaries have been formally mapped to bounded contexts. Premature or incorrect boundary decisions are the single most common cause of microservices migrations that produce a "distributed monolith" — services that are technically separate processes but still deeply coupled through synchronous calls or a shared database.

- **Question**: How were the 8 service boundaries determined? Specifically: are they derived from a domain-driven design exercise (bounded contexts, aggregate roots), from Django app boundaries in the existing codebase, from team ownership lines, or from a different rationale — and do any of the proposed boundaries require frequent synchronous calls between services to complete a single user-facing transaction?
- *Recommendation*: Boundaries should be derived from domain events and data ownership, not from the existing module structure of the monolith (which often reflects historical accident rather than clean domain separation). Before committing to 8, I'd strongly recommend mapping every cross-service data dependency and synchronous call path. If more than ~20% of transactions cross multiple service boundaries, the split is likely wrong and will produce coupling worse than the monolith. Consider starting with 2–3 services for the highest-value extractions and validating the approach before committing to all 8.
