# Mermaid Swimlane Syntax Reference

Use this reference only for Mermaid swimlane diagrams. Swimlanes are a distinct, beta Mermaid diagram type and require Mermaid 11.16.0+; syntax and rendering can evolve.

> **Compatibility warning:** Swimlanes use the beta `swimlane-beta` declaration, and target renderers may not support them. When support and version cannot be confirmed, do not choose swimlanes by default; use a flowchart only if it can faithfully convey the requested process, and disclose the fallback.

## Declaration and direction

Declare a swimlane diagram with `swimlane-beta` and set its direction.

```mermaid
swimlane-beta
    direction LR
```

## Lanes, nodes, and handoffs

Each top-level `subgraph` defines a lane. Give lanes stable IDs and readable labels; only top-level subgraphs are lanes. Nodes and edges use flowchart-style syntax. An edge crossing lanes represents a handoff; label it when its meaning matters.

```mermaid
swimlane-beta
    direction LR
    subgraph requester_lane[Requester]
        submit[Submit request]
    end
    subgraph support_lane[Support]
        review[Review request] --> resolve[Resolve request]
    end
    submit -->|assign| review
```

For shared [node](flowcharts.md#node-ids-and-labels) and [link](flowcharts.md#arrows-lines-and-labels) syntax, consult the flowchart reference.

## Guardrails

- Model one process per diagram and keep ownership consistent within each lane.
- Label cross-lane handoffs when their meaning matters.
- Use only top-level `subgraph` blocks as lanes.
- Confirm beta support in the target renderer and version; render when tooling is available, otherwise state that rendering was not verified.

## Explore further

This focused reference intentionally does not cover: supported directions and defaults, lane IDs versus display labels, accessibility titles and descriptions, flowchart shape catalog and Markdown labels, syntax evolution of the beta diagram, choosing swimlanes versus sequence diagrams. See the [official Mermaid reference](https://mermaid.js.org/syntax/swimlanes.html).

## Official documentation

- [Mermaid swimlane syntax](https://mermaid.js.org/syntax/swimlanes.html)
