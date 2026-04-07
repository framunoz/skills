---
name: tradeoff-analyzer
description:
  Analyze architectural trade-offs between different technical solutions
  or patterns. Use when comparing frameworks, libraries, or architectural patterns.
compatibility: Gemini CLI
metadata:
  author: Francisco Muñoz (@framunoz)
  source: https://github.com/framunoz/skills/blob/main/gemini/skills/tradeoff-analyzer/
  version: 1.1.2
  last-updated: "2026-04-06"
  tags: analysis, architecture, decision, decision-making, design-patterns, tradeoff
  related-with:
    skills:
      - adr-manager
      - effective-functions
      - oop-designer
      - system-modeler
    agents:
      - architect
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
