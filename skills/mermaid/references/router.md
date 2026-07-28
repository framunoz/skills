# Mermaid Diagram Type Router

Use this page to select the supported Mermaid diagram type before reading its focused reference.

| Diagram type | What it represents | Use it when | Reference |
| --- | --- | --- | --- |
| Flowchart | A directed graph of processes, decisions, dependencies, systems, or data | Direction, branching, or relationships matter | [flowcharts.md](flowcharts.md) |
| Tree View | A hierarchical parent-child tree of items, categories, or nested structure | The hierarchy and containment relationships matter | [tree-view.md](tree-view.md) |
| Sequence diagram | A chronological exchange of messages between participants, services, or systems | The order of interactions matters | [sequence-diagrams.md](sequence-diagrams.md) |
| Swimlane | A process partitioned by role, team, system, or phase | Ownership and cross-boundary handoffs matter | [swimlanes.md](swimlanes.md) |

Maintainers: use the [complete diagram-type coverage tracker](diagram-types.md) to register and track supported types.

Mermaid swimlanes are distinct beta diagrams, not flowcharts. See their reference for type-specific compatibility.

## Swimlane compatibility

Swimlanes use the beta `swimlane-beta` declaration, and target renderers may not support them. When support and version cannot be confirmed, do not choose swimlanes by default; use a flowchart only if it can faithfully convey the requested process, and disclose the fallback.

## Decision rules

- Honor an explicit supported type.
- On revisions, preserve the existing diagram declaration unless conversion is requested.
- Choose by information structure, not visual appearance.
- Ask one clarification only when multiple registered types are genuinely plausible.
- Split mixed concerns into separate supported diagrams.
- Do not invent syntax for unsupported types; name the requested type as out of scope.

## Adding a type

For maintainers adding a type manually:

1. Create one focused reference with: when to use and not use it, declaration, syntax, quality rules, pitfalls, compatibility, validated examples, and official documentation.
2. Add one router row that describes its information structure and links to that reference.
3. Validate its examples in the relevant renderer before publishing.

Do not modify `SKILL.md` when adding a registered type; it remains a stable router.
