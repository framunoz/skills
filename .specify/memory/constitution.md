<!--
Sync Impact Report
==================
Version change: 1.2.0 → 2.0.0
Change type: MAJOR (Principle IV removed; remaining principles renumbered)

Modified principles:
  - IV. Agent Docs Sync — AGENTS.md & CLAUDE.md → REMOVED. Rationale: doc-sync
    discipline is a maintainer concern, not a developer-facing governance rule.
    Principles V → IV (License & Upstream Attribution), VI → V (Trigger Testability).

Added sections:
  (none)

Removed sections:
  - Principle IV: Agent Docs Sync — AGENTS.md & CLAUDE.md (Locality-Aware)

Templates status:
  ✅ .specify/memory/constitution.md — updated (this file)
  ⚠ .specify/templates/plan-template.md — pending review for removed Principle IV ref
  ⚠ .specify/templates/spec-template.md — pending review for removed Principle IV ref
  ⚠ .specify/templates/tasks-template.md — pending review for removed Principle IV ref
  ⚠ README.md — pending update to reflect principle renumbering

Deferred items / TODOs:
  (none)
-->

# skills Constitution

This constitution governs how skills, subagents, hooks, and plugins are authored,
tracked, distributed, and consumed within the `skills` repository. Its goal is to
keep every tool reproducible, attributable, and easy to share across AI client
implementations (Claude Code, OpenCode, Gemini, and future compatible clients).

**Canonical repository**: https://github.com/framunoz/skills
**Primary maintainer**: `framunoz`

## Core Principles

### I. Tool Provenance & Traceability (NON-NEGOTIABLE)

Every new tool created for an agent — whether a **skill**, **subagent**, **hook**, or
**plugin** — MUST ship with provenance metadata in its definition file (`SKILL.md`,
`AGENT.md`, or hook manifest). The following keys are required under `metadata`:

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
are lost, and license obligations (Principle IV) cannot be honored. Permalinks make the
origin reproducible over time. Explicit deprecation prevents silent rot — a tool whose
author, origin, version, or lifecycle status cannot be answered in one read of its
frontmatter is non-compliant.

### II. Semantic Versioning & Changelog for Every Tool

