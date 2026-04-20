# Phase 0 Research — Logbook Subagent

All NEEDS CLARIFICATION from Technical Context have been resolved. This document records the investigations behind each decision.

## R1. Subagent definition format for Claude Code

- **Decision**: Use `AGENT.md` under `claude/subagents/logbook/` with YAML frontmatter (`description`, `compatibility`, `metadata`) plus a Markdown system-prompt body, per the repo's root `AGENTS.md` §Subagents.
- **Rationale**: Matches the repo's documented standard (AGENTS.md lines ~160–215). Consistent with existing skills under `claude/skills/`. Single source of truth per tool.
- **Alternatives considered**:
  - Flat `agent-name.md` at repo root: rejected — constitution requires a per-tool directory to host CHANGELOG, scripts, and license reference.
  - JSON manifest: rejected — repo convention is Markdown + YAML frontmatter.

## R2. Avoiding router false activation (FR-002, SC-002)

- **Decision**: The `description` frontmatter field will (a) open with an explicit negative constraint ("Do NOT invoke unless the user asks for the logbook subagent by name"), (b) list concrete trigger phrases, and (c) avoid verbs commonly used by other tasks ("help", "track", "log", "record" standalone). Positive triggers will be anchored on the tool's name: "logbook", "bitácora", "bitacora".
- **Rationale**: Progressive disclosure loads only the description at startup (Constitution VI). A negative lead + proper-noun anchors reduces semantic collision with general "logging/tracking" tasks that the main agent or other subagents might accidentally match.
- **Alternatives considered**:
  - Rely on orchestrator policy: rejected — no enforceable cross-client policy exists.
  - Password/passphrase gating in the description: rejected — brittle and bad UX.
- **Validation**: A curated set of 20 prompts (10 positive, 10 negative) in `contracts/triggering.md` is run against the description using the `grill-me` skill. Success = 0 false positives, ≥9/10 true positives.

## R3. Storage format: JSONL vs single JSON

- **Decision**: JSON Lines (`entries.jsonl`), one entry per line, append-only.
- **Rationale**:
  - Append without parsing the whole file → O(1) push; aligns with SC-003 (prior entries untouched).
  - Minimal git diffs: each push adds exactly one line.
  - Easy partial recovery if a line is corrupted; the rest remains readable.
  - Stream-friendly for the formatter on large logbooks.
- **Alternatives considered**:
  - Single JSON array: rejected — requires rewriting the whole file on every push.
  - SQLite: rejected — not human-editable in a pinch; heavier.
  - Markdown-only: rejected by the user's clarification (Q2) in favor of structured data + separate formatting.

## R4. Per-logbook metadata file

- **Decision**: `logbook/<slug>/meta.json` holds `{ slug, schema_type, created_at, title?, description? }`. Created by `init.py`; read (not written) by `push.py` to know which schema to validate against.
- **Rationale**: Keeps the schema declaration out of every entry line (DRY) and makes `list.py` cheap.
- **Alternatives considered**: Put schema on every entry — rejected (redundant, risks drift).

## R5. Entry identifier strategy

- **Decision**: Per-entry `id` = monotonically increasing integer (1, 2, 3, …) scoped to the logbook, plus `ulid` as a secondary stable id for cross-references (amendments).
- **Rationale**: Integer is friendly to humans ("amend entry 7"); ULID is collision-resistant and time-sortable for future merging across branches without coordination.
- **Alternatives considered**: Plain UUIDv4 (rejected — not time-sortable), timestamp-only (rejected — collisions within the same second possible).

## R6. Amendment semantics

- **Decision**: An amendment is a regular entry with `type: "amendment"` and `amends: { id: <int>, ulid: <ulid> }`. It carries its own body (the corrected content or explanation). The formatter renders amendments chronologically but also injects a visual backlink under the original entry's header.
- **Rationale**: Preserves immutability (FR-006) while giving the reader clear trace of the correction chain.

## R7. Schema validation approach

- **Decision**: Lightweight validation in `_schemas.py` (no `jsonschema` dependency): hand-written predicate functions per schema type. Each returns `(ok: bool, errors: list[str])`.
- **Rationale**: Stdlib-only constraint (Constitution Additional Constraints → scripts self-contained without assuming a package manager). Three schemas, small — no need for a JSON Schema library.

## R8. Sensitive-content detection (FR-008)

- **Decision**: Heuristic regex scan inside `push.py` before writing: look for common patterns (`AKIA[0-9A-Z]{16}`, `-----BEGIN .* PRIVATE KEY-----`, bearer tokens `[A-Za-z0-9_-]{40,}` adjacent to words like `token`, `key`, `secret`, email addresses). If matched, the script exits non-zero with a clear message; the subagent surfaces the warning to the user and re-invokes `push` with an `--acknowledge-sensitive` flag if the user confirms.
- **Rationale**: Cheap, local, no network, and reversible (user confirmation path preserves UX).
- **Alternatives considered**: Full DLP tooling — rejected (overkill, offline constraint).

## R9. Installation path into a consumer project

