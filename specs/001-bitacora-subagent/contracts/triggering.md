# Contract: Subagent Triggering Behavior

Defines **what** makes the `logbook` subagent fire vs. what must **not** trigger it. Tests the `description` field in `AGENT.md` against a curated prompt set. Validates FR-002 and SC-002.

## Description guidelines (authoritative for `AGENT.md`)

The description frontmatter MUST:

1. **Open with a negative constraint**: e.g. *"Invoke ONLY when the user explicitly asks for the logbook subagent by name ('logbook', 'bitácora', 'bitacora'). Do NOT invoke proactively. Do NOT delegate from other subagents without an explicit user request naming this subagent."*
2. **Name the trigger phrases explicitly**: `logbook`, `bitácora`, `bitacora`, `log entry`, `registrar en bitácora`.
3. **List what this subagent does NOT do**: generic logging, general note-taking, TODO tracking, commit messages, changelog writing — none of these should fire it.
4. **Avoid bare generic verbs**: no standalone `help`, `log`, `track`, `record`, `journal` as trigger words.

## Trigger test set

The following prompts are used to evaluate the description. The evaluation is performed via **manual review**: present each prompt to the Claude Code router and verify whether the logbook subagent fires or not.

### Must fire (true positives)

1. "Usa el subagente logbook para registrar lo que salió mal en la prueba X."
2. "Call the logbook subagent to record today's collaboration session."
3. "Bitácora: agrega una entrada sobre el bug del login."
4. "Invoca el logbook para consultar qué fallos tuve la semana pasada."
5. "Open the logbook subagent and create a new amendment for entry 7."
6. "Quiero que la bitacora registre esto: la IA hizo el diseño inicial y yo corregí X."
7. "Logbook, registra en `pruebas-login` que el refresh falla en Safari."
8. "Haz una enmienda en la bitácora para aclarar la entrada 3."
9. "Inicia una nueva bitácora llamada `retro-abril`."
10. "Consulta la bitácora `pruebas-login` y resume los últimos fallos."
11. "@logbook tests-login: salió bien el OAuth redirect, falló el refresh en Safari."
12. "@logbook collab-proj: la IA propuso el esquema, yo reduje a 3 campos y corregí la clave primaria."

### Must NOT fire (negative cases)

1. "Log this error to the console." *(generic logging)*
2. "Keep a record of the files I changed today." *(generic record-keeping)*
3. "Write a changelog entry for version 2.3." *(changelog ≠ logbook)*
4. "Take notes on this meeting." *(general note-taking)*
5. "Track my tasks for this sprint." *(TODO tracking)*
6. "Can you journal my thoughts?" *(ambiguous 'journal' w/o tool name)*
7. "Add a commit message that describes this change." *(git commit message)*
8. "Write an entry in the project's README." *(README ≠ logbook)*
9. "Help me document the API." *(documentation, not logbook)*
10. "Record a summary of what worked today." — *ambiguous on purpose: no explicit tool name. Must NOT fire; the router should ask or the main agent should handle.*

## Pass criteria

- True positives: **≥ 10/12** must fire (shorthand cases 11–12 count equally).
- False positives: **0/10** on negative cases.
- If the negative set produces any fire, the description fails; tighten the negative constraint or remove offending positive keywords before release.

## When to re-run

- Every time `AGENT.md` description is edited (Constitution II PATCH or higher).
- Before tagging a new version of the subagent.