Every skill, subagent, hook, and plugin MUST carry a `version` field following
[Semantic Versioning 2.0](https://semver.org/):

- **MAJOR**: Removes a trigger, breaks expected inputs/outputs, or changes defaults in a
  way that would surprise an existing caller.
- **MINOR**: Adds a new capability, new optional input, or broadens triggers without
  breaking existing usage.
- **PATCH**: Wording, documentation, bug fixes, or internal script refactors that do not
  affect behavior from the agent's perspective.

Every tool directory MUST also contain a `CHANGELOG.md` at its root documenting every
version bump, the bump type, and a one-line description of the change. The version
number alone tells you _what_ changed; the changelog tells you _why_, which is what
makes Principle I's traceability actually useful.

Version bumps and changelog entries MUST accompany every change to the tool's
definition or behavior. A commit that edits a tool without updating `version`,
`last-updated`, and `CHANGELOG.md` is non-compliant.

### III. Shareability & Portability

Every tool published from this repository MUST be easy to share with any consumer —
individual developer, team, or AI client — without requiring knowledge of the original
author's environment or tooling setup. To satisfy this:

- **Self-contained**: All scripts, references, and assets a tool needs at runtime MUST
  live inside the tool's directory. Copying that directory MUST be a complete install.
- **No personal or team assumptions**: Tools MUST NOT reference personal paths, private
  registries, team-internal services, or specific shell configurations. They MUST work
  on any standard machine that meets the declared dependencies.
- **Declared dependencies**: Any runtime dependency (language version, package, CLI
  tool) MUST be documented explicitly in the tool's definition file or README, so a
  new consumer can satisfy them from scratch.
- **Catalog registration**: Tools MUST be registered in the repository catalog/index so
  that discovery tooling can resolve them by name without scanning the tree.
- **Distribution channel**: Where `skills.sh` (`npx skills add <skill-name>`) is
  available, tools SHOULD support it as the primary install path. When it is not yet
  supported, the tool's README MUST document the manual install path.

Tools with `status: deprecated` MUST remain discoverable in the catalog but MUST emit a
deprecation warning referencing `replaced-by` when present. Tools with
`status: archived` MUST be excluded from active install flows by default.

**Rationale**: Tools must serve external consumers, not just the original author's
setup. A tool that only works in one person's environment is not a shareable tool —
it is a personal script. Portability is what allows this repository to function as a
public resource.

### IV. License & Upstream Attribution

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

### V. Trigger Testability

Every skill and subagent MUST have a `description` that is specific enough to be
evaluated by a test: given a natural-language user request, a reader (human or model)
should be able to answer "should this tool fire?" unambiguously.

Descriptions MUST:

- State what the tool does AND when it should be used.
- Include concrete trigger phrases or task shapes where useful.
- Avoid vague verbs ("helps with", "works on") when a concrete verb exists.

Every skill and subagent definition MUST also include a **Test Questions** section
containing at least three scenario prompts that a reviewer can use to verify:

1. A prompt that SHOULD trigger the tool (true positive).
2. A prompt that SHOULD NOT trigger the tool (true negative).
3. A prompt that tests a boundary or ambiguous case (edge case).

**Rationale**: Progressive disclosure means only the description is loaded at startup.
A vague description is a silent failure — the tool exists but never fires. Explicit
test questions make trigger behavior auditable and keep the catalog honest.

## Additional Constraints

- **Directory structure**: Every artifact — skill, subagent, hook, plugin, or any other
  tool type — MUST reside in its canonical top-level folder (`skills/`, `agents/`,
  `hooks/`, `plugins/`, etc. as defined in `AGENTS.md`). No tool may be placed outside
  its designated directory. Tools not in their canonical folder are non-compliant.
- **Layout**: Skills MUST follow the layout defined in `AGENTS.md`
  (`SKILL.md` + optional `scripts/`, `references/`, `assets/`). The same locality
  principle applies to all other tool types.
- **Naming**: Skill, subagent, hook, and plugin names MUST match the regex
  `^[a-z0-9]+(-[a-z0-9]+)*$` and MUST equal their directory name.
- **English-only authoring**: All tool content — `name`, `description`, frontmatter
  values, Markdown body, code identifiers (variables, functions, classes), comments,
  and bundled documentation — MUST be written in English. Non-English content is not
  allowed, including Spanish, even though the primary maintainer is a Spanish speaker.
  This maximizes reach for external consumers and keeps agent triggering predictable.
- **Script testability**: Any non-Markdown executable file (shell script, Python script,
  etc.) included in a tool's `scripts/` directory MUST be testable in its declared
  runtime environment. Testability requires:
  - All dependencies declared explicitly (language version, packages, CLI tools).
  - A documented way to run the script and verify it succeeds (e.g., a `--dry-run`
    flag, an example invocation in the tool README, or a test harness).
  - No silent failures: scripts MUST exit with a non-zero code on error.
- **Secrets**: No tool may hard-code credentials, API keys, or personal paths. These
  MUST be read from the environment or a configured secret store.

## Development Workflow

1. **Place** the skill/subagent/hook/plugin in its canonical top-level folder.
2. **Author** the tool with required frontmatter (Principles I, II, IV, V), including
   the Test Questions section.
3. **Register** the tool in the catalog/index (Principle III).
4. **Version bump + changelog** on every behavior change (Principle II). Commit
   messages SHOULD mention the semver bump type (MAJOR/MINOR/PATCH).
5. **Self-review** pre-merge: the author runs the compliance checklist below.
   Non-compliance blocks merge even on solo changes.

## Governance

- This constitution supersedes ad-hoc conventions. Where a tool-local doc contradicts
  this file, this file wins until the tool-local doc is brought into alignment.
- **Project identity**: The canonical repository is https://github.com/framunoz/skills.
  The primary maintainer handle is `framunoz`. References to the repository in
  tool metadata, documentation, and source permalinks MUST use this URL.
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
  responsible for verifying conformance with Principles I–V before merging their
  own PR. When an external contributor submits a change, an independent reviewer
  (someone other than the contributor, normally the repository maintainer) MUST
  perform the review; self-merged external contributions are not allowed.
- **Compliance checklist** (Principles I–V): metadata complete (author,
  original-author, source permalink, version, last-updated, status, replaced-by
  when applicable); version bumped; `CHANGELOG.md` updated; catalog/index updated;
  tool placed in canonical directory; license/attribution preserved; description is
  testable; Test Questions section present; scripts declare dependencies and are
  testable; content is English-only.
- **Runtime guidance**: For day-to-day execution details (install paths, tooling
  commands, per-client quirks) consult `AGENTS.md` at the appropriate locality.

**Version**: 2.0.0 | **Ratified**: 2026-04-18 | **Last Amended**: 2026-04-19
