<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.1.0
Change type: MINOR (new requirements added, one constraint removed, governance clarified)

Modified principles:
  - I. Tool Provenance & Traceability — `source` now requires a permalink (commit-pinned
    URL); added `status` and optional `replaced-by` metadata for deprecation tracking.
  - II. Semantic Versioning for Every Tool — added CHANGELOG.md requirement per tool.
  - III. Installability via skills.sh — added catalog/index file requirement so that
    `npx skills add` can resolve names without scanning the repository.

Added sections:
  - Additional Constraints → "English-only authoring" rule (identifiers, comments, docs).

Removed sections:
  - Additional Constraints → "Python tooling / uv run" rule (user-specific, not portable
    for external consumers).

Templates status:
  ✅ .specify/memory/constitution.md — updated (this file)
  ⚠ .specify/templates/plan-template.md — pending review for Constitution Check alignment
  ⚠ .specify/templates/spec-template.md — pending review for tool-authoring spec fields
  ⚠ .specify/templates/tasks-template.md — pending review for new task categories
    (catalog registration, CHANGELOG update, deprecation flow)
  ⚠ README.md — pending update to mention `npx skills add` + catalog index
  ⚠ AGENTS.md — pending update to list `status`, `replaced-by`, and permalink `source`
    in recommended metadata keys

Deferred items / TODOs:
  (none)
-->

# my-skills Constitution

This constitution governs how skills, subagents, and hooks are authored, tracked,
distributed, and consumed within the `my-skills` repository. Its goal is to keep every
tool reproducible, attributable, and installable across AI client implementations
(Claude Code, OpenCode, Gemini, and future compatible clients).

## Core Principles

### I. Tool Provenance & Traceability (NON-NEGOTIABLE)

Every new tool created for an agent — whether a **skill**, **subagent**, or **hook** —
MUST ship with provenance metadata in its definition file (`SKILL.md`, `AGENT.md`, or
hook manifest). The following keys are required under `metadata`:

- `author`: the current maintainer's handle or team name.
- `original-author`: the upstream creator when the tool was adapted from elsewhere;
  equals `author` for wholly original work.
- `source`: a **permalink** (commit-pinned URL) to the canonical upstream — either the
  external repository the tool was adapted from, or, for wholly original work, a
  GitHub permalink to the tool's directory inside this repository. Branch-tip URLs
  (e.g. `/tree/main/...`) are not acceptable because they drift.
- `version`: a semver string (see Principle II).
- `last-updated`: ISO date (`YYYY-MM-DD`) of the most recent meaningful change.
- `status`: one of `active`, `deprecated`, `archived`.
- `replaced-by`: REQUIRED when `status` is `deprecated` or `archived`; the name of the
  successor tool, or `null` if none exists.

**Rationale**: Without provenance, adapted skills become orphaned forks, upstream fixes
are lost, and license obligations (Principle V) cannot be honored. Permalinks make the
origin reproducible over time. Explicit deprecation prevents silent rot — a tool whose
author, origin, version, or lifecycle status cannot be answered in one read of its
frontmatter is non-compliant.

### II. Semantic Versioning & Changelog for Every Tool

