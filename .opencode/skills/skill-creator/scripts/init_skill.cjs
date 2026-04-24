#!/usr/bin/env node
// Requires: Node.js 18+, js-yaml
// Usage: node init_skill.cjs <skill-name> --path <output-directory>

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
  console.error('Usage: node init_skill.cjs <skill-name> --path <output-directory>');
  console.error('');
  console.error('Arguments:');
  console.error('  skill-name          Skill identifier (regex: ^[a-z0-9]+(-[a-z0-9]+)*$)');
  console.error('  --path <directory>  Parent directory where the skill folder will be created');
  process.exit(1);
}

function main() {
  const args = process.argv.slice(2);

  if (args.length < 3) {
    printUsage();
  }

  const skillName = args[0];
  const pathIndex = args.indexOf('--path');

  if (pathIndex === -1 || pathIndex + 1 >= args.length) {
    console.error('ERROR: --path argument is required.');
    printUsage();
  }

  const outputDir = args[pathIndex + 1];

  // Validate skill name
  const nameRegex = /^[a-z0-9]+(-[a-z0-9]+)*$/;
  if (!nameRegex.test(skillName) || skillName.length < 1 || skillName.length > 64) {
    console.error('ERROR: Skill name must match ^[a-z0-9]+(-[a-z0-9]+)*$ and be 1-64 characters.');
    process.exit(1);
  }

  const skillDir = path.resolve(outputDir, skillName);

  // Check if directory already exists
  if (fs.existsSync(skillDir)) {
    console.error(`ERROR: Directory ${skillDir} already exists. Choose a different name or remove the existing directory.`);
    process.exit(1);
  }

  // Create directory structure
  const dirs = [
    skillDir,
    path.join(skillDir, 'scripts'),
    path.join(skillDir, 'references'),
    path.join(skillDir, 'assets'),
  ];

  for (const dir of dirs) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const today = new Date().toISOString().split('T')[0];

  // Generate SKILL.md from template
  const skillMd = `---
name: ${skillName}
description: "TODO: Describe what this skill does and when to use it. Include trigger keywords."
license: MIT
compatibility: Designed for OpenCode
metadata:
  author: TODO
  original-author: TODO
  source: TODO
  version: "0.1.0"
  last-updated: "${today}"
  status: active
  replaced-by: "null"
---

# Context & Goal

TODO: Explain why this skill exists and what it aims to achieve.

# Step-by-Step Procedure

TODO: Provide clear, sequential instructions on how the agent should execute the task.

## Step 1: TODO

1. TODO: First action
2. TODO: Second action

## Step 2: TODO

1. TODO: Next action

# Usage of Resources

TODO: If this skill includes scripts, references, or assets, explicitly tell the agent how and when to use them.

- \`scripts/example_script.cjs\`: TODO describe when to run it
- \`references/REFERENCE.md\`: TODO describe when to read it
- \`assets/example_asset.txt\`: TODO describe when to use it

# Constraints & Rules

- TODO: List what the agent MUST NOT do
- TODO: List edge cases to handle
- TODO: List assumptions or prerequisites

# Expected Output

TODO: Define how the agent should conclude the task and present results to the user.
`;

  fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillMd, 'utf8');

  // Generate CHANGELOG.md
  const changelog = `# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - ${today}

### Added

- Initial release of ${skillName}
`;

  fs.writeFileSync(path.join(skillDir, 'CHANGELOG.md'), changelog, 'utf8');

  // Create example files
  fs.writeFileSync(
    path.join(skillDir, 'scripts', 'example_script.cjs'),
    '#!/usr/bin/env node\n// TODO: Replace with your script\nconsole.log("Hello from ' + skillName + '");\n',
    'utf8'
  );

  fs.writeFileSync(
    path.join(skillDir, 'references', 'example_reference.md'),
    '# Reference\n\nTODO: Add reference documentation here.\n',
    'utf8'
  );

  fs.writeFileSync(
    path.join(skillDir, 'assets', 'example_asset.txt'),
    'TODO: Replace with your asset file.\n',
    'utf8'
  );

  console.log(`Success: Created skill '${skillName}' at ${skillDir}`);
  console.log('');
  console.log('Next steps:');
  console.log('  1. Edit SKILL.md to replace TODO markers with real content');
  console.log('  2. Add scripts, references, and assets as needed');
  console.log(`  3. Run: node .opencode/skills/skill-creator/scripts/validate_skill.cjs ${skillDir}`);
  process.exit(0);
}

main();
