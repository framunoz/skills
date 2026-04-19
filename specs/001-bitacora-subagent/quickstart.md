# Quickstart — Logbook Subagent

End-to-end walkthrough for installing and using the logbook tooling in a consumer project. Validates User Stories 1–3 from `spec.md`.

## Prerequisites

- Claude Code installed and configured.
- Python 3 available on `$PATH` (`python3`, stdlib only — no venv required).
- A project where you want to keep a logbook.

## Install

The logbook toolkit ships as a single Claude Code plugin. Install it from the `my-skills` marketplace:

```
/plugin marketplace add <path-or-url-to-my-skills-repo>
/plugin install logbook@my-skills
```

`<path-or-url-to-my-skills-repo>` can be a local clone (e.g. `~/Codes/my-skills`) or a GitHub URL. The marketplace manifest lives at `.claude-plugin/marketplace.json` in the repo root; the plugin itself lives at `plugins/logbook/`.

Installing the plugin registers the subagent (`logbook`) and all six skills (`logbook-push`, `logbook-format`, `logbook-init`, `logbook-list`, `logbook-query`, `logbook-schema`) in one atomic step.

Verify Claude Code sees everything:

```
/plugin list   # should list 'logbook' as installed
/agents        # should list 'logbook'
/              # should offer /logbook-push, /logbook-format, /logbook-init, /logbook-list, /logbook-query
```

## Scenario 1 — Record a test outcome (User Story 1, P1)

1. Initialize a tests-type logbook (via the skill):

   ```
   /logbook-init tests-login tests --title "Login flow tests"
   ```

   Or directly via script (the plugin root is exposed as `$CLAUDE_PLUGIN_ROOT` when active):

   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/skills/logbook-init/scripts/init.py" \
     --logbook tests-login --type tests --title "Login flow tests"
   ```

2. In Claude Code, invoke the subagent by name:

   > "Usa el subagente **logbook** para registrar en `tests-login`: salió bien el OAuth redirect, salió mal el refresh en Safari. Próximo paso: reproducir en staging."

3. The subagent:
   - Composes a payload matching the `tests` schema.
   - Pipes the JSON to `logbook-push` via stdin: `echo '{...}' | python3 .../push.py --logbook tests-login --type tests`.
   - Reports back the new entry id.

4. Inspect:

   ```bash
   cat logbook/tests-login/entries.jsonl
   # or render via the skill
   ```
   ```
   /logbook-format tests-login
   ```
   ```bash
   cat logbook/tests-login/rendered.md
   ```

**Expected**: `entries.jsonl` has exactly one new line; `rendered.md` shows the entry with "Went well" and "Went wrong" sections.

## Scenario 2 — Record AI/human collaboration (User Story 2, P2)

```
/logbook-init collab-v1 collaboration
```

Then:

> "Logbook, en `collab-v1` registra: la IA propuso el esquema inicial de la tabla `users`, yo decidí mantener solo 3 campos y le corregí el nombre de la clave primaria. Hito: diseño DB v1."

**Expected**: the resulting entry has distinct `ai_contribution`, `human_contribution`, and `human_corrections` fields; `milestone: "diseño DB v1"`.

## Scenario 3 — Amend a previous entry (FR-006b)

> "Logbook, haz una enmienda en `tests-login` sobre la entrada 1: el refresh loop solo afecta Safari; Chrome y Firefox están bien."

**Expected**: a new entry with `type: "amendment"`, `amends: {id:1, ulid:"..."}`, and the clarifying body. Entry #1 in the file is unchanged (`diff` shows only appended lines).

## Scenario 4 — Query the logbook (User Story 3, P3)

> "Logbook, muéstrame qué salió mal en `tests-login` en los últimos 7 días."

The subagent delegates to `logbook-query`, which runs `query.py --logbook tests-login --since <date>` to fetch matching entries, then summarizes them grounded in that JSON. **Expected**: only facts present in the file, cited by `id`. If nothing matches, the subagent says so explicitly (no fabrication).

You can also call the skill directly:

```
/logbook-query tests-login --since 2026-04-11
```

## Scenario 5 — False activation check (SC-002)

In a fresh Claude Code session, issue:

> "Can you log this error for me and help me track what I did today?"

**Expected**: the `logbook` subagent is **not** invoked. The main agent handles the request directly (likely by writing to console/terminal or creating a scratchpad note).

## Cleanup

Nothing to clean up — logbooks are plain files; delete `logbook/<slug>/` to remove.
