<!--
Sync Impact Report
==================
Version change: (none) → 1.0.0
Change type: MAJOR (initial ratification)

Modified principles:
  (none — first ratified version)

Added sections:
  - Core Principles
    - I. Tool Provenance & Traceability (NON-NEGOTIABLE)
    - II. Semantic Versioning for Every Tool
    - III. Installability via skills.sh (`npx skills add`)
    - IV. Agent Docs Sync — AGENTS.md & CLAUDE.md (Locality-Aware)
    - V. License & Upstream Attribution
    - VI. Trigger Testability
  - Additional Constraints
  - Development Workflow
  - Governance

Removed sections:
  (none)

Templates status:
  ✅ .specify/templates/constitution-template.md — template preserved (not edited; this is the instantiated output)
  ⚠ .specify/templates/plan-template.md — pending manual review to ensure Constitution Check references principles I–VI
  ⚠ .specify/templates/spec-template.md — pending manual review for tool-authoring spec sections (author, source, version)
  ⚠ .specify/templates/tasks-template.md — pending manual review to add task categories for metadata, install registration, docs sync
  ⚠ README.md — pending update to mention `npx skills add <skill-name>` install path
  ⚠ AGENTS.md — already documents metadata keys (author, source, version); aligned with Principle I
  ⚠ CLAUDE.md — currently only points to plan; will need locality-specific guidance once Principle IV scope is finalized

Deferred items / TODOs:
  - TODO(RATIFICATION_DATE): Confirmed as 2026-04-18 (today, first ratification). Change if the
    intent is to backdate to the repo's first commit.
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
- `source`: the canonical upstream repository URL or reference. For original work this
  MUST be the URL of this repository (or the concrete path within it).
- `version`: a semver string (see Principle II).
- `last-updated`: ISO date (`YYYY-MM-DD`) of the most recent meaningful change.

**Rationale**: Without provenance, adapted skills become orphaned forks, upstream fixes
are lost, and license obligations (Principle V) cannot be honored. A tool whose author,
origin, or version cannot be answered in one read of its frontmatter is non-compliant.

### II. Semantic Versioning for Every Tool

Every skill, subagent, and hook MUST carry a `version` field following
[Semantic Versioning 2.0](https://semver.org/):

- **MAJOR**: Removes a trigger, breaks expected inputs/outputs, or changes defaults in a
  way that would surprise an existing caller.
- **MINOR**: Adds a new capability, new optional input, or broadens triggers without
  breaking existing usage.
- **PATCH**: Wording, documentation, bug fixes, or internal script refactors that do not
  affect behavior from the agent's perspective.

Version bumps MUST accompany every change to the tool's definition or behavior. A commit
that edits a skill without bumping `version` and `last-updated` is non-compliant.

**Rationale**: Traceability through version — explicitly requested — is only meaningful
if the version actually moves when behavior changes. Semver is the shared contract
between the upstream source, local forks, and downstream consumers.

### III. Installability via skills.sh (`npx skills add <skill-name>`)

Every skill published from this repository MUST be installable via:

```
npx skills add <skill-name>
```

backed by `skills.sh`. To satisfy this, each skill MUST:

- Live at a path discoverable by `skills.sh` (the canonical `skills/<skill-name>/`
  directory, with `SKILL.md` at its root).
- Have a `name` frontmatter value that matches its directory name (per the AGENTS.md
  specification).
- Be self-contained: all scripts, references, and assets the skill needs at runtime
  MUST live inside the skill's directory, so that copying that directory is a complete
  install.

Subagents and hooks SHOULD follow the same principle where the installer supports them;
when it does not yet, the tool's README MUST document the manual install path.

**Rationale**: A uniform install command is the difference between a shared catalog and
a pile of scattered files. Enforcing directory self-containment is what makes the one-
line install actually work.

### IV. Agent Docs Sync — AGENTS.md & CLAUDE.md (Locality-Aware)

`AGENTS.md` and `CLAUDE.md` MUST remain authoritative, and updates MUST be
**locality-aware**:

- **Repository-root `AGENTS.md` / `CLAUDE.md`**: Describe cross-cutting conventions
  — the skill/subagent/hook spec, metadata requirements, install command, and any
  rule that applies to every tool in this repo.
- **Skill-local or subagent-local docs** (inside `skills/<name>/` or the agent's
  directory): Describe only that tool's specifics — triggers, inputs, outputs,
  constraints. MUST NOT duplicate repo-wide rules; MAY reference them.
- **Global user-level `~/.claude/CLAUDE.md`**: Out of scope for this repo and MUST
  NOT be modified by repository automation.

Any PR that adds, renames, removes, or changes the contract of a skill/subagent/hook
MUST update the relevant `AGENTS.md` / `CLAUDE.md` at the correct locality in the same
change. Cross-client compatibility notes (OpenCode, Gemini, Claude Code) belong in
root-level `AGENTS.md`.

**Rationale**: Agents read these files to decide what to do. Drift between code and
docs produces wrong delegation decisions. Locality prevents the root docs from
becoming a dumping ground and prevents skill-local docs from contradicting repo rules.

### V. License & Upstream Attribution

When a tool is adapted from an external source:

- The upstream `LICENSE` (or a reference to it) MUST be preserved inside the tool's
  directory.
- The `original-author` and `source` metadata fields MUST point to the upstream.
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
- **Scripts**: Any executable under a tool's `scripts/` directory MUST either be
  self-contained or declare its dependencies explicitly in the tool's docs.
- **Secrets**: No tool may hard-code credentials, API keys, or personal paths. These
  MUST be read from the environment or a configured secret store.
- **Python tooling**: Where a tool uses Python, it MUST be runnable via `uv run`
  (consistent with the user's global conventions).

## Development Workflow

1. **Author** the skill/subagent/hook under the canonical directory with required
   frontmatter (Principles I, II, V, VI).
2. **Register** the tool so `npx skills add <skill-name>` can install it
   (Principle III).
3. **Sync docs** at the correct locality (Principle IV).
4. **Version bump** the tool on every behavior change (Principle II). Commit messages
   SHOULD mention the semver bump type (MAJOR/MINOR/PATCH).
5. **Review** pre-merge: a PR MUST be rejected if it introduces or edits a tool without
   updated metadata, a version bump, or the corresponding docs sync.

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
- **Compliance review**: On every PR that adds or modifies a skill, subagent, or hook,
  the reviewer MUST verify conformance with Principles I–VI. Non-compliance blocks
  merge.
- **Runtime guidance**: For day-to-day execution details (install paths, tooling
  commands, per-client quirks) consult `AGENTS.md` at the appropriate locality.

**Version**: 1.0.0 | **Ratified**: 2026-04-18 | **Last Amended**: 2026-04-18
