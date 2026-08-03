# Quarto Skill Improvement Backlog

This is the durable maintenance backlog for `skills/quarto/`. Prioritize
correctness against the installed Quarto release and the target repository over
adding generic examples.

## Completed in this change

- [x] Replace migration-facing skill routing and catalog language with Quarto
  authoring, configuration, rendering, troubleshooting, and publishing scope.
- [x] Remove migration reference guides. **Scope decision:** migration support
  was removed because it is not needed.
- [x] Add operational routing, authorization, verification, capability, and
  failure guidance to `skills/quarto/SKILL.md`.
- [x] Add concise Quarto-specific guides for configuration, websites, books,
  RevealJS, engines, CLI, profiles, and publishing.
- [x] Record installed-version/provenance guidance rather than claiming a fixed
  Quarto support version.
- [x] Add local Markdown-link and anchor validation with
  `skills/quarto/scripts/validate_reference_links.py`; it excludes fenced code
  examples and external URLs.

## Backlog

### Reference integrity and maintenance

- [ ] Integrate `skills/quarto/scripts/validate_reference_links.py` into CI when
  this repository gains a CI configuration (none exists currently).
- [ ] Audit every reference TOC against headings and repair malformed fences,
  stale examples, and relative links found by automation.
- [ ] Deduplicate overlapping YAML, project, website, book, and format guidance;
  retain one canonical explanation and link to it elsewhere.
- [ ] Add source/provenance metadata or a maintenance date to reference docs,
  without pinning capability claims to an invented Quarto version.

### Configuration and project workflows

- [ ] Expand the precedence/conflict matrix with tested examples for project,
  profile, document, format, execution, metadata-file, and command-line input.
- [ ] Add reviewed examples for project discovery, render selection, output
  directories, resources, and multi-format conflict resolution.
- [ ] Document profiles and directory metadata against current Quarto behavior,
  including safe profile selection and ignored generated output.

### Formats and publishing

- [ ] Add tested workflows for websites, blogs, listings, books, and RevealJS
  that cover navigation, draft content, preview, and format limitations.
- [ ] Extend engine/environment coverage for supported R, Jupyter, Julia, and
  Observable workflows, lockfiles, reproducibility, and kernel discovery.
- [ ] Add current CLI diagnosis for installation, PATH, rendering, preview,
  logging, TeX/PDF, and format-specific failures.
- [ ] Add deployment/provider guidance only after verifying current supported
  options, authentication requirements, previews, and rollback behavior.

### Quality gates

- [ ] Create representative fixtures and evaluations for document, website,
  book, RevealJS, dashboard, manuscript, Typst, engine, missing-Quarto, and
  missing-TeX scenarios.
- [ ] Add a release checklist: run
  `python3 skills/quarto/scripts/validate_reference_links.py`, validate TOCs and
  YAML, review installed Quarto capabilities, and smoke-render only with
  authorization.
