# Quarto Profiles and Directory Metadata

Quarto profiles and directory metadata refine project configuration without
requiring every document to repeat shared settings.

## Table of Contents

- [Profiles](#profiles)
- [Directory Metadata](#directory-metadata)
- [Conflict Handling](#conflict-handling)
- [Safe Changes](#safe-changes)

## Profiles

Use the project's established profile naming and activation workflow. Profiles
are for intentional environment-specific variation, not a second
copy of all project settings. Inspect the selected profile before changing it and
record it when rendering or reporting.

## Directory Metadata

Use `_metadata.yml` for shared metadata and options applying to a directory of
documents when that is already the repository convention. Keep document-specific
title, content, and overrides in document YAML. See [YAML front matter](yaml-front-matter.md).

## Conflict Handling

Project configuration, selected profile, directory metadata, document YAML,
format-specific options, and explicit command-line input can interact. Put a
setting in the least-specific layer that owns it, and verify the effective result
when layers conflict. See [project configuration](project-configuration.md) for
the precedence matrix and capability warnings.

When testing a profile, use `--profile <name>` with one target document and
`--to <format>`. Keep the profile selection in the recorded command; a profile
file alone does not prove it was active. Compare one configuration change at a
time and inspect the resulting output or diagnostic rather than copying options
between `_quarto.yml`, `_metadata.yml`, and document YAML.

## Safe Changes

Do not rename profiles, relocate metadata, or change output/resource paths
without checking all affected documents. Avoid editing generated output and ask
before a full render that would apply a profile globally.
