"""Every file the skill points to exists, and every docs path it cites is in references.md."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
DOCS = [p for p in SKILL.rglob("*.md") if "tests" not in p.parts]
LOCAL = re.compile(r"`((?:concepts|formats|assets|scripts)/[\w./-]+|(?:gotchas|recipes|cheatsheet|glossary|references)\.md)`")
DOCS_PATH = re.compile(
    r"`((?:authoring|computations|projects|output-formats|presentations|websites|books|manuscripts|"
    r"publishing|dashboards|extensions|reference|interactive|advanced|journals|tools|troubleshooting)/[\w/-]+)`"
)


class PointerTests(unittest.TestCase):
    def test_local_pointers_exist(self):
        missing = []
        for doc in DOCS:
            for target in LOCAL.findall(doc.read_text(encoding="utf-8")):
                if not (SKILL / target).exists():
                    missing.append(f"{doc.relative_to(SKILL)} -> {target}")
        self.assertEqual(missing, [])

    def test_docs_paths_listed_in_references(self):
        listed = set(DOCS_PATH.findall((SKILL / "references.md").read_text(encoding="utf-8")))
        missing = sorted(
            {f"{doc.relative_to(SKILL)} -> {path}" for doc in DOCS if doc.name != "references.md"
             for path in DOCS_PATH.findall(doc.read_text(encoding="utf-8")) if path not in listed}
        )
        self.assertEqual(missing, [])

    def test_fences_balanced(self):
        fence = re.compile(r"^\s*(`{3,})")
        for doc in DOCS:
            stack: list[int] = []
            for line in doc.read_text(encoding="utf-8").splitlines():
                m = fence.match(line)
                if not m:
                    continue
                ticks = len(m.group(1))
                rest = line.strip()[ticks:].strip()
                if stack and ticks >= stack[-1] and not rest:
                    stack.pop()
                elif rest or not stack:
                    stack.append(ticks)
            self.assertEqual(stack, [], f"unbalanced fence in {doc.relative_to(SKILL)}")


if __name__ == "__main__":
    unittest.main()
