# Mermaid Tree View Syntax Reference

Use this reference only for Mermaid Tree View diagrams. Tree View is experimental and requires Mermaid 11.14.0+; syntax and rendering can evolve.

> **Compatibility warning:** Tree View uses the beta `treeView-beta` declaration, and target renderers may not support it. Confirm the target renderer and Mermaid version, and render when tooling is available; otherwise state that rendering was not verified.

## When to use Tree View

Use Tree View for strict hierarchical parent-child containment: file trees, taxonomies, organization structures, or nested categories. Use a flowchart for directed processes or branching, a sequence diagram for temporal exchanges, and a mindmap for broad ideation.

## Declaration and basic grammar

Declare a Tree View diagram with `treeView-beta`. Indentation defines the hierarchy. Labels ending in `/` render as bold directories; quote labels containing spaces. Tabs expand to spaces, and comments use `%%`.

```mermaid
treeView-beta
    my-project/
        src/
            index.js
        package.json
        README.md
```

Box-drawing input is also available, but is intentionally deferred to the official documentation.

## Guardrails

- Preserve a strict tree: every item has at most one parent and no cycles or cross-links.
- Tree View has no documented node IDs or direction controls.
- Do not assume configuration or icon support works in the target renderer: icons are hidden by default, and custom icon packs require registration or render as question marks.
- Confirm experimental support in the target renderer and version; render when tooling is available, otherwise state that rendering was not verified.

## Explore further

This focused reference intentionally does not cover: box-drawing input, layout configuration (`rowIndent`, padding, line thickness), built-in/custom icon configuration, and themes/accessibility. See the [official Mermaid reference](https://mermaid.js.org/syntax/treeView.html).

## Official documentation

- [Mermaid Tree View syntax](https://mermaid.js.org/syntax/treeView.html)
