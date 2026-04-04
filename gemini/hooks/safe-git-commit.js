#!/usr/bin/env node
/**
 * @hook safe-git-commit
 * @event BeforeTool
 * @matcher run_shell_command
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

    if (tool !== 'run_shell_command' || !args.command) {
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
    
    // According to Gemini CLI docs, tool mutation is done by returning a payload 
    // with tool_input at the root. We also include decision: allow for clarity.
    output = {
        decision: "allow",
        tool_input: {
            command: newCommand
        },
        systemMessage: "📝 Backticks in commit message were automatically escaped for safety."
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
