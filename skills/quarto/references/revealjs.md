# Quarto RevealJS Presentations

Quarto RevealJS creates an HTML slide deck. Use it when the presentation will
be delivered in a browser rather than as an editable or print-first document.

## Table of Contents

- [Slide Hierarchy](#slide-hierarchy)
- [Speaker Notes](#speaker-notes)
- [Fragments](#fragments)
- [Preview and Presenter Workflow](#preview-and-presenter-workflow)
- [Assets](#assets)
- [Format Limitations](#format-limitations)
- [Verification](#verification)

## Slide Hierarchy

Use a level-one heading for a horizontal slide and a level-two heading for a
vertical slide beneath it. Keep one idea per slide; use horizontal slides for
major topic changes and vertical slides for supporting detail or a short
sequence. Use a horizontal rule (`---`) when an explicit slide boundary is
clearer than heading structure.

```markdown
# Main point

## Supporting detail

---

# Next point
```

Avoid treating heading depth as a generic document outline: deeper headings can
make navigation harder to predict in a deck.

## Speaker Notes

Put delivery-only material in a notes block. Notes are not audience content in
the normal slide view and should not carry essential information.

```markdown
::: {.notes}
Pause after the question and use the example only if needed.
:::
```

Keep citations, qualifications, and instructions needed by the audience on the
slide or in an accompanying handout instead of only in notes.

## Fragments

Use fragments to reveal a short, deliberate sequence. Apply `.fragment` to each
item that should appear incrementally, and ensure the slide remains
understandable if the presenter advances quickly or exports a static copy.

```markdown
- First observation {.fragment}
- Second observation {.fragment}
- Decision {.fragment}
```

Do not use fragments to hide essential context for long periods; they are a
presentation aid, not a substitute for slide structure.

## Preview and Presenter Workflow

Before presenting, open the deck in a browser preview and verify both keyboard
navigation and vertical/horizontal movement. Use the presenter view for notes,
timing, and the upcoming slide when it is available in the selected deck
configuration. Test that view on the presentation machine and display setup,
especially when using two screens.

Ask before previewing or rendering. When authorized, verify navigation, notes,
fragments, executed cells, and asset loading. Use
[CLI and troubleshooting](cli-troubleshooting.md) for render failures.

## Assets

Use repository-relative paths for images, video, and downloadable resources.
Keep files close to the deck or in a clearly named asset directory, use stable
filenames, and include meaningful alt text for images. Test media playback in
the browser that will be used for delivery; linked local files and remote media
can fail because of path, network, autoplay, or browser-policy differences.

Reuse [figures](figures.md), [code cells](code-cells.md), and
[shortcodes](shortcodes.md) for their respective syntax. Treat plugins and
extensions as executable third-party code: inspect and obtain authorization
before installation or upgrade.

## Format Limitations

RevealJS is an HTML presentation format. Slide navigation, fragments, speaker
notes, presenter tooling, CSS, JavaScript, live code, and interactive widgets
are not portable as equivalent features to PDF/LaTeX, DOCX, or Typst. Provide
static content when those features convey meaning, and use
[rendering formats](rendering-formats.md) to select an appropriate target.

## Verification

Check the installed Quarto version before introducing version-sensitive
presentation features. Verify that every slide has a readable hierarchy, that
assets resolve from the deck location, and that the deck remains usable without
presenter-only information.
