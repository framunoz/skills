# ADR Guidelines

Architecture Decision Records (ADRs) are short text files that capture a significant architectural decision and its context.

## When to Document
- **Library/Framework Selection**: Choosing a core library (e.g., "Use FastAPI for our REST API").
- **Directory Structure Changes**: Significant refactors of how code is organized.
- **Pattern Selection**: Deciding on architectural patterns (e.g., "Use a Hexagonal Architecture").
- **External Dependencies**: Decisions about databases, message brokers, or external APIs.
- **Irreversible Choices**: Any decision that would be expensive to change later.

## Status Definitions
- **Proposed**: The decision is still under discussion.
- **Accepted**: The decision has been agreed upon and is being implemented.
- **Rejected**: The proposed decision was not accepted.
- **Deprecated**: The decision is no longer valid but remains for historical context.
- **Superseded**: A new ADR has replaced this one. Reference the new ADR.

## Writing Style
- **Concise**: Keep it to 1-2 pages of Markdown.
- **Objective**: Explain *why* the decision was made, including the downsides.
- **Self-contained**: Anyone reading it later should understand the context without needing to search Slack or emails.