- **Decision**: Ship the whole toolkit as a Claude Code **plugin** (`plugins/logbook/`) registered in a repo-root **marketplace** (`.claude-plugin/marketplace.json`). Consumers run `/plugin marketplace add <repo-url-or-path>` once, then `/plugin install logbook@my-skills`. Subagent + six skills install atomically.
- **Rationale**: Fixes the earlier Principle III gap (subagent was not installable via `skills.sh`). Plugins version the whole bundle together via `plugin.json`, namespace the skills automatically, and give the user one command instead of `npx skills add` × 6 plus a manual `cp -R` for the agent.
- **Alternatives considered**:
  - Six loose skills + manual subagent copy (previous plan): rejected — scattered, and left Principle III partially unmet for the subagent.
  - Single repo-as-plugin (no `plugins/` subdir): rejected — blocks hosting additional unrelated plugins in the same `my-skills` repo in the future.

## R10. Skills-vs-commands architecture

- **Decision**: Package every deterministic operation (push/format/init/list/query) as its own Skill under `claude/skills/logbook-<op>/`, and make the subagent a thin orchestrator that loads those skills via its frontmatter `skills:` array. Do NOT use the legacy `.claude/commands/` format.
- **Rationale**: Per the official Claude Code docs, `.claude/commands/` is legacy; the recommended format is `.claude/skills/<name>/SKILL.md`, which supports the same `/<name>` slash-command invocation PLUS autonomous invocation by Claude. Going skills-first also:
  - Lets each skill bundle its own script and its own operating instructions in one place (no global "where do my scripts live" problem).
  - Makes the scripts installable via `skills.sh` (Constitution III PASS for all scripted logic).
  - Lets the subagent load the skills into its context at startup via the `skills:` field, so the subagent knows how to invoke each operation without dedicated instruction blocks.
  - Enables the user to invoke any operation directly (`/logbook-push`, `/logbook-query`) without going through the subagent, which is useful for scripting and tests.
- **Alternatives considered**:
  - Legacy `.claude/commands/`: rejected per the docs' own deprecation note.
  - All-in-one subagent with inline scripts: rejected because it couples composition with persistence/rendering and kills the `skills.sh` installability angle.

## R11. Model/effort assignment per component

- **Decision**:
  - Subagent `logbook` → `model: sonnet`, `effort: low`, `color: cyan`, `memory: project`, `background: true`. Sonnet is chosen because composing free-form dictation into a validated entry (multi-field structured output in the input language) is a real cognitive task; haiku under-performs on nuanced Spanish/English rewriting.
  - `logbook-push`, `logbook-format`, `logbook-init`, `logbook-list` → `model: haiku`, `effort: low`, `disable-model-invocation: true`. They are wrappers around deterministic scripts; a small model is sufficient for "parse arguments, call Bash, report the result" and keeps cost low.
  - `logbook-query` → `model: sonnet`, `effort: medium`, `disable-model-invocation: true`. Summarizing/filtering entries and producing a grounded response (FR-007, SC-004 "zero hallucination") warrants Sonnet.
  - `logbook-schema` → no model (pure reference content), `disable-model-invocation: true`, `user-invocable: false`. It exists only to be loaded via the subagent's `skills:` list.
- **Rationale**: Match model capacity to cognitive load per operation; `disable-model-invocation` on every skill prevents the router from auto-firing them outside the subagent or explicit user request (reinforces SC-002 false-activation = 0).

## R12. Language policy clarification

- **Decision**: Tool content (AGENT.md, scripts, CHANGELOG, README) is English-only per Constitution Additional Constraints. User-authored logbook _entries_ are treated as data and preserved in whatever language the user writes them (commonly Spanish for this user). The subagent's system prompt instructs it to preserve input language verbatim when generating entries.
- **Rationale**: Keeps tool discoverable by external consumers while respecting user data fidelity.

## R13. Plugin packaging layout

- **Decision**: Use the standard Claude Code plugin layout. Plugin root at `plugins/logbook/` contains `.claude-plugin/plugin.json`, `agents/logbook.md`, and `skills/<name>/SKILL.md`. The repository root acts as a **marketplace** via `.claude-plugin/marketplace.json` listing `plugins/logbook/` (and any future plugins) under relative `source` paths. Scripts reference `${CLAUDE_PLUGIN_ROOT}` (set by Claude Code when the plugin is active) to locate their own files; data paths use `$CLAUDE_PROJECT_DIR`.
- **Rationale**: Follows the documented plugin spec exactly — only `plugin.json` sits inside `.claude-plugin/`; `agents/`, `skills/`, etc. live at the plugin root. Marketplace-at-repo-root is the recommended pattern when a repo hosts multiple plugins.
- **Alternatives considered**:
  - Plugin inside `claude/plugins/` to parallel existing `claude/skills/` and `claude/subagents/`: rejected — `claude/` is this repo's existing layout for loose skills/subagents, mixing plugin trees inside it confuses discovery. A top-level `plugins/` directory matches common convention.
  - Skip the marketplace file and require users to install by direct path: rejected — marketplace gives us a single entry point, documents available plugins in one file, and costs ~10 lines of JSON.
