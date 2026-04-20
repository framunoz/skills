# Quickstart — Logbook Subagent

End-to-end walkthrough for installing and using the logbook tooling in a consumer project. Validates User Stories 1–3 from `spec.md`.

## Prerequisites

- Claude Code installed and configured.
- Python 3 available on `$PATH` (`python3`, stdlib only — no venv required).
- A project where you want to keep a logbook.

## Install

The logbook toolkit ships as a single Claude Code plugin inside the `framunoz-skills` marketplace. Two installation paths:

**From a local clone** (recommended during development):

```
/plugin marketplace add ~/Codes/Personal/my-skills
/plugin install logbook@framunoz-skills
```

**From GitHub**:

```
/plugin marketplace add https://github.com/framunoz/skills
/plugin install logbook@framunoz-skills
```

Installing the plugin registers the subagent (`logbook`) and all five skills (`logbook-push`, `logbook-format`, `logbook-init`, `logbook-list`, `logbook-query`) in one atomic step.

Verify Claude Code sees everything:

```
/plugin list   # should list 'logbook' as installed
/agents        # should list 'logbook'
/              # should offer /logbook-format, /logbook-list, /logbook-query
```

> **Note**: `/logbook-push` and `/logbook-init` are intentionally absent from the user-accessible command list — those are internal subagent operations.

## Scenario 1 — Record a test outcome (User Story 1, P1)

In Claude Code, invoke the subagent by name — using either the full form or the shorthand:

**Shorthand** (slug explicit in the message):

> "@logbook tests-login: salió bien el OAuth redirect, salió mal el refresh en Safari. Próximo paso: reproducir en staging."

**Full form**:

> "Usa el subagente **logbook** para registrar en `tests-login`: salió bien el OAuth redirect, salió mal el refresh en Safari."

The subagent:

1. Identifies the target logbook (`tests-login`).
2. If `tests-login` doesn't exist yet, notifies the user and creates it automatically.
3. Infers entry type `tests` from the content.
4. Optionally enriches the entry with relevant context from the current conversation (open files, recent decisions).
5. Presents the composed entry for confirmation, then pipes the JSON payload to `logbook-push`.
6. Reports back the new entry `id` and the file path written.

Inspect the result:

```bash
cat logbook/tests-login/entries.jsonl
```

Or render to Markdown directly (user-invocable):

```
/logbook-format tests-login
```

```bash
cat logbook/tests-login/rendered.md
```

**Expected**: `entries.jsonl` has exactly one new line; `rendered.md` shows the entry with "Went well" and "Went wrong" sections.

## Scenario 2 — Record AI/human collaboration (User Story 2, P2)

> "@logbook collab-v1: la IA propuso el esquema inicial de la tabla `users`, yo decidí mantener solo 3 campos y le corregí el nombre de la clave primaria. Hito: diseño DB v1."

The subagent creates `collab-v1` if it doesn't exist, infers type `collaboration`, and enriches the entry with context from the session (e.g., which files were open, what was being discussed).

**Expected**: the resulting entry has distinct `ai_contribution`, `human_contribution`, and `human_corrections` fields; `milestone: "diseño DB v1"`.

## Scenario 3 — Amend a previous entry (FR-006b)

> "Logbook, haz una enmienda en `tests-login` sobre la entrada 1: el refresh loop solo afecta Safari; Chrome y Firefox están bien."

**Expected**: a new entry with `type: "amendment"`, `amends: {id:1, ulid:"..."}`, and the clarifying body. Entry #1 in the file is unchanged (`diff` shows only appended lines).

## Scenario 4 — Query the logbook (User Story 3, P3)

> "Logbook, muéstrame qué salió mal en `tests-login` en los últimos 7 días."

The subagent delegates to `logbook-query`, which runs `query.py --logbook tests-login --since <date>` to fetch matching entries, then summarizes them grounded in that JSON. **Expected**: only facts present in the file, cited by `id`. If nothing matches, the subagent says so explicitly (no fabrication).

You can also call the skill directly (bypasses the subagent):

```
/logbook-query tests-login --since 2026-04-11
```

## Scenario 5 — List all logbooks

```
/logbook-list
```

Returns slug and entry count for every logbook in the project. Any agent in the session can call this skill to enrich its own context without going through the logbook subagent.

## Scenario 6 — Render a logbook to Markdown

```
/logbook-format tests-login
```

Overwrites `logbook/tests-login/rendered.md`. Safe to run any time — idempotent, no data changes.

## Scenario 7 — False activation check (SC-002)

In a fresh Claude Code session, issue:

> "Can you log this error for me and help me track what I did today?"

**Expected**: the `logbook` subagent is **not** invoked. The main agent handles the request directly (likely by writing to console/terminal or creating a scratchpad note).

## Cleanup

Nothing to clean up — logbooks are plain files; delete `logbook/<slug>/` to remove.
