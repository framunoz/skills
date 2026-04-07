#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml"]
# ///
import yaml
import re
from pathlib import Path


def update_frontmatter(file_path, new_tags, related_skills):
    path = Path(file_path)
    if not path.exists():
        print(f"Skipping {file_path}: Not found")
        return
    content = path.read_text()

    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        print(f"Skipping {file_path}: No frontmatter")
        return

    try:
        data = yaml.safe_load(match.group(1))
        if "metadata" not in data:
            data["metadata"] = {}

        # Current name
        current_name = data.get("name", path.parent.name)

        # Update Tags (merge with existing)
        existing_tags = data["metadata"].get("tags", "")
        tags_set = set(t.strip() for t in existing_tags.split(",") if t.strip())
        tags_set.update(new_tags)
        data["metadata"]["tags"] = ", ".join(sorted(list(tags_set)))

        # Update Related-with (ensure nested structure)
        if "related-with" not in data["metadata"]:
            data["metadata"]["related-with"] = {"skills": []}

        if not isinstance(data["metadata"]["related-with"], dict):
            data["metadata"]["related-with"] = {"skills": []}

        related_set = set(data["metadata"]["related-with"].get("skills", []))

        # Only add valid skills that are not itself
        related_set.update([s for s in related_skills if s != current_name])
        data["metadata"]["related-with"]["skills"] = sorted(list(related_set))

        # Re-generate YAML
        # Use default_flow_style=False to keep it human-readable
        new_yaml = yaml.dump(
            data, sort_keys=False, allow_unicode=True, default_flow_style=False
        )
        new_content = f"---\n{new_yaml}---\n" + content[match.end() :]
        path.write_text(new_content)
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")


# --- KEDRO CLUSTER ---
kedro_skills = [
    "kedro-authoring",
    "kedro-hooks-plugins",
    "kedro-migration-assistant",
    "kedro-notebook-converter",
]
for s in kedro_skills:
    update_frontmatter(
        f"gemini/skills/{s}/SKILL.md",
        ["python", "kedro", "data-engineering", "pipelines"],
        kedro_skills,
    )

# --- QUARTO CLUSTER ---
quarto_skills = ["quarto-authoring", "quarto-migrations", "quarto-advanced"]
for s in quarto_skills:
    update_frontmatter(
        f"gemini/skills/{s}/SKILL.md",
        ["quarto", "documentation", "publishing", "reproducibility"],
        quarto_skills,
    )

# --- CORE ARCHITECT ---
arch_skills = [
    "adr-manager",
    "tradeoff-analyzer",
    "system-modeler",
    "oop-designer",
    "effective-functions",
]
for s in arch_skills:
    update_frontmatter(
        f"gemini/skills/{s}/SKILL.md",
        ["architecture", "design-patterns", "decision-making"],
        arch_skills,
    )
