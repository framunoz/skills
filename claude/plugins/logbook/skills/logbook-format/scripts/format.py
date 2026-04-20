#!/usr/bin/env python3
"""Render entries.jsonl to rendered.md for a given logbook."""
import argparse
import json
import os
import sys
from pathlib import Path


def _render_tests_entry(entry: dict) -> str:
    lines = []
    went_well = entry.get("went_well") or []
    went_wrong = entry.get("went_wrong") or []
    next_steps = entry.get("next_steps") or []
    context = entry.get("context") or ""

    lines.append("**Went well:**")
    if went_well:
        lines.extend(f"- {item}" for item in went_well)
    else:
        lines.append("*No observations*")

    lines.append("")
    lines.append("**Went wrong:**")
    if went_wrong:
        lines.extend(f"- {item}" for item in went_wrong)
    else:
        lines.append("*No observations*")

    if next_steps:
        lines.append("")
        lines.append("**Next steps:**")
        lines.extend(f"- {item}" for item in next_steps)

    if context:
        lines.append("")
        lines.append(f"*{context}*")

    return "\n".join(lines)


def _render_collaboration_entry(entry: dict) -> str:
    lines = []
    ai = entry.get("ai_contribution") or ""
    human = entry.get("human_contribution") or ""
    corrections = entry.get("human_corrections") or []
    milestone = entry.get("milestone") or ""
    context = entry.get("context") or ""

    lines.append("**AI contribution:**")
    lines.append(ai if ai.strip() else "*No observations*")

    lines.append("")
    lines.append("**Human contribution:**")
    lines.append(human if human.strip() else "*No observations*")

    if corrections:
        lines.append("")
        lines.append("**Human corrections:**")
        lines.extend(f"- {c}" for c in corrections)

    if milestone:
        lines.append("")
        lines.append(f"**Milestone:** {milestone}")

    if context:
        lines.append("")
        lines.append(f"*{context}*")

    return "\n".join(lines)


def _render_free_entry(entry: dict) -> str:
    return entry.get("body") or "*No observations*"


def _render_amendment_entry(entry: dict) -> str:
    amends = entry.get("amends") or {}
    reason = entry.get("reason") or ""
    body = entry.get("body") or ""
    lines = [
        f"**Amends:** #{amends.get('id', '?')} (`{amends.get('ulid', '?')}`)",
        f"**Reason:** {reason}",
        "",
        body,
    ]
    return "\n".join(lines)


def _format_date(iso: str) -> str:
    return iso[:10] if iso else "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logbook", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    project_root = Path(args.project_root or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    lb_dir = project_root / "logbook" / args.logbook
    meta_path = lb_dir / "meta.json"
    entries_path = lb_dir / "entries.jsonl"
    output_path = Path(args.output) if args.output else lb_dir / "rendered.md"

    if not meta_path.exists():
        print(json.dumps({"ok": False, "error": f"Logbook not found: {args.logbook}"}))
        return 10

    try:
        meta = json.loads(meta_path.read_text())
        raw_lines = entries_path.read_text().splitlines()
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    entries = []
    warnings = []
    for i, line in enumerate(raw_lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            warnings.append(f"line {i}: {e}")

    if not entries and warnings:
        print(json.dumps({"ok": False, "error": "No entries could be parsed.", "warnings": warnings}))
        return 15

    # Build amendment lookup: original_id -> list of amendment entries
    amendment_map: dict[int, list] = {}
    for e in entries:
        if e.get("type") == "amendment":
            orig_id = (e.get("amends") or {}).get("id")
            if orig_id is not None:
                amendment_map.setdefault(orig_id, []).append(e)

    # Group non-amendment entries by type
    type_order = ["tests", "collaboration", "free"]
    type_labels = {"tests": "Tests", "collaboration": "Collaboration", "free": "Free Notes"}

    non_amendments = [e for e in entries if e.get("type") != "amendment"]
    amendment_entries = [e for e in entries if e.get("type") == "amendment"]

    sections = []
    present_types = {e.get("type") for e in non_amendments if e.get("type")}
    ordered_types = [t for t in type_order if t in present_types]
    ordered_types.extend(sorted(present_types - set(type_order)))

    for entry_type in ordered_types:
        typed = sorted(
            [e for e in non_amendments if e.get("type") == entry_type],
            key=lambda e: e.get("created_at", ""), reverse=True
        )
        if not typed:
            continue

        section_lines = [f"## {type_labels.get(entry_type, entry_type)}", ""]
        for e in typed:
            date_str = _format_date(e.get("created_at", ""))
            section_lines.append(f"### [#{e['id']}] {e.get('title', '(no title)')} — {date_str}")
            section_lines.append("")

            etype = e.get("type")
            if etype == "tests":
                section_lines.append(_render_tests_entry(e))
            elif etype == "collaboration":
                section_lines.append(_render_collaboration_entry(e))
            elif etype == "free":
                section_lines.append(_render_free_entry(e))

            # Render amendment callouts under this entry
            for amend in sorted(amendment_map.get(e["id"], []), key=lambda a: a.get("created_at", "")):
                amend_date = _format_date(amend.get("created_at", ""))
                reason = amend.get("reason", "")
                section_lines.append("")
                section_lines.append(f"> Amended by #{amend['id']} on {amend_date}: {reason}")

            tags = e.get("tags") or []
            if tags:
                section_lines.append("")
                section_lines.append("**Tags:** " + ", ".join(f"`{t}`" for t in tags))

            author = e.get("author") or ""
            if author:
                section_lines.append(f"**Author:** {author}")

            section_lines.append("")

        sections.append("\n".join(section_lines))

    # Render standalone amendment section
    if amendment_entries:
        sorted_amendments = sorted(amendment_entries, key=lambda e: e.get("created_at", ""), reverse=True)
        amend_section = ["## Amendments", ""]
        for e in sorted_amendments:
            date_str = _format_date(e.get("created_at", ""))
            amend_section.append(f"### [#{e['id']}] {e.get('title', '(no title)')} — {date_str}")
            amend_section.append("")
            amend_section.append(_render_amendment_entry(e))
            amend_section.append("")
        sections.append("\n".join(amend_section))

    title = meta.get("title", args.logbook)
    header = f"# {title}\n\n"
    if meta.get("description"):
        header += f"*{meta['description']}*\n\n"

    full_content = header + "\n\n".join(sections) + "\n"

    try:
        output_path.write_text(full_content)
    except OSError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 20

    result: dict = {"ok": True, "entries_rendered": len(entries), "output": str(output_path.relative_to(project_root))}
    if warnings:
        result["warnings"] = warnings
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
