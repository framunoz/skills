#!/usr/bin/env node
/**
 * @hook block-env-read
 * @event PreToolUse
 * @matcher (Read|Bash)
 * @description Security hook to prevent the agent from reading
 *              sensitive .env files. Allows access to files containing
 *              'example' in the path/name.
 * @dependencies Node.js, fs, path
 * @performance Low - Synchronous file name check, minimal overhead.
 */
const fs = require('fs');
const logger = require('./utils/logger');

let output = {};

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('block-env-read', input);

    const tool = input.tool_name;
    const args = input.tool_input || {};

    let target = "";

    if (tool === 'Read') {
        target = args.file_path || "";
    } else if (tool === 'Bash') {
        target = args.command || "";
    }

    if (target) {
        // Block if it contains '.env' but NOT 'example' (case-insensitive)
        const hasEnv = target.toLowerCase().includes('.env');
        const hasExample = target.toLowerCase().includes('example');

        if (hasEnv && !hasExample) {
            logger.warn(`🔒 Blocking access to: ${target}`);
            output = {
                decision: "block",
                reason: "🔒 Security Policy: Reading .env files is blocked to prevent secret exposure. If you need configuration values, please ask the user directly.",
            };
        }
    }
} catch (e) {
    logger.error(`Error in hook: ${e.message}`);
}

logger.finish(output);

// Output decision to stdout
console.log(JSON.stringify(output));
