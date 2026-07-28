# Mermaid Diagram Type Router

Use this page to select a supported Mermaid diagram type before reading its focused reference. Preserve an existing supported declaration during a revision unless the user requests conversion or it can no longer represent the required meaning.

| Diagram type | What it represents | Use it when | Reference |
| --- | --- | --- | --- |
| Flowchart | A directed graph of processes, decisions, dependencies, systems, or data | Direction, branching, or relationships matter | [behavior/flowcharts.md](behavior/flowcharts.md) |
| Architecture diagram | A high-level view of system services, components, groups, and relationships | System structure, deployment boundaries, or component relationships matter | [structure/architectures.md](structure/architectures.md) |
| Tree View | A hierarchical parent-child tree of items, categories, or nested structure | The hierarchy and containment relationships matter | [structure/tree-view.md](structure/tree-view.md) |
| Mindmap | A radial, non-linear map of ideas and related concepts | Broad ideation, brainstorming, or conceptual exploration matters | [structure/mindmaps.md](structure/mindmaps.md) |
| Timeline | A chronological view of events, milestones, and periods | Dates, milestones, or historical progression over time matter | [time/timelines.md](time/timelines.md) |
| Sequence diagram | A chronological exchange of messages between participants, services, or systems | The order of interactions matters | [behavior/sequence-diagrams.md](behavior/sequence-diagrams.md) |
| Swimlane | A process partitioned by role, team, system, or phase | Ownership and cross-boundary handoffs matter | [behavior/swimlanes.md](behavior/swimlanes.md) |

Mermaid swimlanes are distinct beta diagrams, not flowcharts. See their reference for type-specific compatibility.

## Quick decision questions

Ask these questions in order:

1. Is the request an edit to an existing supported diagram? Keep its declaration unless conversion is requested or necessary for correctness.
2. Is the primary structure message order between participants? Choose a Sequence diagram.
3. Is it chronological milestones or periods without participant exchange? Choose a Timeline.
4. Is it strict parent-child containment? Choose Tree View; is it non-linear ideation? Choose Mindmap.
5. Is it services, groups, deployment boundaries, and their relationships? Choose an Architecture diagram.
6. Is it a process whose ownership or handoffs must be visible? Consider Swimlane only after its compatibility check; otherwise choose a Flowchart for directed flow, decisions, dependencies, or general relationships.

Ask one concise clarification only if these questions leave two supported types equally plausible.

## Tie-break and revision rules

- Honor an explicit supported type.
- On a revision, preserve the declaration, diagram type, stable identifiers, and meaning unless the requested change requires conversion.
- Prefer the type whose information structure is primary, not the type with the preferred visual appearance: message order over ownership, ownership over generic process flow, strict hierarchy over ideation, and chronology over causal branching.
- If a process needs both ownership and branching, choose Swimlane only when the target renderer supports it; otherwise use a Flowchart and disclose that ownership lanes were not preserved.
- Split genuinely mixed concerns into separate supported diagrams rather than forcing one type to carry all relationships.

## Swimlane compatibility

Swimlanes use the beta `swimlane-beta` declaration, and target renderers may not support them. When support and version cannot be confirmed, do not choose swimlanes by default; use a flowchart only if it can faithfully convey the requested process, and disclose the fallback.

## Unsupported or undocumented syntax

Do not invent syntax, configuration, interaction, or accessibility features that are unsupported, undocumented, or absent from the selected focused reference and confirmed target renderer. State the limitation, preserve the valid portion of the requested diagram, and offer only a documented supported alternative when one exists. If no faithful supported alternative exists, mark the request out of scope rather than silently converting it.
