#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml", "tomli", "networkx", "jinja2"]
# ///

import re
import yaml
import tomli
import json
import networkx as nx
from pathlib import Path


def extract_metadata(file_path):
    path = Path(file_path)
    content = path.read_text()

    # Platform detection
    if "gemini" in str(path).lower():
        platform = "gemini"
    elif "opencode" in str(path).lower():
        platform = "opencode"
    else:
        platform = "common"

    # Defaults
    name = path.parent.name if path.name == "SKILL.md" else path.stem
    metadata = {"name": name, "platform": platform, "type": "unknown", "related": []}

    if "skills" in str(path):
        metadata["type"] = "skill"
    elif "agents" in str(path):
        metadata["type"] = "agent"
    elif "commands" in str(path):
        metadata["type"] = "command"

    # Extract YAML frontmatter
    if path.suffix == ".md":
        match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if match:
            try:
                data = yaml.safe_load(match.group(1))
                metadata["name"] = data.get("name", name)
                related_data = data.get("metadata", {}).get("related-with", {})
                if isinstance(related_data, dict):
                    for cat in ["skills", "agents", "commands"]:
                        metadata["related"].extend(
                            [f"{platform}__{r}" for r in related_data.get(cat, [])]
                        )
            except Exception:
                pass

    # Extract TOML (Gemini Commands)
    elif path.suffix == ".toml":
        try:
            data = tomli.loads(content)
            prompt = data.get("prompt", "")
            skills_found = re.findall(r"skills/([^/]+)/", prompt)
            metadata["related"].extend([f"gemini__{s}" for s in skills_found])

            if "metadata" in data and "related-with" in data["metadata"]:
                rel = data["metadata"]["related-with"]
                for cat in ["skills", "agents", "commands"]:
                    metadata["related"].extend(
                        [f"gemini__{r}" for r in rel.get(cat, [])]
                    )
        except Exception:
            pass

    return metadata


def generate_mermaid(G):
    lines = ["graph LR"]
    platforms = {"gemini": [], "opencode": [], "common": []}

    for node, data in G.nodes(data=True):
        platforms[data.get("platform", "common")].append(node)

    for plat, nodes in platforms.items():
        if not nodes:
            continue
        lines.append(
            f"    subgraph {plat.upper()}_PLATFORM [{plat.capitalize()} Ecosystem]"
        )
        for node in nodes:
            data = G.nodes[node]
            name = data.get("name")
            type_ = data.get("type", "unknown")
            style = ""
            if type_ == "skill":
                style = ":::skillStyle"
            elif type_ == "agent":
                style = ":::agentStyle"
            elif type_ == "command":
                style = ":::commandStyle"
            lines.append(f"        {node}({name}){style}")
        lines.append("    end")

    for u, v in G.edges():
        lines.append(f"    {u} --- {v}")

    # High Contrast Class Definitions
    lines.append(
        "    classDef skillStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#000"
    )
    lines.append(
        "    classDef agentStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000"
    )
    lines.append(
        "    classDef commandStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000"
    )

    return "\n".join(lines)


def main():
    root = Path(".")
    G = nx.Graph()

    files = (
        list(root.glob("**/SKILL.md"))
        + list(root.glob("gemini/commands/*.toml"))
        + list(root.glob("gemini/agents/*.md"))
        + list(root.glob("opencode/commands/*.md"))
        + list(root.glob("opencode/agents/*.md"))
    )

    for f in files:
        meta = extract_metadata(f)
        node_id = f"{meta['platform']}__{meta['name']}"
        G.add_node(node_id, **meta)
        for r in meta["related"]:
            if r != node_id:
                G.add_edge(node_id, r)

    # Export JSON
    with open("knowledge-graph.json", "w") as f:
        json.dump(nx.node_link_data(G), f, indent=2)

    # Export Mermaid
    mermaid = generate_mermaid(G)
    with open("RELATIONS.md", "w") as f:
        f.write("# Repository Knowledge Graph\n\n")
        f.write("```mermaid\n" + mermaid + "\n```\n")

    print("Graph generated with high-contrast styles!")


if __name__ == "__main__":
    main()