Every skill, subagent, and hook MUST carry a `version` field following
[Semantic Versioning 2.0](https://semver.org/):

- **MAJOR**: Removes a trigger, breaks expected inputs/outputs, or changes defaults in a
  way that would surprise an existing caller.
- **MINOR**: Adds a new capability, new optional input, or broadens triggers without
  breaking existing usage.
- **PATCH**: Wording, documentation, bug fixes, or internal script refactors that do not
  affect behavior from the agent's perspective.

Every tool directory MUST also contain a `CHANGELOG.md` at its root documenting every
version bump, the bump type, and a one-line description of the change. The version
number alone tells you *what* changed; the changelog tells you *why*, which is what
makes Principle I's traceability actually useful.

Version bumps and changelog entries MUST accompany every change to the tool's
definition or behavior. A commit that edits a tool without updating `version`,
`last-updated`, and `CHANGELOG.md` is non-compliant.

### III. Installability via skills.sh (`npx skills add <skill-name>`)

Every skill published from this repository MUST be installable via:

```
npx skills add <skill-name>
```

backed by `skills.sh`. To satisfy this, the repository and each skill MUST:

- **Repository**: Maintain a **catalog/index file** (e.g. `skills/index.json`) that
  enumerates every installable skill with at least `name`, `path`, `version`, and
  `status`. `npx skills add` MUST resolve names through this index rather than
  scanning the tree, so renames and moves stay consistent.
- **Per skill**: Live at a path discoverable through the index, with `SKILL.md` at the
  directory root, and a `name` frontmatter value that equals the directory name (per
  the AGENTS.md specification).
- **Self-contained**: All scripts, references, and assets the skill needs at runtime
  MUST live inside the skill's directory, so that copying that directory is a complete
  install.

Skills with `status: deprecated` MUST remain resolvable by the installer but emit a
deprecation warning referencing `replaced-by` when present. Skills with
`status: archived` MUST be rejected by the installer by default.

Subagents and hooks SHOULD follow the same principle where the installer supports them;
when it does not yet, the tool's README MUST document the manual install path.

### IV. Agent Docs Sync — AGENTS.md & CLAUDE.md (Locality-Aware)

`AGENTS.md` and `CLAUDE.md` MUST remain authoritative, and updates MUST be
**locality-aware**:

- **Repository-root `AGENTS.md` / `CLAUDE.md`**: Describe cross-cutting conventions
  — the skill/subagent/hook spec, metadata requirements, install command, and any
  rule that applies to every tool in this repo. `AGENTS.md` is the canonical
  cross-client document and covers OpenCode, Gemini, and other compatible clients;
  client-specific files (e.g. `OPENCODE.md`, `GEMINI.md`) are NOT required unless a
  client genuinely diverges from `AGENTS.md`.
- **Skill-local or subagent-local docs** (inside `skills/<name>/` or the agent's
  directory): Describe only that tool's specifics — triggers, inputs, outputs,
  constraints. MUST NOT duplicate repo-wide rules; MAY reference them.
- **Global user-level `~/.claude/CLAUDE.md`** or equivalents: Out of scope for this
  repo and MUST NOT be modified by repository automation.

Any PR that adds, renames, removes, or changes the contract of a skill/subagent/hook
MUST update the relevant `AGENTS.md` / `CLAUDE.md` at the correct locality in the same
change.

**Rationale**: Agents read these files to decide what to do. Drift between code and
docs produces wrong delegation decisions. Locality prevents the root docs from
becoming a dumping ground and prevents skill-local docs from contradicting repo rules.

### V. License & Upstream Attribution

When a tool is adapted from an external source:

- The upstream `LICENSE` (or a reference to it) MUST be preserved inside the tool's
  directory.
- The `original-author` and `source` (permalink) metadata fields MUST point to the
  upstream.
- License-required notices MUST be retained verbatim where the upstream license
  requires it.

Wholly original tools MUST declare a `license` field (in `SKILL.md` frontmatter or
equivalent) or inherit the repository `LICENSE` by explicit reference.

**Rationale**: This repository consumes and redistributes third-party work. Attribution
and license retention are legal obligations, and they also make Principle I auditable.

### VI. Trigger Testability

Every skill and subagent MUST have a `description` that is specific enough to be
evaluated by a test: given a natural-language user request, a reader (human or model)
should be able to answer "should this tool fire?" unambiguously.

Descriptions MUST:

- State what the tool does AND when it should be used.
- Include concrete trigger phrases or task shapes where useful.
- Avoid vague verbs ("helps with", "works on") when a concrete verb exists.

**Rationale**: Progressive disclosure means only the description is loaded at startup.
A vague description is a silent failure — the tool exists but never fires. Testability
keeps the catalog honest.

## Additional Constraints

- **Directory structure**: Skills MUST follow the layout defined in `AGENTS.md`
  (`SKILL.md` + optional `scripts/`, `references/`, `assets/`).
- **Naming**: Skill and subagent names MUST match the regex
  `^[a-z0-9]+(-[a-z0-9]+)*$` and MUST equal their directory name.
- **English-only authoring**: All tool content — `name`, `description`, frontmatter
  values, Markdown body, code identifiers (variables, functions, classes), comments,
  and bundled documentation — MUST be written in English. Non-English content is not
  allowed, including Spanish, even though the primary maintainer is a Spanish speaker.
  This maximizes reach for external consumers and keeps agent triggering predictable.
- **Scripts**: Any executable under a tool's `scripts/` directory MUST either be
  self-contained or declare its dependencies explicitly in the tool's docs. Scripts
  MUST NOT assume a specific package manager, runtime wrapper, or personal shell
  configuration on the consumer's machine.
- **Secrets**: No tool may hard-code credentials, API keys, or personal paths. These
  MUST be read from the environment or a configured secret store.

## Development Workflow

1. **Author** the skill/subagent/hook under the canonical directory with required
   frontmatter (Principles I, II, V, VI).
2. **Register** the tool in the catalog/index so `npx skills add <skill-name>` can
   install it (Principle III).
3. **Sync docs** at the correct locality (Principle IV).
4. **Version bump + changelog** on every behavior change (Principle II). Commit
   messages SHOULD mention the semver bump type (MAJOR/MINOR/PATCH).
5. **Self-review** pre-merge: the author runs the compliance checklist below.
   Non-compliance blocks merge even on solo changes.

## Governance

- This constitution supersedes ad-hoc conventions. Where a tool-local doc contradicts
  this file, this file wins until the tool-local doc is brought into alignment.
- **Amendments**: Any change to this constitution requires (a) a PR editing
  `.specify/memory/constitution.md`, (b) a Sync Impact Report (as an HTML comment at
  the top of this file) enumerating version change, modified principles, and template
  follow-ups, and (c) a version bump per the rules below.
- **Versioning policy for the constitution**:
  - **MAJOR**: Removing or redefining a principle in a backward-incompatible way.
  - **MINOR**: Adding a principle or materially expanding governance.
  - **PATCH**: Clarifications, typos, or non-semantic edits.
- **Compliance review**: This is primarily a solo project, so the default model is
  **self-review against the compliance checklist** — the author of a change is
  responsible for verifying conformance with Principles I–VI before merging their
  own PR. When an external contributor submits a change, an independent reviewer
  (someone other than the contributor, normally the repository maintainer) MUST
  perform the review; self-merged external contributions are not allowed.
- **Compliance checklist** (Principles I–VI): metadata complete (author,
  original-author, source permalink, version, last-updated, status, replaced-by
  when applicable); version bumped; `CHANGELOG.md` updated; catalog/index updated;
  relevant `AGENTS.md`/`CLAUDE.md` synced; license/attribution preserved;
  description is testable; content is English-only.
- **Runtime guidance**: For day-to-day execution details (install paths, tooling
  commands, per-client quirks) consult `AGENTS.md` at the appropriate locality.

**Version**: 1.1.0 | **Ratified**: 2026-04-18 | **Last Amended**: 2026-04-18