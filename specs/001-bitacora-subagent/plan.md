# Implementation Plan: Logbook Subagent (Subagente de Bitácora)

**Branch**: `001-bitacora-subagent` | **Date**: 2026-04-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-bitacora-subagent/spec.md`

## Summary

Deliver a Claude Code subagent named `logbook` that helps the user capture structured logbook entries (test outcomes, AI-vs-human co-creation notes, free-form notes) across multiple per-project logbooks. A project can host many logbooks under `logbook/<slug>/`; each logbook declares a fixed schema (`tests`, `collaboration`, or `free`) at creation. Entries are stored append-only in a machine-readable JSON Lines file and rendered to Markdown by a separate formatting command. The subagent is invoked explicitly by the user (or by another agent acting on the user's explicit instruction); its description is crafted to avoid router false positives.

Technical approach: ship the whole toolkit as a **Claude Code plugin** (`plugins/logbook/`) that bundles the thin subagent (composer + orchestrator) and six co-located skills (`logbook-push`, `logbook-format`, `logbook-init`, `logbook-list`, `logbook-query`, `logbook-schema`). The repository root doubles as a **plugin marketplace** (`.claude-plugin/marketplace.json`) so this plugin — and future ones — can be installed with a single `/plugin install logbook@my-skills`. The subagent loads the skills via the `skills:` frontmatter field so their content is in its context at startup; users can also invoke them directly as `/logbook-push`, `/logbook-format`, etc. The subagent never edits `entries.jsonl` textually — it always goes through the skills/scripts. Tool code lives under `plugins/logbook/`; **data** (`logbook/<slug>/`) lives in each consumer project.

## Technical Context

**Language/Version**: Subagent + skills defined in Markdown/YAML frontmatter (per official Claude Code docs). Helper scripts in Python 3 stdlib only, shebang `#!/usr/bin/env python3`. **No `uv`, no `.venv`, no package manager dependency** (Constitution "scripts self-contained").
**Primary Dependencies**: Python stdlib only (`json`, `uuid`, `datetime`, `argparse`, `pathlib`, `re`, `sys`). No third-party packages.
**Storage**: JSON Lines file per logbook at `<project>/logbook/<slug>/entries.jsonl` (one JSON object per line = append-only, minimal diff, easy to recover). A `<project>/logbook/<slug>/meta.json` holds logbook name, schema type, created-at.
**Testing**: `pytest` for the helper scripts (schema validation, push idempotency, amendment flow). Trigger behavior (FR-002, no false activation) validated via the `grill-me` eval skill against the subagent's description — see Phase 1 contracts.
**Target Platform**: Claude Code on macOS/Linux. Subagent invoked via Claude Code's subagent mechanism; scripts run in the user's project working directory.
**Project Type**: Tool for this repository (a subagent + its helper scripts), installable into downstream projects.
**Performance Goals**: Push operation completes in <1 s for logbooks up to 10k entries (append-only, no full rewrite). Format operation renders 1k entries in <2 s.
**Constraints**: Offline-capable (FR-010, no network). Scripts must be self-contained (Constitution Additional Constraints). No personal paths or credentials baked in.
**Scale/Scope**: A single user per project; dozens of logbooks per project at most; entries per logbook typically <1k.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Provenance & Traceability | PASS (planned) | `AGENT.md` frontmatter will carry `author`, `original-author`, `source` (commit permalink), `version: 0.1.0`, `last-updated`, `status: active`. |
| II. SemVer + CHANGELOG | PASS (planned) | Initial release at `0.1.0`; `claude/subagents/logbook/CHANGELOG.md` created alongside. |
| III. Installability | PASS | The entire tool ships as a single Claude Code plugin (`plugins/logbook/` + root-level `.claude-plugin/marketplace.json`). One command — `/plugin marketplace add <repo>` then `/plugin install logbook@my-skills` — installs subagent and all six skills atomically. No manual `cp -R` step; subagent and skills version together via `plugin.json`. |
| IV. Agent Docs Sync | PASS (planned) | Will add a short entry to root `AGENTS.md` under `## Subagents` noting the `logbook` subagent exists and linking to its directory. Repo-root `CLAUDE.md` gets a single reference line if subagents are listed there. Subagent-local `AGENT.md` holds tool-specific triggers/constraints. |
| V. License & Attribution | PASS | Wholly original work; inherits repository `LICENSE` via explicit reference in `AGENT.md` frontmatter (`license: inherits repository LICENSE`). |
| VI. Trigger Testability | PASS (planned) | Description explicitly states: "Invoke **only** when the user asks for the logbook subagent by name (e.g., 'logbook', 'bitácora'). Do not proactively delegate." Trigger phrases listed; negative examples listed to prevent false activation. Grill-me eval documented in `contracts/triggering.md`. |
| Additional — English-only authoring | PASS (planned) | All tool content (frontmatter, `AGENT.md` body, script identifiers/comments, CHANGELOG, helper docs) will be in English. **User data** (logbook entries themselves) is out of scope for this rule — the user may write entries in Spanish; the subagent preserves the input language. The Spec Kit artifacts (`spec.md` written in Spanish) are project design documents, not tool content; they remain in Spanish by user preference. |
| Additional — Naming | PASS | `logbook` matches `^[a-z0-9]+(-[a-z0-9]+)*$` and equals its directory name. |
| Additional — Scripts self-contained | PASS (planned) | Scripts use Python stdlib only and declare `#!/usr/bin/env python3` (no `uv` shebang dependency); an optional `uv run` wrapper is documented but not required. |
| Additional — Secrets | PASS | No credentials or personal paths. |

