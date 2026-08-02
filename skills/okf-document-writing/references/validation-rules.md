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

`index.md` and `log.md` are optional reserved files and may appear at any hierarchy level. Unknown extension keys are preserved by the Pydantic models and are outside this validator's checks.
