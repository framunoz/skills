# Implementation Plan: Logbook Subagent (Subagente de Bitácora)

**Branch**: `001-bitacora-subagent` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-bitacora-subagent/spec.md`

## Summary

Deliver a Claude Code subagent named `logbook` that helps the user capture structured logbook entries (test outcomes, AI-vs-human co-creation notes, free-form notes) across multiple per-project logbooks. A project can host many logbooks under `logbook/<slug>/`; each logbook declares a default `schema_type` hint (`tests`, `collaboration`, or `free`) at creation — logbooks are neutral containers and entries of any type can coexist (mixed schema). Entries are stored append-only in a machine-readable JSON Lines file and rendered to Markdown by a separate formatting command. The subagent is invoked explicitly by the user (or by another agent acting on the user's explicit instruction); its description is crafted to avoid router false positives.

Technical approach: ship the whole toolkit as a **Claude Code plugin** (`claude/plugins/logbook/`) that bundles the thin subagent (composer + orchestrator) and five co-located skills (`logbook-push`, `logbook-format`, `logbook-init`, `logbook-list`, `logbook-query`). Schema definitions (entry schemas, validation rules) live in `logbook-push/references/schemas.md` and are referenced from `logbook-push/SKILL.md` — the subagent gets schema context by loading `logbook-push` at startup via the `skills:` frontmatter field. A dedicated `logbook-schema` skill is not needed: it would be purely a context-injection artifact (`user-invocable: false`, no scripts, no model), and co-locating the schema reference inside `logbook-push` achieves the same result with less indirection. The repository root doubles as a **plugin marketplace** (`.claude-plugin/marketplace.json`) so this plugin — and future ones — can be installed with a single `/plugin install logbook@my-skills`. Users can also invoke the read-only skills directly as `/logbook-list`, `/logbook-query`, etc. The subagent never edits `entries.jsonl` textually — it always goes through `logbook-push`. Tool code lives under `claude/plugins/logbook/`; **data** (`logbook/<slug>/`) lives in each consumer project.

## Technical Context

**Language/Version**: Subagent + skills defined in Markdown/YAML frontmatter (per official Claude Code docs). Helper scripts in Python 3 stdlib only, shebang `#!/usr/bin/env python3`. **No `uv`, no `.venv`, no package manager dependency** (Constitution "scripts self-contained").
**Primary Dependencies**: Python stdlib only (`json`, `uuid`, `datetime`, `argparse`, `pathlib`, `re`, `sys`). No third-party packages.
**Storage**: JSON Lines file per logbook at `<project>/logbook/<slug>/entries.jsonl` (one JSON object per line = append-only, minimal diff, easy to recover). A `<project>/logbook/<slug>/meta.json` holds logbook name, schema type, created-at.
**Testing**: `pytest` for the helper scripts (schema validation, push idempotency, amendment flow). Trigger behavior (FR-002, no false activation) validated manually against the Test Questions section required by Constitution Principle V — no external eval skill required.
**Target Platform**: Claude Code on macOS/Linux. Subagent invoked via Claude Code's subagent mechanism; scripts run in the user's project working directory.
**Project Type**: Tool for this repository (a subagent + its helper scripts), installable into downstream projects.
**Performance Goals**: Push operation completes in <1 s for logbooks up to 10k entries (append-only, no full rewrite). Format operation renders 1k entries in <2 s.
**Constraints**: Offline-capable (FR-010, no network). Scripts must be self-contained (Constitution Additional Constraints). No personal paths or credentials baked in.
**Scale/Scope**: A single user per project; dozens of logbooks per project at most; entries per logbook typically <1k.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Provenance & Traceability | PASS (planned) | `AGENT.md` frontmatter carries `author`, `original-author`, `source` (commit permalink — to be updated post-merge per T037), `version`, `last-updated`, `status: active`. |
| II. SemVer + CHANGELOG | PASS (planned) | Initial release at `0.1.0`; `CHANGELOG.md` at each skill root and plugin root, updated on every bump. |
| III. Shareability & Portability | PASS | Ships as a single Claude Code plugin (`claude/plugins/logbook/` + `.claude-plugin/marketplace.json`). One command installs subagent and all five skills atomically. Self-contained; Python stdlib only; no personal paths. |
| IV. License & Attribution | PASS | Wholly original work; inherits repository `LICENSE` via explicit reference in frontmatter (`license: inherits repository LICENSE`). |
| V. Trigger Testability | PASS (planned) | Description explicitly states: "Invoke ONLY when the user asks for the logbook subagent by name." Trigger phrases and negative examples listed. Test Questions section included in `logbook.md` (Constitution Principle V). Evaluated manually via `contracts/triggering.md` test set. |
| Additional — English-only authoring | PASS (planned) | All tool content in English. User data (logbook entries) preserves the user's input language (Spanish). Spec Kit artifacts remain in Spanish by user preference — they are design documents, not tool content. |
| Additional — Naming | PASS | `logbook` matches `^[a-z0-9]+(-[a-z0-9]+)*$` and equals its directory name. |
| Additional — Scripts self-contained | PASS (planned) | Python stdlib only; `#!/usr/bin/env python3` shebang; no package manager dependency at runtime. |
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
│   ├── push-skill.md            # logbook-push SKILL.md + script contract (includes schema reference)
│   ├── format-skill.md          # logbook-format SKILL.md + script contract
│   ├── init-list-skills.md      # logbook-init + logbook-list contracts
│   ├── query-skill.md           # logbook-query SKILL.md + script contract
│   └── triggering.md            # trigger test cases — manual review against subagent description
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
.claude-plugin/
└── marketplace.json              # repo-root marketplace catalog

