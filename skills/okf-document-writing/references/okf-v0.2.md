# OKF v0.2: Writing Reference

## Purpose

This non-normative convenience guide summarizes the working structural baseline for OKF v0.2 authoring and review. Read the vendored [official specification](OKF-SPEC-v0.2.md) for structural decisions; it is authoritative if this guide differs. This guide distinguishes mandatory document structure from optional descriptive metadata. It does not define publication or computation execution.

## Concept documents

A concept document is a Markdown document with:

1. YAML frontmatter at the start of the file, delimited by `---` and parseable as YAML.
2. A nonempty `type` value in that frontmatter.
3. A freeform Markdown body.

Minimal form:

```markdown
---
type: concept
---

# Title

Freeform Markdown content.
```

The actual `type` must come from the document owner or applicable convention; do not invent it.

## Recommended and optional metadata

Recommended fields are `title`, `description`, `resource`, and `tags`. They improve interoperability but are not structural requirements for every concept document.

Optional provenance uses `sources`, a list of mappings. Every entry requires `resource`; it may be a URL, a bundle-relative or relative path, or a scope descriptor. `id` is optional and, when a source is cited in the Markdown body, joins `sources[].id` to the corresponding footnote; for example, `id: source-1` corresponds to `[^source-1]`.

If `generated` exists, `generated.by` is required and `generated.at` is optional. Optional `verified` is a mapping or list of events; every event requires `by` and `at`. Lifecycle metadata uses `status: draft|stable|deprecated` (absent means `stable`) and optional `stale_after`. `lifecycle`, `gen`, and `verify` are not standardized substitutes, but unknown extension keys must be preserved rather than rejected.

`type: Attested Computation` requires `runtime` in its frontmatter. Other types do not acquire that requirement merely by describing computation.

Do not fabricate source citations, generation details, lifecycle states, verification claims, dates, or runtime details to make a document appear complete.

The body can contain any Markdown. When helpful, use sections such as:

- `## Schema` for a data or conceptual structure.
- `## Examples` for user-provided illustrative cases.
- `## Computation` to describe intended or recorded computational work.

Describing computation does not mean it was executed.

## Bundles

A bundle is a directory of related Markdown documents. `index.md` and `log.md` are reserved names:

- `index.md` is the bundle entry point or navigation document.
- `log.md` records changes or events.

They are not ordinary concept documents merely because they are Markdown files. Apply concept-document requirements to other concept files; validate reserved files according to their bundle role and requested convention.

Use Markdown links absolute relative to the bundle root:

```markdown
[Concept](/concept.md)
[Nested document](/models/forecast.md)
```

The leading `/` is rooted at the bundle, not the filesystem. This is the recommended form; standard relative Markdown links are also supported. Avoid machine-specific filesystem paths. Broken links are tolerated and are not structural conformance errors.

## Validation vocabulary

- **Passed:** all checked structural requirements were satisfied.
- **Failed:** a checked requirement was not satisfied, such as absent/unparseable frontmatter or empty `type` in a concept document.
- **Partially verified:** some checks could not be performed, such as a link target unavailable in the supplied bundle.

Structural validation does not prove the body is true, sources are reliable, a computation ran, or content was published.
