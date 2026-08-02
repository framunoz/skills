# Validator Rule Reference

Run the standalone validator with `uv run --with pydantic --with pyyaml scripts/validate_okf.py <file-or-bundle>`. It safely loads YAML with PyYAML and validates standardized concept metadata with Pydantic v2 while preserving unknown producer extension keys. It is read-only and does not prove truth, source reliability, publication, computation execution, or full Markdown conformance.

Relative links are supported by OKF but intentionally ignored by this narrow validator. Root-relative link checks remove query/fragment suffixes and ignore fenced and inline code, but are not full Markdown parsing.

| Rule code | Severity | Requirement or limitation |
| --- | --- | --- |
| `PATH_NOT_FOUND`, `TARGET_NOT_MARKDOWN`, `BUNDLE_ROOT_INVALID`, `FILE_UNREADABLE` | ERROR | The target and optional bundle root must be usable. |
| `FRONTMATTER_OPENING`, `FRONTMATTER_CLOSING`, `YAML_INVALID`, `YAML_NOT_MAPPING` | ERROR | A concept needs delimited, mapping YAML frontmatter. |
| `TYPE_MISSING` | ERROR | A non-reserved concept requires nonempty string `type`; no other field is universally required. |
| `SOURCES_NOT_LIST`, `SOURCE_NOT_MAPPING`, `SOURCE_RESOURCE_MISSING` | ERROR | Present `sources` must be a list of mappings; every mapping requires a usable `resource`, not necessarily a URL. |
| `GENERATED_NOT_MAPPING`, `GENERATED_BY_MISSING`, `GENERATED_AT_INVALID` | ERROR | Present `generated` must be a mapping with `by`; optional `at` must be a parseable ISO 8601 datetime when supplied. |
| `VERIFIED_EVENT_INVALID`, `VERIFIED_EVENT_MISSING_FIELDS` | ERROR | Each present `verified` event needs mapping fields `by` and parseable `at`. |
| `STATUS_INVALID`, `STALE_AFTER_INVALID` | ERROR | `status` must be `draft`, `stable`, or `deprecated`; `stale_after` must be a parseable ISO date. |
| `RUNTIME_MISSING`, `RUNTIME_INVALID` | ERROR | An Attested Computation requires nonempty string `runtime`. |
| `COMPUTATION_MISSING`, `COMPUTATION_INVALID` | ERROR | An Attested Computation needs a nonempty `computation` path or level-1 `# Computation` heading. |
| `INDEX_FRONTMATTER_NOT_ALLOWED`, `INDEX_FRONTMATTER_KEY` | ERROR | Only a bundle-root `index.md` may have frontmatter, and it may declare only `okf_version`. |
| `LOG_DATE_INVALID`, `LOG_DATES_NOT_NEWEST_FIRST` | ERROR | `log.md` date headings must use `YYYY-MM-DD` and descend newest first. |
| `SOURCE_FOOTNOTE_UNMATCHED` | WARNING | A checked body footnote has no matching `sources[].id`. |
| `ROOT_LINK_CHECK_SKIPPED`, `LINK_TARGET_UNAVAILABLE` | WARNING | Root links cannot be resolved in file mode without `--bundle-root`, or have no available bundle target. Broken links are not conformance errors. |
| `POLICY_ROOT_MISSING`, `POLICY_YAML_INVALID`, `POLICY_NOT_MAPPING`, `POLICY_VERSION_UNSUPPORTED`, `POLICY_OKF_VERSION_UNSUPPORTED`, `POLICY_OKF_VERSION_CONFLICT`, `POLICY_UNKNOWN_KEY`, `POLICY_SCOPE_INVALID`, `POLICY_VALUE_INVALID`, `POLICY_FIELD_CONFLICT`, `POLICY_BASELINE_TYPE_WEAKENED`, `POLICY_REQUIRED_FILE_MISSING`, `POLICY_REQUIRED_FIELD_MISSING` | ERROR | A local policy is invalid, conflicts with the root index version, or adds an unmet local requirement. These are local validator findings, not OKF conformance requirements. |
| `POLICY_SUGGESTED_FIELD_MISSING` | WARNING | A local policy suggests a non-null frontmatter field. It does not make validation invalid. |

`index.md` and `log.md` are optional reserved files and may appear at any hierarchy level. Unknown extension keys are preserved by the Pydantic models and are outside this validator's checks.

## Local `_okf_policy.yaml` overlays

`_okf_policy.yaml` is validator configuration, not an OKF file or Markdown link target. It is discovered only during bundle validation: from the bundle root through the ancestors of each concept document. In single-file mode, it is considered only when `--bundle-root <directory>` is supplied. With no root policy, baseline validation is unchanged; a nested policy without a root policy produces `POLICY_ROOT_MISSING` and does not apply.

The bundle-root policy must declare `policy_version: 1` and exactly `okf_version: "0.2"`; copy the ready-to-use [`_okf_policy.yaml` template](../templates/_okf_policy.yaml) to start one. Nested policies must declare `policy_version: 1` and must omit `okf_version`. Every policy is strict: its only other top-level keys are `reserved` and `frontmatter`; unknown keys, malformed YAML, invalid shapes, and invalid values reject the complete policy rather than applying part of it. If root `index.md` uses its permitted `okf_version` frontmatter, it must be `"0.2"`.

```yaml
policy_version: 1
okf_version: "0.2"
reserved:
  index.md: optional
  log.md: optional
frontmatter:
  required:
    add: []
    remove: []
  suggested:
    add: []
    remove: []
```

All sections after the required root version fields are optional. `reserved` accepts only `required` or `optional`. Reserved settings merge root-to-leaf per filename, with the nearest explicit value winning. The validator checks the resulting requirements in every directory that contains Markdown: inherited `required` settings apply to descendants, and a nested `optional` setting relaxes that filename for its directory and descendants.

Frontmatter policies merge root to leaf as a stateful set. The baseline required set is `{type}` and the baseline suggested set is empty. `required.add` promotes a field; `suggested.add` demotes it; each removes the field from the other set. `required.remove` and `suggested.remove` remove fields from their respective sets. A field may appear in only one operation in a policy. `type` cannot be removed or demoted, although adding it to `required` is harmless. Policies check only that a concept's top-level field exists and is non-null; they do not impose field types or values. Required misses are errors, suggested misses are warnings, and neither applies to `index.md` or `log.md`.
