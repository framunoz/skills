# Quarto Publishing and Deployment

Publishing moves rendered Quarto output to a remote service or deployment target.

## Table of Contents

- [Pre-Publish Checks](#pre-publish-checks)
- [Authorization and Credentials](#authorization-and-credentials)
- [Deployment Workflow](#deployment-workflow)
- [Verification and Rollback](#verification-and-rollback)

## Pre-Publish Checks

Inspect the project type, selected profile, output directory, existing provider
configuration, and repository deployment conventions. Confirm the intended
format and whether rendering executes code. Use [project configuration](project-configuration.md)
and [CLI troubleshooting](cli-troubleshooting.md) first.

## Authorization and Credentials

Always obtain explicit authorization before publishing, deploying, or invoking a
provider CLI. Explain the target, files, network operation, authentication, and
visibility impact. Never expose, add, rotate, or commit credentials without a
specific request and an established secure workflow.

## Deployment Workflow

Use the repository's existing provider and command rather than inventing a new
host. Render only when authorized, review generated output and changed files,
then publish the intended output directory. Do not assume a provider integration
or CLI capability without checking the installed tooling and project setup.

## Verification and Rollback

Report the target, profile, format, command, generated output, and publish
result. Check the published URL only when authorized. Preserve the documented
rollback route; if none exists, report that risk before publishing.