**No unjustified violations. Gate PASSED.**

## Project Structure

### Documentation (this feature)

```text
specs/001-bitacora-subagent/
├── plan.md              # This file
├── research.md          # Phase 0: resolved unknowns
├── data-model.md        # Phase 1: entry + logbook schemas
├── quickstart.md        # Phase 1: how the user installs and invokes the subagent
├── contracts/
│   ├── plugin-manifest.md       # plugin.json + root marketplace.json shape
│   ├── subagent-frontmatter.md  # AGENT.md frontmatter contract
│   ├── push-skill.md            # logbook-push SKILL.md + script contract
│   ├── format-skill.md          # logbook-format SKILL.md + script contract
│   ├── init-list-skills.md      # logbook-init + logbook-list contracts
│   ├── query-skill.md           # logbook-query SKILL.md + script contract
│   └── triggering.md            # trigger-test eval cases
└── checklists/
    └── requirements.md  # already present
```

### Source Code (repository root)

```text
.claude-plugin/
└── marketplace.json              # repo-root marketplace catalog (lists logbook + any future plugins)

plugins/
└── logbook/
    ├── .claude-plugin/
    │   └── plugin.json           # name, version, description, author, license, repository
    ├── CHANGELOG.md              # plugin-level changelog (tracks the bundle as a whole)
    ├── README.md                 # install + usage
    ├── LICENSE                   # reference to repo LICENSE
    ├── agents/
    │   └── logbook.md            # subagent: model: sonnet, color: cyan, memory: project, background: true
    └── skills/
        ├── logbook-push/         # SKILL.md (haiku, low, disable-model-invocation) + scripts/push.py + _schemas.py + CHANGELOG.md
        ├── logbook-format/       # SKILL.md (haiku, low) + scripts/format.py + CHANGELOG.md
        ├── logbook-init/         # SKILL.md (haiku, low) + scripts/init.py + CHANGELOG.md
        ├── logbook-list/         # SKILL.md (haiku, low) + scripts/list.py + CHANGELOG.md
        ├── logbook-query/        # SKILL.md (sonnet, medium) + scripts/query.py + CHANGELOG.md
        └── logbook-schema/       # SKILL.md (no model, user-invocable: false) + references/schemas.md

tests/
└── logbook/
    ├── test_push.py
    ├── test_format.py
    ├── test_init.py
    ├── test_list.py
    ├── test_query.py
    ├── test_amendment.py
    └── fixtures/
```

**Structure Decision**: The plugin bundles subagent + six skills in one installable unit. The repository root hosts a plugin marketplace (`.claude-plugin/marketplace.json`) so this plugin — and future ones in `plugins/` — install via a single `/plugin install logbook@my-skills`. The subagent lives at `plugins/logbook/agents/logbook.md`; skills at `plugins/logbook/skills/<name>/`. Tests live at repo root under `tests/logbook/`. The *data* (`logbook/<slug>/`) lives in each *consumer* project — the plugin only ships code and instructions.

Script resolution at runtime uses `$CLAUDE_PLUGIN_ROOT` (provided by Claude Code when a plugin is active) to locate `plugins/logbook/skills/<name>/scripts/*.py`. The data path uses `$CLAUDE_PROJECT_DIR` (consumer project root).

## Complexity Tracking

No unjustified deviations. Packaging as a plugin + marketplace resolves the previous Principle III carve-out (subagent + skills now install together as one unit).
