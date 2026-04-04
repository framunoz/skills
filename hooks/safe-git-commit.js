#!/usr/bin/env node
/**
 * @hook safe-git-commit
 * @event PreToolUse
 * @matcher Bash
 * @description Automatically escapes backticks (`) in git commit -m commands
 *              to prevent accidental shell execution or errors.
 *              Robustly handles already escaped characters and single quotes.
 * @dependencies Node.js, fs
 * @performance Low - Simple string replacement.
 */
const fs = require('fs');
const logger = require('./utils/logger');

let output = { decision: "allow" };

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('safe-git-commit', input);

    const tool = input.tool_name;
    const args = input.tool_input || {};

    if (tool !== 'Bash' || !args.command) {
        throw new Error('Skip: Not a shell command');
    }

    const command = args.command.trim();

    // Supports -m, -am, --message, --message=, etc.
    // Added /s flag to handle multiline commands robustly.
    const isGitCommit = /\bgit\s+commit\b.*\s+(-[a-zA-Z]*m|--message)(=|\s*)/s.test(command);

    if (!isGitCommit) {
        throw new Error('Skip: Not a git commit command');
    }

    logger.debug(`Original command: ${command}`);

    // Robust approach: match escaped chars or backticks
    // We remove the '[^']*' skip because it fails with apostrophes inside double quotes
    // and backticks should generally be escaped in git commits to be safe in shell.
    // 1. \\. matches any escaped character (handles \\` correctly)
    // 2. ` matches unescaped backticks and we replace them
    let modified = false;
    const newCommand = command.replace(/\\.|`/g, (match) => {
        if (match === '`') {
            modified = true;
            return '\\`';
        }
        return match;
    });

    if (!modified) {
        throw new Error('Skip: No backticks to escape');
    }

    logger.info(`🛡️ Escaped backticks in git commit message.`);
    logger.debug(`New command: ${newCommand}`);
    
    output = {
        tool_input: {
            command: newCommand
        },
    };
} catch (e) {
    if (!e.message.startsWith('Skip:')) {
        logger.error(`Error in hook: ${e.message}`);
    }
}

logger.finish(output);

// Output decision to stdout and exit explicitly
process.stdout.write(JSON.stringify(output) + '\n');
process.exit(0);
