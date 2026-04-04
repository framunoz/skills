#!/usr/bin/env node
/**
 * @hook py-format-silent
 * @event AfterTool
 * @matcher (write_file|replace)
 * @description Automatically formats modified Python files using black
 *              and ruff. 
 * @dependencies Node.js, uv (black, ruff), fs, path, child_process
 * @performance Medium - Spawns shell commands; uses a 10s timeout to
 *              prevent hanging.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const logger = require('./utils/logger');

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('py-format-silent', input);

    const filePath = input.tool_input?.file_path;

    // Standard exclusion rules
    const excludes = ['.venv', 'venv', '__pycache__', '.git', 'node_modules', 'dist', 'build'];

    if (filePath && filePath.endsWith('.py') && !filePath.split(path.sep).some(p => excludes.includes(p))) {
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
            runFormatter(`uvx ruff check --fix "${filePath}"`);
            logger.info(`Successfully formatted ${filePath}`);
        } catch (error) {
            logger.error(`Formatting tools failed: ${error.message}`);
        }
    }
} catch (e) {
    logger.error(`Error in hook logic: ${e.message}`);
}

const output = { decision: 'allow', suppressOutput: true };
logger.finish(output);
console.log(JSON.stringify(output));
