# Quarto Books

Quarto books organize a sequence of chapters and shared book configuration.

## Table of Contents

- [Book Configuration](#book-configuration)
- [Chapter Workflow](#chapter-workflow)
- [Formats and Rendering](#formats-and-rendering)
- [Related References](#related-references)

## Book Configuration

Use the existing `_quarto.yml` as the authority for `project: type: book`, the
chapter order, bibliography, and output formats. Do not reorder chapters or
change the landing page merely to add content. See [project configuration](project-configuration.md).

## Chapter Workflow

Create or edit the named chapter file, follow the established heading and label
conventions, and maintain cross-references across the book. Use
[cross-references](cross-references.md), [citations](citations.md), and
[figures](figures.md) rather than duplicating their syntax here.

## Formats and Rendering

Book output can vary by format; validate HTML navigation, PDF/TeX dependencies,
and DOCX/Typst limitations independently. Ask before a full book render because
it can execute many documents and replace generated output. For failures, use
[CLI and troubleshooting](cli-troubleshooting.md).

## Related References

- [Project configuration](project-configuration.md)
- [YAML front matter](yaml-front-matter.md)
- [Typst](typst.md)
