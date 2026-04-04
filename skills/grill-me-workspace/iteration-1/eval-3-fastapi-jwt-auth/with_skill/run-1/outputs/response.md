# Grill-Me Skill Evaluation — FastAPI JWT Auth Migration

## 1. Research Performed

**Codebase exploration**: Not applicable — no real codebase exists for this hypothetical scenario. The skill instructs using an `Agent` tool with `subagent_type=Explore` and reading `docs/decisions/` ADRs. Neither was available here.

**Web search**: Attempted two searches on JWT security best practices and JWT vs session cookie tradeoffs. WebSearch permission was denied in this environment. Research was conducted from model knowledge (cutoff August 2025).

**Key findings from prior knowledge used to inform the question:**

- JWTs are stateless by default, which makes **token revocation** the single hardest problem in any JWT migration. With sessions+cookies, revocation is trivial (delete the session row). With JWTs, an access token remains valid until expiry even after logout or credential change.
- The most common mitigation is a short-lived access token (e.g., 15 min) paired with a longer-lived refresh token stored server-side in a revocation-capable store (Redis, DB). This partially reintroduces statefulness.
- FastAPI has no built-in JWT support; the ecosystem typically uses `python-jose` or `PyJWT` plus custom middleware.
- Refresh token rotation and refresh token families (detecting reuse = compromise indicator) are best-practice patterns (RFC 6819, OAuth 2.0 Security BCP).
- With ~10k active users the scalability argument for JWTs (avoiding DB hits per request) is valid but relatively modest — a well-indexed session table handles this load trivially.
- The motivation for the migration is not stated, making it the most important first question.

---

## 2. First Question (Skill Output Format)

### 1. Motivación del Cambio

No hay codebase disponible para inspeccionar, pero el escenario describe una migración desde sesiones con cookies hacia JWT + refresh tokens en una aplicación FastAPI con ~10k usuarios activos. Antes de evaluar cualquier aspecto técnico del diseño, es crítico entender por qué se está haciendo este cambio: el riesgo de una migración de autenticación mal motivada es alto (complejidad añadida sin beneficio real), y la arquitectura óptima depende fuertemente del driver.

- **Question**: ¿Cuál es el problema concreto que esta migración busca resolver? ¿Por qué las sesiones con cookies ya no son suficientes?

  Opciones:
  - **A) Escalabilidad horizontal**: Necesitas correr múltiples instancias del servidor y no quieres sticky sessions ni un store de sesiones compartido (Redis/DB).
  - **B) Clientes no-browser**: Tienes o planeas tener clientes móviles, CLIs, o APIs de terceros donde las cookies son incómodas o inviables.
  - **C) Arquitectura de microservicios**: Quieres que otros servicios internos puedan verificar identidad sin llamar de vuelta al servicio de auth.
  - **D) Exigencia externa**: Un auditor, estándar de compliance (OAuth2, OIDC), o integración con un IdP externo lo requiere.
  - **E) Tendencia / modernización**: No hay un problema específico; JWT se percibe como "la forma moderna" de hacer auth.
  - **F) Otra razón** (describir).

- *Recommendation*: Si la respuesta es **E**, la migración probablemente no vale la pena. Las sesiones con cookies son más simples, más fáciles de revocar, y menos propensas a vulnerabilidades de implementación. Para 10k usuarios activos, el argumento de rendimiento a favor de JWT es marginal. Si la respuesta es **A, B, C, o D**, hay casos legítimos — pero cada uno implica un diseño distinto (p. ej., para A basta con un Redis session store; solo B o C justifican realmente JWT stateless). Conocer el driver real permite recomendar si JWT es la solución correcta o si existe una alternativa más simple.

---

## 3. AskUserQuestion Tool

**Would use it**: Yes. The skill explicitly instructs using the `AskUserQuestion` tool for each question. In a real Claude Code session this question would be delivered via that tool (with the multiple-choice options formatted as choices), waiting for the user's answer before proceeding to the next question.

---

## 4. Observations and Issues

| # | Observation |
|---|-------------|
| 1 | **`subagent_type=Explore` agent**: The skill instructs using an `Agent` tool with `subagent_type=Explore` to investigate the codebase. This parameter does not exist in the standard Claude Code `Agent` tool schema — it would likely be ignored or error. The intent (codebase exploration) is valid but the instruction may be outdated or refer to a non-standard configuration. |
| 2 | **WebSearch unavailable**: The skill instructs using WebSearch for external validation. In this eval environment the tool was denied, so external validation could not be performed. The skill should perhaps make WebSearch optional or degrade gracefully. |
| 3 | **`docs/decisions/` write step**: The skill instructs writing ADR files to `docs/decisions/` inside the current project. With no codebase present this is impossible, but the instruction is also premature for a first question — ADRs should be written after decisions are made, not before. The placement of this instruction alongside the research step is slightly ambiguous. |
| 4 | **Language handling**: The user prompt was in Spanish. The skill instructions are in English but contain no language directive. The skill responded naturally in Spanish, which is correct behavior — worth noting that the skill is language-agnostic by default. |
| 5 | **No question count limit**: The skill correctly instructs "do not limit the number of questions," which is appropriate for a stress-testing interview. This means the grill can be extensive and thorough. |
