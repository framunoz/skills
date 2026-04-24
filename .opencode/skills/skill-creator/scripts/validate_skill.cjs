#!/usr/bin/env node
// Requires: Node.js 18+, js-yaml
// Usage: node validate_skill.cjs <path-to-skill-directory> [--strict]

const fs = require('fs');
const path = require('path');

// Check for js-yaml
let yaml;
try {
  yaml = require('js-yaml');
} catch (err) {
  console.error('ERROR: js-yaml is required. Install with: npm install js-yaml');
  process.exit(1);
}

function printUsage() {
  console.error('Usage: node validate_skill.cjs <path-to-skill-directory> [--strict]');
  console.error('');
  console.error('Arguments:');
  console.error('  path-to-skill-directory  Path to the skill directory to validate');
  console.error('  --strict                 Treat warnings as errors');
  process.exit(1);
}

function findFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      findFiles(fullPath, files);
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

function scanForTodos(skillDir) {
  const warnings = [];
  const files = findFiles(skillDir);
  const todoRegex = /TODO:/i;

  for (const filePath of files) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (todoRegex.test(lines[i])) {
        const relPath = path.relative(skillDir, filePath);
        warnings.push(`TODO marker found in ${relPath}:${i + 1}`);
      }
    }
  }

  return warnings;
}

function validateSkill(skillDir, strictMode) {
  const errors = [];
  const warnings = [];

  // VR-001: SKILL.md must exist
  const skillMdPath = path.join(skillDir, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) {
    errors.push('SKILL.md not found in the skill directory.');
    return { status: 'invalid', errors, warnings, exitCode: 1 };
  }

  const content = fs.readFileSync(skillMdPath, 'utf8');

  // VR-002: Frontmatter delimiters present
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    errors.push('SKILL.md does not start with YAML frontmatter delimited by ---');
    return { status: 'invalid', errors, warnings, exitCode: 1 };
  }

  const frontmatterYaml = frontmatterMatch[1];

  // VR-003: Frontmatter parseable by js-yaml
  let frontmatter;
  try {
    frontmatter = yaml.load(frontmatterYaml);
  } catch (err) {
    errors.push(`Frontmatter YAML parse error: ${err.message}`);
    return { status: 'invalid', errors, warnings, exitCode: 1 };
  }

  if (!frontmatter || typeof frontmatter !== 'object') {
    errors.push('Frontmatter must be a YAML mapping/object.');
    return { status: 'invalid', errors, warnings, exitCode: 1 };
  }

  // VR-004: name validation
  const dirName = path.basename(skillDir);
  if (!frontmatter.name) {
    errors.push('Frontmatter field "name" is required.');
  } else {
    const nameRegex = /^[a-z0-9]+(-[a-z0-9]+)*$/;
    if (!nameRegex.test(frontmatter.name)) {
      errors.push(`Field "name" must match regex ^[a-z0-9]+(-[a-z0-9]+)*$. Got: "${frontmatter.name}"`);
    } else if (frontmatter.name.length > 64) {
      errors.push(`Field "name" must be 1-64 characters. Got: ${frontmatter.name.length}`);
    }
    if (frontmatter.name !== dirName) {
      errors.push(`Field "name" (${frontmatter.name}) must match directory name (${dirName}).`);
    }
  }

  // VR-005: description validation
  if (!frontmatter.description) {
    errors.push('Frontmatter field "description" is required.');
  } else {
    if (typeof frontmatter.description !== 'string') {
      errors.push('Field "description" must be a string.');
    } else {
      if (frontmatter.description.length < 1 || frontmatter.description.length > 1024) {
        errors.push(`Field "description" must be 1-1024 characters. Got: ${frontmatter.description.length}`);
      }
      if (frontmatter.description.includes('\n')) {
        errors.push('Field "description" must be a single-line string (no newlines).');
      }
    }
  }

  // VR-006: license validation
  if (frontmatter.license !== undefined) {
    if (typeof frontmatter.license !== 'string' || frontmatter.license.length === 0) {
      errors.push('Field "license" if present must be a non-empty string.');
    }
  }

  // VR-007: compatibility validation
  if (frontmatter.compatibility !== undefined) {
    if (typeof frontmatter.compatibility !== 'string') {
      errors.push('Field "compatibility" must be a string.');
    } else if (frontmatter.compatibility.length < 1 || frontmatter.compatibility.length > 500) {
      errors.push(`Field "compatibility" must be 1-500 characters. Got: ${frontmatter.compatibility.length}`);
    }
  }

  // VR-008: metadata validation
  if (frontmatter.metadata !== undefined) {
    if (typeof frontmatter.metadata !== 'object' || frontmatter.metadata === null || Array.isArray(frontmatter.metadata)) {
      errors.push('Field "metadata" must be a mapping/object.');
    } else {
      for (const [key, value] of Object.entries(frontmatter.metadata)) {
        if (typeof key !== 'string') {
          errors.push(`Metadata key "${key}" must be a string.`);
        }
        if (typeof value !== 'string') {
          errors.push(`Metadata value for "${key}" must be a string. Got: ${typeof value}`);
        }
      }
    }
  }

  // VR-009: TODO markers
  const todoWarnings = scanForTodos(skillDir);
  warnings.push(...todoWarnings);

  // Determine status
  if (errors.length > 0) {
    return { status: 'invalid', errors, warnings, exitCode: 1 };
  }

  if (warnings.length > 0 && strictMode) {
    return { status: 'invalid', errors, warnings, exitCode: 1 };
  }

  if (warnings.length > 0) {
    return { status: 'valid_with_warnings', errors, warnings, exitCode: 0 };
  }

  return { status: 'valid', errors, warnings, exitCode: 0 };
}

function printReport(report, skillName) {
  console.log(`Skill: ${skillName}`);
  console.log(`Status: ${report.status}`);
  console.log('');

  if (report.errors.length > 0) {
    console.log('Errors:');
    for (const err of report.errors) {
      console.log(`  - ${err}`);
    }
    console.log('');
  }

  if (report.warnings.length > 0) {
    console.log('Warnings:');
    for (const warn of report.warnings) {
      console.log(`  - ${warn}`);
    }
    console.log('');
  }
}

function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    printUsage();
  }

  const skillDir = path.resolve(args[0]);
  const strictMode = args.includes('--strict');

  if (!fs.existsSync(skillDir)) {
    console.error(`ERROR: Directory does not exist: ${skillDir}`);
    process.exit(1);
  }

  const dirName = path.basename(skillDir);
  const report = validateSkill(skillDir, strictMode);

  printReport(report, dirName);
  process.exit(report.exitCode);
}

main();
