---
name: tradeoff-analyzer
description: Analyze architectural trade-offs between different technical solutions or patterns. Use this to compare Framework A vs Framework B or Pattern X vs Pattern Y.
metadata:
  author: Gemini CLI (@architect)
  version: "1.0.0"
  last-updated: "2026-04-06"
  tags: architecture,tradeoff,decision,analysis
---

# Tradeoff Analyzer

Every technical decision is a compromise. This skill helps you visualize and evaluate those compromises.

## Workflow

1.  **Define the Options**: List the competing solutions (e.g., "PostgreSQL" vs "MongoDB").
2.  **Establish Criteria**: Determine the key metrics for evaluation:
    - **Scalability**: Can it handle 10x or 100x current load?
    - **Developer Experience (DX)**: Is it easy to use, learn, and debug?
    - **Maintainability**: What is the long-term support and community size?
    - **Cost**: Infrastructure costs, licensing, and engineer time.
    - **Security**: What new attack vectors are introduced?
3.  **Perform the Analysis**: Create a comparison matrix in Markdown.

```markdown
### Decision Matrix: [Topic]

| Criteria | [Option A] | [Option B] |
|---|---|---|
| **Scalability** | ✅ / 🟡 / 🔴 [Comment] | ✅ / 🟡 / 🔴 [Comment] |
| **DX** | ✅ / 🟡 / 🔴 [Comment] | ✅ / 🟡 / 🔴 [Comment] |
| **Maintainability** | ✅ / 🟡 / 🔴 [Comment] | ✅ / 🟡 / 🔴 [Comment] |
| **Cost** | ✅ / 🟡 / 🔴 [Comment] | ✅ / 🟡 / 🔴 [Comment] |
| **Security** | ✅ / 🟡 / 🔴 [Comment] | ✅ / 🟡 / 🔴 [Comment] |

**Recommendation**: [Recommended option based on weighted criteria.]
**Risk Statement**: [What we are giving up by choosing this.]
```

4.  **Integrate with ADR**: The output of this skill often becomes the "Consequences" section of an ADR.

## Advanced Usage
If you have access to `websearch` and `webfetch`, use them to find:
- Real-world case studies of migrations between these options.
- Known performance benchmarks (e.g., TechEmpower Framework Benchmarks).
- Community trends (GitHub stars, NPM downloads, StackOverflow questions).
