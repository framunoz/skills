#!/usr/bin/env node
/**
 * @hook py-format-silent
 * @event PostToolUse
 * @matcher (Write|Edit)
 * @description Automatically formats modified Python files using black.
 *              Maintains session-specific JSON state for the Quality Gate phase.
 *              Ruff linting is deferred to the Stop hook (py-quality-gate).
 * @dependencies Node.js, uv (black), fs, path, child_process
 * @performance Medium - Spawns shell commands; uses a 10s timeout to
 *              prevent hanging.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const logger = require('./utils/logger');
const stateManager = require('./utils/state-manager');

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('py-format-silent', input);

    const filePath = input.tool_input?.file_path;
    const sessionId = input.session_id;

    // Standard exclusion rules
    const excludes = ['.venv', 'venv', '__pycache__', '.git', 'node_modules', 'dist', 'build'];

    if (
        filePath
        && filePath.endsWith('.py')
        && !filePath.split(path.sep).some(p => excludes.includes(p))
    ) {
        logger.info(`Formatting ${filePath}...`);

        const runFormatter = (cmd) => {
            try {
                execSync(cmd, { stdio: 'pipe', timeout: 10000 });
            } catch (error) {
                const stdout = error.stdout ? error.stdout.toString().trim() : '';
                const stderr = error.stderr ? error.stderr.toString().trim() : '';
                let details = error.message;
                if (stderr) details += `\nSTDERR: ${stderr}`;
                if (stdout) details += `\nSTDOUT: ${stdout}`;
                throw new Error(details);
            }
        };

        try {
            runFormatter(`uvx black "${filePath}"`);
            logger.info(`Successfully formatted ${filePath}`);
        } catch (error) {
            logger.error(`Formatting tools failed: ${error.message}`);
        }

        // Update session-specific state
        const state = stateManager.loadState(sessionId);
        if (!state.files.includes(filePath)) {
            state.files.push(filePath);
        }
        stateManager.saveState(sessionId, state);
        logger.debug(`Logged touched file to state_${sessionId || 'default'}.json`);
    }
} catch (e) {
    logger.error(`Error in hook logic: ${e.message}`);
}

const output = {};
logger.finish(output);
console.log(JSON.stringify(output));
