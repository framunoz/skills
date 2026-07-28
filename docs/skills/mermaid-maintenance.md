# Mermaid Skill Maintenance

Maintenance guide for the runtime Mermaid skill at [`skills/mermaid/SKILL.md`](../../skills/mermaid/SKILL.md). Runtime authoring and routing instructions remain in that skill and its references.

## Metadata ownership

`skills/mermaid/SKILL.md` owns these front-matter fields:

- `mermaid_baseline`: the Mermaid version against which supported guidance was validated, or an explicitly documented compatibility target.
- `last_verified`: the date that baseline or compatibility review was completed.

Update both fields when a Mermaid release, renderer compatibility change, or syntax/support change affects the registered guidance. Keep general validation, security, and accessibility rules in `SKILL.md`; retain type-specific minimum versions and beta or experimental constraints in the relevant focused reference.

## Update process

1. Identify affected registered types in the [coverage tracker](../../skills/mermaid/references/diagram-types.md) and review their focused references.
2. Update only documented, supported syntax and preserve existing runtime routing guidance unless the information structure changes.
3. Revise compatibility constraints, examples, and official-documentation links where needed.
4. Validate and report the change before publishing, then update `mermaid_baseline` and `last_verified`.

## Registering a diagram type

1. Create one focused reference under `skills/mermaid/references/` that covers when to use and not use the type, declaration, supported syntax, quality rules, pitfalls, compatibility, validated examples, and official documentation.
2. Add a router row in [`references/router.md`](../../skills/mermaid/references/router.md) describing the type's information structure and linking to the new reference.
3. Mark the type as supported in the [coverage tracker](../../skills/mermaid/references/diagram-types.md). Do not modify `SKILL.md` merely to register a type; it remains the stable runtime entry point.

## Required validation and reporting

Follow the validation protocol in [`SKILL.md`](../../skills/mermaid/SKILL.md#validation-and-compatibility). Before publishing, record:

- Validation status: `passed`, `failed`, or `rendering unverified`.
- Target host/renderer and Mermaid version, when known.
- Exact renderer command, renderer version, input source, and output or error when renderer tooling is available.
- When rendering is unavailable: source-review evidence, unavailable tooling, assumed or unknown target version, and type-specific compatibility risks.
- Warnings for beta, experimental, or version-gated syntax.

Do not install a renderer or invent a command solely for validation. Do not treat source review as a successful render.