claude/
├── hooks/                        # existing hooks (unchanged)
├── skills/                       # existing skills (unchanged)
└── plugins/
    └── logbook/
        ├── .claude-plugin/
        │   └── plugin.json           # name, version, description, author, license, repository
        ├── CHANGELOG.md              # plugin-level changelog
        ├── README.md                 # install + usage
        ├── LICENSE                   # reference to repo LICENSE
        ├── agents/
        │   └── logbook.md            # subagent: model: sonnet, color: cyan, memory: project, background: true
        └── skills/
            ├── logbook-push/         # SKILL.md (haiku, low, disable-model-invocation) + scripts/push.py + references/schemas.md + CHANGELOG.md
            ├── logbook-format/       # SKILL.md (haiku, low) + scripts/format.py + CHANGELOG.md
            ├── logbook-init/         # SKILL.md (haiku, low) + scripts/init.py + CHANGELOG.md
            ├── logbook-list/         # SKILL.md (haiku, low) + scripts/list.py + CHANGELOG.md
            └── logbook-query/        # SKILL.md (sonnet, medium) + scripts/query.py + CHANGELOG.md

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

**Structure Decision**: The plugin lives under `claude/plugins/logbook/`, consistent with the repository convention that all Claude tooling resides in `claude/` (`hooks/`, `skills/`, `plugins/`). Schema definitions live in `logbook-push/references/schemas.md`, referenced from `logbook-push/SKILL.md`. A separate `logbook-schema` skill is explicitly **not shipped**: it would be a non-invocable, scriptless reference-doc skill whose only role is context injection — and the subagent already gets that context by loading `logbook-push` at startup. Removing it simplifies the skills list, reduces maintenance overhead, and co-locates schema knowledge with the operation that uses it. The repository root hosts a plugin marketplace (`.claude-plugin/marketplace.json`) so this plugin — and future ones in `claude/plugins/` — install via a single `/plugin install logbook@my-skills`. Tests live at repo root under `tests/logbook/`. The *data* (`logbook/<slug>/`) lives in each *consumer* project — the plugin only ships code and instructions.

Script resolution at runtime uses `${CLAUDE_SKILL_DIR}` (the skill's own directory, resolved by Claude Code) to locate `scripts/*.py` within each skill. The data path uses `$CLAUDE_PROJECT_DIR` (consumer project root).

## Complexity Tracking

No unjustified deviations. Packaging as a plugin + marketplace resolves the previous Principle III carve-out (subagent + skills now install together as one unit). Schema co-located in `logbook-push` is simpler than a dedicated `logbook-schema` skill.
