# grill-me v3.0.0 — Eval Run: FastAPI JWT Auth Migration

**Prompt**: "Quiero que me hagas el grill. Voy a reemplazar nuestro sistema de auth actual (sesiones con cookies) por JWT + refresh tokens. Somos una app FastAPI con ~10k usuarios activos."

---

## Phase 0 — Model Check

> ⚠️ **grill-me works best with a powerful model.** If you're not on Opus, consider switching with `/model claude-opus-4-6` before we begin.

---

## Phase 1 — Research

No real codebase provided — operating on hypothetical plan. No `docs/decisions/` to scan. WebSearch/WebFetch unavailable. Proceeding from training knowledge.

**Key findings from domain knowledge:**

- **Cookie sessions vs JWT**: Cookie sessions are stateful (server holds session state, typically Redis or DB). JWT is stateless — the server cannot revoke a token without a denylist or short expiry. This is the central architectural tension in this migration.
- **Refresh token security**: Refresh tokens are long-lived credentials. In a browser context, they are typically stored in httpOnly cookies (same security posture as the current system); if stored in localStorage they are vulnerable to XSS. The choice of storage is the single biggest security decision.
- **Token rotation**: Best practice for refresh tokens is refresh token rotation — each use of a refresh token issues a new one and invalidates the old. This requires server-side state for refresh tokens, partially negating the "stateless" claim of JWT.
- **Revocation**: Without a denylist, compromised JWTs remain valid until expiry. For ~10k active users this is manageable with Redis (in-memory lookup is fast), but it must be a conscious design decision.
- **Migration strategy**: Existing sessions cannot be silently migrated to JWT. There will be a forced logout event unless a compatibility shim is built (e.g., validate old session cookie → issue JWT on first hit). For ~10k active users, a forced logout is noticeable but recoverable.
- **FastAPI specifics**: `fastapi-users`, `python-jose` / `PyJWT`, and `authlib` are the common JWT libraries in the FastAPI ecosystem. Middleware vs dependency injection (`Depends`) is the standard integration point. OAuth2PasswordBearer is often used but is not the only pattern.
- **Known failure modes**:
  - Clock skew between services causing premature expiry (`nbf`/`exp` validation).
  - Access token expiry too long (security risk) or too short (UX hammering refresh endpoint).
  - Refresh token not rotated → replay attack surface.
  - Missing `aud`/`iss` claims → token substitution attacks across environments (staging token valid in prod).
  - No logout endpoint that invalidates refresh tokens server-side → ghost sessions.

---

## Phase 2 — Assumption Map

---
**Assumption Map**

| # | Assumption | Risk |
|---|---|---|
| 1 | JWT will make the system stateless, reducing DB/cache load | 🟡 Refresh tokens still require server-side storage if rotation or revocation is needed |
| 2 | Access tokens will be stored safely on the client (not localStorage) | 🔴 If stored in localStorage, XSS exposure is a blocker-level security regression |
| 3 | The current ~10k active users can tolerate a forced logout during migration | 🟡 If zero-downtime migration is required, a compatibility shim is needed |
| 4 | Refresh token rotation will be implemented | 🔴 Without rotation, a stolen refresh token grants indefinite access |
| 5 | There is a mechanism to revoke tokens (e.g., logout, account compromise) | 🔴 Pure stateless JWT has no revocation — this must be an explicit design decision |
| 6 | Access token expiry is short (e.g., 15 min) | 🟡 Long expiry negates security benefits; too short hurts UX |
| 7 | The app currently runs as a single service (not microservices sharing tokens) | 🟡 If multiple services consume the same JWT, `aud` claim validation and key distribution become critical |
| 8 | HTTPS is enforced everywhere (tokens in transit are protected) | 🔴 Tokens over HTTP are trivially stolen |
| 9 | The team understands that JWT ≠ authentication — it only proves the token was signed, not that the user is still valid | 🟡 Deactivated users can still authenticate until token expiry without a denylist |
| 10 | There is a plan for key rotation (the signing key used for JWT) | 🟡 A compromised signing key means all tokens in the wild are forged |

---

**Does this look complete? Anything missing before we start?**

*(Simulation: proceeding directly to Phase 3 per eval constraints.)*

---

## Phase 3 — Interrogation

### 1. Token Storage Strategy 🔴

No codebase to inspect, but this is the highest-impact security decision in any JWT migration for a web app. The current cookie-session system almost certainly uses httpOnly cookies, which are inaccessible to JavaScript. If refresh tokens move to localStorage (a common mistake), the security posture regresses significantly — any XSS vulnerability can exfiltrate long-lived credentials.

- **Question**: Where do you plan to store the access token and refresh token on the client? Options:
  - **A)** Access token in memory (JS variable), refresh token in httpOnly cookie — best security, same posture as your current system, survives page refresh via silent refresh pattern.
  - **B)** Both tokens in httpOnly cookies — simple, secure, but stateless benefit is minimal; effectively similar to your current setup.
  - **C)** Access token in memory, refresh token in localStorage — refresh token exposed to XSS.
  - **D)** Both in localStorage — highest XSS risk, not recommended for any app with sensitive data.
- *Recommendation*: **Option A**. Keep the refresh token in an httpOnly, Secure, SameSite=Strict cookie — this preserves the security model of your current system while gaining the stateless access token benefit. Use a short-lived access token (15 min) held in memory, with a silent refresh on app load and before expiry.
