---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
license: MIT
compatibility: OpenCode
metadata:
  author: Matt Pocock (@mattpocock)
  co-author: Francisco Muñoz (@framunoz)
  source: https://github.com/mattpocock/skills
  version: "1.1.0"
  last-updated: "2026-04-05"
  tags: prd,product-requirements,feature-planning,github-issue
---

This skill will be invoked when the user wants to create a PRD. You may skip steps if you don't consider them necessary.

## Step 1 — Problem Description

Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions. Use the `question` tool to gather this information.

## Step 2 — Codebase Exploration

Explore the repo to verify their assertions and understand the current state of the codebase.

- If the `task` tool is available, delegate to an `explore` subagent
- Alternatively, use `glob`, `grep`, and `read` directly
- Run multiple lookups in parallel in a single message

## Step 3 — Deep Interview

Interview the user relentlessly about every aspect of this plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

You may use the `grill-me` skill to conduct a thorough structured interview. Load it with: `skill("grill-me")`

## Step 4 — Module Design

Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A **deep module** (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

## Step 5 — Write PRD

Once you have a complete understanding of the problem and solution, use the PRD template at `assets/prd-template.md` to write the PRD.

To load the template, read `opencode/skills/write-a-prd/assets/prd-template.md` or copy its content and fill in each section.

## Step 6 — Submit as GitHub Issue

Ask the user if they want to submit the PRD as a GitHub issue. If yes, use the `bash` tool to create the issue via `gh`:

```bash
gh issue create --title "PRD: [Feature Name]" --body "$(cat path/to/prd.md)"
```

Or use the `question` tool to ask how they want to proceed.