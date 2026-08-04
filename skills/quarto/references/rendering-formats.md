# Quarto Rendering Formats

Choose the output format before relying on a format-specific feature. Source
Markdown, citations, tables, and static images are usually portable; layout,
styling, and interactivity are not.

## Capability, Dependency, and Portability Matrix

| Format | Primary capability | Typical dependency | Portability considerations |
| --- | --- | --- | --- |
| HTML | Browser document with CSS and JavaScript | Quarto and a browser | Best target for interactive widgets and embedded media. Browser behavior, local fonts, and external assets can vary. |
| PDF/LaTeX | Print-oriented, paginated document | A working LaTeX installation and required packages | Static output; HTML/CSS/JavaScript features do not transfer. Font and package availability affect reproducibility. |
| DOCX | Editable Microsoft Word document | Quarto; an optional reference DOCX for house styles | Use semantic headings, paragraphs, and tables. Browser layout and raw HTML are not portable to Word. |
| Typst | Print-oriented PDF with Typst typesetting | Typst installation supplied or located by Quarto | A LaTeX alternative for PDF output. Typst templates and raw Typst are not portable to LaTeX or HTML. |
| RevealJS | Browser slide deck with navigation and speaker tools | Quarto and a modern browser | HTML-only presentation format. Slide controls, fragments, notes, and JavaScript do not become document-format features. |

## Portable Authoring Baseline

- Prefer semantic Markdown headings, lists, tables, citations, and image alt
  text for content intended for several formats.
- Keep format-specific styling, raw markup, and layout overrides isolated so
  they can be replaced or omitted for another target.
- Provide static fallbacks for information carried by interactive controls,
  widgets, animation, or speaker notes.
- Treat local fonts, LaTeX packages, Typst packages, and reference documents as
  build dependencies that must be available wherever the document is rendered.

## Format Selection

Use HTML for interactive reading, PDF/LaTeX or Typst for a fixed print layout,
DOCX for an editable handoff, and RevealJS for a browser-delivered talk. A
single source can target multiple formats, but equivalent content does not
guarantee equivalent appearance or behavior.

For presentation-specific authoring guidance, see [RevealJS presentations](revealjs.md).
