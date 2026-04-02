# Grill-Me Session — FastAPI JWT + Refresh Token Migration
**Skill version**: grill-me v3.1.0
**Date**: 2026-04-01
**Prompt**: "Quiero que me hagas el grill. Voy a reemplazar nuestro sistema de auth actual (sesiones con cookies) por JWT + refresh tokens. Somos una app FastAPI con ~10k usuarios activos."

---

## Phase 0 — Model Check

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

---

## Phase 1 — Research

### Background Agent Outcomes

**Agent 1 — Explore (codebase + docs/decisions/)**
- **Outcome**: No real codebase provided (hypothetical plan per eval constraints). No `docs/decisions/` directory found under `/Users/franciscomunoz/Codes/Personal/my-skills`. No prior ADRs on this topic.
- **Finding**: No existing auth implementation, migration scripts, or prior decisions to draw from. All questions must go to the user.

**Agent 2 — WebSearch / WebFetch (external research)**
- **Outcome**: `WebSearch` permission denied in this environment. Fell back to training knowledge as instructed by the skill.
- **Finding (from training knowledge)**:

  Key facts about the JWT + refresh token space for FastAPI at ~10k active users:

  1. **Statelessness is a double-edged sword.** JWTs are stateless by design — the server cannot invalidate a token before expiry without adding a server-side store (blocklist/allowlist). This directly negates the "we don't need a DB for auth" argument unless you accept a time window of live-but-revoked tokens.

  2. **Refresh token rotation is the current industry baseline.** RFC 9068 and OAuth 2.0 Security Best Current Practice (BCP) explicitly recommend rotating refresh tokens on every use and detecting reuse as a signal of theft. Libraries like `fastapi-users` and `authlib` support this but require persistent storage.

  3. **Cookie vs. localStorage for JWT storage.** Storing JWTs in `localStorage` is the most common mistake in the wild — it is XSS-vulnerable. The secure pattern is `httpOnly` + `SameSite=Strict` cookies, which ironically makes JWT look very similar to the cookie-session approach being replaced.

  4. **Token size matters.** JWTs grow with every claim added. At 10k active users making concurrent requests, if claims are bloated (roles, permissions, org data), this adds measurable overhead per request.

  5. **Clock skew.** Distributed deployments with JWTs require synchronized clocks (NTP). A 30–60 second `leeway` is standard but adds a security window.

  6. **`python-jose` / `PyJWT` ecosystem.** Both are common in FastAPI stacks. `python-jose` had a CVE (CVE-2024-33663) related to algorithm confusion attacks — library choice and `algorithms=` pinning is non-trivial.

  7. **Session migration path.** Moving 10k active users from sessions to JWT without forced logout requires a dual-stack period or a coordinated cutover. Rolling deployments without a plan will result in auth failures mid-session.

---

## Phase 2 — Interrogation

### 1. Refresh Token Storage 🔴

Refresh tokens are long-lived credentials. For them to be revocable (logout, compromise response, password reset), they must be stored server-side. Without that, a stolen refresh token is valid until expiry — which can be days or weeks.

The choice here cascades into: schema changes, cache layer decisions, token family design, and how you handle distributed deployments.

- **Question**: Where do you plan to store refresh tokens server-side — relational DB (e.g., a `refresh_tokens` table), a cache (e.g., Redis), or are you considering stateless refresh tokens with no server-side store?

- **Recommendation**: Use Redis with a TTL matching the refresh token lifetime. It gives you O(1) lookup, atomic revocation, and built-in expiry cleanup — without bloating your relational DB. Pair it with token family rotation (each refresh issues a new token + invalidates the old one; reuse of a consumed token revokes the entire family).

---

*Session stopped here per eval constraints (Phase 0 through first question of Phase 2 only).*

---

## Key Findings Summary

| Finding | Source | Severity |
|---|---|---|
| No prior ADRs or codebase to reference | Codebase explore | — |
| WebSearch unavailable; relied on training knowledge | Agent 2 | — |
| JWT statelessness conflicts with revocation requirements | Training knowledge | 🔴 |
| Refresh token rotation is required baseline (RFC 9068 / OAuth BCP) | Training knowledge | 🔴 |
| `python-jose` CVE — algorithm confusion risk | Training knowledge | 🔴 |
| JWT in localStorage = XSS-vulnerable (common mistake) | Training knowledge | 🔴 |
| 10k active users need a migration path to avoid forced logout | Training knowledge | 🟡 |
| Clock skew / NTP requirements for distributed JWT validation | Training knowledge | 🟡 |

---

## Recommendation (post-Phase 1)

Before writing a single line of code, the team needs to answer three questions in sequence:

1. **Revocation story**: Will you accept a time-bounded window where revoked tokens are still live, or do you need hard revocation? (This determines whether you need Redis at all.)
2. **Storage location**: Where do refresh tokens live server-side? (Redis is recommended; absence of this is a blocker.)
3. **Client storage**: Will JWTs be stored in `httpOnly` cookies or `Authorization` headers + `localStorage`? (The former is strongly preferred; the latter re-introduces XSS risk.)

The migration itself is feasible at 10k users but requires a dual-stack cutover plan. The risk level is **high** until these three questions are answered with explicit decisions.
