# Grill Session: FastAPI JWT + Refresh Token Migration

## Context

No existing codebase to explore. The plan is to migrate a FastAPI application serving ~10k active users from cookie-based sessions to JWT + refresh tokens.

---

### 1. Token Storage Strategy on the Client

The current system uses server-side sessions with cookies, which means the server controls session invalidation. JWT shifts that control to the client — and where tokens are stored has major security implications.

- **Question**: Where do you plan to store the JWT access token and the refresh token on the client side? Options:
  - A) Both in `localStorage` / `sessionStorage` (simple, but XSS-vulnerable)
  - B) Access token in memory (JS variable), refresh token in an `HttpOnly` cookie (recommended — combines statelessness with XSS protection)
  - C) Both in `HttpOnly` cookies (most secure against XSS, but partially re-introduces stateful cookie behavior)
  - D) Access token in memory, refresh token also in memory (most stateless, but loses session on page refresh)

- *Recommendation*: Option B. Storing the access token in memory and the refresh token in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie is the industry standard for SPAs. It protects the refresh token from XSS while keeping the access token short-lived and out of persistent storage. This also means your FastAPI backend still needs a `/auth/refresh` endpoint that reads the cookie — which is worth designing carefully upfront.
