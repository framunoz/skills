# Fixtures

Run from the skill root:

```bash
python3 -m unittest discover -s tests            # fast: scripts, pointers, fences
QUARTO_RENDER_TESTS=1 python3 -m unittest discover -s tests   # + renders fixtures (~15 s)
```

Small Quarto sources exercised by `tests/`. Unlike plain examples, they are rendered by
`tests/test_render_fixtures.py` (opt-in: `QUARTO_RENDER_TESTS=1`) into a temporary copy, so the
repository never receives generated output.

| Fixture | Proves |
|---|---|
| `cross-references/` | every crossref type (incl. custom float, listing, subfigures) resolves without warnings |
| `profile-freeze-execute-dir/` | `execute-dir: project` under `project:` runs code from the root (R) |
| `revealjs/` | `.incremental`, inline `[…]{.fragment}`, pause, notes, vertical navigation |
| `formats/` | one source to html + docx + typst, list table, conditional content |
| `citations/` | local bibliography resolves |
| `configuration/` | preflight sees profiles and `_metadata.yml` (not rendered) |
