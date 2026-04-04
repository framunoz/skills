#!/usr/bin/env node
/**
 * @hook py-format-silent
 * @event PostToolUse
 * @matcher (Write|Edit)
 * @description Automatically formats modified Python files using black.
 * @dependencies Node.js, uv (black), fs, path, child_process
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

    if (
        filePath
        && filePath.endsWith('.py')
        && !filePath.split(path.sep).some(p => excludes.includes(p))
    ) {
        logger.info(`🎨 Formatting ${filePath}...`);

        function runSafeUvTool(tool, args, options) {
            let stdout = "";
            let stderr = "";
            let success = false;
            let error = null;

            try {
                stdout = execSync(`uv run ${tool} ${args}`, options).toString();
                success = true;
            } catch (err) {
                const errStderr = err.stderr ? err.stderr.toString() : '';
                if (err.code === 'ENOENT' || errStderr.includes(`Failed to spawn:`)) {
                    logger.info(`⚠️ '${tool}' not found in local environment. Falling back to 'uvx ${tool}'...`);
                    try {
                        stdout = execSync(`uvx ${tool} ${args}`, options).toString();
                        success = true;
                    } catch (fallbackErr) {
                        error = fallbackErr;
                        stdout = fallbackErr.stdout ? fallbackErr.stdout.toString() : '';
                        stderr = fallbackErr.stderr ? fallbackErr.stderr.toString() : '';
                    }
                } else {
                    error = err;
                    stdout = err.stdout ? err.stdout.toString() : '';
                    stderr = err.stderr ? err.stderr.toString() : '';
                }
            }

            return { success, stdout, stderr, error };
        }

        const options = { stdio: 'pipe', timeout: 10000 };
        
        const blackResult = runSafeUvTool('black', `"${filePath}"`, options);
        if (!blackResult.success) {
            let details = blackResult.error ? blackResult.error.message : 'Unknown error';
            if (blackResult.stderr) details += `\nSTDERR: ${blackResult.stderr}`;
            if (blackResult.stdout) details += `\nSTDOUT: ${blackResult.stdout}`;
            logger.error(`❌ Formatting failed: ${details}`);
        } else {
            logger.info(`✅ Successfully formatted ${filePath}`);
        }
    }
} catch (e) {
    logger.error(`Error in hook logic: ${e.message}`);
}

const output = {};
logger.finish(output);
console.log(JSON.stringify(output));
