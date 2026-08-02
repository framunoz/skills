"""Targeted self-contained checks for the read-only OKF validator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_okf.py"
class ValidateOkfTest(unittest.TestCase):
    """Exercise file, bundle, reserved-file, and advisory-field behavior."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.bundle = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, name: str, content: str) -> Path:
        path = self.bundle / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_validator(self, *arguments: str) -> tuple[int, set[str]]:
        code, diagnostics = self.run_validator_details(*arguments)
        return code, {item["code"] for item in diagnostics}

    def run_validator_details(self, *arguments: str) -> tuple[int, list[dict[str, object]]]:
        result = subprocess.run([sys.executable, str(SCRIPT), "--json", *arguments], text=True, capture_output=True, check=False)
        self.assertTrue(result.stdout, result.stderr)
        payload = json.loads(result.stdout)
        return result.returncode, payload["diagnostics"]

    def test_file_mode_skips_root_resolution_without_bundle_root(self) -> None:
        document = self.write("concept.md", "---\ntype: Concept\n---\n[Missing](/missing.md)\n")
        code, findings = self.run_validator(str(document))
        self.assertEqual(code, 0)
        self.assertIn("ROOT_LINK_CHECK_SKIPPED", findings)
        code, findings = self.run_validator("--bundle-root", str(self.bundle), str(document))
        self.assertEqual(code, 0)
        self.assertIn("LINK_TARGET_UNAVAILABLE", findings)

    def test_bundle_reserved_files_and_root_links(self) -> None:
        self.write("index.md", "---\nokf_version: '0.2'\n---\n[Target](/nested/target.md?view=1#part)\n")
        self.write("nested/target.md", "---\ntype: Concept\n---\n")
        self.write("nested/index.md", "---\nokf_version: '0.2'\n---\n")
        self.write("log.md", "## 2026-01-01\n* New\n\n## 2026-02-01\n* Older heading second\n\n## not-a-date\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("INDEX_FRONTMATTER_NOT_ALLOWED", findings)
        self.assertIn("LOG_DATE_INVALID", findings)
        self.assertIn("LOG_DATES_NOT_NEWEST_FIRST", findings)
        self.assertNotIn("LINK_TARGET_UNAVAILABLE", findings)

    def test_attested_computation_requires_runtime_and_representation(self) -> None:
        self.write("attested.md", "---\ntype: Attested Computation\n---\n# Title\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("RUNTIME_MISSING", findings)
        self.assertIn("COMPUTATION_MISSING", findings)

    def test_advisory_shapes_and_code_are_checked_narrowly(self) -> None:
        self.write("metadata.md", "---\ntype: Concept\nsources:\n  - id: known\n  - text\ngenerated: {}\nverified:\n  - by: process:test\nstatus: current\nstale_after: '2026-02-30'\n---\n[^missing]: Not a source\n`[Inline](/ignored.md)`\n```markdown\n[Fenced](/also-ignored.md)\n```\n")
        self.write("footnote.md", "---\ntype: Concept\nsources:\n  - id: known\n    resource: relative/source.md\n---\n[^missing]: Not a source\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertTrue({"SOURCE_RESOURCE_MISSING", "SOURCE_NOT_MAPPING", "GENERATED_BY_MISSING", "VERIFIED_EVENT_MISSING_FIELDS", "STATUS_INVALID", "STALE_AFTER_INVALID", "SOURCE_FOOTNOTE_UNMATCHED"}.issubset(findings))
        self.assertNotIn("LINK_TARGET_UNAVAILABLE", findings)

    def test_generated_at_accepts_iso_datetime_and_rejects_malformed_data(self) -> None:
        valid = self.write("generated-valid.md", "---\ntype: Concept\ngenerated:\n  by: process:writer\n  at: 2026-06-20T22:53:05Z\n---\n")
        code, findings = self.run_validator(str(valid))
        self.assertEqual(code, 0)
        self.assertNotIn("GENERATED_AT_INVALID", findings)

        invalid = self.write("generated-invalid.md", "---\ntype: Concept\ngenerated:\n  by: process:writer\n  at: not-a-datetime\n---\n")
        code, findings = self.run_validator(str(invalid))
        self.assertEqual(code, 1)
        self.assertIn("GENERATED_AT_INVALID", findings)

    def test_invalid_runtime_and_inline_representation(self) -> None:
        self.write("bad-runtime.md", "---\ntype: Attested Computation\nruntime: [python]\n---\n# Computation\ncode\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("RUNTIME_INVALID", findings)
        self.assertNotIn("COMPUTATION_MISSING", findings)

    def test_root_policy_requires_and_suggests_frontmatter_fields(self) -> None:
        self.write("_okf_policy.yaml", "policy_version: 1\nokf_version: '0.2'\nfrontmatter:\n  required:\n    add: [title]\n  suggested:\n    add: [description]\n")
        self.write("concept.md", "---\ntype: Concept\n---\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("POLICY_REQUIRED_FIELD_MISSING", findings)
        self.assertIn("POLICY_SUGGESTED_FIELD_MISSING", findings)

    def test_policy_inheritance_demotion_and_sibling_isolation(self) -> None:
        self.write("_okf_policy.yaml", "policy_version: 1\nokf_version: '0.2'\nfrontmatter:\n  required:\n    add: [title]\n")
        self.write("nested/_okf_policy.yaml", "policy_version: 1\nfrontmatter:\n  suggested:\n    add: [title]\n")
        self.write("nested/concept.md", "---\ntype: Concept\n---\n")
        self.write("sibling/concept.md", "---\ntype: Concept\n---\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("POLICY_REQUIRED_FIELD_MISSING", findings)
        self.assertIn("POLICY_SUGGESTED_FIELD_MISSING", findings)

    def test_policy_reserved_requirements_apply_to_markdown_directories(self) -> None:
        self.write("_okf_policy.yaml", "policy_version: 1\nokf_version: '0.2'\nreserved:\n  index.md: required\n")
        self.write("nested/_okf_policy.yaml", "policy_version: 1\nreserved:\n  log.md: required\n")
        self.write("nested/concept.md", "---\ntype: Concept\n---\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("POLICY_REQUIRED_FILE_MISSING", findings)

    def test_reserved_policy_inherits_and_allows_nested_relaxation(self) -> None:
        self.write("_okf_policy.yaml", "policy_version: 1\nokf_version: '0.2'\nreserved:\n  index.md: required\n  log.md: optional\n")
        self.write("index.md", "# Root index\n")
        self.write("child/_okf_policy.yaml", "policy_version: 1\nreserved:\n  log.md: required\n")
        self.write("child/concept.md", "---\ntype: Concept\n---\n")
        self.write("relaxed/_okf_policy.yaml", "policy_version: 1\nreserved:\n  index.md: optional\n")
        self.write("relaxed/concept.md", "---\ntype: Concept\n---\n")
        code, diagnostics = self.run_validator_details(str(self.bundle))
        self.assertEqual(code, 1)
        missing_paths = {
            item["path"]
            for item in diagnostics
            if item["code"] == "POLICY_REQUIRED_FILE_MISSING"
        }
        self.assertEqual(missing_paths, {str((self.bundle / "child").resolve())})
        self.assertEqual(sum(item["code"] == "POLICY_REQUIRED_FILE_MISSING" for item in diagnostics), 2)

    def test_invalid_policies_and_missing_root_policy_do_not_apply(self) -> None:
        self.write("_okf_policy.yaml", "policy_version: 1\nokf_version: '0.2'\n")
        self.write("unknown/_okf_policy.yaml", "policy_version: 1\nunknown: true\n")
        self.write("invalid/_okf_policy.yaml", "policy_version: 1\nreserved:\n  index.md: mandatory\n")
        self.write("malformed/_okf_policy.yaml", "policy_version: [\n")
        self.write("weaken/_okf_policy.yaml", "policy_version: 1\nfrontmatter:\n  required:\n    remove: [type]\n")
        self.write("unknown/concept.md", "---\ntype: Concept\n---\n")
        self.write("invalid/concept.md", "---\ntype: Concept\n---\n")
        self.write("malformed/concept.md", "---\ntype: Concept\n---\n")
        self.write("weaken/concept.md", "---\ntype: Concept\n---\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertTrue({"POLICY_YAML_INVALID", "POLICY_UNKNOWN_KEY", "POLICY_VALUE_INVALID", "POLICY_BASELINE_TYPE_WEAKENED"}.issubset(findings))

        self.temporary_directory.cleanup()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.bundle = Path(self.temporary_directory.name)
        self.write("nested/_okf_policy.yaml", "policy_version: 1\nfrontmatter:\n  required:\n    add: [title]\n")
        self.write("nested/concept.md", "---\ntype: Concept\n---\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("POLICY_ROOT_MISSING", findings)
        self.assertNotIn("POLICY_REQUIRED_FIELD_MISSING", findings)

    def test_policy_index_version_conflict_and_file_mode_bundle_root(self) -> None:
        self.write("_okf_policy.yaml", "policy_version: 1\nokf_version: '0.2'\nfrontmatter:\n  required:\n    add: [title]\n")
        self.write("index.md", "---\nokf_version: '0.3'\n---\n# Index\n")
        document = self.write("concept.md", "---\ntype: Concept\n---\n")
        code, findings = self.run_validator(str(self.bundle))
        self.assertEqual(code, 1)
        self.assertIn("POLICY_OKF_VERSION_CONFLICT", findings)
        self.assertIn("POLICY_REQUIRED_FIELD_MISSING", findings)
        code, findings = self.run_validator("--bundle-root", str(self.bundle), str(document))
        self.assertEqual(code, 1)
        self.assertIn("POLICY_REQUIRED_FIELD_MISSING", findings)


if __name__ == "__main__":
    unittest.main()
