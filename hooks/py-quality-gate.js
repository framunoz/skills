#!/usr/bin/env node
/**
 * @hook py-quality-gate
 * @event Stop
 * @description Global quality enforcement hook. Runs Ruff linting and
 *              Pyrefly typing checks only if Python files were modified.
 *              Blocks agent stop if errors found (with 3 auto-retries).
 * @dependencies Node.js, uv (ruff, pyrefly), fs, path, child_process
 * @performance High - Runs global diagnostics; only executes if files touched.
 */
const fs = require('fs');
const { execSync } = require('child_process');
const logger = require('./utils/logger');
const stateManager = require('./utils/state-manager');

let output = {};

try {
    const input = JSON.parse(fs.readFileSync(0, 'utf-8'));
    logger.init('py-quality-gate', input);

    const sessionId = input.session_id;

    // --- Periodic Cleanup (24 hours) ---
    stateManager.cleanupStaleStates();

    const stateFile = stateManager.getStatePath(sessionId);
    logger.debug(`Checking state at: ${stateFile}`);

    if (!fs.existsSync(stateFile)) {
        logger.info("No files touched, allowing completion.");
    } else {
        const state = stateManager.loadState(sessionId);
        logger.info(`Starting global diagnostics (Retry ${state.retryCount + 1}/3)...`);

        const errorReport = runDiagnostics();

        if (errorReport.trim().length > 0) {
            output = handleFailure(sessionId, state, errorReport);
        } else {
            output = handleSuccess(sessionId);
        }
    }
} catch (e) {
    logger.error(`Error in hook logic: ${e.message}`);
    output = {}; // Fail-open
}

logger.finish(output);
console.log(JSON.stringify(output));

/**
 * Runs Ruff and Pyrefly diagnostics and returns a combined error report.
 */
function runDiagnostics() {
    let report = "";
    const options = { stdio: 'pipe', timeout: 30000 };

    // --- Ruff Check ---
    try {
        logger.info("Running Ruff checks...");
        execSync(`uvx ruff check --fix .`, options);
    } catch (error) {
        const stdout = error.stdout?.toString() || "";
        const stderr = error.stderr?.toString() || "";
        const hasRealErrors = (stdout && !stdout.includes("No Python files found")) || stderr;

        if (hasRealErrors) {
            report += `\n## Linting Errors (Ruff):\n`;
            if (stdout) report += `STDOUT:\n${stdout}\n`;
            if (stderr) report += `STDERR:\n${stderr}\n`;
        }
    }

    // --- Pyrefly Check ---
    try {
        logger.info("Running Pyrefly checks...");
        execSync(`uvx pyrefly check .`, options);
    } catch (error) {
        const stdout = error.stdout?.toString() || "";
        const stderr = error.stderr?.toString() || "";

        const isNoFiles = stdout.includes("No Python files matched pattern");
        const isZeroErrors = stdout.includes("0 errors");
        const isExcluded = stderr.includes("is matched by `project-excludes` or ignore file");

        const isNoise = (!stdout && !stderr) || isNoFiles || isZeroErrors || isExcluded;

        if (!isNoise) {
            report += `\n## Typing Errors (Pyrefly):\n`;
            if (stdout) report += `STDOUT:\n${stdout}\n`;
            if (stderr) report += `STDERR:\n${stderr}\n`;
        }
    }

    return report;
}

/**
 * Handles diagnostic success.
 */
function handleSuccess(sessionId) {
    logger.info("All global checks passed successfully.");
    stateManager.deleteState(sessionId);
    return {};
}

/**
 * Handles diagnostic failure with retry logic.
 */
function handleFailure(sessionId, state, errorReport) {
    if (state.retryCount >= 2) {
        logger.error("Max retries reached. Allowing completion with errors.");
        console.error(`\n⚠️  QUALITY GATE FAILED after 3 attempts:\n${errorReport}\n`);
        stateManager.deleteState(sessionId);
        return {
            stopReason: "Quality Gate failed after multiple attempts. Please fix manually."
        };
    }

    state.retryCount += 1;
    stateManager.saveState(sessionId, state);

    logger.warn(`Issues detected. Blocking stop (Attempt ${state.retryCount}).`);

    const reason = `Your changes introduced errors. Please fix them before finishing.\n${errorReport}`;
    logger.finish({ decision: "block" });
    return { decision: "block", reason };

}
