---
name: tradeoff-analyzer
description: Analyze architectural trade-offs between different technical solutions or patterns. Use when comparing frameworks, libraries, or architectural patterns.
metadata:
  author: Gemini CLI (@architect)
  version: "1.1.0"
  last-updated: "2026-04-06"
  tags: architecture,tradeoff,decision,analysis
---

# Tradeoff Analyzer

Every technical decision involves compromises. Use this skill to evaluate and visualize these choices.

## Core Resources
- **Decision Matrix**: Use [tradeoff-matrix.md](assets/tradeoff-matrix.md) to compare options.

## Workflow

1.  **Define Options**: List the competing solutions (e.g., PostgreSQL vs MongoDB).
2.  **Establish Criteria**: Choose relevant metrics for evaluation (Scalability, DX, Cost, etc.).
3.  **Perform Analysis**: Populate the [tradeoff-matrix.md](assets/tradeoff-matrix.md) with detailed comparisons.
4.  **Integration**: Use the results to populate the "Consequences" section of an ADR.

## Advanced Usage
Leverage `websearch` and `webfetch` to find benchmarks, community trends, and case studies for the options being compared.
