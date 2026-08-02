---
name: okf-document-writing
description: Author, update, correct, and structurally validate OKF v0.2 concept documents and Markdown bundles. Use when a user asks to create, revise, review, or check OKF documents, index.md, log.md, YAML frontmatter, bundle links, lifecycle metadata, sources, schemas, examples, or computation descriptions. Do not use for publishing or executing computations.
metadata:
  version: 0.1.0
  okf_version: "0.2"
  tags: okf, documentation, markdown, validation
---

# OKF v0.2 Document Writing

Use this skill to author, update, or validate local OKF v0.2 concept documents and bundles. Before making any structural decision, read the official vendored [OKF v0.2 specification](references/OKF-SPEC-v0.2.md). [The concise v0.2 guide](references/okf-v0.2.md) is non-normative convenience material; it summarizes correct mechanics but does not override the official specification.

## Scope and consent

- Edit files **only** when the user explicitly asks to create, update, or correct them. Otherwise, provide proposed content, findings, or a validation report without writing files.
- Write generated document content and reports in the user's language. Keep this skill's instructions and reference material in English.
- Covers authoring, updating, correction, and structural validation. It excludes publication, deployment, registry submission, and computation execution.
- Preserve user-provided facts, wording, identifiers, and history unless a requested correction requires a change. Ask about material ambiguity instead of guessing.

## Workflow

### Author or update

1. Identify the requested target: a standalone concept document or a bundle. Inspect existing files when a target is supplied.
2. Confirm the requested action authorizes an edit. For a new concept document, collect or request its nonempty `type`; do not infer it.
3. Create or revise the minimum relevant content. Concept documents need parseable YAML frontmatter and a nonempty `type`; their Markdown body remains freeform. `title`, `description`, `resource`, and `tags` are recommended, not universally required.
4. For a bundle, use `index.md` as its navigational entry point and `log.md` as its record of changes/events. Treat both names as reserved rather than concept-document names.
5. Add optional `Schema`, `Examples`, or `Computation` sections only when useful and supported by the user's information. A Computation section describes work; it does not authorize execution.
6. Prefer links absolute relative to the bundle root, such as `[Model](/model.md)` or `[Orders](/tables/orders.md)`; relative Markdown links are also supported. Broken links are not structural conformance errors.
7. Run `uv run --with pydantic --with pyyaml scripts/validate_okf.py <file-or-bundle>` for read-only structural validation. Add `--json` for machine-readable diagnostics, `--bundle-root <directory>` to resolve root-relative links in single-file mode, and `--no-link-check` only when link checking is intentionally out of scope.
8. Report evidence and limits, and summarize the exact edits.

### Review or validate without editing

1. State the files and checks reviewed.
2. Check the required structure and internal bundle links without changing content.
3. Separate confirmed errors from recommendations and unknowns. Offer a patch only if requested.

### Validator limits

- The validator checks concept frontmatter and `type`, Attested Computation runtime and computation representation, reserved index/log constraints, optional local `_okf_policy.yaml` overlays, and available bundle-root-absolute Markdown link targets. Relative links are intentionally ignored; unavailable root links are warnings, not conformance errors.
- It is read-only and does not execute documents or computations.
- The standalone script requires Pydantic v2 and PyYAML. The canonical `uv run --with pydantic --with pyyaml` command supplies them ephemerally without adding a project dependency file; direct execution without them stops with a dependency instruction. PyYAML safely loads frontmatter, and Pydantic validates standardized metadata while preserving unknown producer extensions.
- It is not a full Markdown parser; fenced and inline code are excluded from its narrow link, footnote, heading checks.
- Read [the rule reference](references/validation-rules.md) before treating a diagnostic as a specification result.

## Structural validation checklist

For each concept document (a Markdown file other than reserved `index.md` and `log.md`):

- YAML frontmatter starts the file, is delimited by `---`, and parses as a mapping.
- `type` exists and is nonempty after trimming.
- The body is Markdown and may use any appropriate freeform structure.
- `title`, `description`, `resource`, and `tags` are recommended; their absence is not a structural failure.
- Optional `sources` is a list of mappings. Each entry requires `resource`, which may be a URL, bundle path, relative path, or scope descriptor. `id` is optional and joins `sources[].id` to a body footnote only when used.
- If optional `generated` exists, it requires `by`; `at` is optional. Optional `verified` is a mapping or list of events, and every event requires `by` and `at`.
- Optional lifecycle metadata uses `status` (`draft`, `stable`, or `deprecated`; absent means `stable`) and optional `stale_after`.
- `lifecycle`, `gen`, and `verify` are not standardized substitutes for these fields. Preserve unknown extension keys when round-tripping rather than rejecting them.
- A document with `type: Attested Computation` requires a nonempty string `runtime` and either a `computation` path or level-1 `# Computation` heading.

For a bundle:

- Do not classify `index.md` or `log.md` as ordinary concept documents.
- If present, root-relative links (for example, `/tables/orders.md`) can be checked against the available bundle; relative links are supported but outside this validator's narrow link check. Treat unavailable targets as warnings, not conformance errors.
- Report absent optional metadata, missing reserved files, or unresolved links as observations according to the user's requested convention; do not silently fabricate or repair them.
- An optional bundle-root [`_okf_policy.yaml` template](templates/_okf_policy.yaml) is a strict, local validator overlay, not an OKF document or conformance requirement. In bundle validation, reserved-file settings merge root-to-leaf and apply to every directory containing Markdown; a nested `optional` value can relax an inherited `required` value. Nested policies must omit `okf_version`. Read [the rule reference](references/validation-rules.md) before authoring one; use `--bundle-root` for a single-file validation that should apply bundle policies.

## Evidence and safety rules

- Never invent sources, verification results, generator details, lifecycle state, authors, dates, identifiers, or computation outputs.
- Preserve existing evidence faithfully. Add a source, date, or verification claim only when the user provides it or explicitly directs its inclusion.
- Mark unperformed checks as not verified; structural review is not semantic, published, or execution validation.
- Do not execute code, commands, notebooks, or external computations described by a document. Do not publish, upload, submit, or register content.
- When requested work depends on unavailable facts, use a clearly labeled placeholder only with user approval; otherwise ask a focused question or leave the optional field absent.

## Reporting

For every review or edit, report:

1. **Action and scope:** files reviewed or changed.
2. **Structural result:** passed, failed, or partially verified, with each failing requirement.
3. **Evidence limits:** checks not run, unresolved links, and unsupported claims not asserted.
4. **No-execution/publishing status:** when relevant, confirm neither occurred.

## Boundaries

- No publication workflow, registry integration, remote synchronization, or access-control guidance.
- No execution, calculation, or claim that a computation was run.
- No invented organization-specific schema, policy, lifecycle vocabulary, or mandatory fields beyond user-supplied local `_okf_policy.yaml` rules and v0.2 requirements in the reference.
- For future or intentionally unsupported work, consult [TODO.md](TODO.md).
